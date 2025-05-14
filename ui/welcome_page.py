from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont


class WelcomePage(QWidget):
    home_requested = pyqtSignal()  # C'est le seul signal dont vous avez besoin
    help_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        # Main vertical layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(40)

        # Add vertical spacer at top to help center content
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Logo
        self.logo = QLabel()
        self.logo.setAlignment(Qt.AlignCenter)
        pixmap = QPixmap("images/logo.png")
        if not pixmap.isNull():
            self.logo.setPixmap(pixmap.scaled(300, 300, Qt.KeepAspectRatio))
        else:
            self.logo.setText("Analyse Comptable")
            self.logo.setFont(QFont('Arial', 24, QFont.Bold))

        # Button container (horizontal layout)
        button_container = QWidget()
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)
        button_layout.setContentsMargins(0, 0, 0, 0)

        # Aide Button (transparent with blue border)
        self.help_btn = QPushButton("Aide")
        self.help_btn.setFixedSize(180, 50)
        self.help_btn.setStyleSheet("""
                   QPushButton {
                       background-color: transparent;
                       color: #2196F3;
                       border: 2px solid #2196F3;
                       border-radius: 6px;
                       font-size: 16px;
                       font-weight: 500;
                   }
                   QPushButton:hover {
                       background-color: rgba(33, 150, 243, 0.1);
                   }
                   QPushButton:pressed {
                       background-color: rgba(33, 150, 243, 0.2);
                       color: #1976D2;
                       border-color: #1976D2;
                   }
               """)
        self.help_btn.clicked.connect(self.help_requested.emit)

        # Commencer Button (blue)
        self.start_btn = QPushButton("Commencer")
        self.start_btn.setFixedSize(180, 50)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        # Changez cette ligne pour utiliser home_requested au lieu de start_requested
        self.start_btn.clicked.connect(self.home_requested.emit)

        # Add buttons to horizontal layout
        button_layout.addWidget(self.help_btn)
        button_layout.addWidget(self.start_btn)

        button_container.setLayout(button_layout)

        # Add widgets to main layout
        main_layout.addWidget(self.logo)
        main_layout.addWidget(button_container)

        # Add vertical spacer at bottom to help center content
        main_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(main_layout)