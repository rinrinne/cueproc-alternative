# -*- coding: utf-8 -*-

"""
    Output Plugin for MP3 Encoder

    Copyright (c) 2006-2007 by Nyaochi

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

from celib import *
import eyeD3
import os.path, codecs

TAG_FMT = "%-12s: %s"

class LameEyeD3Output(OutputModule):
    def __init__(self):
        self.name = 'lame_eyed3'
        self.ext = '.mp3'
        self.is_utf8 = True
        self.cmd = 'lame'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            "LAME MP3 Encoder",
            "eyeD3 (Python module for tagging ID3)"
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = ('TITLE','ARTIST','ALBUMARTIST','ALBUM','COMPOSER','TRACKNUMBER','TOTALTRACKS','DISCNUMBER','TOTALDISCS','GENRE','DATE','COMMENT','BPM','COPYRIGHT','ALBUMART','COMPILATION')
        
        self.tagversion = 23
        self.tagcharset = 'utf-16'
        
    def __formattag(self, track, tag):
        return self.console.write(TAG_FMT % (tag, track.get(tag, u"")))

    def handle_track(self, track, options):
        args = []
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for MP3 encoder.
        args.append(qstr(self.cmd))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')
        args.append(qstr(track['output']))

        # Execute the command.
        cmdline = args_to_string(args)
        ret = self.console.execute(cmdline)
        if ret != 0:
            return ret
        
        # Add Tag
        if not eyeD3.isMp3File(track['output'].encode(options.syscharset)):
            return -1
        
        tag = eyeD3.Tag()
        tag.link(track['output'].encode(options.syscharset))
        if self.tagversion == 23:
            tag.setVersion(eyeD3.ID3_V2_3)
        elif self.tagversion == 24:
            tag.setVersion(eyeD3.ID3_V2_4)
        else:
            tag.setVersion(eyeD3.ID3_V2_3)
        
        try:
            charset = codecs.lookup(self.tagcharset).name
            if 'iso8859-1' in charset:
                tag.setTextEncoding(eyeD3.LATIN1_ENCODING)
            elif 'utf-8' in  charset:
                tag.setTextEncoding(eyeD3.UTF_8_ENCODING)
            elif 'utf-16' in  charset:
                tag.setTextEncoding(eyeD3.UTF_16_ENCODING)
            else:
                tag.setTextEncoding(eyeD3.LATIN1_ENCODING)
        except LookupError:
            tag.setTextEncoding(eyeD3.LATIN1_ENCODING)

        self.console.write("================ ID3 TAG (eyeD3) ================")
            
        if track.get('TITLE'):
            tag.setTitle(track.get('TITLE'))
            self.__formattag(track, 'TITLE')
        if track.get('ARTIST'):
            tag.setArtist(track.get('ARTIST'))
            self.__formattag(track, 'ARTIST')
        if track.get('ALBUM'):
            tag.setAlbum(track.get('ALBUM'))
            self.__formattag(track, 'ALBUM')
        if track.get('GENRE'):
            tag.setGenre(eyeD3.Genre(None,track.get('GENRE').encode(options.syscharset)))
            self.__formattag(track, 'GENRE')
        if track.get('DATE'):
            tag.setDate(track.get('DATE'))
            self.__formattag(track, 'DATE')
        if track.get('BPM'):
            tag.setBPM(track.get('BPM'))
            self.__formattag(track, 'BPM')
        if track.get('ALBUMARTIST'):
            tag.setArtist(track.get('ALBUMARTIST'), eyeD3.frames.BAND_FID)
            self.__formattag(track, 'ALBUMARTIST')
        if track.get('COMPOSER'):
            tag.setArtist(track.get('COMPOSER'), eyeD3.frames.COMPOSER_FID)
            self.__formattag(track, 'COMPOSER')
        if track.get('COPYRIGHT'):
            tag.setArtist(track.get('COPYRIGHT'), "TCOP")
            self.__formattag(track, 'COPYRIGHT')
    
        Nums = [None, None]
        if track.get('TRACKNUMBER'):
            Nums[0] = int(track.get('TRACKNUMBER'))
            self.__formattag(track, 'TRACKNUMBER')
        if track.get('TOTALTRACKS'):
            Nums[1] = int(track.get('TOTALTRACKS'))
            self.__formattag(track, 'TOTALTRACKS')
        tag.setTrackNum(tuple(Nums))
                
        Nums = [None, None]
        if track.get('DISCNUMBER'):
            Nums[0] = int(track.get('DISCNUMBER'))
            self.__formattag(track, 'DISCNUMBER')
        if track.get('TOTALDISCS'):
            Nums[1] = int(track.get('TOTALDISCS'))
            self.__formattag(track, 'TOTALDISCS')
        tag.setDiscNum(tuple(Nums))
        
        if track.get('COMPILATION'):
            if bool(track['COMPILATION']):
                tag.setTextFrame("TCMP", "1")
                self.console.write(TAG_FMT % ('COPMPILATION', u"1"))
            
        if track.get('COMMENT'):
            tag.removeComments()
            tag.addComment(track.get('COMMENT'))
            self.console.write(TAG_FMT % ('COMMENT', '\n' + track.get('COMMENT', u"")))
        if track.get('ALBUMART'):
            if os.path.isfile(track.get('ALBUMART').encode(options.syscharset)):
                tag.addImage(eyeD3.ImageFrame.FRONT_COVER, track.get('ALBUMART').encode(options.syscharset))
        
        tag.update()
        return 0
