import hou

import subprocess

import os

numberWedges=3

def GetDeadlineCommand():
    deadlineBin = ""
    try:
        deadlineBin = os.environ['DEADLINE_PATH']
    except KeyError:
        #if the error is a key error it means that DEADLINE_PATH is not set. however Deadline command may be in the PATH or on OSX it could be in the file /Users/Shared/Thinkbox/DEADLINE_PATH
        pass

    # On OSX, we look for the DEADLINE_PATH file if the environment variable does not exist.
    if deadlineBin == "" and  os.path.exists( "/Users/Shared/Thinkbox/DEADLINE_PATH" ):
        with open( "/Users/Shared/Thinkbox/DEADLINE_PATH" ) as f:
            deadlineBin = f.read().strip()

    deadlineCommand = os.path.join(deadlineBin, "deadlinecommand")

    return deadlineCommand
    
def CallDeadlineCommand( arguments, hideWindow=True, readStdout=True ):
    deadlineCommand = GetDeadlineCommand()
    startupinfo = None
    creationflags = 0
    if os.name == 'nt':
        if hideWindow:
            # Python 2.6 has subprocess.STARTF_USESHOWWINDOW, and Python 2.7 has subprocess._subprocess.STARTF_USESHOWWINDOW, so check for both.
            if hasattr( subprocess, '_subprocess' ) and hasattr( subprocess._subprocess, 'STARTF_USESHOWWINDOW' ):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess._subprocess.STARTF_USESHOWWINDOW
            elif hasattr( subprocess, 'STARTF_USESHOWWINDOW' ):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        else:
            # still show top-level windows, but don't show a console window
            CREATE_NO_WINDOW = 0x08000000   #MSDN process creation flag
            creationflags = CREATE_NO_WINDOW

    environment = {}
    for key in os.environ.keys():
        environment[key] = str(os.environ[key])

    # Need to set the PATH, cuz windows seems to load DLLs from the PATH earlier that cwd....
    if os.name == 'nt':
        deadlineCommandDir = os.path.dirname( deadlineCommand )
        if not deadlineCommandDir == "" :
            environment['PATH'] = deadlineCommandDir + os.pathsep + os.environ['PATH']

    arguments.insert( 0, deadlineCommand )

    # Specifying PIPE for all handles to workaround a Python bug on Windows. The unused handles are then closed immediatley afterwards.
    proc = subprocess.Popen(arguments, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, env=environment, creationflags=creationflags)

    output = ""
    if readStdout:
        output, errors = proc.communicate()

    return output.strip()

#program='"C:/Program Files/Thinkbox/Deadline10/bin/deadlinecommand.exe"'
#program= os.path.normpath(program)

fileName=hou.hipFile.basename()

fileName=fileName.rsplit('.',1)

#\\ryzen01\repository\jobs\wedge\

deadlineRepo=os.path.join('//Ryzen01','repository','jobs','wedge')
deadlineRepo=os.path.normpath(deadlineRepo)

#print fileName
#print deadlineRepo

for i in range (0,numberWedges):

    #fileSave=os.path.join(deadlineRepo,%sfileName[0],'%s'%i,'.hip')
    fileSave=os.path.join(deadlineRepo,'%s.%s.hip'%(fileName[0],i))
    #print fileSave
    
    #break
    
    #fileSave=os.path.normpath(fileSave)
    hou.putenv('WEDGE','%d'%(i))
    
    
    #print fileSave
    if not os.path.exists(deadlineRepo):
        os.makedirs(deadlineRepo)
    
    hou.hipFile.save(file_name='%s'%(fileSave))
    
    jobPluginFile = os.path.join(deadlineRepo, "%s_plugin_%d.job") %(fileName[0],i)
    
    with open( jobPluginFile, "w" ) as fileHandle:
        fileHandle.write( "SceneFile=%s\n" %(fileSave) )
        fileHandle.write( "OutputDriver=/out/SIm_River\n" )
        fileHandle.write( "IgnoreInputs=0\n" )
        fileHandle.write( "Version=16.5\n" )
        fileHandle.write( "Build=64bit\n" )
        fileHandle.write( "SimJob=True\n" )
        
    jobInfoFile = os.path.join(deadlineRepo, "%s_info_%d.job") %(fileName[0],i)
    
    with open( jobInfoFile, "w" ) as fileHandle:
        fileHandle.write( "Name=%s_%s - /out/SIm_River\n" %(fileName[0],i))
        fileHandle.write( "Plugin=Houdini\n")
        
    #arguments=('%s %s %s'%(os.path.join(deadlineRepo, "%s_info_%d.job" %(fileName[0],i)), os.path.join(deadlineRepo, "%s_plugin_%d.job" %(fileName[0],i)), fileSave ))
    #arguments=os.path.normpath(arguments)
    #arguments=arguments.replace('\\','/')
    #print arguments
    print jobInfoFile
    arguments= [jobInfoFile, jobPluginFile]
    #arguments.append('%s'%(fileSave))
    CallDeadlineCommand( arguments)
