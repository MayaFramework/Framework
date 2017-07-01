import baseCheck
from checks import renderingChecks

rendering_checks_list = [
    renderingChecks.LightsInScene(),
    ]
    
RenderingBattery = baseCheck.BaseBatteryCheck("Rendering Checks",rendering_checks_list)

ALLBATTERIES = [RenderingBattery]