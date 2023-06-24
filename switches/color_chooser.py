from switches.interfaces import BaseSwitch, SwitchType
import subprocess as sp


class ColorChooserSwitch(BaseSwitch):
    def __init__(self):
        super().__init__(
            name="颜色选择器",
            icon="color-select-symbolic",
            type=SwitchType.INSTANT,
        )

    def set(self):
        sp.run("kcolorchooser &", shell=True)
        print("Color chooser set.")
