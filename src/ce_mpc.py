# -*- coding: utf-8 -*-

"""
    Output Plugin for MusePack encoder

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

class MusePackOutput(OutputModule):
    def __init__(self):
        self.name = 'mpc'
        self.is_utf8 = False
        self.ext = '.mpc'
        self.cmd = 'mppenc'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'MusePack Encoder (mppenc)',
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE','COMPILATION'
            )

    def handle_track(self, track, options):
        args = []
        
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for mppenc.
        args.append(qstr(self.cmd))
        args.append(optstr('--title', track.get('TITLE')))
        args.append(optstr('--artist', track.get('ARTIST')))
        args.append(optstr('--album', track.get('ALBUM')))
        args.append(optstr('--track', track.get('TRACKNUMBER')))
        args.append(optstr('--genre', track.get('GENRE')))
        args.append(optstr('--releasedate', track.get('DATE')))
        if bool(track.get('COMPILATION')):
            args.append(optstr('--tag', 'compilation=1'))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')
        args.append(qstr(track['output']))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
