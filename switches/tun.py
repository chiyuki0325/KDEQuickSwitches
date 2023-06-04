from switches.interface import ISwitch
import yaml
import subprocess as sp


class TUNSwitch(ISwitch):
    def __init__(self):
        super().__init__(
            name="TUN",
            icon="network-receive-symbolic",
            icon_disabled="network-disconnected-symbolic",
            needs_sudo=True,
            cmd_name="set-tun",
        )
        self.path = "/etc/clash-meta/config.yaml"
        self.state = self.get()
        print(f"TUN is {self.state}.")

    def get(self) -> bool:
        return yaml.safe_load(open(self.path))["tun"]["enable"]

    def set(self, value: bool):
        self.state = value
        if self.sudo_me(value):
            self.update_ui()
            return
        # 使用字符串替换的方式修改配置文件
        # 这样可以保留注释
        config = open(self.path).readlines()
        for i in range(len(config)):
            if "tun:" in config[i]:
                # 编辑下一行
                config[i + 1] = config[i + 1].replace(
                    str(not value).lower(), str(value).lower()
                )
                break
        open(self.path, "w").writelines(config)
        sp.run(["systemctl", "restart", "clash-meta.service"])
        print(f"Set TUN to {value}.")
