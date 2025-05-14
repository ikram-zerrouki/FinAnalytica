import pandas as pd
import unicodedata
from PyQt5.QtCore import QObject, pyqtSignal


class BilanModel(QObject):
    data_updated = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.raw_data = {}
        self.processed_data = pd.DataFrame()
        self.trends = {}

    @staticmethod
    def clean_value(value):
        if isinstance(value, str):
            value = value.replace(',', '.')
            value = ''.join(c for c in value if c.isdigit() or c == '.' or c == '-')
            try:
                return float(value)
            except:
                return 0
        return value if pd.notna(value) else 0

    @staticmethod
    def normalize(text):
        if not isinstance(text, str):
            text = str(text) if text is not None else ""
        text = text.lower()
        text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
        return text.strip()