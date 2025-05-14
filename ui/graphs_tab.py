from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton,
                             QScrollArea, QMessageBox, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from matplotlib import rcParams


class GraphsTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # Configuration des styles matplotlib (tailles réduites mais lisibles)
        rcParams.update({
            'font.size': 10,
            'axes.titlesize': 12,
            'axes.titleweight': 'bold',
            'axes.grid': True,
            'grid.alpha': 0.2,
            'legend.fontsize': 9,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'figure.titlesize': 13,
            'xtick.labelsize': 9,
            'ytick.labelsize': 9,
            'figure.dpi': 100,
            'lines.linewidth': 2,
            'lines.markersize': 6
        })

        self._init_ui()

    def _init_ui(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Titre
        title = QLabel("Analyse Graphique")
        title.setFont(QFont('Montserrat', 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        # Zone de défilement
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical { width: 10px; background: #f1f1f1; }
            QScrollBar::handle:vertical { background: #c1c1c1; border-radius: 4px; }
        """)

        # Conteneur des graphiques
        self.container = QWidget()
        self.graphs_layout = QVBoxLayout(self.container)
        self.graphs_layout.setContentsMargins(5, 5, 15, 5)
        self.graphs_layout.setSpacing(20)  # Espacement réduit entre graphiques
        self.graphs_layout.setAlignment(Qt.AlignTop)

        self.scroll.setWidget(self.container)
        main_layout.addWidget(self.scroll)

    def update_graphs(self):
        """Met à jour les graphiques avec une taille plus compacte"""
        # Nettoyage
        while self.graphs_layout.count():
            item = self.graphs_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        df = self.controller.get_processed_data()
        if df is None or df.empty:
            return

        try:
            colors = {
                'blue': '#3498db',
                'green': '#2ecc71',
                'red': '#e74c3c',
                'orange': '#f39c12',
                'purple': '#9b59b6'
            }

            # Taille réduite des graphiques (8x4 au lieu de 10x5)
            fig_size = (8, 3.5)  # Plus compact mais reste lisible

            # Graphique 1: CA
            fig1 = Figure(figsize=fig_size)
            ax1 = fig1.add_subplot(111)
            df['Chiffre_affaires'].plot(kind='bar', ax=ax1, color=colors['blue'], alpha=0.8, width=0.6)
            ax1.set_title('Évolution du Chiffre d\'Affaires', pad=10)
            ax1.set_ylabel('DZD')
            canvas1 = FigureCanvas(fig1)
            canvas1.setMinimumHeight(350)  # Hauteur réduite
            self.graphs_layout.addWidget(canvas1)

            # Graphique 2: Charges
            fig2 = Figure(figsize=fig_size)
            ax2 = fig2.add_subplot(111)
            width = 0.3  # Barres plus fines
            x = np.arange(len(df.index))
            ax2.bar(x, df['Charges_variables'] / 1e6, width, color=colors['orange'], alpha=0.8, label='Variables')
            ax2.bar(x, df['Charges_fixes'] / 1e6, width, bottom=df['Charges_variables'] / 1e6, color=colors['purple'],
                    label='Fixes')
            ax2.set_title('Répartition des Charges', pad=10)
            ax2.set_ylabel('Millions DZD')
            ax2.set_xticks(x)
            ax2.set_xticklabels(df.index)
            ax2.legend(loc='upper right', fontsize=9)
            canvas2 = FigureCanvas(fig2)
            canvas2.setMinimumHeight(350)
            self.graphs_layout.addWidget(canvas2)

            # Graphique 3: Rentabilité
            fig3 = Figure(figsize=fig_size)
            ax3 = fig3.add_subplot(111)
            ax3.plot(df.index, df['Taux_rentabilite'], marker='o', color=colors['green'], label='Rentabilité')
            ax3.plot(df.index, df['ROE'], marker='s', color=colors['blue'], label='ROE')
            ax3.plot(df.index, df['ROA'], marker='^', color=colors['red'], label='ROA')
            ax3.set_title('Indicateurs de Rentabilité', pad=10)
            ax3.set_ylabel('%')
            ax3.legend(loc='upper right', fontsize=9)
            canvas3 = FigureCanvas(fig3)
            canvas3.setMinimumHeight(350)
            self.graphs_layout.addWidget(canvas3)

            # Graphique 4: Bilan
            fig4 = Figure(figsize=fig_size)
            ax4 = fig4.add_subplot(111)
            bar_width = 0.3  # Barres plus fines
            x_pos = np.arange(len(df.index))
            ax4.bar(x_pos, df['Total_actif'] / 1e6, bar_width, color=colors['blue'], alpha=0.8, label='Actifs')
            ax4.bar(x_pos + bar_width, df['Total_passif'] / 1e6, bar_width, color=colors['green'], alpha=0.8,
                    label='Passifs')
            ax4.set_title('Structure du Bilan', pad=10)
            ax4.set_ylabel('Millions DZD')
            ax4.set_xticks(x_pos + bar_width / 2)
            ax4.set_xticklabels(df.index)
            ax4.legend(loc='upper right', fontsize=9)
            canvas4 = FigureCanvas(fig4)
            canvas4.setMinimumHeight(350)
            self.graphs_layout.addWidget(canvas4)

            # Graphique 5: Liquidité
            fig5 = Figure(figsize=fig_size)
            ax5 = fig5.add_subplot(111)
            ax5.plot(df.index, df['Ratio_liquidite'], marker='o', color=colors['purple'])
            ax5.axhline(y=1, color=colors['red'], linestyle='--', alpha=0.7)
            ax5.set_title('Ratio de Liquidité', pad=10)
            ax5.set_ylabel('Ratio')
            canvas5 = FigureCanvas(fig5)
            canvas5.setMinimumHeight(350)
            self.graphs_layout.addWidget(canvas5)

            # Graphique 6: Trésorerie
            fig6 = Figure(figsize=fig_size)
            ax6 = fig6.add_subplot(111)
            ax6.plot(df.index, df['Tresorerie'] / 1e6, marker='o', color=colors['orange'])
            ax6.set_title('Évolution de la Trésorerie', pad=10)
            ax6.set_ylabel('Millions DZD')
            canvas6 = FigureCanvas(fig6)
            canvas6.setMinimumHeight(350)
            self.graphs_layout.addWidget(canvas6)

        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur génération graphiques:\n{str(e)}")

    def _export_pdf(self):
        """Export PDF simplifié"""
        try:
            success, message = self.controller.export_controller.export_to_pdf("rapport_analyse.pdf")
            if success:
                QMessageBox.information(self, "Succès", "Rapport exporté!")
            else:
                QMessageBox.warning(self, "Erreur", message)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur export:\n{str(e)}")