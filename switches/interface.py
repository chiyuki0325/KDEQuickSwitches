from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QInputDialog
import os
import subprocess as sp
from enum import Enum
from time import sleep


class SwitchType(Enum):
    BOOL = 1
    INSTANT = 2
    STRING = 3


class ISwitch:
    def __init__(
        self,
        name: str,
        icon: str,
        type: SwitchType | None = SwitchType.BOOL,
        needs_sudo: bool | None = False,
        icon_disabled: str | None = None,
        cmd_name: str | None = None,
        prompt: str | None = None,
    ) -> None:
        self.name = name
        self.icon = icon
        self.type = type
        self.icon_disabled = icon_disabled
        self.needs_sudo = needs_sudo
        self.cmd_name = cmd_name
        self.prompt = prompt
        self.main_module_file_name = None
        self.state = None
        self.ref_window = None
        self.ref_button = None
        self.ref_label = None
        self.ref_app = None

    def get(self):
        pass

    def set(self, value):
        self.state = value
        pass

    def trigger(self):
        match self.type:
            case SwitchType.BOOL:
                self.set(not self.state)
            case SwitchType.INSTANT:
                self.set()
            case SwitchType.STRING:
                value, ok = QInputDialog.getText(
                    self.ref_window,
                    self.name,
                    self.prompt,
                )
                if ok:
                    self.set(value)
        self.update_ui()
        sleep(0.3)
        self.ref_window.hide()

    @property
    def label_text(self):
        if self.type == SwitchType.BOOL:
            return f"{self.name}: {'开' if self.state else '关'}"
        elif self.type == SwitchType.INSTANT:
            return self.name
        else:
            return f"{self.name}: {self.state}"

    def sudo_me(self, value) -> bool:
        if os.getuid() == 0:
            return False
        if self.needs_sudo:
            cmd = [
                "sudo",
                "python3",
                self.main_module_file_name,
                self.cmd_name,
                str(value),
            ]
            sp.run(cmd)
            return True
        else:
            return False

    def update_ui(self):
        self.ref_label.setText(self.label_text)
        if self.type == SwitchType.BOOL:
            self.ref_button.setIcon(
                QIcon.fromTheme(
                    self.icon if self.state else self.icon_disabled
                )
            )
        else:
            self.ref_button.setIcon(QIcon.fromTheme(self.icon))
        self.ref_app.processEvents()

    def set_ref(self, button, label, window, app):
        self.ref_button = button
        self.ref_label = label
        self.ref_window = window
        self.ref_app = app
