# -*- coding: utf-8 -*-

"""
    CueProc standard library.

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

import exceptions
import os
import string
import sys

class InvalidParameter(exceptions.ValueError):
    pass

def qstr(value):
    """ Convert the value to a unicode string quoted if necessary.
    """
    value = unicode(value)
    escapes = (' ', "'", '&', '<', '>', '|')
    for escape in escapes:
        if value.find(escape) >= 0:
            return u'"' + value + u'"'
    return value

def fstr(value):
    """ Convert the value to a unicode string suitable for a filename.
    """
    value = value.replace('\\', ' ')
    value = value.replace('/', ' ')
    value = value.replace(':', ' ')
    value = value.replace('*', ' ')
    value = value.replace('?', ' ')
    value = value.replace('"', ' ')
    value = value.replace('<', ' ')
    value = value.replace('>', ' ')
    value = value.replace('|', ' ')
    return value

def pstr(value):
    """ Convert the value to a unicode string suitable for a filename.
    """
    value = value.replace('*', ' ')
    value = value.replace('?', ' ')
    value = value.replace('"', ' ')
    value = value.replace('<', ' ')
    value = value.replace('>', ' ')
    value = value.replace('|', ' ')
    return value

class optstr:
    def __init__(self, name = None, value = None):
        self.name = name
        self.value = value
    def __unicode__(self):
        if self.name is not None and self.value is not None:
            return unicode(qstr(self.name)) + u' ' + unicode(qstr(self.value))
        else:
            return u''

class optstr3:
    def __init__(self, name = None, name2 = None, value = None):
        self.name = name
        self.name2 = name2
        self.value = value
    def __unicode__(self):
        if self.name is not None and self.name2 is not None and self.value is not None:
            return unicode(qstr(self.name)) + u' ' + unicode(qstr(self.name2 + self.value))
        else:
            return u''

def args_to_string(args):
    l = []
    for arg in args:
        if arg is not None and arg:
            l.append(unicode(arg))
    return unicode(' ').join(l)

class Console:
    def __init__(self):
        self.writable = True
        self.executable = True
        self.syscharset = 'iso8859-1'

    def write(self, line):
        if self.writable:
            sys.stdout.write(line)
            sys.stdout.write('\n')

    def execute(self, line):
        if self.writable:
            sys.stderr.write(line)
            sys.stderr.write('\n')
        if self.executable:
            return os.system(line.encode(self.syscharset))
        else:
            return -1

class InputModule:
    def __init__(self):
        pass
    def get_cmdln_track(self, track, is_utf8, extopt = ''):
        pass
    def test(self, filename):
        pass

class OutputModuleDocument:
    def __init__(self):
        self.tools = None
        self.commands = None
        self.limitations = None
        self.tags = None

class OutputModule:
    def __init__(self):
        self.name = None
        self.ext = None
        self.console = None
        self.is_utf8 = False
        self.doc = OutputModuleDocument()
    def handle_track(self, track, incmdln):
        pass

def find_input_object(cf, filename, options):
    for obj in cf:
        if obj.test(filename, options):
            return obj
    return None

def find_object_by_name(cf, name):
    for obj in cf:
        if obj.name == name:
            return obj
    return None

def evaluate_expression(strexp, track, globals, locals):
    # Evaluate conditions in strexp.
    tmpl = ''           # Resultant template string.
    conditions = []     # Condition stack.
    i = 0
    while i < len(strexp):
        if strexp.startswith('##', i):
            tmpl += '#'
            i += 2
        elif strexp.startswith('#if{', i):
            begin = i + 4
            end = strexp.find('}', begin)
            if begin <= end:
                b = eval(strexp[begin:end], globals, locals)
                conditions.append(b)
                i = end + 1
            else:
                raise exceptions.ValueError("'}' is missing (pos = %d)\n%s" % (i, strexp))
        elif strexp.startswith('#elif{', i):
            conditions.pop()
            begin = i + 6
            end = strexp.find('}', begin)
            if begin <= end:
                b = eval(strexp[begin:end], globals, locals)
                conditions.append(b)
                i = end + 1
            else:
                raise exceptions.ValueError("'}' is missing (pos = %d)\n%s" % (i, strexp))
        elif strexp.startswith('#else', i):
            if not conditions:
                raise exceptions.ValueError("Corresponding #if is missing (pos = %d)\n%s" % (i, strexp))
            i += 5
            b = conditions.pop()
            condidions.append(not b)
        elif strexp.startswith('#endif', i):
            if not conditions:
                raise exceptions.ValueError("Corresponding #if is missing (pos = %d)\n%s" % (i, strexp))
            i += 6
            b = conditions.pop()
        elif not conditions or conditions[-1]:
            tmpl += strexp[i]
            i += 1
        else:
            i += 1

    return string.Template(tmpl).substitute(track)
