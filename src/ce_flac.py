# -*- coding: utf-8 -*-

"""
    Output Plugin for FLAC

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

class FlacOutput(OutputModule):
    def __init__(self):
        self.name = 'flac'
        self.is_utf8 = False
        self.ext = '.flac'
        self.cmd = 'flac'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'FLAC Encoder',
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','ALBUMARTIST','TRACKNUMBER',
            'TOTALTRACKS','DISCNUMBER','TOTALDISCS','GENRE','DATE','COMMENT',
            'ALBUMART')

    def handle_track(self, track, options):
        args = []
        
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for lame.
        args.append(qstr(self.cmd))
        args.append(optstr3('-T', 'Title=', track.get('TITLE')))
        args.append(optstr3('-T', 'Artist=', track.get('ARTIST')))
        args.append(optstr3('-T', 'Album=', track.get('ALBUM')))
        args.append(optstr3('-T', 'Albumartist=', track.get('ALBUMARTIST')))
        args.append(optstr3('-T', 'Tracknumber=', track.get('TRACKNUMBER')))
        args.append(optstr3('-T', 'Totaltracks=', track.get('TOTALTRACKS')))
        args.append(optstr3('-T', 'Discnumber=', track.get('DISCNUMBER')))
        args.append(optstr3('-T', 'Totaldiscs=', track.get('TOTALDISCS')))
        args.append(optstr3('-T', 'Genre=', track.get('GENRE')))
        args.append(optstr3('-T', 'Date=', track.get('DATE')))
        args.append(optstr3('-T', 'Comment=', track.get('COMMENT')))
        args.append(optstr('--picture', track.get('ALBUMART')))
        args.append(optstr('-o', track['output']))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
