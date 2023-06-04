from switches.interface import ISwitch
import subprocess as sp


class PerformanceModeSwitch(ISwitch):
    def __init__(self):
        super().__init__(
            name="性能模式",
            icon="preferences-system-power-symbolic",
            icon_disabled="battery-level-100-symbolic",
            needs_sudo=False,  # sudo 直接在 Python 里写好了，无需以 sudo 自己的方式切换
        )
        self.state = self.get()
        print(f"Performance mode is {self.state}.")

    @property
    def label_text(self):
        return "性能模式" if self.state else "节能模式"

    def get(self) -> bool:
        governor = (
            open("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
            .read()
            .strip()
        )
        return governor == "performance"

    def set(self, value: bool):
        self.state = value
        sp.run(
            [
                "sudo",
                "cpupower",
                "-c",
                "all",
                "frequency-set",
                "-g",
                "performance" if value else "powersave",
            ]
        )
        print(f"Set performance mode to {value}.")