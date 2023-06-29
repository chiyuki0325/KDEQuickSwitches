from switches.interfaces import BaseSwitch, SwitchType
import subprocess as sp
import requests


class DMLiveSwitch(BaseSwitch):
    def __init__(self):
        super().__init__(
            name="B 站播放",
            icon="media-video-symbolic",
            type=SwitchType.STRING,
            prompt="输入视频链接或直播连接",
        )

    def get(self):
        return ""

    def set(self, value: str):
        # Case 1: Bilibili client
        # Input: 【玩腻了1.20原版生存？来试试1.20魔法生存吧！】https://www.bilibili.com/video/BV1v14y127Gc?vd_source=2cc6393117a2813990e47faa55dffa42
        # Output: https://www.bilibili.com/video/BV1v14y127Gc
        if value[0] == "【":
            real_url = value.split("】")[1].split("?")[0]
        # Case 2: Bilibili web
        # Input: https://www.bilibili.com/video/BV1v14y127Gc?vd_source=2cc6393117a2813990e47faa55dffa42
        # Output: https://www.bilibili.com/video/BV1v14y127Gc
        elif value[0:4] == "http" and 'bilibili.com' in value:
            real_url = value.split("?")[0]
        # Case 3: Bilibili mobile (1)
        # Input: https://b23.tv/BV1QF411h7EK
        # Output: https://www.bilibili.com/video/BV1QF411h7EK
        elif 'b23.tv' in value:
            if 'b23.tv/BV' in value:
                real_url = 'https://www.bilibili.com/video/BV' + value.split('b23.tv/BV')[1]
            elif 'b23.tv/av' in value:
                real_url = 'https://www.bilibili.com/video/av' + value.split('b23.tv/av')[1]
        # Case 4: Bilibili mobile (2)
        # Input: https://b23.tv/kpLP9MF
        # Output: https://www.bilibili.com/video/BV1QF411h7EK
            else:
                response = requests.get(value, allow_redirects=False)
                real_url = response.headers['Location'].split('?')[0]
        # Else
        else:
            real_url = value
        sp.run(
            [
                "dmlive",
                "-u",
                real_url,
            ]
        )
        print(f"DMLive: {real_url}")

    @property
    def label_text(self):
        return "B 站播放"
