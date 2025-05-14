from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QComboBox, QPushButton,
                             QGridLayout, QGroupBox, QVBoxLayout, QHBoxLayout,
                             QFrame, QSizePolicy, QScrollArea)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class DataInputForm(QWidget):
    calculate_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_styles()

    def setup_styles(self):
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI';
                font-size: 12px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                border: 1px solid #d3d3d3;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px;
            }
            QLineEdit {
                border: 1px solid #d3d3d3;
                border-radius: 3px;
                padding: 5px;
                min-width: 150px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)

    def init_ui(self):
        # Layout principal avec ScrollArea
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)

        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # Titre
        title = QLabel("Formulaire de Saisie Manuelle")
        title.setFont(QFont('Segoe UI', 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Container for balance sheet (horizontal layout)
        balance_container = QWidget()
        balance_container_layout = QHBoxLayout(balance_container)
        balance_container_layout.setContentsMargins(0, 0, 0, 0)
        balance_container_layout.setSpacing(15)

        # Assets Frame
        assets_frame = QFrame()
        assets_frame.setFrameShape(QFrame.StyledPanel)
        assets_layout = QVBoxLayout(assets_frame)
        assets_layout.setContentsMargins(10, 10, 10, 10)

        # Current Assets
        current_assets_group = QGroupBox("Actifs Courants")
        current_assets_layout = QGridLayout()
        current_assets_layout.setVerticalSpacing(10)
        current_assets_layout.setHorizontalSpacing(15)

        self.cash = self.create_input(current_assets_layout, "Trésorerie", 0, 0)
        self.accounts_receivable = self.create_input(current_assets_layout, "Comptes clients", 1, 0)
        self.inventory = self.create_input(current_assets_layout, "Stocks", 2, 0)
        self.other_current_assets = self.create_input(current_assets_layout, "Autres actifs courants", 3, 0)

        current_assets_group.setLayout(current_assets_layout)
        assets_layout.addWidget(current_assets_group)

        # Non-Current Assets
        non_current_assets_group = QGroupBox("Actifs Non Courants")
        non_current_assets_layout = QGridLayout()
        non_current_assets_layout.setVerticalSpacing(10)
        non_current_assets_layout.setHorizontalSpacing(15)

        self.fixed_assets = self.create_input(non_current_assets_layout, "Immobilisations corporelles", 0, 0)
        self.intangible_assets = self.create_input(non_current_assets_layout, "Immobilisations incorporelles", 1, 0)
        self.long_term_investments = self.create_input(non_current_assets_layout, "Investissements long terme", 2, 0)
        self.other_non_current_assets = self.create_input(non_current_assets_layout, "Autres actifs non courants", 3, 0)

        non_current_assets_group.setLayout(non_current_assets_layout)
        assets_layout.addWidget(non_current_assets_group)

        balance_container_layout.addWidget(assets_frame)

        # Liabilities Frame
        liabilities_frame = QFrame()
        liabilities_frame.setFrameShape(QFrame.StyledPanel)
        liabilities_layout = QVBoxLayout(liabilities_frame)
        liabilities_layout.setContentsMargins(10, 10, 10, 10)

        # Current Liabilities
        current_liabilities_group = QGroupBox("Passifs Courants")
        current_liabilities_layout = QGridLayout()
        current_liabilities_layout.setVerticalSpacing(10)
        current_liabilities_layout.setHorizontalSpacing(15)

        self.accounts_payable = self.create_input(current_liabilities_layout, "Dettes fournisseurs", 0, 0)
        self.short_term_debt = self.create_input(current_liabilities_layout, "Emprunts court terme", 1, 0)
        self.tax_payable = self.create_input(current_liabilities_layout, "Dettes fiscales", 2, 0)
        self.other_current_liabilities = self.create_input(current_liabilities_layout, "Autres passifs courants", 3, 0)

        current_liabilities_group.setLayout(current_liabilities_layout)
        liabilities_layout.addWidget(current_liabilities_group)

        # Non-Current Liabilities
        non_current_liabilities_group = QGroupBox("Passifs Non Courants")
        non_current_liabilities_layout = QGridLayout()
        non_current_liabilities_layout.setVerticalSpacing(10)
        non_current_liabilities_layout.setHorizontalSpacing(15)

        self.long_term_debt = self.create_input(non_current_liabilities_layout, "Emprunts long terme", 0, 0)
        self.provisions = self.create_input(non_current_liabilities_layout, "Provisions pour risques", 1, 0)
        self.other_non_current_liabilities = self.create_input(non_current_liabilities_layout,
                                                               "Autres passifs non courants", 2, 0)

        non_current_liabilities_group.setLayout(non_current_liabilities_layout)
        liabilities_layout.addWidget(non_current_liabilities_group)

        # Equity
        equity_group = QGroupBox("Capitaux Propres")
        equity_layout = QGridLayout()
        equity_layout.setVerticalSpacing(10)
        equity_layout.setHorizontalSpacing(15)

        self.share_capital = self.create_input(equity_layout, "Capital social", 0, 0)
        self.reserves = self.create_input(equity_layout, "Réserves", 1, 0)
        self.net_income = self.create_input(equity_layout, "Résultat de l'exercice", 2, 0)

        equity_group.setLayout(equity_layout)
        liabilities_layout.addWidget(equity_group)

        balance_container_layout.addWidget(liabilities_frame)
        main_layout.addWidget(balance_container)

        # Income Statement
        income_group = QGroupBox("Compte de Résultat")
        income_layout = QGridLayout()
        income_layout.setVerticalSpacing(10)
        income_layout.setHorizontalSpacing(15)

        # First column
        self.cogs = self.create_input(income_layout, "Coût des ventes", 0, 0)
        self.gross_profit = self.create_input(income_layout, "Résultat brut", 1, 0)
        self.operating_expenses = self.create_input(income_layout, "Charges d'exploitation", 2, 0)
        self.operating_income = self.create_input(income_layout, "Résultat d'exploitation", 3, 0)

        # Second column
        self.financial_income = self.create_input(income_layout, "Produits financiers", 0, 2)
        self.financial_expenses = self.create_input(income_layout, "Charges financières", 1, 2)
        self.income_before_tax = self.create_input(income_layout, "Résultat avant impôts", 2, 2)
        self.tax_expense = self.create_input(income_layout, "Impôts sur les bénéfices", 3, 2)
        self.net_profit = self.create_input(income_layout, "Résultat net", 4, 2)

        income_group.setLayout(income_layout)
        main_layout.addWidget(income_group)

        # Additional Data
        other_group = QGroupBox("Données Complémentaires")
        other_layout = QGridLayout()
        other_layout.setVerticalSpacing(10)
        other_layout.setHorizontalSpacing(15)

        self.employees = self.create_input(other_layout, "Nombre d'employés", 0, 0)
        self.market_cap = self.create_input(other_layout, "Valeur marchande (si cotée)", 1, 0)

        self.industry = QComboBox()
        self.industry.addItems(["Technologie", "Industrie", "Services", "Commerce", "Autre"])
        other_layout.addWidget(QLabel("Secteur d'activité"), 2, 0)
        other_layout.addWidget(self.industry, 2, 1)

        other_group.setLayout(other_layout)
        main_layout.addWidget(other_group)

        # Boutons en bas
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        self.calculate_btn = QPushButton("Calculer les Indicateurs")
        self.calculate_btn.clicked.connect(self.calculate_clicked.emit)
        buttons_layout.addWidget(self.calculate_btn)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

        scroll.setWidget(main_widget)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(scroll)

    def create_input(self, layout, label, row, col):
        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-weight: bold;")
        layout.addWidget(label_widget, row, col)

        input_field = QLineEdit()
        input_field.setPlaceholderText("0.00")
        input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        layout.addWidget(input_field, row, col + 1)
        return input_field

    def get_input_data(self):
        data = {
            # Actifs
            'cash': float(self.cash.text() or 0),
            'accounts_receivable': float(self.accounts_receivable.text() or 0),
            'inventory': float(self.inventory.text() or 0),
            'other_current_assets': float(self.other_current_assets.text() or 0),
            'fixed_assets': float(self.fixed_assets.text() or 0),
            'intangible_assets': float(self.intangible_assets.text() or 0),
            'long_term_investments': float(self.long_term_investments.text() or 0),
            'other_non_current_assets': float(self.other_non_current_assets.text() or 0),

            # Passifs
            'accounts_payable': float(self.accounts_payable.text() or 0),
            'short_term_debt': float(self.short_term_debt.text() or 0),
            'tax_payable': float(self.tax_payable.text() or 0),
            'other_current_liabilities': float(self.other_current_liabilities.text() or 0),
            'long_term_debt': float(self.long_term_debt.text() or 0),
            'provisions': float(self.provisions.text() or 0),
            'other_non_current_liabilities': float(self.other_non_current_liabilities.text() or 0),

            # Capitaux propres
            'share_capital': float(self.share_capital.text() or 0),
            'reserves': float(self.reserves.text() or 0),
            'net_income': float(self.net_income.text() or 0),

            # Compte de résultat
            'cogs': float(self.cogs.text() or 0),
            'gross_profit': float(self.gross_profit.text() or 0),
            'operating_expenses': float(self.operating_expenses.text() or 0),
            'operating_income': float(self.operating_income.text() or 0),
            'financial_income': float(self.financial_income.text() or 0),
            'financial_expenses': float(self.financial_expenses.text() or 0),
            'income_before_tax': float(self.income_before_tax.text() or 0),
            'tax_expense': float(self.tax_expense.text() or 0),
            'net_profit': float(self.net_profit.text() or 0),

            # Autres
            'employees': int(self.employees.text() or 0),
            'market_cap': float(self.market_cap.text() or 0),
            'industry': self.industry.currentText()
        }
        return data