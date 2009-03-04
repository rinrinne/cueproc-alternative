# -*- coding: utf-8 -*-

"""
    Input Plugin for Generic audio (getaudio)

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

import string, unicodedata
from celib import *

class GetAudioInput(InputModule):
    def __init__(self):
        self.name = 'getaudio'
        self.cmd = 'getaudio'

    def get_cmdln_track(self, track, is_utf8 = False, extopt = ''):
        args = []
        args.append(qstr(self.cmd))
        if is_utf8:
            args.append('--utf8')
        if track.begin:
            args.append(optstr('--begin', track.begin))
        if track.end:
            args.append(optstr('--end', track.end))
        args.append(extopt)
        args.append(qstr(track.url))
        return args_to_string(args)

    def test(self, filename, options, is_utf8 = False):
        args = []
        args.append(qstr(self.cmd))
        if is_utf8:
            args.append('--utf8')
        args.append('--test')
        args.append(qstr(filename))
        cmdln = args_to_string(args)
        f = os.popen(cmdln.encode(options.syscharset), 'r')
        line = f.readline()
        return line.startswith('TEST OK')

    def get_tag(self, filename, tagname, options):
        args = []
        args.append(qstr(self.cmd))
        args.append('--utf8')
        args.append(optstr('--tag', tagname))
        args.append(qstr(filename))
        cmdln = args_to_string(args)
        f = os.popen(cmdln.encode(options.syscharset), 'r')
        line = f.readline()
        if line.startswith('GETTAG OK'):
            return map(lambda x: x.decode('utf8'), f.readlines())
