import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal


class DataLoader(QObject):
    loading_complete = pyqtSignal(dict)
    loading_failed = pyqtSignal(str)

    def load_excel(self, file_path):
        try:
            xls = pd.ExcelFile(file_path)
            data = {}
            for sheet in xls.sheet_names:
                if sheet.isdigit() and len(sheet) == 4:
                    df = pd.read_excel(xls, sheet_name=sheet).fillna("")
                    data[int(sheet)] = df
            self.loading_complete.emit(data)
        except Exception as e:
            self.loading_failed.emit(f"Erreur de chargement: {str(e)}")