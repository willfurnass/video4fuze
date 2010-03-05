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

#include "riff.h"

#include <limits.h>
#include <ctype.h>
#include <stdlib.h>
#include <assert.h>

#define MIN(a,b) ((a)<(b)?(a):(b))
#define MAX(a,b) ((a)>(b)?(a):(b))
#define EVEN(a) ((a)%2==0)
#define TOEVEN(a) ((a)+(a)%2)


#define PRINT(c) (isprint(c)?(c):'?')
#define FOURCCSTR(id) ((char[5]){ \
        PRINT((unsigned char)id),       PRINT((unsigned char)(id>>8)), \
        PRINT((unsigned char)(id>>16)), PRINT((unsigned char)(id>>24)), 0})

static void
fskip(FILE *f, uint32_t size)
{
    while (size) {
        long n = MIN(size, LONG_MAX);
        fseek(f, n, SEEK_CUR);
        size -= n;
    }
}

void to_le16(char buf[2], uint16_t n)
{
    ((unsigned char*)buf)[0] = n;
    ((unsigned char*)buf)[1] = n >> 8;
}


void to_le32(char buf[4], uint32_t n)
{
    ((unsigned char*)buf)[0] = n;
    ((unsigned char*)buf)[1] = n >> 8;
    ((unsigned char*)buf)[2] = n >> 16;
    ((unsigned char*)buf)[3] = n >> 24;
}

void to_le64(char buf[8], uint64_t n)
{
    to_le32(buf, n);
    to_le32(buf + 4, n >> 32);
}

uint32_t from_le32(const char buf[4])
{
    return (uint32_t)((unsigned char*)buf)[0] |
           (uint32_t)((unsigned char*)buf)[1] << 8 |
           (uint32_t)((unsigned char*)buf)[2] << 16 |
           (uint32_t)((unsigned char*)buf)[3] << 24;
}


static void peek(riffread *r)
{
    uint32_t parentrest = -1;
    if (r->depth > 0)
        parentrest = r->liststack[r->depth - 1].endoffset - r->offset;
    if (parentrest == 0) { r->chunkid = r->datasize = r->listid = 0; return; }

    fpos_t p;
    fgetpos(r->file, &p);

    char buf[12];
    size_t c = fread(buf, 4, MIN(3, parentrest / 4), r->file);
    if (c >= 2) {
        r->chunkid = from_le32(buf);
        r->datasize = from_le32(buf + 4);

        if (r->datasize + 8 > parentrest) {
            fprintf(stderr, "Warning: invalid size %lu of chunk %s.\n",
                    (unsigned long)r->datasize, FOURCCSTR(r->chunkid));
            r->chunkid = r->datasize = r->listid = 0;
        } else if (ISLIST(r->chunkid) && c == 3 &&
                   r->datasize >= 4 && EVEN(r->datasize))
            r->listid = from_le32(buf + 8);
        else
            r->listid = 0;
    } else {
        r->chunkid = r->datasize = r->listid = 0;
    }
    fsetpos(r->file, &p);
}

void riffread_init(riffread *r, FILE *f)
{
    *r = (riffread) {
        .depth = 0,
        .offset = 0,
        .file = f
    };
    peek(r);
}

bool riffread_search(riffread *r, uint32_t chunkid, uint32_t listid)
{
    while (r->chunkid) {
        if (r->chunkid == chunkid && r->listid == listid) return true;
        else riffread_chunkdata(r, 0, 0);
    }
    return false;
}

void riffread_chunkdata(riffread *r, void *buffer, fpos_t *datapos)
{
    assert(r->chunkid);
    fseek(r->file, 8, SEEK_CUR);
    if (datapos) fsetpos(r->file, datapos);
    if (buffer) fread(buffer, r->datasize, 1, r->file);
    else fskip(r->file, r->datasize);
    if (!EVEN(r->datasize)) fseek(r->file, 1, SEEK_CUR);
    r->offset += 8 + TOEVEN(r->datasize);
    peek(r);
}

void riffread_listbegin(riffread *r)
{
    assert(r->depth < RIFFMAXDEPTH && ISLIST(r->chunkid) && r->listid);
    r->liststack[r->depth++].endoffset = r->offset + 8 + r->datasize;
    fseek(r->file, 12, SEEK_CUR);
    r->offset += 12;
    peek(r);
}

void riffread_listend(riffread *r)
{
    assert(r->depth > 0);
    uint32_t eo = r->liststack[--r->depth].endoffset;
    fskip(r->file, eo - r->offset);
    r->offset = eo;
    peek(r);
}

void riffread_cleanup(riffread *r)
{
    while (r->depth) riffread_listend(r);
}


static void fwritezeroes(size_t size, FILE *f)
{
    static char zeroes[64];
    while (size) {
        size_t n = MIN(size, sizeof zeroes);
        fwrite(zeroes, n, 1, f);
        size -= n;
    }
}


void riffwrite_init(riffwrite *w, FILE *f)
{
    *w = (riffwrite) {
        .depth = 0,
        .offset = 0,
        .file = f
    };
}

void riffwrite_chunk(riffwrite *w, uint32_t chunkid,
                void *data, uint32_t datasize, fpos_t *datapos)
{
    char buf[8];
    to_le32(buf, chunkid);
    to_le32(buf + 4, datasize);
    fwrite(buf, 4, 2, w->file);

    if (datapos) fgetpos(w->file, datapos);
    if (data) fwrite(data, datasize, 1, w->file);
    else fwritezeroes(datasize, w->file);

    w->offset += 8 + datasize;
    if (datasize % 2) {
        fwritezeroes(1, w->file);
        w->offset++;
    }
}

void riffwrite_listbegin(riffwrite *w, uint32_t listid)
{
    assert(w->depth < RIFFMAXDEPTH);
    char buf[8];
    to_le32(buf, w->depth > 0 ? FOURCC_LIST : FOURCC_RIFF);
    fwrite(buf, 4, 1, w->file);
    fgetpos(w->file, &w->liststack[w->depth].sizefpos);
    to_le32(buf, 0);
    to_le32(buf + 4, listid);
    fwrite(buf, 4, 2, w->file);
    w->liststack[w->depth].contentoffset = w->offset += 12;
    w->depth++;
}

void riffwrite_listend(riffwrite *w)
{
    assert(w->depth > 0);
    w->depth--;
    fpos_t current;
    fgetpos(w->file, &current);
    fsetpos(w->file, &w->liststack[w->depth].sizefpos);
    char buf[4];
    to_le32(buf, 4 + w->offset - w->liststack[w->depth].contentoffset);
    fwrite(buf, 4, 1, w->file);
    fsetpos(w->file, &current);
}


void riffwrite_cleanup(riffwrite *w)
{
    while (w->depth) riffwrite_listend(w);
}

