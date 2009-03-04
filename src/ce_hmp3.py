# -*- coding: utf-8 -*-

"""
    Output Plugin for Helix MP3 encoder

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

class HelixMP3Output(OutputModule):
    def __init__(self):
        self.name = 'hmp3'
        self.is_utf8 = False
        self.ext = '.mp3'
        self.cmd = 'hmp3'
        self.cmdtag = 'tag'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'Helix MPEG Layer III audio encoder (hmp3)',
            'Tag - Automatic Tag from filename',
            )
        self.doc.commands = (self.cmd, self.cmdtag)
        self.doc.limitations = (
            'Writes APEv2 tags',
            )
        self.doc.tags = ('TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE')

    def handle_track(self, track, options):
        # Add the command line to read the source audio.
        args = []
        args.append(track['input_cmdline'])
        args.append('|')

        # Add arguments for mp3sencoder.
        args.append(qstr(self.cmd))
        args.append(qstr('-'))
        args.append(qstr(track['output']))
        args.append(track.get('output_option'))
        cmdline = args_to_string(args)
        self.console.execute(cmdline)

        # Tag the output file.
        args = []
        args.append(qstr(self.cmdtag))      
        args.append(optstr('--title', track.get('TITLE')))
        args.append(optstr('--artist', track.get('ARTIST')))
        args.append(optstr('--album', track.get('ALBUM')))
        args.append(optstr('--track', track.get('TRACKNUMBER')))
        args.append(optstr('--genre', track.get('GENRE')))
        args.append(optstr('--year', track.get('DATE')))
        args.append('--ape2')
        args.append(track.get('output_option_tag'))
        args.append(qstr(track['output']))

        # if track.get('COMPILATION'):
        #   args.append(optstr('--comment', 'COMPILATION=1'))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
