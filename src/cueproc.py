#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    CueProc main.

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

This program requires Python 2.4 or later.
"""



# Program version and author
VERSION = '1.10'
AUTHOR = 'Nyaochi'



import codecs
import exceptions
import fnmatch
import logging
import optparse
import os
import sys
import string
import shutil

import cuesheet
from celib import *
import ce_getaudio
import ce_wave
import ce_oggenc
import ce_lame
import ce_lame_eyed3
import ce_fiismp3
import ce_hmp3
import ce_mpc
import ce_wma
import ce_ctmp4
import ce_nero
#import ce_nero_mpeg4ip
#import ce_nero_ap
import ce_flac
import ce_wavpack
import ce_extpipe



# Add audio input objects.
input_class_factory = [
    ce_getaudio.GetAudioInput(),
]

# Add audio output objects.
output_class_factory = [
    ce_wave.WaveOutput(),
    ce_flac.FlacOutput(),
    ce_wavpack.WavPackOutput(),
    ce_oggenc.OggEncOutput(),
    ce_lame.LameOutput(),
    ce_lame_eyed3.LameEyeD3Output(),
    ce_fiismp3.FiisMP3Output(),
    ce_hmp3.HelixMP3Output(),
    ce_mpc.MusePackOutput(),
    ce_wma.WmaOutput(),
    ce_ctmp4.CTMP4Output(),
    ce_nero.NeroMP4Output(),
#   ce_nero_mpeg4ip.NeroMP4Output(),
#   ce_nero_ap.NeroMP4Output(),
    ce_extpipe.GenericEncoderPipingOutput(),
]

def set_track_attributes(track, target, options, is_embedded):
    """Initialize track attributes (variables).

    This function updates the dictionary of the track.
    """

    # Set filename to the target file if the cuesheet is embedded.
    if is_embedded:
        track.filename = target
    else:
        if not os.path.isabs(track.filename):
            track.filename = os.path.join(os.path.dirname(target), track.filename)

    track.url = os.path.abspath(track.filename)

    track['audio'] = track.filename
    track['audio_path'] = os.path.dirname(track.filename)
    track['audio_path_drive'] = os.path.splitdrive(track['audio_path'])[0]
    track['audio_path_dir'] = os.path.splitdrive(track['audio_path'])[1]
    track['audio_base'] = os.path.basename(track.filename)
    track['audio_file'] = os.path.splitext(track['audio_base'])[0]
    track['audio_ext'] = os.path.splitext(track['audio_base'])[1]
    track['audio_absolute'] = track.url
    track['audio_absolute_path'] = os.path.dirname(track['audio_absolute'])
    track['audio_absolute_path_drive'] = os.path.splitdrive(os.path.dirname(track['audio_absolute_path']))[0]
    track['audio_absolute_path_dir'] = os.path.splitdrive(os.path.dirname(track['audio_absolute_path']))[1]
    track['cuesheet'] = target
    track['cuesheet_path'] = os.path.dirname(target)
    track['cuesheet_path_drive'] = os.path.splitdrive(track['cuesheet_path'])[0]
    track['cuesheet_path_dir'] = os.path.splitdrive(track['cuesheet_path'])[1]
    track['cuesheet_base'] = os.path.basename(target)
    track['cuesheet_file'] = os.path.splitext(track['cuesheet_base'])[0]
    track['cuesheet_ext'] = os.path.splitext(track['cuesheet_base'])[1]
    track['cuesheet_absolute'] = os.path.abspath(target)
    track['cuesheet_absolute_path'] = os.path.dirname(track['cuesheet_absolute'])
    track['cuesheet_absolute_path_drive'] = os.path.splitdrive(os.path.dirname(track['cuesheet_absolute_path']))[0]
    track['cuesheet_absolute_path_dir'] = os.path.splitdrive(os.path.dirname(track['cuesheet_absolute_path']))[1]
    track['audio_range_begin'] = track.begin
    track['audio_range_end'] = track.end
    track['cuesheet_embedded'] = is_embedded

    track['output_plugin'] = options.codec
    track['output_command'] = options.encodercmd

    track['quot'] = '"'

def set_compilation_flag(tracks):
    # Collect artist names in the tracks
    artists = set()
    for track in tracks:
        artists.add(track['ARTIST'])

    # Determine the compilation flag.
    compilation = (len(artists) != 1)
    
    for track in tracks:
        if not track.has_key('COMPILATION'):
            track['COMPILATION'] = compilation

def set_albumart(track, options):
    if not track.get('ALBUMART'):
        images = options.albumart_files.split(',')
        images.append('%s.jpg' % track['cuesheet_file'])
        images.append('%s.jpeg' % track['cuesheet_file'])
        images.append('%s.png' % track['cuesheet_file'])
        images.append('%s.gif' % track['cuesheet_file'])
        for image in images:
            name = evaluate_expression(image, track, globals(), locals())
            fn = os.path.join(track['cuesheet_path'], name)
            if os.path.exists(fn):
                track['ALBUMART'] = fn
                break

def copy_albumart(track, options):
    src = track.get('ALBUMART')
    if src is not None:
        filepart = os.path.basename(src)
        dst = os.path.join(track['output_path'], filepart)
        if not os.path.exists(dst) or os.path.getmtime(dst) < os.path.getmtime(src):
            shutil.copy2(src, dst)

def open_text(target, charset):
    boms = (
        (codecs.BOM_UTF8, 'utf8'),
        (codecs.BOM_UTF16, 'utf16'),
        (codecs.BOM_UTF32, 'utf32'),
        )
    
    f = open(target, 'rb')
    test = f.read(4)
    for bom, cs in boms:
        if test.startswith(bom):
            fi = codecs.open(target, 'r', cs)
            fi.read(len(bom))
            return fi
    return codecs.open(target, 'r', charset)

def open_target(target, options):
    """Open a target cuesheet.

    This function parse the target cuesheet and returns a list of tracks.
    If the target file is an audio file with an embedded cuesheet, the
    function uses an input audio object to obtain the CUESHEET tag value.
    """

    is_embedded = False
    # Check the extension of the target cuesheet
    if target.lower().endswith('.cue'):
        # An external cuesheet
        fi = open_text(target, options.cscharset)
        tracks = cuesheet.reader(fi, options.hidden_track1)
    else:
        # Possibly an embedded cuesheet
        inobj = find_input_object(input_class_factory, target, options)
        if not inobj:
            return
        lines = inobj.get_tag(target, "CUESHEET", options)
        if not lines:
            return
        tracks = cuesheet.reader(
            lines,
            options.hidden_track1
            )
        is_embedded = True

    # Initialize track attributes.
    for track in tracks:
        set_track_attributes(track, target, options, is_embedded)

    return tracks

def warn(msg):
    print >>sys.stderr, 'WARNING:', msg

def error(msg):
    print >>sys.stderr, 'ERROR:', msg

def list_codec(fo, options):
    """List the names of all supported codecs.
    """

    fo.write('Supported codecs:\n')
    for outobj in output_class_factory:
        fo.write('  %s\n' % outobj.name)

def show_help_codec(fo, name):
    """Show information about the output codec.
    """

    # Find an output object with the specified name.
    outobj = find_object_by_name(output_class_factory, name)
    if not outobj:
        warn("No suitable output codec found for '%s'" % name)

    if outobj.doc.tools:
        fo.write('Tool:\n')
        for tool in outobj.doc.tools:
            fo.write('  %s\n' % tool)
    if outobj.doc.commands:
        fo.write('Dependencies:\n')
        for command in outobj.doc.commands:
            fo.write('  %s\n' % command)
    if outobj.doc.limitations:
        fo.write('Limitations:\n')
        for limitation in outobj.doc.limitations:
            fo.write('  %s\n' % limitation)
    if outobj.doc.tags:
        fo.write('Supported fields:\n')
        l = list(outobj.doc.tags)
        l.sort(lambda x, y: cmp(x, y))
        for tag in l:
            fo.write('  %s\n' % tag)

    fo.write('Default extension: %s\n' % outobj.ext)

def show_help_all_codecs(fo, options):
    """Show information about all output codec.
    """

    for outobj in output_class_factory:
        fo.write('[%s]\n' % outobj.name)
        show_help_codec(fo, outobj.name)
        fo.write('\n')

def show_variables(fo, track):
    """Show values of all variables in the track.
    """

    fo.write('Variables:\n')
    l = track.items()
    l.sort(lambda x, y: cmp(x[0], y[0]))
    for name, value in l:
        line = u'  %s=%s' % (name, value)
        fo.write(line)
        fo.write('\n')

def find_callback((fo, encoding, pattern), dirname, names):
    dirname = dirname.decode(encoding)
    for name in names:
        name = name.decode(encoding)
        if fnmatch.fnmatch(name, pattern):
            fo.write(os.path.join(dirname, name))
            fo.write('\n')
    
def find(fo, options):
    os.path.walk('', find_callback, (fo, options.syscharset, options.find))

def get_track_range(strrange):
    track_list = []
    values = strrange.split(',')
    for value in values:
        track_list.append(int(value))
    track_list.sort()
    return track_list

def process(options, target):
    fo = sys.stdout
    fe = sys.stderr

    # Find an output object with the specified name.
    outobj = find_object_by_name(output_class_factory, options.codec)
    if not outobj:
        warn('No suitable output class found')
        return

    # Change the encoder command if specified.
    if options.encodercmd:
        outobj.cmd = options.encodercmd
    if options.encoderext:
        outobj.ext = options.encoderext

    # Bind console object
    console = Console()
    console.syscharset = options.syscharset
    if options.rehearsal:
        console.executable = False
    if options.hide_cmdln:
        console.writable = False
    outobj.console = console

    # Open the target.
    tracks = open_target(target, options)
    if not tracks:
        warn('Failed to open a target, %s' % target)
        return

    # Determine compilation flag.
    if options.auto_compilation:
        set_compilation_flag(tracks)

    #
    valid_tracks = None
    if options.track:
        valid_tracks = get_track_range(options.track)

    # Loop for tracks
    for track in tracks:
        # Check if we're going to process this track.
        if valid_tracks is not None:
            if track['tracknumber'] not in valid_tracks:
                continue

        # Determine albumart variable.
        if options.auto_albumart:
            set_albumart(track, options)

        # Report the progress.
        fo.write('CueProc: %s [%02d/%02d]\n' % (
            target, track['tracknumber'], int(track['TOTALTRACKS'])))

        # Determine an input module suitable for this track.
        inobj = find_input_object(input_class_factory, track.url, options)
        if not inobj:
            warn('No suitable input class found for track #%d, %s' % (
                track['tracknumber'],
                track.url)
                )
            continue

        # Obtain the command-line for extracting the source audio.
        incmdln = inobj.get_cmdln_track(track, outobj.is_utf8)

        # Generate an output directory name
        odir = evaluate_expression(options.outputdir, track, globals(), locals())
        odir = pstr(odir).strip()

        # Generate an output filename.
        ofn = evaluate_expression(options.outputfn, track, globals(), locals())
        ofn = fstr(ofn).strip()

        # Set more variables of the current track
        track['input_cmdline'] = incmdln
        track['output'] = os.path.join(odir, ofn + outobj.ext)
        track['output_ext'] = outobj.ext
        track['output_path'] = odir
        track['output_base'] = ofn

        # Evaluate output_cmdln variable.
        if options.outputcmdln:
            track['output_cmdline'] = evaluate_expression(
                options.outputcmdln[0], track, globals(), locals())
            for i in range(1, len(options.outputcmdln)):
                track['output_cmdline' + str(i)] = evaluate_expression(
                    options.outputcmdln[i], track, globals(), locals())

        # Evaluate output_option variable.
        track['output_option'] = ''
        if options.encoderopt:
            opts = []
            for encoderopt in options.encoderopt:
                opts.append(evaluate_expression(encoderopt, track, globals(), locals()))
            track['output_option'] = ' '.join(opts)

        # Set optional variables specified by options.setvars.
        for setvar in options.setvars:
            pos = setvar.find('=')
            if pos >= 0:
                name = setvar[:pos]
                value = setvar[pos+1:]
                track[name] = evaluate_expression(
                    value, track, globals(), locals())
            else:
                warn('Skipping an optional variable, %s' % strvar)

        # Show variables if specified.
        if options.show_variables:
            show_variables(sys.stdout, track)

        # Check the existence of the output file.
        print track['output']
        if not options.overwrite and os.path.exists(track['output']):
            warn('Skipping existing file, %s' % track['output'])
            continue

        # Create the output directory if it does not exist
        if not os.path.exists(os.path.dirname(track['output'])):
            os.makedirs(os.path.dirname(track['output']))

        # Copy albumart images if specified.
        if options.albumart_action in ('copy', 'both'):
            copy_albumart(track, options)

        # Remove albumart variable for 'copy' action so that
        # the output object cannot refer to this variable.
        if options.albumart_action == 'copy':
            if track.has_key('ALBUMART'):
                del track['ALBUMART']

        outobj.handle_track(track, options)

        fo.write('\n')

    return True

if __name__ == '__main__':
    # Show copyright information.
    sys.stderr.write('Cuesheet Processor (CueProc) Version %s Copyright (c) 2006-2008 by %s\n' % (VERSION, AUTHOR))
    sys.stderr.write('\n')

    # For py2exe use only. sitecustomize.py and site.py are not available for py2exe, but we can call sys.setdefaultencoding directly.
    # Force to use UTF-8 encoding for internal string representations for the best compatibility (to avoid so-called 'dame-moji' problem in Shift_JIS encoding)
    if hasattr(sys, 'setdefaultencoding'):
        sys.setdefaultencoding('utf8')

    # Define a command-line option parser.
    parser = optparse.OptionParser(
        usage="%prog [options] <target> [<target2> ...]\n"
        "Execute a job for each track in the target CD image(s).",
        version="CueProc %s" % VERSION
        )
    parser.add_option(
        "-c", "--output",
        action="store", type="string", dest="codec",
        metavar="PLUGIN",
        help="Specify an output plugin for the target(s)."
        )
    parser.add_option(
        "-x", "--outputcmd",
        action="store", type="string", dest="encodercmd",
        default='',
        metavar="COMMAND",
        help="Specify a command name for PLUGIN. "
        "An output plugin uses its default command name without this option specified.",
        )
    parser.add_option(
        "-p", "--outputopt",
        action="append", type="string", dest="encoderopt",
        default=None,
        metavar="PATTERN",
        help="Specify a template pattern to pass optional arguments to PLUGIN. "
        "Variable expressions ${<variable-name>} will be replaced with the actual values for the track(s). "
        "Conditional expressions such as #if{<condition>}, #elif{<condition>}, #else, #endif will be evaluated, where a condition <condition> is expressed by a Python code snippet.",
        )
    parser.add_option(
        "-e", "--outputext",
        action="store", type="string", dest="encoderext",
        default='',
        metavar="EXT",
        help="Specify an extension for output files. "
        "An output plugin uses its default extension without this option specified.",
        )
    parser.add_option(
        "-o", "--outputfn",
        action="store", type="string", dest="outputfn",
        default='${TRACKNUMBER}_${TITLE}',
        metavar="PATTERN",
        help="Specify a template pattern for output filenames. "
        "Although the specification of template pattern is the same as -p (--outputopt) option, any characters invalid for a filename will be replaced with spaces."
        )
    parser.add_option(
        "-d", "--outputdir",
        action="store", type="string", dest="outputdir",
        default=".",
        metavar="PATTERN",
        help="Specify a template pattern for output directory names. "
        "Although the specification of template pattern is the same as -p (--outputopt) option, any characters invalid for a directory name will be replaced with spaces."
        )
    parser.add_option(
        "-m", "--outputcmdln",
        action="append", type="string", dest="outputcmdln",
        default=[],
        metavar="PATTERN",
        help="Specify a template pattern for 'extpipe' plugin. "
        "The specification of template pattern is the same as -p (--outputopt) option. "
        "The plugin can invoke multiple processes sequencially with this option specified multiple times."
        )
    parser.add_option(
        "-s", "--setvar",
        action="append", type="string", dest="setvars", metavar="NAME=VALUE",
        default=[],
        help="Define a user-defined track variable whose name is NAME and value is VALUE. "
        "This option can also overwrite the value of an existing variable. "
        "NAME must consist of alphanumeric and '_' letters. "
        "VALUE will be evaluated as a pattern similarly to the -p (--outputopt) option."
        )
    parser.add_option(
        "--no-auto-compilation",
        action="store_false", dest="auto_compilation",
        default=True,
        help="By default, CueProc sets COMPILATION flag to true for all tracks in the target cuesheet with multiple distinct PERFORMER names. "
        "This option disables the automatic process of activating compilation flag."
        )
    parser.add_option(
        "--albumart-files",
        action="store", dest="albumart_files",
        default="cover.jpg,albumart.jpg,folder.jpg",
        help="Specify the list of files for albumart images in comma-separated values. "
        "CueProc sets ALBUMART variable if one of these file exists in the same directory as the cuesheet. "
        " The default value of the list is, 'cover.jpg,albumart.jpg,folder.jpg'."
        )
    parser.add_option(
        "--no-auto-albumart",
        action="store_false", dest="auto_albumart",
        default=True,
        help="This option disables the automatic detection of albumart image based on the esistence of image files."
        )
    parser.add_option(
        "--albumart-action",
        action="store", dest="albumart_action",
        choices=("embed", "copy", "both"),
        default="embed",
        help="This option specifies the action when albumart images are detected, embed to output files (embed), copy to output directories (copy), or both (both)."
        )
    parser.add_option(
        "-t", "--track",
        action="store", type="string", dest="track",
        default=None,
        help="Specify track range where the job is applicable in comma separated values (CSV)."
        )
    parser.add_option(
        "--hidden-track1",
        action="store_true", dest="hidden_track1",
        default=False,
        help="This option assumes the first track to begin at INDEX 00 (or PREGAP)."
        )
    parser.add_option(
        "--target",
        action="store", type="string", dest="targets",
        default=None,
        help="Specify a text file describing the list of target filenames. Useful for converting a number of CD images at a time with a list file generated by --find option."
        )
    parser.add_option(
        "-W", "--syscharset",
        action="store", type="string", dest="syscharset",
        default="mbcs",
        help="Specify a charset for the current operating system. The default value for this option is '%default'."
        )
    parser.add_option(
        "-w", "--cscharset",
        action="store", type="string", dest="cscharset",
        default="mbcs",
        help="Specify a charset for the target cuesheet(s). The default value for this option is '%default'."
        )
    parser.add_option(
        "-f", "--overwrite",
        action="store_true", dest="overwrite",
        help="Force to overwrite existing output files. "
        "The default behavior (not overwriting) is useful "
        "to process tracks only in new CD images."
        )
    parser.add_option(
        "--tempdir",
        action="store", type="string", dest="tempdir",
        default=None,
        help="Specify a directory for temporary files to which some plugins create during the jobs."
        )
    parser.add_option(
        "-n", "--rehearsal",
        action="store_true", dest="rehearsal",
        help="Do not execute the jobs but only shows command-lines to be invoked by this program. Useful for debugging a job without running it."
        )
    parser.add_option(
        "--find",
        action="store", type="string", dest="find", metavar="PATTERN",
        default=None,
        help="Find files under the current directory (including its sub directories) that match the specified pattern."
        )
    parser.add_option(
        "--show-variables",
        action="store_true", dest="show_variables",
        help="Show values of the track variable for each track in the target(s). "
        "This option provides useful information for debugging a job."
        )
    parser.add_option(
        "-l", "--list-plugin",
        action="store_true", dest="list_codec",
        help="List names of installed plugins."
        )
    parser.add_option(
        "--help-plugin",
        action="store", dest="help_codec", metavar="PLUGIN",
        help="Show documentation for the specified plugin."
        )
    parser.add_option(
        "--help-all-plugins",
        action="store_true", dest="help_all_codecs",
        help="Show documentation for all installed plugins."
        )
    parser.add_option(
        "--hide-cmdln",
        action="store_true", dest="hide_cmdln",
        help="Do not display command-lines invoked by this program."
        )

    # Parse command-line arguments.
    (options, args) = parser.parse_args()

    # Wrap IO streams.
    sys.stdout = codecs.getwriter(options.syscharset)(sys.stdout)
    sys.stderr = codecs.getwriter(options.syscharset)(sys.stderr)
    fo = sys.stdout
    fe = sys.stderr

    # Run the jobs.
    if options.list_codec:
        list_codec(fo, options)
    elif options.help_codec:
        show_help_codec(fo, options.help_codec)
    elif options.help_all_codecs:
        show_help_all_codecs(fo, options)
    elif options.find:
        find(fo, options)
    else:
        # Determine targets.
        targets = []
        for arg in args:
            targets.append(arg.decode(options.syscharset))
        if options.targets:
            f = open_text(options.targets, options.syscharset)
            targets += map(string.strip, f.readlines())

        if not targets:
            warn("No target specified. Use -h or --help to see the usage.")
            sys.exit(1)

        # Execulte job(s)
        for target in targets:
            process(options, target)
