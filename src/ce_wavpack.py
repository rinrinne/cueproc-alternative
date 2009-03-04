# -*- coding: utf-8 -*-

"""
    Output Plugin for WavPack

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

class WavPackOutput(OutputModule):
    def __init__(self):
        self.name = 'wavpack'
        self.is_utf8 = False
        self.ext = '.wv'
        self.cmd = 'wavpack'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'WavPack Encoder',
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','ALBUMARTIST','GENRE','DATE',
            'TRACKNUMBER','TOTALTRACKS','DISCNUMBER','TOTALDISCS','COMMENT'
            )

    def handle_track(self, track, options):
        args = []
        
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for lame.
        args.append(qstr(self.cmd))
        args.append(optstr3('-w', 'Title=', track.get('TITLE')))
        args.append(optstr3('-w', 'Artist=', track.get('ARTIST')))
        args.append(optstr3('-w', 'Album=', track.get('ALBUM')))
        args.append(optstr3('-w', 'Albumartist=', track.get('ALBUMARTIST')))
        args.append(optstr3('-w', 'Track=', track.get('TRACKNUMBER')))
        args.append(optstr3('-w', 'Totaltracks=', track.get('TOTALTRACKS')))
        args.append(optstr3('-w', 'Disc=', track.get('DISCNUMBER')))
        args.append(optstr3('-w', 'Totaldiscs=', track.get('TOTALDISCS')))
        args.append(optstr3('-w', 'Genre=', track.get('GENRE')))
        args.append(optstr3('-w', 'Date=', track.get('DATE')))
        args.append(optstr3('-w', 'Comment=', track.get('COMMENT')))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')
        args.append(qstr(track['output']))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
