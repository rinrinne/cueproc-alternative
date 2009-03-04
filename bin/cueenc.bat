@rem A batch file (alias) to cueproc.exe (or cueproc.py)
@rem 
@rem If you want to use the script version (cueproc.py) rather than Win32
@rem pre-compiled binary (cueproc.exe), change the value of CUEPROCCMD to:
@rem set CUEPROCCMD=python "C:\path_to_script\cueproc.py"

@set CUEPROCCMD=cueproc
@set CUEPROCOPT=

@%CUEPROCCMD% %CUEPROCOPT% -d ..\${output_plugin}\${cuesheet_path} -o "#if{track.has_key('DISCNUMBER')}${DISCNUMBER}_#endif${TRACKNUMBER}_${TITLE}" %*
