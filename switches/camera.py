from switches.interfaces import BaseSwitch, SudoableSwitch
import subprocess as sp


class CameraSwitch(BaseSwitch, SudoableSwitch):
    def __init__(self):
        super().__init__(
            name="摄像头",
            icon="camera-web-symbolic",
            icon_disabled="camera-video-symbolic",
            cmd_name="set-camera",
        )
        self.state = self.get()
        print(f"Camera is {self.state}.")
        if self.state:
            # 获取摄像头的端口号和总线号
            lsusb_results = (
                sp.run(["lsusb", "-t"], capture_output=True)
                .stdout.decode()
                .split("\n")
            )
            uvcvideo_line_num = 0
            port_num = 0
            bus_num = 0
            for i, line in enumerate(lsusb_results):
                if "Driver=uvcvideo" in line:
                    uvcvideo_line_num = i
                    port_num = int(line.split("Port ")[1].split(":")[0].strip())
                    break
            if uvcvideo_line_num != 0:
                for i in range(uvcvideo_line_num, 0, -1):
                    if "Bus " in lsusb_results[i]:
                        bus_num = int(
                            lsusb_results[i].split("Bus ")[1].split(".")[0]
                        )
                        break
            else:
                return Exception("No camera found.")
            self.bind_args = f"{bus_num}-{port_num}"
        else:
            self.bind_args = "1-5"  # fallback

    def get(self) -> bool:
        lsusb_result = sp.run(
            ["lsusb", "-t"], capture_output=True
        ).stdout.decode()
        return "Driver=uvcvideo" in lsusb_result

    def set(self, value: bool):
        self.state = value
        if self.sudo_me(value):
            self.update_ui()
            return
        open(
            "/sys/bus/usb/drivers/usb/" + ("bind" if value else "unbind"), "w"
        ).write(self.bind_args)
        print(f"Set camera to {value}.")
