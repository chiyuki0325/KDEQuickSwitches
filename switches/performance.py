from switches.interfaces import BaseSwitch, SudoableSwitch
import subprocess as sp


class PerformanceModeSwitch(BaseSwitch, SudoableSwitch):
    def __init__(self):
        super().__init__(
            name="性能模式",
            icon="preferences-system-power-symbolic",
            icon_disabled="battery-level-100-symbolic",
            cmd_name="set-performance-mode",
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
        if self.sudo_me(value):
            self.update_ui()
            return
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
