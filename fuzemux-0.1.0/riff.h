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

#ifndef RIFF_H_INCLUDED
#define RIFF_H_INCLUDED

#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

#define FOURCC(c0,c1,c2,c3) \
    ((uint32_t)c0 | (uint32_t)c1<<8 | (uint32_t)c2<<16 | (uint32_t)c3<<24)

#define FOURCC_LIST FOURCC('L','I','S','T')
#define FOURCC_RIFF FOURCC('R','I','F','F')
#define ISLIST(chunkid) ((chunkid) == FOURCC_LIST || (chunkid) == FOURCC_RIFF)

void to_le16(char buf[2], uint16_t n);
void to_le32(char buf[4], uint32_t n);
void to_le64(char buf[8], uint64_t n);
uint32_t from_le32(const char buf[4]);

#define RIFFMAXDEPTH 20

/* READING RIFF FILES */

typedef struct {
    /* information about current (next readable) chunk, updated after each call
       to the rifread_xxx functions */
    uint32_t chunkid;       /* id of current chunk, or 0 if no chunk available
                               (at end of current list or file) */
    uint32_t datasize;      /* data size (without header) of current chunk */
    uint32_t listid;        /* listid, or 0 if not a list */
    uint32_t offset;        /* file offset of header of current chunk */

    unsigned depth;         /* current list recursion depth, 0 for file level
                               where the RIFF list is expected. */
    struct {
        uint32_t endoffset; /* offset of end of list content */
    } liststack[RIFFMAXDEPTH];
    FILE *file;
} riffread;

/* initialize riffread object */
void riffread_init(riffread *r, FILE *f);

/* search current list for chunk (or also sublist) with specific id,
   set r->chunkid to nonzero if found. */
bool riffread_search(riffread *r, uint32_t chunkid, uint32_t listid);

/* If datapos != NULL, store position of chunk contents there.
   If buffer != NULL, read chunk contents into buffer (with size r->datasize).
   Then move to next chunk in list. */
void riffread_chunkdata(riffread *r, void *buffer, fpos_t *datapos);

/* if current chunk is a list, go down to first chunk of this list.
   Should be matched with riffread_listend call */
void riffread_listbegin(riffread *r);

/* skip rest of current list and go to next chunk of parent list */
void riffread_listend(riffread *r);

/* clean up riffread object */
void riffread_cleanup(riffread *r);


/* WRITING RIFF FILES */

typedef struct {
    uint64_t offset;             /* current file offset, will be offset of
                                    next chunk written */
    unsigned depth;              /* current list recursion depth */
    struct {
        fpos_t sizefpos;         /* fpos of list's size entry */
        uint64_t contentoffset;  /* file offset of list content (after listid)*/
    } liststack[RIFFMAXDEPTH];
    FILE *file;
} riffwrite;

/* initialize riffwrite object */
void riffwrite_init(riffwrite *w, FILE *f);

/* write a chunk. If data == NULL, (datasize) zero bytes are written instead.
   If datapos != NULL, the position of chunk data is stored there so it can be
   rewritten later. */
void riffwrite_chunk(riffwrite *w, uint32_t chunkid,
                void *data, uint32_t datasize, fpos_t *datapos);

/* insert a LIST (or RIFF on top level) element. should be matched with
   call to riffwrite_listend. */
void riffwrite_listbegin(riffwrite *w, uint32_t listid);

/* finish a list and sets the correct length. */
void riffwrite_listend(riffwrite *w);

/* clean up riffwrite object */
void riffwrite_cleanup(riffwrite *w);


#endif // RIFF_H_INCLUDED
