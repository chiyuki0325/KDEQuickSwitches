from switches.interfaces import BaseSwitch, SwitchType
import subprocess as sp


class DDNSSwitch(BaseSwitch):
    def __init__(self):
        super().__init__(
            name="DDNS",
            icon="network-workgroup-symbolic",
            type=SwitchType.INSTANT,
        )

    def set(self):
        sp.run("ddns-go -noweb &", shell=True)
        print("DDNS set.")
