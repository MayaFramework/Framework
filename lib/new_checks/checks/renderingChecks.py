from .. import baseCheck as baseCheck
import maya.cmds as cmds

class LightsInScene(baseCheck.BaseCheck):
    """Summary
    
    Attributes:
        description (str): Description
        fixable (bool): Description
        name (str): Description
        output (TYPE): Description
        selectable (bool): Description
        state (TYPE): Description
    """

    LIGHTS = [
        "aiPhotometricLight",
        "aiSkyDomeLight",
        "aiLightPortal",
        "aiSkyDomeLight",
        "ambientLight",
        "directionalLight",
        "pointLight",
        "spotLight",
        "areaLight",
        "volumeLight",
        "aiMeshLight",
        "aiAreaLight",
    ]

    def __init__(self):
        """Summary
        """
        super(LightsInScene, self).__init__()
        self.name = "Lights in Scene"
        self.description = "Check if there are any Light in the scene"

    def execute(self):
        self.lights_in_scene = cmds.ls(type=self.LIGHTS)
        self.setLog("Checking Lights", "start")
        if not self.lights_in_scene:
            self.state = self.CHECK_PASSED
            self.fixable = False
            self.setLog("Not lights found!", "final")
        else:
            self.state = self.CHECK_FAILLED
            self.fixable = True
            self.setLog("There are some lights in the scene!", "final")
            self.affectedElements = self.lights_in_scene

    def fix(self):
        cmds.delete([cmds.listRelatives(light, p=True)[0] for light in self.lights_in_scene])
        self.state = self.CHECK_PASSED
        self.fixable = False
        self.setLog("Fixed!")