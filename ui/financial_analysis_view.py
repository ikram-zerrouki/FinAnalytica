from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QSizePolicy, QSpacerItem, QScrollArea)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from ui.data_input import DataInputForm
from ui.results_view import ResultsView


class FinancialAnalysisView(QWidget):
    return_requested = pyqtSignal()  # Signal for returning to home page

    def __init__(self, controller=None):
        super().__init__()
        self.controller = controller
        self.setup_ui()
        self.setup_styles()

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QTabWidget::pane {
                border: 1px solid #dcdcdc;
                border-radius: 4px;
                margin-top: 5px;
            }
            QTabBar::tab {
                background: #f5f5f5;
                border: 1px solid #dcdcdc;
                padding: 8px 12px;
                min-width: 120px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #2196F3;
                color: white;
                border-bottom-color: #2196F3;
            }
            QTabBar::tab:hover {
                background: #e3f2fd;
            }
        """)

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 10)

        self.return_btn = QPushButton("← Retour")
        self.return_btn.setFixedWidth(80)
        self.return_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
        """)
        self.return_btn.clicked.connect(self.return_requested.emit)
        header_layout.addWidget(self.return_btn)
        header_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        main_layout.addLayout(header_layout)

        self.tabs = QTabWidget()
        self.tabs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        main_layout.addWidget(self.tabs)

        self.data_input = DataInputForm()
        self.data_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tabs.addTab(self.data_input, "Saisie des Données")

        self.results_view = ResultsView()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.results_view)

        self.tabs.addTab(scroll_area, "Résultats et Graphiques")

    def show_results_tab(self):
        self.tabs.setCurrentIndex(1)

    def get_input_data(self):
        return self.data_input.get_input_data()

    def display_results(self, results):
        self.results_view.display_results(results)
        self.show_results_tab()
