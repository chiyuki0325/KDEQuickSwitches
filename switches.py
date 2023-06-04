#!/usr/bin/env python3

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QGridLayout,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSystemTrayIcon,
    QMenu,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QSize
import sys
import darkdetect

from switches.interface import ISwitch
from switches.tun import TUNSwitch
from switches.dark import DarkModeSwitch
from switches.performance import PerformanceModeSwitch
from switches.ddns import DDNSSwitch
from switches.base64 import Base64Switch
from switches.color_chooser import ColorChooserSwitch

SCREEN_WIDTH: int = 1920
WINDOW_WIDTH: int = 510
WINDOW_HEIGHT: int = 300
SWITCH_WIDTH: int = 4
SWITCH_HEIGHT: int = 3

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # 初始化状态
        switches: list[ISwitch] = [
            TUNSwitch(),
            DarkModeSwitch(),
            PerformanceModeSwitch(),
            DDNSSwitch(),
            Base64Switch(),
            ColorChooserSwitch(),
        ]

        for switch in switches:
            if switch.needs_sudo:
                switch.main_module_file_name = __file__
                # 否则会返回 interface.py 的路径而不是主模块的路径

        # GUI
        app = QApplication([])

        # 托盘图标
        tray = QSystemTrayIcon()
        tray.setIcon(QIcon.fromTheme("settings-configure"))
        tray.setToolTip("快捷开关")
        tray_menu = QMenu()
        tray_menu.addAction("退出", app.quit)
        tray.setContextMenu(tray_menu)
        tray.show()

        # 初始化窗口
        window = QWidget()
        window.setObjectName("mainWindow")
        window.setWindowTitle("快捷开关")
        window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
        window.setFixedSize(window.width(), window.height())
        window.move(SCREEN_WIDTH - WINDOW_WIDTH, 0)
        color = "242" if darkdetect.isLight() else "40"
        window.setStyleSheet(
            """
            #mainWindow {
                background: rgb(COLOR, COLOR, COLOR);
                margin: 0px;
                padding: 0px;
            }
        """.replace(
                "COLOR", color
            )
        )
        for flag in [
            Qt.FramelessWindowHint,
            Qt.WindowStaysOnTopHint
        ]:
            window.setWindowFlag(flag)

        # 网格布局
        grid_layout = QGridLayout()
        window.setLayout(grid_layout)

        # 按钮
        positions = [
            (y, x) for y in range(SWITCH_HEIGHT) for x in range(SWITCH_WIDTH)
        ]

        for position, switch in zip(positions, switches):
            frame = QFrame()
            frame.setFixedSize(128, 128)

            v_layout = QVBoxLayout()
            v_layout.setAlignment(Qt.AlignCenter)

            button = QPushButton("")
            button.setFixedSize(64, 64)
            button.setIconSize(QSize(40, 40))

            button.clicked.connect(switch.trigger)

            label = QLabel()
            label.setAlignment(Qt.AlignCenter)

            v_layout.addWidget(button)
            v_layout.addWidget(label)

            switch.set_ref(button, label, window, app)
            switch.update_ui()

            frame.setLayout(v_layout)
            grid_layout.addWidget(frame, *position)

        # 显示窗口

        def show_or_hide_window(window):
            if window.isVisible():
                window.hide()
            else:
                window.show()

        def tray_clicked(_):
            show_or_hide_window(window)

        tray.activated.connect(tray_clicked)

        app.exec_()
    else:
        match sys.argv[1]:
            case "set-tun":
                TUNSwitch().set(sys.argv[2] == "True")
