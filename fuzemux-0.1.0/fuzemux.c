/*
 *  Copyright (C) 2010 Daniel Pirch
 *
 *  This file is part of Fuzemux.
 *
 *  Fuzemux is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Fuzemux is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Fuzemux.  If not, see <http://www.gnu.org/licenses/>.
 */

 #define USAGESCREEN \
 "Usage: fuzemux INPUTFILE OUTPUTFILE\n\n" \
 "fuzemux version 0.1.0\n" \
 "project home page: http://code.google.com/p/fuzemux\n"


#include "riff.h"

#include <stdlib.h>
#include <string.h>
#include <limits.h>

#define AVIHEADERSIZE    56
#define STREAMHEADERSIZE 56
#define ODMLHEADERSIZE   248
#define VIDEOFORMATSIZE  40
#define AUDIOFORMATSIZE  30

#define INDEXLEN         4000
#define SUPERINDEXLEN    2000
#define INDEXSIZE        (24 + 8 * INDEXLEN)
#define SUPERINDEXSIZE   (24 + 16 * SUPERINDEXLEN)

#define VIDEOID1 FOURCC('0','0','d','b')
#define VIDEOID2 FOURCC('0','0','d','c')
#define AUDIOID FOURCC('0','1','w','b')

#define MIN(a,b) ((a)<(b)?(a):(b))



/* result of parsing the input file (all we need for writing the output
   besides the actual frames) */
struct inputinfo {
    struct headers {
        char aviheader[AVIHEADERSIZE];
        char videoheader[STREAMHEADERSIZE];
        char audioheader[STREAMHEADERSIZE];
        char videoformat[VIDEOFORMATSIZE];
        char audioformat[AUDIOFORMATSIZE];
    } headers;

    size_t nvideoframes;
    struct { uint32_t offset; uint32_t size; bool iskeyframe; } *videoframes;

    size_t naudioframes;
    struct { uint32_t offset; uint32_t size; } *audioframes;
};


/* struct for either video or audio stream beeing written */
struct outputstream {

    char *superindex;
    char *currentindex;

    uint32_t superindexfill;
    uint32_t currentindexfill;
    uint32_t currentindexsamples;
    uint64_t currentbaseoffset;

    uint32_t samplecount;

    fpos_t superindexpos;
    fpos_t currentindexpos;
    fpos_t headerpos;
    fpos_t formatpos;

    uint32_t idkey, idother, idindex;
};

struct output {
    fpos_t aviheaderpos;
    fpos_t odmlheaderpos;
    struct outputstream video, audio;
};

static void fail(const char *msg) {
    fprintf(stderr, "%s\n", msg);
    exit(EXIT_FAILURE);
}


static void *xmalloc(size_t size)
{
    void *p = malloc(size);
    if (!p && size) {fprintf(stderr, "Out of memory\n"); exit(EXIT_FAILURE);}
    return p;
}


static void
fwrite_at(const void *buf, size_t size, FILE *f, fpos_t *pos)
{
    fpos_t current;
    fgetpos(f, &current);
    fsetpos(f, pos);
    fwrite(buf, size, 1, f);
    fsetpos(f, &current);
}


/* read the legacy index to fill the videoframes and audioframes arrays */
static void
parse_legacy_index(struct inputinfo *info, uint32_t movioffset, riffread *r)
{
    size_t indexlen = r->datasize / 16;
    char (*index)[4][4] = xmalloc(r->datasize);
    riffread_chunkdata(r, index, 0);

    /* count audio and video frames index*/
    info->nvideoframes = info->naudioframes = 0;
    for (size_t i = 0; i < indexlen; i++) {
        uint32_t id = from_le32(index[i][0]);
        if (id == VIDEOID1 || id == VIDEOID2) info->nvideoframes++;
        else if (id == AUDIOID) info->naudioframes++;
    }

    /* +8 because we need the chunk data, not headers */
    uint32_t frameoffset = 8;
    /* frame offsets are relative to movi list (listid tag) in some files */
    if (from_le32(index[0][2]) < movioffset + 4)
        frameoffset += movioffset;

    size_t nvideokeyframes = 0;

    /* create video/audio frame lists */
    info->videoframes = xmalloc(info->nvideoframes * sizeof *info->videoframes);
    info->audioframes = xmalloc(info->naudioframes * sizeof *info->audioframes);
    for (size_t i = 0, vi = 0, ai = 0; i < indexlen; i++) {
        uint32_t id = from_le32(index[i][0]);
        if (id == VIDEOID1 || id == VIDEOID2) {
            info->videoframes[vi].offset = from_le32(index[i][2]) + frameoffset;
            info->videoframes[vi].size = from_le32(index[i][3]);
            if ((info->videoframes[vi].iskeyframe = index[i][1][0] & 0x10)) nvideokeyframes++;
            vi++;
        } else if (id == AUDIOID) {
            info->audioframes[ai].offset = from_le32(index[i][2]) + frameoffset;
            info->audioframes[ai].size = from_le32(index[i][3]);
            ai++;
        }
    }
    free(index);

    printf("%lu video frames (%lu keyframes); %lu audio frames\n",
           (unsigned long)info->nvideoframes, (unsigned long)nvideokeyframes,
           (unsigned long)info->naudioframes);

}

/* parse input avi file from the beginning to fill the inputinfo structure */
static void
parse_input_file(struct inputinfo *info, FILE *file)
{
    riffread r;
    riffread_init(&r, file);
    if (!riffread_search(&r, FOURCC_RIFF, FOURCC('A','V','I',' '))) fail("not an avi file");
    riffread_listbegin(&r);
    if (!riffread_search(&r, FOURCC_LIST, FOURCC('h','d','r','l'))) fail("header list missing");
    riffread_listbegin(&r);

    if (!riffread_search(&r, FOURCC('a','v','i','h'),0)) fail("avi header missing");
    if (r.datasize != AVIHEADERSIZE) fail("avi header has the wrong size");
    riffread_chunkdata(&r, info->headers.aviheader, 0);

    /* assume the first stream is video and the second audio... */

    if (!riffread_search(&r, FOURCC_LIST, FOURCC('s','t','r','l'))) fail("video stream list missing");
    riffread_listbegin(&r); /* strl */
    if (!riffread_search(&r, FOURCC('s','t','r','h'),0)) fail("video stream header missing");
    if (r.datasize != STREAMHEADERSIZE) fail("video stream header has the wrong size");
    riffread_chunkdata(&r, info->headers.videoheader, 0);
    if (!riffread_search(&r, FOURCC('s','t','r','f'),0)) fail("video stream format missing");
    if (r.datasize != VIDEOFORMATSIZE) fail("video stream format has the wrong size");
    riffread_chunkdata(&r, info->headers.videoformat, 0);
    riffread_listend(&r); /* strl */

    if (!riffread_search(&r, FOURCC_LIST, FOURCC('s','t','r','l'))) fail("audio stream list missing");
    riffread_listbegin(&r); /* strl */
    if (!riffread_search(&r, FOURCC('s','t','r','h'),0)) fail("audio stream header missing");
    if (r.datasize != STREAMHEADERSIZE) fail("audio stream header has the wrong size");
    riffread_chunkdata(&r, info->headers.audioheader, 0);
    if (!riffread_search(&r, FOURCC('s','t','r','f'),0)) fail("audio stream format missing");
    if (r.datasize != AUDIOFORMATSIZE) fail("audio stream format has the wrong size");
    riffread_chunkdata(&r, info->headers.audioformat, 0);
    riffread_listend(&r); /* strl */
    riffread_listend(&r); /* hdrl */

    if (!riffread_search(&r, FOURCC_LIST, FOURCC('m','o','v','i'))) fail("movi list missing");
    uint32_t movioffset = r.offset + 8; /* offset of "movi" listid */

    if (!riffread_search(&r, FOURCC('i','d','x','1'),0)) fail("legacy index missing (we need it!)");
    parse_legacy_index(info, movioffset, &r);

    riffread_listend(&r); /* avi */
    riffread_cleanup(&r);
}


/* write (audio or video) header streamlist and init outputstream objects
   for adding chunks */
static void
outputstream_init(struct outputstream *os, size_t formatsize,
                  uint32_t idkey, uint32_t idother,
                  uint32_t idindex, riffwrite *w)
{
    riffwrite_listbegin(w, FOURCC('s','t','r','l'));
    riffwrite_chunk(w, FOURCC('s','t','r','h'), 0, STREAMHEADERSIZE, &os->headerpos);
    riffwrite_chunk(w, FOURCC('s','t','r','f'), 0, formatsize, &os->formatpos);
    if (w->offset % 4) riffwrite_chunk(w, FOURCC('J','U','N','K'), 0, 2, 0);
    riffwrite_chunk(w, FOURCC('i','n','d','x'), 0, SUPERINDEXSIZE, &os->superindexpos);
    riffwrite_listend(w); /* strl */

    os->superindex = xmalloc(SUPERINDEXSIZE);
    os->superindexfill = 0;
    memset(os->superindex, 0, SUPERINDEXSIZE);
    to_le16(os->superindex, 4);
    to_le32(os->superindex + 8, idkey);

    os->currentindex = xmalloc(INDEXSIZE);
    os->currentindexfill = 0; /* recreate for next chunk */
    os->currentindexsamples = 0;
    os->samplecount = 0;

    os->idkey = idkey;
    os->idother = idother;
    os->idindex = idindex;
}


/* begin a new standard index, add it to the buffered super index */
static void
outputstream_beginindex(struct outputstream *os, riffwrite *w)
{
    if (os->superindexfill < SUPERINDEXLEN) {
        to_le64(os->superindex + os->superindexfill * 16 + 24, w->offset);
        to_le32(os->superindex + os->superindexfill * 16 + 32, INDEXSIZE + 8);
    }

    riffwrite_chunk(w, os->idindex, 0, INDEXSIZE, &os->currentindexpos);
    memset(os->currentindex, 0, INDEXSIZE);
    to_le16(os->currentindex, 2);
    os->currentindex[3] = 1; /* AVI_INDEX_OF_CHUNKS */
    to_le32(os->currentindex + 8, os->idkey);
}

/* complete the current standard index (rewrite the buffered index to the file) */
static void
outputstream_finishindex(struct outputstream *os, FILE *f)
{
    if (os->superindexfill < SUPERINDEXLEN) {
        to_le32(os->superindex + os->superindexfill * 16 + 36, os->currentindexsamples);
        os->superindexfill++;
    }
    to_le32(os->currentindex + 4, os->currentindexfill);
    to_le64(os->currentindex + 12, os->currentbaseoffset);
    fwrite_at(os->currentindex, INDEXSIZE, f, &os->currentindexpos);
    os->currentindexfill = 0;
    os->currentindexsamples = 0;
}


/* write a frame chunk to file and add its entry to the buffered standard index.
   if necessary begin a new standard index */
static void
outputstream_addframe(struct outputstream *os, char *data, uint32_t datasize,
                      bool keyframe, uint32_t samples, riffwrite *w)
{
    uint64_t chunkoffset = w->offset;
    riffwrite_chunk(w, keyframe ? os->idkey : os->idother, data, datasize, 0);

    if (os->currentindexfill == 0)
        os->currentbaseoffset = chunkoffset;

    to_le32(os->currentindex + os->currentindexfill * 8 + 24,
                chunkoffset - os->currentbaseoffset + 8);
    to_le32(os->currentindex + os->currentindexfill * 8 + 28,
                datasize | (keyframe ? 0 : 0x80000000));

    os->currentindexfill++;
    os->currentindexsamples += samples;
    os->samplecount += samples;

    if (os->currentindexfill == INDEXLEN) {
        outputstream_finishindex(os, w->file);
        outputstream_beginindex(os, w);
    }
}

/* rewrite the current standard index and superindex to the file, cleanup
   outputstream data structure */
static void
outputstream_cleanup(struct outputstream *os, FILE *f)
{
    if (os->currentindexfill > 0)
        outputstream_finishindex(os, f);
    to_le32(os->superindex + 4, os->superindexfill);
    fwrite_at(os->superindex, SUPERINDEXSIZE, f, &os->superindexpos);
    free(os->currentindex);
    free(os->superindex);
}


/* create all video and audio frames and indexes between them */
static void
writeframes(struct output *of, riffwrite *w,
            struct inputinfo *info, FILE *inputfile)
{
    char *aframein = 0;
    uint32_t aframeinsize;
    uint32_t aframeinpos;

    outputstream_beginindex(&of->video, w);
    outputstream_beginindex(&of->audio, w);

    for (uint32_t ivin = 0, iain = 0;
            ivin < info->nvideoframes || iain < info->naudioframes || aframein;)
    {
        for (int vpair = 0; vpair < 2 && ivin < info->nvideoframes;
                vpair++, ivin++)
        {
            uint32_t datasize = info->videoframes[ivin].size;
            char *data = xmalloc(datasize);
            fseek(inputfile, info->videoframes[ivin].offset, SEEK_SET); /* does not work for large files... */
            fread(data, datasize, 1, inputfile);

            outputstream_addframe(&of->video, data, datasize,
                       info->videoframes[ivin].iskeyframe, 1, w);
            free(data);
        }
        if (iain < info->naudioframes || aframein) {
            size_t datamax = ivin < info->nvideoframes ? 1600 : 2000;

            char *data = xmalloc(datamax);
            uint32_t datafill = 0;
            while (datafill < datamax) {
                if (!aframein) {
                    if (iain == info->naudioframes) break;
                    aframeinsize = info->audioframes[iain].size;
                    aframein = xmalloc(aframeinsize);
                    fseek(inputfile, info->audioframes[iain].offset, SEEK_SET);
                    fread(aframein, aframeinsize, 1, inputfile);
                    aframeinpos = 0;
                    iain++;
                }
                size_t n = MIN(aframeinsize - aframeinpos, datamax - datafill);
                memcpy(data + datafill, aframein + aframeinpos, n);
                datafill += n;
                aframeinpos += n;
                if (aframeinpos == aframeinsize) { free(aframein); aframein = 0; }
            }
            outputstream_addframe(&of->audio, data, datafill, true, datafill, w);
            free(data);
        }
    }
}


static void
rewriteheaders(struct output *of, struct inputinfo *info, FILE *outfile)
{
    struct headers h = info->headers;
    char odmlheader[ODMLHEADERSIZE];


    /* AVI main header (AVIMAINHEADER structure) */
    fwrite_at(h.aviheader, AVIHEADERSIZE, outfile, &of->aviheaderpos);

    /* OpenDML extended AVI header  */
    to_le32(odmlheader, of->video.samplecount);
    memset(odmlheader+4, 0, ODMLHEADERSIZE-4);
    fwrite_at(odmlheader, ODMLHEADERSIZE, outfile, &of->odmlheaderpos);

    /* video stream header (AVISTREAMHEADER structure) */
    to_le32(h.videoheader+20,   500000);  /* dwScale */
    to_le32(h.videoheader+24, 10000000);  /* dwRate */
    fwrite_at(h.videoheader, STREAMHEADERSIZE, outfile, &of->video.headerpos);

    /* audio header (AVISTREAMHEADER structure) */
    to_le32(h.audioheader+20, 1);                       /* dwScale */
    to_le32(h.audioheader+24, 16000);                   /* dwRate */
    double audioratefactor = (double)16000 *
        from_le32(info->headers.audioheader + 20) /
        from_le32(info->headers.audioheader + 24);
    uint32_t audiostart = 0.5 + audioratefactor *
        from_le32(info->headers.audioheader + 28);
    to_le32(h.audioheader+28, audiostart);              /* dwStart */
    to_le32(h.audioheader+32, of->audio.samplecount);   /* dwLength */
    to_le32(h.audioheader+36, 2000 + 8);                /* dwSuggestedBufferSize */
    to_le32(h.audioheader+44, 1);                       /* dwSampleSize */
    fwrite_at(h.audioheader, STREAMHEADERSIZE, outfile, &of->audio.headerpos);

    /* video format (BITMAPINFOHEADER structure) */
    fwrite_at(h.videoformat, VIDEOFORMATSIZE, outfile, &of->video.formatpos);

    /* audio format (MPEGLAYER3WAVEFORMAT) */
    to_le16(h.audioformat+12, 1);                       /* nBlockAlign */
    fwrite_at(h.audioformat, AUDIOFORMATSIZE, outfile, &of->audio.formatpos);
}



static void
writeoutput(FILE *outfile, FILE *infile, struct inputinfo *info)
{
    struct output of;

    riffwrite w;
    riffwrite_init(&w, outfile);

    riffwrite_listbegin(&w, FOURCC('A','V','I',' '));
    riffwrite_listbegin(&w, FOURCC('h','d','r','l'));

    riffwrite_chunk(&w, FOURCC('a','v','i','h'), 0, AVIHEADERSIZE, &of.aviheaderpos);

    outputstream_init(&of.video, VIDEOFORMATSIZE,
                      FOURCC('0','0','d','b'), FOURCC('0','0','d','c'),
                      FOURCC('i','x','0','0'), &w);

    outputstream_init(&of.audio, AUDIOFORMATSIZE,
                      FOURCC('0','1','w','b'), FOURCC('0','1','w','b'),
                      FOURCC('i','x','0','1'), &w);

    /* open dml header */
    riffwrite_listbegin(&w, FOURCC('o','d','m','l'));
    riffwrite_chunk(&w, FOURCC('d','m','l','h'), 0, ODMLHEADERSIZE, &of.odmlheaderpos);
    riffwrite_listend(&w); /* odml */

    riffwrite_listend(&w); /* hdrl */

    riffwrite_listbegin(&w, FOURCC('I','N','F','O'));
    riffwrite_chunk(&w, FOURCC('I','S','F','T'), "fuzemux\0\0\0\0", 12, 0);
    riffwrite_listend(&w); /* INFO */

    riffwrite_listbegin(&w, FOURCC('m','o','v','i'));
    writeframes(&of, &w, info, infile);
    riffwrite_listend(&w); /* movi */

    riffwrite_listend(&w); /* AVI */
    riffwrite_cleanup(&w);

    rewriteheaders(&of, info, outfile);

    outputstream_cleanup(&of.video, outfile);
    outputstream_cleanup(&of.audio, outfile);
}



int main(int argc, char *argv[])
{
    if (argc != 3) {
        fputs(USAGESCREEN, stderr);
        exit(EXIT_FAILURE);
    }


    char *infilename = argv[1];
    char *outfilename = argv[2];

    FILE *infile = fopen(infilename, "rb");
    if (!infile) fail("Cannot open input file");
    FILE *outfile = fopen(outfilename, "wb");
    if (!outfile) fail("Cannot open output file");

    fprintf(stderr, "Parsing input...\n");
    struct inputinfo inputinfo;
    parse_input_file(&inputinfo, infile);

    fprintf(stderr, "Writing output...\n");
    writeoutput(outfile, infile, &inputinfo);

    fclose(infile);
    fclose(outfile);

    fprintf(stderr, "Done.\n");
    return 0;
}










