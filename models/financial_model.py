"""from PyQt5.QtCore import QObject, pyqtSignal

from utils.constants import CATEGORY_NAMES


class FinancialModel:
    calculation_complete = pyqtSignal(dict)
    def __init__(self):
        self.data = {}
        self.ratios = {}
        self.graph_data = {}

    def update_data(self, data):
        self.data = data
        # Calculate revenue automatically
        self.data['revenue'] = self.data['gross_profit'] + self.data['cogs']

    def calculate_all_ratios(self):
        # Calculate totals
        total_current_assets = (self.data['cash'] + self.data['accounts_receivable'] +
                                self.data['inventory'] + self.data['other_current_assets'])

        total_non_current_assets = (self.data['fixed_assets'] + self.data['intangible_assets'] +
                                    self.data['long_term_investments'] + self.data['other_non_current_assets'])

        total_assets = total_current_assets + total_non_current_assets

        total_current_liabilities = (self.data['accounts_payable'] + self.data['short_term_debt'] +
                                     self.data['tax_payable'] + self.data['other_current_liabilities'])

        total_non_current_liabilities = (self.data['long_term_debt'] + self.data['provisions'] +
                                         self.data['other_non_current_liabilities'])

        total_liabilities = total_current_liabilities + total_non_current_liabilities

        total_equity = (self.data['share_capital'] + self.data['reserves'] +
                        self.data['net_income'])

        # Liquidity Ratios
        current_ratio = total_current_assets / total_current_liabilities if total_current_liabilities != 0 else 0
        quick_ratio = (total_current_assets - self.data[
            'inventory']) / total_current_liabilities if total_current_liabilities != 0 else 0
        cash_ratio = self.data['cash'] / total_current_liabilities if total_current_liabilities != 0 else 0

        # Solvency Ratios
        debt_to_equity = total_liabilities / total_equity if total_equity != 0 else 0
        financial_leverage = total_assets / total_equity if total_equity != 0 else 0
        interest_coverage = self.data['operating_income'] / self.data['financial_expenses'] if self.data[
                                                                                                   'financial_expenses'] != 0 else 0

        # Profitability Ratios
        gross_margin = self.data['gross_profit'] / self.data['revenue'] if self.data['revenue'] != 0 else 0
        operating_margin = self.data['operating_income'] / self.data['revenue'] if self.data['revenue'] != 0 else 0
        net_margin = self.data['net_profit'] / self.data['revenue'] if self.data['revenue'] != 0 else 0
        roa = self.data['net_profit'] / total_assets if total_assets != 0 else 0
        roe = self.data['net_profit'] / total_equity if total_equity != 0 else 0

        # Activity Ratios
        inventory_turnover = self.data['cogs'] / self.data['inventory'] if self.data['inventory'] != 0 else 0
        days_sales_outstanding = (self.data['accounts_receivable'] / self.data['revenue']) * 365 if self.data[
                                                                                                        'revenue'] != 0 else 0
        days_payable_outstanding = (self.data['accounts_payable'] / self.data['cogs']) * 365 if self.data[
                                                                                                    'cogs'] != 0 else 0

        # Organize all ratios
        self.ratios = {
            'liquidity': {
                'current_ratio': {
                    'value': current_ratio,
                    'components': (total_current_assets, total_current_liabilities),
                    'description': "Capacité à payer les dettes court terme (Liquidité générale)"
                },
                'quick_ratio': {
                    'value': quick_ratio,
                    'components': (total_current_assets - self.data['inventory'], total_current_liabilities),
                    'description': "Capacité à payer les dettes court terme sans les stocks (Liquidité réduite)"
                },
                'cash_ratio': {
                    'value': cash_ratio,
                    'components': (self.data['cash'], total_current_liabilities),
                    'description': "Capacité à payer les dettes court terme avec la trésorerie disponible"
                }
            },
            'solvency': {
                'debt_to_equity': {
                    'value': debt_to_equity,
                    'components': (total_liabilities, total_equity),
                    'description': "Proportion de la dette par rapport aux capitaux propres"
                },
                'financial_leverage': {
                    'value': financial_leverage,
                    'components': (total_assets, total_equity),
                    'description': "Niveau d'endettement de l'entreprise"
                },
                'interest_coverage': {
                    'value': interest_coverage,
                    'components': (self.data['operating_income'], self.data['financial_expenses']),
                    'description': "Capacité à couvrir les charges financières avec le résultat d'exploitation"
                }
            },
            'profitability': {
                'gross_margin': {
                    'value': gross_margin,
                    'components': (self.data['gross_profit'], self.data['revenue']),
                    'description': "Marge dégagée après coût des ventes"
                },
                'operating_margin': {
                    'value': operating_margin,
                    'components': (self.data['operating_income'], self.data['revenue']),
                    'description': "Marge dégagée après charges d'exploitation"
                },
                'net_margin': {
                    'value': net_margin,
                    'components': (self.data['net_profit'], self.data['revenue']),
                    'description': "Marge nette après tous les coûts et impôts"
                },
                'roa': {
                    'value': roa,
                    'components': (self.data['net_profit'], total_assets),
                    'description': "Rentabilité des actifs totaux"
                },
                'roe': {
                    'value': roe,
                    'components': (self.data['net_profit'], total_equity),
                    'description': "Rentabilité des capitaux propres"
                }
            },
            'activity': {
                'inventory_turnover': {
                    'value': inventory_turnover,
                    'components': (self.data['cogs'], self.data['inventory']),
                    'description': "Nombre de fois que le stock est renouvelé dans l'année"
                },
                'days_sales_outstanding': {
                    'value': days_sales_outstanding,
                    'components': (self.data['accounts_receivable'], self.data['revenue']),
                    'description': "Jours moyens pour recouvrer les créances clients"
                },
                'days_payable_outstanding': {
                    'value': days_payable_outstanding,
                    'components': (self.data['accounts_payable'], self.data['cogs']),
                    'description': "Jours moyens pour payer les fournisseurs"
                }
            }
        }

        # Prepare graph data
        self.prepare_graph_data()
        self.calculation_complete.emit(self.ratios)

        return self.ratios

    def prepare_graph_data(self):
        self.graph_data = {
            'liquidity': {
                'labels': [ratio['description'] for ratio in self.ratios['liquidity'].values()],
                'values': [ratio['value'] for ratio in self.ratios['liquidity'].values()],
                'amounts': [ratio['components'][0] for ratio in self.ratios['liquidity'].values()],
                'title': "Ratios de Liquidité"
            },
            'solvency': {
                'labels': [ratio['description'] for ratio in self.ratios['solvency'].values()],
                'values': [ratio['value'] for ratio in self.ratios['solvency'].values()],
                'amounts': [ratio['components'][0] for ratio in self.ratios['solvency'].values()],
                'title': "Ratios de Solvabilité"
            },
            'profitability': {
                'labels': [ratio['description'] for ratio in self.ratios['profitability'].values()],
                'values': [ratio['value'] for ratio in self.ratios['profitability'].values()],
                'amounts': [ratio['components'][0] for ratio in self.ratios['profitability'].values()],
                'title': "Ratios de Rentabilité"
            },
            'activity': {
                'labels': [ratio['description'] for ratio in self.ratios['activity'].values()],
                'values': [ratio['value'] for ratio in self.ratios['activity'].values()],
                'amounts': [ratio['components'][0] for ratio in self.ratios['activity'].values()],
                'title': "Ratios d'Activité"
            }
        }

    def get_graph_data(self, graph_type=None):
        if not graph_type:
            graph_type = 'liquidity'
        return self.graph_data.get(graph_type.lower(), {})

    def get_graph_data(self, graph_type=None):
        if not graph_type:
            graph_type = 'liquidity'

        data = self.graph_data.get(graph_type.lower(), {})
        if not data:
            return {}

        # Format the data for the view
        return {
            'labels': [ratio['description'] for ratio in self.ratios[graph_type].values()],
            'values': [ratio['value'] for ratio in self.ratios[graph_type].values()],
            'amounts': [ratio['components'][0] for ratio in self.ratios[graph_type].values()],
            'title': f"Ratios de {CATEGORY_NAMES.get(graph_type, graph_type)}"
        }

    def get_graph_data(self, graph_type):
        if not hasattr(self, 'ratios') or graph_type not in self.ratios:
            return {}

        # Prepare data for the graph
        labels = []
        values = []
        amounts = []

        for ratio_name, ratio_data in self.ratios[graph_type].items():
            labels.append(ratio_data['description'])
            values.append(ratio_data['value'])
            amounts.append(ratio_data['components'][0])

        return {
            'labels': labels,
            'values': values,
            'amounts': amounts,
            'title': f"Ratios de {CATEGORY_NAMES.get(graph_type, graph_type)}"
        }"""

from PyQt5.QtCore import QObject, pyqtSignal
from utils.constants import CATEGORY_NAMES


class FinancialModel(QObject):  # Hérite de QObject pour les signaux
    calculation_complete = pyqtSignal(dict)

    def __init__(self):
        super().__init__()  # N'oubliez pas d'appeler le parent
        self.data = {}
        self.ratios = {}
        self.graph_data = {}

    def update_data(self, data):
        self.data = data
        # Calculate revenue automatically
        if 'gross_profit' in data and 'cogs' in data:
            self.data['revenue'] = data['gross_profit'] + data['cogs']

    def calculate_all_ratios(self):
        try:
            # Vérification des données requises
            required_fields = ['cash', 'accounts_receivable', 'inventory', 'fixed_assets',
                               'accounts_payable', 'short_term_debt', 'share_capital',
                               'gross_profit', 'operating_income', 'net_profit']
            for field in required_fields:
                if field not in self.data:
                    raise ValueError(f"Champ manquant: {field}")

            # Calculate totals
            total_current_assets = (self.data['cash'] + self.data['accounts_receivable'] +
                                    self.data['inventory'] + self.data.get('other_current_assets', 0))

            total_non_current_assets = (self.data['fixed_assets'] + self.data.get('intangible_assets', 0) +
                                        self.data.get('long_term_investments', 0) + self.data.get(
                        'other_non_current_assets', 0))

            total_assets = total_current_assets + total_non_current_assets

            total_current_liabilities = (self.data['accounts_payable'] + self.data['short_term_debt'] +
                                         self.data.get('tax_payable', 0) + self.data.get('other_current_liabilities',
                                                                                         0))

            total_non_current_liabilities = (self.data.get('long_term_debt', 0) + self.data.get('provisions', 0) +
                                             self.data.get('other_non_current_liabilities', 0))

            total_liabilities = total_current_liabilities + total_non_current_liabilities

            total_equity = (self.data['share_capital'] + self.data.get('reserves', 0) +
                            self.data.get('net_income', 0))

            # Calcul des ratios (comme avant)
            current_ratio = total_current_assets / total_current_liabilities if total_current_liabilities != 0 else 0
            quick_ratio = (total_current_assets - self.data[
                'inventory']) / total_current_liabilities if total_current_liabilities != 0 else 0
            cash_ratio = self.data['cash'] / total_current_liabilities if total_current_liabilities != 0 else 0
            debt_to_equity = total_liabilities / total_equity if total_equity != 0 else 0
            financial_leverage = total_assets / total_equity if total_equity != 0 else 0
            interest_coverage = self.data['operating_income'] / self.data.get('financial_expenses', 1) if self.data.get(
                'financial_expenses', 0) != 0 else 0
            gross_margin = self.data['gross_profit'] / self.data['revenue'] if self.data.get('revenue', 0) != 0 else 0
            operating_margin = self.data['operating_income'] / self.data['revenue'] if self.data.get('revenue',
                                                                                                     0) != 0 else 0
            net_margin = self.data['net_profit'] / self.data['revenue'] if self.data.get('revenue', 0) != 0 else 0
            roa = self.data['net_profit'] / total_assets if total_assets != 0 else 0
            roe = self.data['net_profit'] / total_equity if total_equity != 0 else 0
            inventory_turnover = self.data.get('cogs', 0) / self.data['inventory'] if self.data['inventory'] != 0 else 0
            days_sales_outstanding = (self.data['accounts_receivable'] / self.data['revenue']) * 365 if self.data.get(
                'revenue', 0) != 0 else 0
            days_payable_outstanding = (self.data['accounts_payable'] / self.data.get('cogs',
                                                                                      1)) * 365 if self.data.get('cogs',
                                                                                                                 0) != 0 else 0

            # Organisation des ratios (comme avant)
            self.ratios = {
                'liquidity': {
                    'current_ratio': {'value': current_ratio,
                                      'components': (total_current_assets, total_current_liabilities),
                                      'description': "Liquidité générale"},
                    'quick_ratio': {'value': quick_ratio, 'components': (
                    total_current_assets - self.data['inventory'], total_current_liabilities),
                                    'description': "Liquidité réduite"},
                    'cash_ratio': {'value': cash_ratio, 'components': (self.data['cash'], total_current_liabilities),
                                   'description': "Liquidité immédiate"}
                },
                'solvency': {
                    'debt_to_equity': {'value': debt_to_equity, 'components': (total_liabilities, total_equity),
                                       'description': "Endettement"},
                    'financial_leverage': {'value': financial_leverage, 'components': (total_assets, total_equity),
                                           'description': "Levier financier"},
                    'interest_coverage': {'value': interest_coverage, 'components': (
                    self.data['operating_income'], self.data.get('financial_expenses', 0)),
                                          'description': "Couverture des intérêts"}
                },
                'profitability': {
                    'gross_margin': {'value': gross_margin,
                                     'components': (self.data['gross_profit'], self.data['revenue']),
                                     'description': "Marge brute"},
                    'operating_margin': {'value': operating_margin,
                                         'components': (self.data['operating_income'], self.data['revenue']),
                                         'description': "Marge opérationnelle"},
                    'net_margin': {'value': net_margin, 'components': (self.data['net_profit'], self.data['revenue']),
                                   'description': "Marge nette"},
                    'roa': {'value': roa, 'components': (self.data['net_profit'], total_assets), 'description': "ROA"},
                    'roe': {'value': roe, 'components': (self.data['net_profit'], total_equity), 'description': "ROE"}
                },
                'activity': {
                    'inventory_turnover': {'value': inventory_turnover,
                                           'components': (self.data.get('cogs', 0), self.data['inventory']),
                                           'description': "Rotation des stocks"},
                    'days_sales_outstanding': {'value': days_sales_outstanding,
                                               'components': (self.data['accounts_receivable'], self.data['revenue']),
                                               'description': "Jours clients"},
                    'days_payable_outstanding': {'value': days_payable_outstanding, 'components': (
                    self.data['accounts_payable'], self.data.get('cogs', 0)), 'description': "Jours fournisseurs"}
                }
            }

            self.prepare_graph_data()
            self.calculation_complete.emit(self.ratios)
            return self.ratios

        except Exception as e:
            print(f"Erreur dans calculate_all_ratios: {str(e)}")
            raise

    def prepare_graph_data(self):
        """Prépare les données pour les graphiques"""
        self.graph_data = {}
        for category in self.ratios:
            self.graph_data[category] = {
                'labels': [ratio['description'] for ratio in self.ratios[category].values()],
                'values': [ratio['value'] for ratio in self.ratios[category].values()],
                'amounts': [ratio['components'][0] for ratio in self.ratios[category].values()],
                'title': f"Ratios de {CATEGORY_NAMES.get(category, category)}"
            }

    def get_graph_data(self, graph_type='liquidity'):
        """Retourne les données formatées pour un type de graphique spécifique"""
        return self.graph_data.get(graph_type.lower(), {})