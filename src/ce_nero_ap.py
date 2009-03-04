# -*- coding: utf-8 -*-

"""
    Output Plugin for Nero Digital MPEG-4 & 3GPP Encoder
                                                (with AtomicParsley)

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

class NeroMP4Output(OutputModule):
    def __init__(self):
        self.name = 'neromp4_ap'
        self.is_utf8 = False
        self.ext = '.m4a'
        self.cmd = 'neroaacenc_sse2'
        self.cmdtag = 'atomicparsley'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'Nero Digital Audio Reference MPEG-4 & 3GPP Audio Encoder',
            'AtomicParsley',
            )
        self.doc.commands = (self.cmd, self.cmdtag)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE','COMMENT',
            'NUMTRACKS','DISCNUMBER','TOTALDISCS','COPYRIGHT','COMPOSER',
            'ALBUMARTIST', 'COMPILATION', 'ALBUMART'
        )

    def handle_track(self, track, options, func):
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
        func(cmdline, options)

        # Tag the file.
        args = []
        args.append(qstr(self.cmdtag))
        args.append(qstr(track['output']))
        args.append(optstr('--artist', track.get('ARTIST')))
        args.append(optstr('--title', track.get('TITLE')))
        args.append(optstr('--album', track.get('ALBUM')))
        args.append(optstr('--genre', track.get('GENRE')))
        if track.has_key('TRACKNUMBER'):
            if track.has_key('NUMTRACKS'):
                args.append(optstr(
                    '--tracknum',
                    track['TRACKNUMBER'] + '/' + str(track['NUMTRACKS'])
                    ))
            else:
                args.append(optstr('--tracknum', track['TRACKNUMBER']))
        if track.has_key('DISCNUMBER'):
            if track.has_key('TOTALDISCS'):
                args.append(optstr(
                    '--tracknum',
                    track['DISCNUMBER'] + '/' + str(track['TOTALDISCS'])
                    ))
            else:
                args.append(optstr('--tracknum', track['DISCNUMBER']))
        args.append(optstr('--comment', track.get('COMMENT')))
        args.append(optstr('--year', track.get('DATE')))
        args.append(optstr('--composer', track.get('COMPOSER')))
        args.append(optstr('--copyright', track.get('COPYRIGHT')))
        args.append(optstr('--artwork', track.get('ALBUMART')))
        args.append(optstr('--albumArtist', track.get('ALBUMARTIST')))
        if track.has_key('COMPILATION'):
            if bool(track['COMPILATION']):
                args.append(optstr('--compilation', 'true'))
            else:
                args.append(optstr('--compilation', 'false'))
        args.append(track.get('output_option_tag'))

        # Execute the command.
        cmdline = args_to_string(args)
        return func(cmdline, options)
