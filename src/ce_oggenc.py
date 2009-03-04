# -*- coding: utf-8 -*-

"""
    Output Plugin for Ogg Vorbis Encoder (OggEnc).

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

from celib import *

def append_comment_field(args, name, value):
    if value:
        args.append(optstr('--comment', '%s=%s' % (name, str(value))))

class OggEncOutput(OutputModule):
    def __init__(self):
        self.name = 'oggenc'
        self.ext = '.ogg'
        # Windows does not support a UTF-8 command-line.
        self.is_utf8 = False
        self.cmd = 'oggenc'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'Ogg Vorbis Encoder (oggenc)',
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE','COMMENT',
            'COMPILATION', 'TOTALTRACKS', 'DISCNUMBER', 'TOTALDISCS',
            'COMPOSER', 'ISRC','BPM','COPYRIGHT','ALBUMARTIST'
            )

    def handle_track(self, track, options):
        args = []
        
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for oggenc.
        args.append(qstr(self.cmd))
        if self.is_utf8:
            args.append('--utf8')
        args.append(optstr('--title', track.get('TITLE')))
        args.append(optstr('--artist', track.get('ARTIST')))
        args.append(optstr('--album', track.get('ALBUM')))
        args.append(optstr('--tracknum', track.get('TRACKNUMBER')))
        args.append(optstr('--genre', track.get('GENRE')))
        args.append(optstr('--date', track.get('DATE')))
        append_comment_field(args, 'TOTALTRACKS', track.get('TOTALTRACKS'))
        append_comment_field(args, 'DISCNUMBER', track.get('DISCNUMBER'))
        append_comment_field(args, 'TOTALDISCS', track.get('TOTALDISCS'))
        append_comment_field(args, 'COMPOSER', track.get('COMPOSER'))
        append_comment_field(args, 'ISRC', track.get('ISRC'))
        append_comment_field(args, 'COMMENT', track.get('COMMENT'))
        append_comment_field(args, 'COPYRIGHT', track.get('COPYRIGHT'))
        append_comment_field(args, 'BPM', track.get('BPM'))
        if bool(track.get('COMPILATION')):
            append_comment_field(args, 'COMPILATION', '1')
            append_comment_field(args, 'ALBUMARTIST', track.get('ALBUMARTIST'))
            append_comment_field(args, 'ALBUM ARTIST', track.get('ALBUMARTIST'))
        args.append(optstr('-o', track['output']))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
