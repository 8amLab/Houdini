
numberWedges=3

fileName=hou.hipFile.basename()

fileName=fileName.rsplit('.',1)


deadlineRepo='R:/jobs/wedge'
#deadlineRepo=os.path.normpath(deadlineRepo)

#print fileName

for i in range (0,numberWedges):

    fileSave='%s%s_%s%s' %('R:/jobs/wedge/',fileName[0],i,'.hip')
    
    fileSave=os.path.normpath(fileSave)
    hou.putenv('WEDGE','%d'%(i))
    
    
    print fileSave
    if not os.path.exists(deadlineRepo):
        os.makedirs(deadlineRepo)
    
    hou.hipFile.save(file_name='%s'%(fileSave))
    
    jobPluginFile = os.path.join(deadlineRepo, "%s_plugin_%d.job") %(fileName[0],i)
    
    with open( jobPluginFile, "w" ) as fileHandle:
        fileHandle.write( "SceneFile=%s" %(fileSave) )
        fileHandle.write( "OutputDriver=/out/SIm_River" )
        fileHandle.write( "IgnoreInputs=0" )
        fileHandle.write( "Version=16.5" )
        fileHandle.write( "Build=64bit" )
        fileHandle.write( "SimJob=True" )
        
    jobSubmitFile = os.path.join(deadlineRepo, "%s_info_%d.job") %(fileName[0],i)
    
    with open( jobSubmitFile, "w" ) as fileHandle:
        fileHandle.write( "Name=%s - /out/SIm_River" %(fileName[0]))
        fileHandle.write( "Plugin=Houdini")