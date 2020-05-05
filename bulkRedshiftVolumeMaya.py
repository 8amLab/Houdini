import glob, os
import pymel.core as pm

path="X:/theboat/mundo/vfx/shots/mun_02B_010/fx/publish/mun_02B_010_fx_cloudDir_v077"
os.chdir(path)
for file in glob.glob("*.vdb"):
    
    
    volumeNode=pm.createNode( 'RedshiftVolumeShape')
    filename="%s/%s" % (path,file)
    volumeNode.fileName.set(filename)
    volumeNode.displayMode.set(1)
    transformVol = pm.listRelatives( volumeNode, parent=True, type="transform" )
    transformVol= transformVol[0]
    file=file.split(".")
    file=file[0]
    pm.rename(transformVol,file)
    #break
