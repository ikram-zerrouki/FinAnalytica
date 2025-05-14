from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QTextBrowser, QPushButton, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class HelpPage(QWidget):
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._init_ui()

    def _init_ui(self):
        # Main layout with better spacing
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)

        # Header with back button
        header = QHBoxLayout()

        # Back button with icon-style
        back_btn = QPushButton("← Retour")
        back_btn.clicked.connect(self.back_requested.emit)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)

        # Title with better typography
        title = QLabel("Centre d'Aide")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333;
                margin-bottom: 10px;
            }
        """)

        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(title)
        header.addStretch()
        header.addSpacing(100)  # Balance the layout

        # Help content container with shadow effect
        content_frame = QFrame()
        content_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)

        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # Help content with better formatting
        help_content = QTextBrowser()
        help_content.setStyleSheet("""
            QTextBrowser {
                background-color: transparent;
                border: none;
                font-size: 14px;
                color: #444;
            }
            a {
                color: #2196F3;
                text-decoration: none;
            }
        """)
        help_content.setOpenExternalLinks(True)
        help_content.setHtml(self._get_help_content())

        content_layout.addWidget(help_content)

        # Add widgets to main layout
        layout.addLayout(header)
        layout.addWidget(content_frame)

        self.setLayout(layout)
        self.setStyleSheet("background-color: #f5f7fa;")

    def _get_help_content(self):
        return """
        <style>
            h2 {
                color: #2196F3;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            h3 {
                color: #333;
                margin-top: 15px;
                margin-bottom: 8px;
            }
            p {
                margin-top: 5px;
                margin-bottom: 5px;
                line-height: 1.5;
            }
            .card {
                background-color: #f9f9f9;
                border-left: 4px solid #2196F3;
                padding: 10px;
                margin: 10px 0;
                border-radius: 0 4px 4px 0;
            }
            .highlight {
                background-color: #E3F2FD;
                padding: 2px 4px;
                border-radius: 3px;
            }
            .formula {
                font-family: monospace;
                background-color: #f0f0f0;
                padding: 2px 5px;
                border-radius: 3px;
            }
        </style>

        <div class='card'>
            <h2>Comment utiliser l'application</h2>
            <p><b>1.</b> Cliquez sur <span class='highlight'>Commencer</span> pour accéder à l'application</p>
            <p><b>2.</b> Importez un fichier Excel ou saisissez les données manuellement</p>
            <p><b>3.</b> Visualisez les résultats dans les différents onglets</p>
        </div>

        <h2>Indicateurs calculés</h2>

        <div class='card'>
            <h3>📊 Indicateurs de rentabilité</h3>
            <p><b>Taux de rentabilité</b>: <span class='formula'>Résultat net / Chiffre d'affaires × 100</span></p>
            <p><b>ROE (Return on Equity)</b>: <span class='formula'>Résultat net / Capitaux propres × 100</span></p>
            <p><b>ROA (Return on Assets)</b>: <span class='formula'>Résultat net / Total actif × 100</span></p>
            <p><i>Mesurent la capacité de l'entreprise à générer des profits</i></p>
        </div>

        <div class='card'>
            <h3>🏦 Indicateurs de structure financière</h3>
            <p><b>Ratio d'endettement</b>: <span class='formula'>(Total passif - Capitaux propres) / Capitaux propres × 100</span></p>
            <p><b>Ratio de liquidité générale</b>: <span class='formula'>Actif courant / Passif courant</span></p>
            <p><i>Évaluent la solvabilité et la structure financière de l'entreprise</i></p>
            <p>• <b>Endettement</b>: Faible (<50%), Modéré (50-100%), Élevé (>100%)</p>
            <p>• <b>Liquidité</b>: Excellente (>1.5), Bonne (1.0-1.5), Problématique (<1.0)</p>
        </div>

        <div class='card'>
            <h3>📈 Indicateurs d'activité</h3>
            <p><b>Marge brute</b>: <span class='formula'>Chiffre d'affaires - Coût de production</span></p>
            <p><b>Taux de marge brute</b>: <span class='formula'>Marge brute / Chiffre d'affaires × 100</span></p>
            <p><b>Ratio de productivité</b>: <span class='formula'>Valeur ajoutée / Charges de personnel</span></p>
            <p><b>Variation du chiffre d'affaires</b>: <span class='formula'>(CA actuel - CA précédent) / CA précédent × 100</span></p>
            <p><i>Mesurent l'efficacité opérationnelle de l'entreprise</i></p>
        </div>

        <div class='card'>
            <h3>💰 Analyse des coûts</h3>
            <p><b>Coût de production</b>: <span class='formula'>Achats consommés + Services extérieurs</span></p>
            <p><b>Charges variables</b>: <span class='formula'>Achats consommés + Services extérieurs</span></p>
            <p><b>Charges fixes</b>: <span class='formula'>Charges de personnel + Impôts et taxes</span></p>
            <p><b>Taux de taxes</b>: <span class='formula'>Impôts et taxes / Chiffre d'affaires × 100</span></p>
            <p><i>Permettent d'analyser la structure des coûts de l'entreprise</i></p>
        </div>

        <div class='card'>
            <h3>🔄 Besoin en fonds de roulement (BFR)</h3>
            <p><b>BFR</b>: <span class='formula'>Stocks + (Actif courant - Stocks - Trésorerie) - Passif courant</span></p>
            <p><i>Indique le besoin de financement à court terme de l'entreprise</i></p>
            <p>• Positif: besoin de financement</p>
            <p>• Négatif: excédent de ressources</p>
        </div>

        <div class='card'>
            <h3>📉 Variations</h3>
            <p><b>Variation des stocks</b>: <span class='formula'>Stocks actuels - Stocks précédents</span></p>
            <p><i>Montre l'évolution de la gestion des stocks</i></p>
        </div>

        <div style='margin-top: 30px; color: #666; font-size: 13px;'>
            <p>Pour plus d'informations, contactez notre support technique.</p>
        </div>
        """