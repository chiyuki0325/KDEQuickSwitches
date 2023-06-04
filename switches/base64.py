from switches.interface import ISwitch, SwitchType
import pyperclip
from base64 import b64encode
import subprocess as sp


class Base64Switch(ISwitch):
    def __init__(self):
        super().__init__(
            name="Base64",
            icon="gedit-symbolic",
            type=SwitchType.STRING,
            prompt="输入要编码的字符串",
        )

    def get(self):
        return ""

    def set(self, value: str):
        encoded = b64encode(value.encode()).decode()
        copy, _ = pyperclip.init_klipper_clipboard()
        copy(encoded)
        sp.run(
            [
                "notify-send",
                "已复制到剪贴板",
                encoded,
                "-i",
                "gedit-symbolic",
                "-a",
                "Base64",
            ]
        )
        print(f"Base64: {encoded}")

    @property
    def label_text(self):
        return "Base64"
