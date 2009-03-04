#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    CueProc setup.

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

from distutils.core import setup
import py2exe

setup(
    name='cueproc',
    version='1.9',
    description='Cuesheet Processor (CueProc)',
    author='nyaochi',
    author_email='nyaochi2008@nyaochi.sakura.ne.jp',
    url='http://nyaochi.sakura.ne.jp/',
    py_modules=[
        "cueproc",
        "celib",
        "cuesheet",
        "ce_getaudio",
        "ce_oggenc",
        "ce_lame",
        "ce_fiismp3",
        "ce_hmp3",
        "ce_ctmp4",
        "ce_nero",
        "ce_mpc",
        "ce_wma",
        ],
    console=['cueproc.py'],
    options={"py2exe": {"packages": ["encodings"]}},
    )
