# -*- coding: utf-8 -*-

"""
    Output Plugin for Microsoft Riff-WAVE.

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

class WaveOutput(OutputModule):
    def __init__(self):
        self.name = 'wave'
        self.is_utf8 = False
        self.ext = '.wav'
        self.cmd = ''

        self.doc = OutputModuleDocument()
        self.doc.tools = None
        self.doc.commands = None
        self.doc.limitations = None
        self.doc.tags = None

    def handle_track(self, track, options):
        args = []
        args.append(track['input_cmdline'])
        args.append('>')
        args.append(qstr(track['output']))
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
