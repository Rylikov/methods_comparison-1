import sys
import os

from PyQt5 import QtWidgets
import numpy as np

from aplication.design import Ui_MainWindow
from aplication.dialog import Ui_Dialog
from core.data import Data


class DialogView(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.dimension_spinbox.valueChanged.connect(self.spinbox_change)
        self.dimension_slider.valueChanged.connect(self.slider_change)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def slider_change(self):
        # will be realised later
        pass

    def spinbox_change(self):
        # will be realised later
        pass

    @staticmethod
    def get_matrx():
        dialog = DialogView()
        result = dialog.exec_()
        matr = [[], [], []]
        for i in range(3):
            matr[0].append(dialog.matr_layout.itemAt(i).widget().value())
        for i in range(3, 6):
            matr[1].append(dialog.matr_layout.itemAt(i).widget().value())
        for i in range(6, 9):
            matr[2].append(dialog.matr_layout.itemAt(i).widget().value())
        return result, matr


class AppView(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.task = None
        # connections goes here
        self.pushButton.clicked.connect(self.calc)
        self.input_button.clicked.connect(self.set_matrix)
        self.radio_file.toggled.connect(self.button_title_set_file)
        self.radio_keyboard.toggled.connect(self.button_title_set_kb)
        self.min_type_radio.toggled.connect(self.set_task_type)
        self.max_type_radio.toggled.connect(self.set_task_type)

    def calc(self):
        if not self.task:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText("Enter matrix first!")
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            self.brute_info_browser.append("Your's matrix:\n")
            self.bellman_info_browser.append("Your's matrix:\n")
            for row in self.task.matrix:
                tmp_string = '|   '
                for item in row:
                    tmp_string += (str(item) + '   ')
                tmp_string += "|"
                self.brute_info_browser.append(tmp_string)
                self.bellman_info_browser.append(tmp_string)
            first_city = self.first_city_spin_box.value()
            first_city = first_city if first_city != 1 else 1
            self.task.solve(first_city=first_city)
            self.brute_info_browser.append('Solve results:\nAnswer: %s\nSolve time: % 1.6f seconds' %
                                           (self.task.result, self.task.resolve_time))

            self.task.solve(method='dynamic', first_city=first_city)
            self.bellman_info_browser.append('Solve results:\nAnswer: %s\nSolve time: % 1.6f seconds' %
                                             (self.task.result, self.task.resolve_time))

    def set_matrix(self):
        if self.radio_file.isChecked():
            file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Choose file', os.path.expanduser('~'),
                                                              'Text file (*.txt);;All files (*)')[0]
            if file_name:
                task_type = 'min'
                if self.max_type_radio.isChecked():
                    task_type = 'max'
                self.task = Data(file_name, task_type=task_type, from_file=True)
                self.first_city_spin_box.setMaximum(len(self.task.matrix))
        if self.radio_keyboard.isChecked():
            task_type = 'min'
            if self.max_type_radio.isChecked():
                task_type = 'max'
            dialog = DialogView.get_matrx()
            if dialog[0]:
                matrix = np.array(dialog[1])
                self.task = Data(matrix, task_type=task_type)
                self.first_city_spin_box.setMaximum(len(self.task.matrix))

    def button_title_set_file(self):
        self.input_button.setText('Choose file')

    def button_title_set_kb(self):
        self.input_button.setText('Enter matrix')

    def set_task_type(self):
        if self.task:
            if self.min_type_radio.isChecked():
                self.task.task_type = 'min'
            else:
                self.task.task_type = 'max'


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = AppView()
    window.setWindowTitle("Methods comparison")
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
