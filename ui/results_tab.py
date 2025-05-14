from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
                             QHeaderView, QLabel, QFrame)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor, QBrush


class ResultsTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self._init_ui()

    def _init_ui(self):
        # Main layout with spacing and margins
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Title label
        title = QLabel("Résultats Financiers")
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
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 6px;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
        """)

        # Header styling
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        header.setHighlightSections(False)

        vertical_header = self.table.verticalHeader()
        vertical_header.setDefaultAlignment(Qt.AlignRight)
        vertical_header.setHighlightSections(False)
        vertical_header.setSectionResizeMode(QHeaderView.Fixed)
        vertical_header.setDefaultSectionSize(30)

        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_results(self):
        df = self.controller.get_processed_data()
        if df.empty:
            return

        # Transposer le DataFrame pour avoir une vue verticale
        df = df.transpose()

        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels([str(col) for col in df.columns])
        self.table.setVerticalHeaderLabels([str(idx).replace('_', ' ').title() for idx in df.index])

        # Color thresholds for financial metrics
        positive_color = QColor("#27ae60")  # Green
        negative_color = QColor("#e74c3c")  # Red
        neutral_color = QColor("#2c3e50")  # Dark blue

        for i, row in enumerate(df.index):
            for j, col in enumerate(df.columns):
                value = df.loc[row, col]
                item = QTableWidgetItem(f"{value:,.2f}" if isinstance(value, (int, float)) else str(value))
                item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                # Apply conditional formatting
                if isinstance(value, (int, float)):
                    if 'ratio' in str(row).lower() or 'taux' in str(row).lower():
                        if value > 1:
                            item.setForeground(QBrush(positive_color))
                        elif value < 1:
                            item.setForeground(QBrush(negative_color))
                    elif value < 0:
                        item.setForeground(QBrush(negative_color))
                    else:
                        item.setForeground(QBrush(neutral_color))

                # Highlight important rows
                if 'profit' in str(row).lower() or 'bénéfice' in str(row).lower():
                    item.setFont(QFont('Arial', weight=QFont.Bold))

                self.table.setItem(i, j, item)

        # Adjust column widths after data is loaded
        self.table.resizeColumnsToContents()
        self.table.setAlternatingRowColors(True)