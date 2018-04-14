import maya.cmds as cmds
import maya.mel as mel
import playblasterUI
import os


def changeRotateOrder(newRotateOrder, *args):
    selection = cmds.ls(sl=True)
    if selection:
        scriptPath = (os.path.dirname(playblasterUI.__file__)+ '/zooChangeRoo.mel').replace('\\','/')
        scriptUtilsPath = (os.path.dirname(playblasterUI.__file__)+ '/zooUtils.mel').replace('\\','/')
        mel.eval('source "%s"' % scriptPath)
        mel.eval('source "%s"' % scriptUtilsPath)
        mel.eval("zooChangeRoo " + newRotateOrder)
        mel.eval('performEulerFilter graphEditor1FromOutliner')
    else:
        cmds.warning('there is no object selected')     


def keyInRange(*args):
    start=cmds.playbackOptions(q=True, min=True)
    end=cmds.playbackOptions(q=True, max=True)

    selection = cmds.ls(sl=True)
    if selection:

        keysInFrames=cmds.keyframe(time=(start,end), query=True);
        simplifiedList=[]

        for o in keysInFrames:
            if o not in simplifiedList:
                simplifiedList.append(o)

        simplifiedList.sort()

        for o in range(len(simplifiedList)):
            cmds.currentTime(cmds.findKeyframe(timeSlider=True, which="next"), edit=True)
            cmds.setKeyframe()
    else:
        cmds.warning('there is no object selected')    


def stepTangents(*args):
    selection=cmds.ls(sl=True)
    if selection:
        cmds.selectKey() 
        cmds.keyTangent(itt='linear', ott='step')
        cmds.keyTangent(g=True, itt='linear', ott= 'step')
    else:
        cmds.warning('there is no object selected but new keys will be in stepped')

def autoTangents(*args):
    selection=cmds.ls(sl=True)
    if selection:
        cmds.selectKey()
        cmds.keyTangent(itt='auto', ott= 'auto')
        cmds.keyTangent(g=True, itt='auto', ott= 'auto')
    else:
        cmds.warning('there is no object selected but new keys will be in auto')

def intermediateAndConstraint(*args):
    selection= cmds.ls(sl=True)
    if len(selection) == 2:
        slave= selection[-1]
        master= selection[0]
        #first create a locator and offset it:
        locator= cmds.spaceLocator(n='intermediate_' + slave)[0]
        offset= cmds.group(locator,n=locator+'_offset')
        #align the offset with the slave
        cmds.delete(cmds.parentConstraint(slave,offset, mo=False))
        #constraint the slave with the intermediate object
        cmds.parentConstraint(locator,slave, mo=False)
        cmds.parentConstraint(master,offset, mo=True)

    else:
        cmds.warning('please select first master and then slave to create and intermediate object and constraint with it')
