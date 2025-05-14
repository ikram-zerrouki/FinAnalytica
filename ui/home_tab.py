
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QFileDialog, QMessageBox, QFrame, QApplication)
from PyQt5.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor


class HomeTab(QWidget):
    return_requested = pyqtSignal()
    import_successful = pyqtSignal()
    manual_entry_requested = pyqtSignal()  # Nouveau signal

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()
        self._setup_animations()

    def _init_ui(self):
        # Layout principal
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.setStyleSheet("background-color: #f5f7fa; border: none;")

        # Header avec bouton retour (aligné à gauche)
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 20)

        self.return_btn = QPushButton("← Retour")
        self.return_btn.setFixedSize(100, 40)
        self.return_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                padding: 8px;
            }
            QPushButton:hover { background-color: #1976D2; }
            QPushButton:pressed { background-color: #0D47A1; }
        """)
        self.return_btn.clicked.connect(self.return_requested.emit)
        header_layout.addWidget(self.return_btn)
        header_layout.addStretch()  # Pousse le bouton à gauche
        self.main_layout.addLayout(header_layout)

        # Conteneur pour centrer la carte
        center_container = QWidget()
        center_layout = QHBoxLayout(center_container)
        center_layout.setAlignment(Qt.AlignCenter)
        center_layout.setContentsMargins(0, 0, 0, 0)

        # Carte centrée
        self.card = QFrame()
        self.card.setFrameShape(QFrame.NoFrame)
        self.card.setStyleSheet("""
            QFrame { 
                background-color: white; 
                border-radius: 12px; 
                border: none;
            }
        """)
        self.card.setFixedWidth(500)

        card_layout = QVBoxLayout(self.card)
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(25)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # Logo
        self.logo = QLabel()
        pixmap = QPixmap("images/logo.png").scaled(140, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(Qt.AlignCenter)
        self.logo.setStyleSheet("border: none;")
        card_layout.addWidget(self.logo)

        # Description
        desc = QLabel("Importez un fichier Excel ou remplissez le formulaire")
        desc.setFont(QFont('Open Sans', 12))
        desc.setStyleSheet("color: #6c757d; border: none; background: transparent;")
        desc.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(desc)

        # Bouton d'import
        self.import_btn = QPushButton("Importer un fichier")
        self.import_btn.setIcon(QIcon("assets/upload.png"))
        self.import_btn.setIconSize(QSize(20, 20))
        self.import_btn.setFixedSize(280, 50)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 14px;
                font-weight: 500;
                padding: 0px 40px 0px 20px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton:pressed { background-color: #1d6fa5; }
            QPushButton::icon { left: auto; right: 15px; }
        """)
        self.import_btn.clicked.connect(self._import_file)
        card_layout.addWidget(self.import_btn, 0, Qt.AlignCenter)

        # Bouton de saisie manuelle
        self.manual_btn = QPushButton("Remplir le formulaire")
        self.manual_btn.setIcon(QIcon("assets/form.png"))
        self.manual_btn.setIconSize(QSize(20, 20))
        self.manual_btn.setFixedSize(280, 50)
        self.manual_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 14px;
                font-weight: 500;
                padding: 0px 40px 0px 20px;
            }
            QPushButton:hover { background-color: #27ae60; }
            QPushButton:pressed { background-color: #219653; }
            QPushButton::icon { left: auto; right: 15px; }
        """)
        self.manual_btn.clicked.connect(self._manual_entry)
        card_layout.addWidget(self.manual_btn, 0, Qt.AlignCenter)

        # Message de statut
        self.status_label = QLabel()
        self.status_label.setFont(QFont('Open Sans', 10))
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("padding: 5px 0;")
        self.status_label.hide()
        card_layout.addWidget(self.status_label)

        center_layout.addWidget(self.card)
        self.main_layout.addWidget(center_container, 1)

    def _setup_animations(self):
        self.shadow_anim = QPropertyAnimation(self.card, b"geometry")
        self.shadow_anim.setDuration(300)
        self.shadow_anim.setEasingCurve(QEasingCurve.OutQuad)
        self.logo_anim = QPropertyAnimation(self.logo, b"geometry")
        self.logo_anim.setDuration(200)

    def _import_file(self):
        self.status_label.hide()
        self.import_btn.setEnabled(False)
        self.import_btn.setText("Traitement en cours")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 0px 40px 0px 20px;
                border-radius: 15px;
            }
            QPushButton::icon { left: auto; right: 15px; }
        """)
        self._animate_card_press()
        QApplication.processEvents()

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un fichier Excel", "",
            "Fichiers Excel (*.xlsx *.xls);;Tous les fichiers (*)"
        )

        if file_path:
            success, message = self.controller.file_controller.load_excel_file(file_path)
            if success:
                self.status_label.setText("Importation réussie!")
                self.status_label.setStyleSheet("color: #2ecc71;")
                self.import_successful.emit()
            else:
                self.status_label.setText("Erreur lors de l'importation.")
                self.status_label.setStyleSheet("color: #e74c3c;")
            self.status_label.show()

        self.import_btn.setEnabled(True)
        self.import_btn.setText("Importer un fichier")
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 0px 40px 0px 20px;
                border-radius: 15px;
            }
            QPushButton:hover { background-color: #2980b9; }
            QPushButton::icon { left: auto; right: 15px; }
        """)
        self._animate_card_release()

    def _manual_entry(self):
        """Gère le clic sur le bouton de saisie manuelle"""
        self.manual_entry_requested.emit()

    def _animate_card_press(self):
        current = self.card.geometry()
        self.shadow_anim.setStartValue(current)
        self.shadow_anim.setEndValue(current.adjusted(0, 2, 0, 2))
        self.shadow_anim.start()
        logo_current = self.logo.geometry()
        self.logo_anim.setStartValue(logo_current)
        self.logo_anim.setEndValue(logo_current.adjusted(0, -5, 0, -5))
        self.logo_anim.start()

    def _animate_card_release(self):
        current = self.card.geometry()
        self.shadow_anim.setStartValue(current)
        self.shadow_anim.setEndValue(current.adjusted(0, -2, 0, -2))
        self.shadow_anim.start()
        logo_current = self.logo.geometry()
        self.logo_anim.setStartValue(logo_current)
        self.logo_anim.setEndValue(logo_current.adjusted(0, 5, 0, 5))
        self.logo_anim.start()
