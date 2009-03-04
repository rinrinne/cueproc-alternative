# -*- coding: utf-8 -*-

"""
    Output Plugin for Coding Technology MP4 encoder.

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
        args.append(u'-meta:%s="%s"' % (name, value))

def append_meta_user(args, name, value):
    if value:
        args.append(u'-meta-user:%s="%s"' % (name, value))

class CTMP4Output(OutputModule):
    def __init__(self):
        self.name = 'ctmp4'
        self.is_utf8 = False
        self.ext = '.mp4'
        self.cmd = 'enc_aacplus'
        self.cmdtag = 'neroaactag'

        self.doc = OutputModuleDocument()
        self.doc.tools = (
            'AACPlus v2 Encoder (using Winamp 5.3 enc_aacplus.dll)',
            'MP4Box',
            'Nero Digital Audio Reference MPEG-4 & 3GPP Audio Tagger',
            )
        self.doc.commands = (self.cmd, 'mp4box', self.cmdtag)
        self.doc.limitations = None
        self.doc.tags = (
            'TITLE','ARTIST','ALBUM','TRACKNUMBER','GENRE','DATE',
            'TOTALTRACKS', 'DISCNUMBER', 'TOTALDISCS', 'URL',
            'COPYRIGHT', 'COMMENT', 'COMPOSER', 'ISRC',
            )

    def handle_track(self, track, options):
        args = []       
        args.append(track['input_cmdline'])
        args.append('|')
        args.append(qstr(self.cmd))
        args.append('-')
        args.append(qstr(track['output']))
        args.append(track.get('output_option'))
        args.append('--mp4box')
        cmdline = args_to_string(args)
        self.console.execute(cmdline)

        # Tag the file.
        args = []
        args.append(qstr(self.cmdtag))
        args.append(qstr(track['output']))
        append_meta(args, 'title', track.get('TITLE'))
        append_meta(args, 'artist', track.get('ARTIST'))
        append_meta(args, 'year', track.get('DATE'))
        append_meta(args, 'album', track.get('ALBUM'))
        append_meta(args, 'genre', track.get('GENRE'))
        append_meta(args, 'track', track.get('TRACKNUMBER'))
        append_meta(args, 'totaltracks', track.get('TOTALTRACKS'))
        append_meta(args, 'disc', track.get('DISCNUMBER'))
        append_meta(args, 'totaldiscs', track.get('TOTALDISCS'))
        append_meta(args, 'url', track.get('URL'))
        append_meta(args, 'copyright', track.get('COPYRIGHT'))
        append_meta(args, 'comment', track.get('COMMENT'))
        append_meta(args, 'composer', track.get('COMPOSER'))
        append_meta(args, 'isrc', track.get('ISRC'))
        # I don't want to standardize non-standard tag fields.
        # append_meta_user(args, 'albumartist', track.get('ALBUMARTIST'))

        # I'm not sure how to support the compilation flag for now.
        # if track.get('COMPILATION'):
        #   args.append(u'-meta-user:compilation=1')
        args.append(track.get('output_option_tag'))

        # Execute the command.
        cmdline = args_to_string(args)
        return self.console.execute(cmdline)
