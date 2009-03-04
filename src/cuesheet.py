# -*- coding: utf-8 -*-

"""
    Cuesheet parser.

    Copyright (c) 2006-2008 by Nyaochi

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA, or visit
http://www.gnu.org/copyleft/gpl.html .
"""

import string, sys, os

class Format:
    def __init__(self, format = None, sample_rate = 0, sample_bit = 0, channels = 0):
        self.format = format
        self.sample_rate = sample_rate
        self.sample_bit = sample_bit
        self.channels = channels

class CuesheetParseError(Exception):
    def __init__(self, num_lines, msg):
        self.num_lines = num_lines
        self.msg = msg
    def __str__(self):
        return self.num_lines + self.msg

class CuesheetTrackNumberError(CuesheetParseError):
    """
    """

class CuesheetFieldError(CuesheetParseError):
    """
    """


class CSTrack:
    def __init__(self):
        self.filename = None
        self.title = None
        self.performer = None
        self.rem = {}
        self.indexes = {}
        self.isrc = None
        self.catalog = None
    def __repr__(self):
        r = "{filename: %r, title: %r, performer: %r}" % (
            self.filename, self.title, self.performer
            )
        return r

class Track(dict):
    def __init__(self):
        self.filename = None
        self.url = None
        self.begin = None
        self.end = None

def __split(line):
    fields = []
    field = ""
    quote = False

    for i in range(0, len(line)):
        c = line[i]
        if c in string.whitespace:
            if quote:
                field += c
            elif field:
                fields.append(field)
                field = ""
        elif c == '"':
            if quote:
                if i+1 < len(line) and line[i+1] == '"':
                    i += 1
                    field += c
                else:
                    quote = False
            elif not field:
                quote = True
            else:
                field += c
        else:
            field += c
    if field:
        fields.append(field)

    return fields

def __let(x, y):
    if x is None:
        return y
    else:
        return x
    
def read_cuesheet(fp):
    tracks = [CSTrack(),]
    num = 0
    audiofile = ''

    for line in fp:
        num += 1
        
        fields = __split(unicode(line).strip())     
        if not fields:
            continue

        command = fields[0].upper()
        if command == "TRACK":
            if len(fields) > 2 and fields[2].upper() == "AUDIO":
                if len(tracks) != int(fields[1]):
                    raise CuesheetTrackNumberError(num, line)
                tracks.append(CSTrack())
                tracks[-1].filename = audiofile
            else:
                raise CuesheetFieldError(num, line)
        elif command == "TITLE":
            if len(fields) > 1:
                tracks[-1].title = fields[1]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "PERFORMER":
            if len(fields) > 1:
                tracks[-1].performer = fields[1]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "FILE":
            if len(fields) > 1:
                audiofile = fields[1]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "INDEX":
            if len(fields) > 2:
                index = int(fields[1])
                tracks[-1].indexes[index] = fields[2]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "ISRC":
            if len(fields) > 1:
                tracks[-1].isrc = fields[1]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "CATALOG":
            if len(fields) > 1:
                tracks[-1].catalog = fields[1]
            else:
                raise CuesheetFieldError(num, line)
        elif command == "REM":
            if len(fields) > 1:
                if len(fields) > 2:
                    tracks[-1].rem[fields[1].upper()] = ' '.join(fields[2:])
                else:
                    tracks[-1].rem[fields[1].upper()] = None
            else:
                raise CuesheetFieldError(num, line)

    return tracks

def to_playlist(cs, pregap = False, delgap = False):
    pl = []
    
    if len(cs) < 1:
        return pl
    
    for i in range(1, len(cs)):
        # Create a track and set the url
        track = Track()
        track.filename = __let(cs[i].filename, cs[0].filename)

        # Assign begin
        if i == 1 and pregap and cs[i].indexes.has_key(0):
            track.begin = cs[i].indexes[0]
        elif cs[i].indexes.has_key(1):
            track.begin = cs[i].indexes[1]
        # Assign end
        if i != len(cs) - 1:
            if cs[i].filename == cs[i+1].filename:
                if delgap and cs[i+1].indexes.has_key(0):
                    track.end = cs[i+1].indexes[0]
                else:
                    track.end = cs[i+1].indexes[1]
        # Assign title
        track['TITLE'] = __let(cs[i].title, "")
        track['ARTIST'] = __let(cs[i].performer, cs[0].performer)
        track['ALBUMARTIST'] = cs[0].performer
        track['ALBUM'] = cs[0].title
        track['GENRE'] = __let(cs[i].rem.get("GENRE"), cs[0].rem.get("GENRE"))
        track['tracknumber'] = i
        track['TRACKNUMBER'] = '%02d' % i
        track['totaltracks'] = len(cs)-1
        track['TOTALTRACKS'] = '%02d' % (len(cs)-1)
        track['DATE'] = __let(cs[i].rem.get("DATE"), cs[0].rem.get("DATE"))
        track['ISRC'] = __let(cs[i].isrc, cs[0].isrc)
        track['CATALOG'] = __let(cs[i].catalog, cs[0].catalog)
        track['COMMENT'] = __let(cs[i].rem.get("COMMENT"), cs[0].rem.get("COMMENT"))
        # Obtain custom fields
        for key, value in cs[0].rem.iteritems():
            if key not in ("GENRE", "DATE", "COMMENT"):
                track[key] = value
        for key, value in cs[i].rem.iteritems():
            if key not in ("GENRE", "DATE", "COMMENT"):
                track[key] = value
        # Add this track
        pl.append(track)
    return pl
    
def reader(fp, pregap = False, delgap = False):
    return to_playlist(read_cuesheet(fp), pregap, delgap)
