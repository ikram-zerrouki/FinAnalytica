from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFrame
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from functools import partial

class Sidebar(QWidget):
    nav_requested = pyqtSignal(str)
    return_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.buttons = {}
        self.current_page = None
        self._init_ui()

    def _init_ui(self):
        self.setFixedWidth(220)
        self.setStyleSheet("""
            QWidget { background-color: #2196F3; color: white; }
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                text-align: left;
                padding: 12px 20px;
                font-size: 15px;
                font-weight: 500;
                border-radius: 4px;
                margin: 2px 8px;
            }
            QPushButton:hover { background-color: rgba(255, 255, 255, 0.1); }
            QPushButton:checked {
                background-color: rgba(255, 255, 255, 0.2);
                font-weight: bold;
                border-left: 3px solid white;
            }
            #retourButton {
                background-color: transparent;
                margin: 8px;
                text-align: left;
                padding: 12px 20px;
            }
            #retourButton:hover { background-color: rgba(255, 255, 255, 0.1); }
            #separator {
                background-color: rgba(255, 255, 255, 0.2);
                border: none;
                height: 1px;
                margin: 10px 15px;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 15, 0, 15)
        layout.setSpacing(0)

        # Modified navigation items - removed "Accueil"
        nav_items = ["Données", "Résultats", "Graphiques"]
        for item in nav_items:
            btn = QPushButton(item)
            btn.setCheckable(True)
            btn.clicked.connect(partial(self._on_nav_click, item))
            self.buttons[item] = btn
            layout.addWidget(btn)

        separator = QFrame()
        separator.setObjectName("separator")
        layout.addWidget(separator)

        retour_btn = QPushButton("Retour")
        retour_btn.setObjectName("retourButton")
        retour_btn.clicked.connect(self.return_requested.emit)
        layout.addWidget(retour_btn)

        layout.addStretch()
        self.setLayout(layout)

    def _on_nav_click(self, button_name):
        if self.current_page == button_name:
            return  # Prevent reloading the same tab

        self.current_page = button_name
        for name, btn in self.buttons.items():
            btn.setChecked(name == button_name)

        self.nav_requested.emit(button_name)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor("#2196F3"))
        super().paintEvent(event)