# -*- coding: utf-8 -*-

"""
    Output Plugin for LAME (for 3.98 or later)

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

class LameOutput(OutputModule):
    def __init__(self):
        self.name = 'lame'
        self.is_utf8 = False
        self.ext = '.mp3'
        self.cmd = 'lame'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            "LAME MP3 Encoder (3.98 or later)",
            )
        self.doc.commands = (self.cmd,)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUMARTIST','ALBUM','COMPOSER',
            'TRACKNUMBER','TOTALTRACKS','DISCNUMBER','TOTALDISCS',
            'GENRE','DATE','COMMENT','BPM','COPYRIGHT','COMPILATION',
            'ALBUMART'
            )

    def handle_track(self, track, options):
        args = []
        
        # Add the command line to read the source audio.
        args.append(track['input_cmdline'])
        
        # Pipe the source audio to this encoder.
        args.append('|')

        # Add arguments for lame.
        args.append(qstr(self.cmd))
        args.append('--add-id3v2')
        args.append('--ignore-tag-errors')
        args.append(optstr('--tt', track.get('TITLE')))
        args.append(optstr('--ta', track.get('ARTIST')))
        args.append(optstr3('--tv', 'TPE2=', track.get('ALBUMARTIST')))
        args.append(optstr3('--tv', 'TCOM=', track.get('COMPOSER')))
        args.append(optstr3('--tv', 'TCOP=', track.get('COPYRIGHT')))
        args.append(optstr('--tl', track.get('ALBUM')))
        if track.get('TRACKNUMBER'):
            if track.get('TOTALTRACKS'):
                args.append(optstr3('--tv', 'TRCK=', '%(TRACKNUMBER)s/%(TOTALTRACKS)s' % track))
            else:
                args.append(optstr3('--tv', 'TRCK=', '%(TRACKNUMBER)s' % track))
        if track.get('DISCNUMBER'):
            if track.get('TOTALDISCS'):
                args.append(optstr3('--tv', 'TPOS=', '%(DISCNUMBER)s/%(TOTALDISCS)s' % track))
            else:
                args.append(optstr3('--tv', 'TPOS=', '%(DISCNUMBER)s' % track))
        args.append(optstr3('--tv', 'TCON=', track.get('GENRE')))
        args.append(optstr('--ty', track.get('DATE')))
        args.append(optstr('--tc', track.get('COMMENT')))
        args.append(optstr3('--tv', 'TBPM=', track.get('BPM')))
        if track.get('COMPILATION'):
            if bool(track['COMPILATION']):
                args.append('--tv TCMP=1')
        args.append(optstr('--ti', track.get('ALBUMART')))
        args.append(track.get('output_option'))
        args.append(track.get('output_option_tag'))
        args.append('-')
        args.append(qstr(track['output']))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
