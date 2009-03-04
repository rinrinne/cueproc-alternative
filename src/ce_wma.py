# -*- coding: utf-8 -*-

"""
    Output Plugin for Windows Media Audio (WMA) via WMCmd.vbs.

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

import os
from celib import *

class WmaOutput(OutputModule):
    def __init__(self):
        self.name = 'wma'
        self.is_utf8 = False
        self.ext = '.wma'
        self.cmd = 'cscript "C:\Program Files\Windows Media Components\Encoder\WMCmd.vbs"'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'Microsoft (R) Windows Media Encoder Command Line Script Utility (2006-08-25)',
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = ''
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE','COPYRIGHT'
            )

    def handle_track(self, track, options):
        # Generate a name for a temporary WAVE file for this track.
        tmpfn = os.tempnam(options.tempdir, 'track') + '.wav'

        # Send the audio data of this track to the temporay file.
        args = []
        args.append(track['input_cmdline'])
        args.append('>')
        args.append(qstr(tmpfn))
        cmdline = args_to_string(args)
        self.console.execute(cmdline)
        
        # Encode the temporary file by using WMCmd.vbs.
        args = []
        args.append(self.cmd)
        args.append(optstr('-title', track.get('TITLE')))
        args.append(optstr('-author', track.get('ARTIST')))
        args.append(optstr('-album', track.get('ALBUM')))
        args.append(optstr('-trackno', track.get('TRACKNUMBER')))
        args.append(optstr('-genre', track.get('GENRE')))
        args.append(optstr('-year', track.get('DATE')))
        args.append(optstr('-copyright', track.get('COPYRIGHT')))
        args.append('-audioonly')
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append(optstr('-input', tmpfn))
        args.append(optstr('-output', track['output']))
        cmdline = args_to_string(args)
        self.console.execute(cmdline)

        # Remove the temporary file.
        os.remove(tmpfn)
