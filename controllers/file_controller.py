from PyQt5.QtCore import QObject


class FileController(QObject):
    def __init__(self, main_controller):
        super().__init__()
        self.main_controller = main_controller

    def load_excel_file(self, file_path):
        return self.main_controller.model.load_excel_data(file_path)