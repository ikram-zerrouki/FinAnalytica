from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush, QLinearGradient


class DataTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # Main layout with some spacing
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Title label
        title = QLabel("Données Comptables")
        title.setFont(QFont('Montserrat', 18, QFont.Bold))
        title.setStyleSheet("color: #2c3e50;")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #e1e5eb; margin: 5px 0;")
        self.layout.addWidget(separator)

        # Create the table with modern styling
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        # Table styling
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #dee2e6;
                gridline-color: #e9ecef;
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
        """)

        # Header styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setDefaultAlignment(Qt.AlignCenter)
        header.setHighlightSections(False)

        vertical_header = self.table.verticalHeader()
        vertical_header.setSectionResizeMode(QHeaderView.ResizeToContents)
        vertical_header.setDefaultAlignment(Qt.AlignRight)
        vertical_header.setHighlightSections(False)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_data(self):
        raw_data = self.controller.get_raw_data()
        if not raw_data:
            return

        years = sorted(raw_data.keys())
        metrics = list(raw_data[years[0]].keys())

        self.table.setRowCount(len(metrics))
        self.table.setColumnCount(len(years))
        self.table.setHorizontalHeaderLabels([f"Année {year}" for year in years])
        self.table.setVerticalHeaderLabels([m.replace('_', ' ').title() for m in metrics])

        # Set alternating row colors
        for row in range(len(metrics)):
            if row % 2 == 0:
                self.table.setRowHeight(row, 30)  # Slightly taller rows
            else:
                self.table.setRowHeight(row, 30)

        for col, year in enumerate(years):
            for row, metric in enumerate(metrics):
                value = raw_data[year][metric]
                item = QTableWidgetItem(f"{value:,.2f}" if isinstance(value, (int, float)) else str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # Formatting based on value type
                if isinstance(value, (int, float)):
                    if value < 0:
                        item.setForeground(QBrush(QColor("#e74c3c")))  # Red for negative
                    else:
                        item.setForeground(QBrush(QColor("#27ae60")))  # Green for positive

                # Highlight current year column
                if year == max(years):
                    item.setBackground(QBrush(QColor("#f8f9fa")))

                self.table.setItem(row, col, item)

        # Additional styling after data is loaded
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(self.table.styleSheet() + """
            QTableWidget {
                alternate-background-color: #f8f9fa;
            }
        """)