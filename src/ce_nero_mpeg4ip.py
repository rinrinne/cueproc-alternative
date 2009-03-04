# -*- coding: utf-8 -*-

"""
    Output Plugin for Nero Digital MPEG-4 & 3GPP Encoder (with mpeg4ip)

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

def append_meta(args, name, value):
    if value:
        args.append(qstr('-meta:%s=%s' % (name, value)))

def append_meta_user(args, name, value):
    if value:
        args.append(qstr('-meta-user:%s=%s' % (name, value)))

class NeroMP4Output(OutputModule):
    def __init__(self):
        self.name = 'neromp4_ip'
        self.is_utf8 = False
        self.ext = '.m4a'
        self.cmd = 'neroaacenc_sse2'
        self.cmdtag = 'mp4tags'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'Nero Digital Audio Reference MPEG-4 & 3GPP Audio Encoder',
            'mp4tags -- tool to set iTunes-compatible metadata tags',
            )
        self.doc.commands = (self.cmd, self.cmdtag)
        self.doc.limitations = None,
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE','COMMENT',
            'NUMTRACKS','DISCNUMBER','TOTALDISCS','URL','COPYRIGHT','COMPOSER',
            'ISRC','ALBUMART'
        )

    def handle_track(self, track, options):
        # Add the command line to read the source audio.
        args = []       
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for neroaacenc_sse2.
        args.append(qstr(self.cmd))
        args.append(track.get('output_option'))
        args.append(optstr('-if', '-'))
        args.append(optstr('-of', track['output']))

        # Encode the track
        cmdline = args_to_string(args)
        self.console.execute(cmdline)

        # Tag the file.
        args = []
        args.append(qstr(self.cmdtag))
        args.append(optstr('-A', track.get('ALBUM')))
        args.append(optstr('-a', track.get('ARTIST')))
        args.append(optstr('-b', track.get('TEMPO')))
        args.append(optstr('-c', track.get('COMMENT')))
        args.append(optstr('-d', track.get('DISCNUMBER')))
        args.append(optstr('-D', track.get('TOTALDISCS')))
        args.append(optstr('-g', track.get('GENRE')))
        args.append(optstr('-G', track.get('GROUPING')))
        args.append(optstr('-P', track.get('ALBUMART')))
        args.append(optstr('-R', track.get('ALBUMARTIST')))
        args.append(optstr('-s', track.get('TITLE')))
        args.append(optstr('-t', track.get('TRACKNUMBER')))
        args.append(optstr('-T', track.get('TOTALTRACKS')))
        if track.get('COMPILATION'):
            if bool(track['COMPILATION']):
                args.append('-V 1')
        args.append(optstr('-w', track.get('COMPOSER')))
        args.append(optstr('-y', track.get('DATE')))
        args.append(qstr(track['output']))
        args.append(track.get('output_option_tag'))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
