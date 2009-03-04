CueProc 1.9 (2007-06-10)
- Encoder 'lame_nyaochi' was removed to replace 'lame' codec. The 'lame' encoder now supports albumart images.
- New option, --albumart-action, to configure the action when albumart images are detected. CueProc now supports 'copy' action, which copies albumart images to the output directory.

CueProc 1.8 (2007-04-09)
- Support LAME with Nyaochi's patches applied as 'lame_nyaochi' encoder. Please obtain lame.exe with these patches applied at RareWares ( http://www.rarewares.org/mp3.html ) (thanks john33 for hosting this binary). This encoder supports albumartist, bpm, composer, copyright, disc-number, total-discs, and compilation variables as well as the standard LAME encoder.
- CueProc detects cover.jpg, albumart.jpg, or folder.jpg file as the albumart image. By default, CueProc will set ALBUMART variable if either of these files exists in the cuesheet directory. You can disable this feature by --no-auto-albumart option. CueProc does not overwrite ALBUMART variable if it is specified in the cuesheet.
- The batch file cueenc.bat now supports arguments more than 9.
- Support FLAC encoder as 'flac' encoder.
- Support WavPack encoder as 'wavpack' encoder.
- New option, --albumart-files, to configure the list of albumart filenames.
- New option, --hidden-track1, to assume the first track to begin at INDEX 00 (or PREGAP).
- Fixed incorrect character-encoding problems in some places (e.g., for file names, --find option).

CueProc 1.7 (2007-01-07)
- Force the character encoding for internal string representation to UTF-8.
- Fixed a bug (incorrect audio file and duration) with splitted cuesheets.
- Special thanks to Bubu and Jin for the bug reports.

CueProc 1.6 (2006-11-21)
- Fixed a bug of non-ASCII character handling in getaudio.exe.
- Added --ignore-tag-errors option to LAME command-line.
- Added a support for unquoted REM values (i.e. REM values without double-quotation marks) alghouth it is not recommended to omit double-quotation marks in REM values. Note that the current implementation replaces multiple continuous whitespace characters in unquoted REM values with a single whitespace character.
- Special thanks to Bubu for the bug report.

CueProc 1.5 (2006-10-21)
- Show a warning when no target is specified.
- Show track numbers in the progress report with two digits.
- Added a new option -s (--setvar) to define/modify a track variable in an
  arbitrary manner.
- Automatic detection of compilation album, which sets COMPILAION flag only if multiple PERFORMER names exist in a cuesheet. You can disable this feature by --no-auto-compilation option.
- Added --hide-cmdln option not to display command-lines invoked by CueProc.
- Tag totaltracks, disc, totaldiscs, url, copyright, comment, composer, isrc fields for 'neromp4' and 'ctmp4'.
- Tag copyright for 'wma'.
- Tag TOTALTRACKS, DISCNUMBER, TOTALDISCS, COMPOSER, ISRC, COMMENT, COPYRIGHT, COMPILATION, ALBUMARTIST, ALBUM ARTIST (this field name derives from foobar2000's recommendation) for 'oggenc'.
- Rename the term "codec" to "output plugin".

CueProc 1.4 (2006-10-16)
- Fixed a bug to obtain the value of CUESHEET tag from FLAC files.
- Show an error message on failure of openning a target file.

CueProc 1.3 (2006-10-15)
- Added -e (--codecext) option to change the extension of output files
  from the default extension set by the codec.

CueProc 1.2 (2006-10-14)
- Fixed a bug when -d option was not specified.
- Revised the specification of some variables.
- Documentation about variables at the Web site.

CueProc 1.1 (2006-10-14)
- Fixed a bug in legitimization of path names.
- Fixed several bugs in handling embedded cuesheets.
- Special thanks to NeXT for the bug report.

CueProc 1.0 (2006-10-11)
- The initial release.
