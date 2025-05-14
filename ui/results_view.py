from PyQt5.QtWidgets import (QWidget, QLabel, QTreeWidget, QTreeWidgetItem,
                             QComboBox, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QSizePolicy, QHeaderView)
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtGui import QFont, QColor
import matplotlib

matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from utils.constants import *


class ResultsView(QWidget):
    graph_type_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.graph_data = None
        self.current_graph_type = 'liquidity'
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        results_group = QGroupBox("Ratios Financiers")
        results_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px;
                border: 1px solid #3A7BFF;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        results_layout = QVBoxLayout()
        results_layout.setContentsMargins(10, 15, 10, 10)

        self.results_tree = QTreeWidget()
        self.results_tree.setStyleSheet("""
            QTreeWidget {
                font: 12px;
                border: 1px solid #DDD;
                border-radius: 3px;
            }
            QTreeWidget::item {
                padding: 5px 0;
            }
            QTreeWidget::item:hover {
                background-color: #E6F0FF;
            }
        """)
        self.results_tree.setHeaderLabels(["Description", f"Valeur ({CURRENCY})", "Pourcentage", "Interprétation"])
        self.results_tree.setColumnWidth(0, 350)
        self.results_tree.setColumnWidth(1, 150)
        self.results_tree.setColumnWidth(2, 100)
        self.results_tree.setColumnWidth(3, 400)
        self.results_tree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.results_tree.setMinimumHeight(250)

        header = self.results_tree.header()
        header.setStyleSheet("""
            QHeaderView::section {
                background-color: #3A7BFF;
                color: white;
                padding: 5px;
                border: none;
                font: bold 12px;
            }
        """)
        header.setSectionResizeMode(3, QHeaderView.Stretch)

        results_layout.addWidget(self.results_tree)
        results_group.setLayout(results_layout)
        layout.addWidget(results_group)

        graph_group = QGroupBox("Visualisation")
        graph_group.setStyleSheet("""
            QGroupBox {
                font: bold 14px;
                border: 1px solid #3A7BFF;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
        """)
        graph_layout = QVBoxLayout()
        graph_layout.setContentsMargins(10, 15, 10, 10)
        graph_layout.setSpacing(10)

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel("Type de graphique:")
        label.setStyleSheet("font: 12px;")

        self.graph_selector = QComboBox()
        self.graph_selector.setStyleSheet("""
            QComboBox {
                font: 12px;
                padding: 5px;
                border: 1px solid #CCC;
                border-radius: 3px;
                min-width: 150px;
            }
            QComboBox:hover {
                border: 1px solid #3A7BFF;
            }
        """)
        self.graph_selector.addItems(["Liquidité", "Solvabilité", "Rentabilité", "Activité"])
        self.graph_selector.currentTextChanged.connect(self.on_graph_type_changed)

        controls_layout.addWidget(label)
        controls_layout.addWidget(self.graph_selector)
        controls_layout.addStretch()
        graph_layout.addLayout(controls_layout)

        self.figure = Figure(figsize=(10, 6), tight_layout=True)
        self.figure.set_facecolor('#F5F5F5')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: white; border: 1px solid #DDD; border-radius: 3px;")
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas.setMinimumHeight(350)

        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background-color: #F5F5F5;
                border: 1px solid #DDD;
                border-radius: 3px;
                padding: 2px;
            }
            QToolButton {
                background-color: transparent;
                border: 1px solid transparent;
                border-radius: 3px;
                padding: 3px;
            }
            QToolButton:hover {
                background-color: #E6F0FF;
                border: 1px solid #3A7BFF;
            }
        """)

        graph_layout.addWidget(self.toolbar)
        graph_layout.addWidget(self.canvas)
        graph_group.setLayout(graph_layout)
        layout.addWidget(graph_group)

    def sizeHint(self):
        return QSize(1000, 800)

    def on_graph_type_changed(self, text):
        mapping = {
            "Liquidité": "liquidity",
            "Solvabilité": "solvency",
            "Rentabilité": "profitability",
            "Activité": "activity"
        }
        self.current_graph_type = mapping.get(text, "liquidity")
        self.update_graph()

    def display_results(self, ratios):
        self.results_tree.clear()

        for category, category_ratios in ratios.items():
            category_item = QTreeWidgetItem([CATEGORY_NAMES.get(category, category), "", "", ""])
            category_item.setFlags(category_item.flags() | Qt.ItemIsTristate)
            category_item.setBackground(0, QColor('#E6F0FF'))
            category_item.setFont(0, QFont('Arial', 12, QFont.Bold))

            for ratio_name, ratio_data in category_ratios.items():
                value = ratio_data['value']
                description = ratio_data['description']
                components = ratio_data['components']

                if isinstance(components, tuple):
                    components_str = f"{components[0]:,.2f} / {components[1]:,.2f}"
                else:
                    components_str = f"{components:,.2f}"

                if category == 'liquidity':
                    interpretation = get_interpretation(value, LIQUIDITY_THRESHOLDS)
                elif category == 'solvency':
                    if ratio_name == 'debt_to_equity':
                        interpretation = get_interpretation(value, DEBT_EQUITY_THRESHOLDS)
                    elif ratio_name == 'financial_leverage':
                        interpretation = get_interpretation(value, LEVERAGE_THRESHOLDS)
                    else:
                        interpretation = get_interpretation(value, INTEREST_COVERAGE_THRESHOLDS)
                elif category == 'profitability':
                    interpretation = get_interpretation(value, PROFITABILITY_THRESHOLDS)
                elif category == 'activity':
                    if ratio_name == 'inventory_turnover':
                        interpretation = get_interpretation(value, INVENTORY_TURNOVER_THRESHOLDS)
                    elif ratio_name == 'days_sales_outstanding':
                        interpretation = get_interpretation(value, DSO_THRESHOLDS)
                    else:
                        interpretation = get_interpretation(value, DPO_THRESHOLDS)
                else:
                    interpretation = "Non interprétable"

                if ratio_name in ['days_sales_outstanding', 'days_payable_outstanding']:
                    value_str = f"{value:.1f} jours"
                elif ratio_name == 'inventory_turnover':
                    value_str = f"{value:.2f}x"
                else:
                    value_str = f"{value:.2%}"

                ratio_item = QTreeWidgetItem([
                    description,
                    components_str,
                    value_str,
                    interpretation
                ])

                if self.results_tree.indexOfTopLevelItem(category_item) % 2 == 0:
                    for i in range(4):
                        ratio_item.setBackground(i, QColor('#F9F9F9'))

                category_item.addChild(ratio_item)

            self.results_tree.addTopLevelItem(category_item)

        self.results_tree.expandAll()

    def update_graph_data(self, graph_data):
        self.graph_data = graph_data
        self.update_graph()

    def update_graph(self):
        if not self.graph_data:
            return

        try:
            data = self.graph_data.get(self.current_graph_type, {})
            if not data:
                return

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.set_facecolor('#F5F5F5')
            ax.grid(True, linestyle='--', alpha=0.6)

            x = range(len(data['labels']))
            width = 0.35

            bars1 = ax.bar(x, data['values'], width, color='#3A7BFF', label='Ratio')
            ax.set_ylabel('Valeur du ratio', fontweight='bold')
            ax.set_title(data['title'], fontweight='bold', pad=20)

            ax2 = ax.twinx()
            bars2 = ax2.bar([i + width for i in x], data['amounts'], width, color='#FF914D',
                            label=f'Montant ({CURRENCY})')
            ax2.set_ylabel(f'Montant ({CURRENCY})', fontweight='bold')

            ax.set_xticks([i + width / 2 for i in x])
            ax.set_xticklabels(data['labels'], rotation=45, ha='right', fontsize=10)

            lines1, labels1 = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            ax.legend(lines1 + lines2, labels1 + labels2, loc='upper right')

            for bar in bars1:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2, height,
                        f'{height:.2%}',
                        ha='center', va='bottom', fontsize=9)

            for bar in bars2:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width() / 2, height,
                         f'{height:,.2f}',
                         ha='center', va='bottom', fontsize=9)

            self.canvas.draw()
        except Exception as e:
            print("Erreur lors de l'affichage du graphique :", e)
