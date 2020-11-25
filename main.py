from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QTableWidgetItem
from PyQt5 import uic

import sys
import sqlite3


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.tw.itemDoubleClicked.connect(self.open_inf)

        self.fill_table()

    def fill_table(self):
        self.tw.setColumnCount(7)
        self.tw.setHorizontalHeaderLabels(
            ['ID', 'Название', 'Степень обжарки', 'Тип',
             'Описание', 'Цена', 'Объём упаковки'])

        cur = self.con.cursor()
        for i in cur.execute('''SELECT * FROM Drinks
        INNER JOIN Roasts
        ON Drinks.roast=Roasts.id''').fetchall():
            i = i[:2] + (i[-1],) + i[3:-2]
            self.tw.setRowCount(self.tw.rowCount() + 1)
            for j in enumerate(i):
                print(j)
                if j[0] == 3:
                    j = (j[0], 'Молотый' if j[1] else 'В зёрнах')
                self.tw.setItem(self.tw.rowCount() - 1, j[0], QTableWidgetItem(str(j[1])))

    def open_inf(self, item):
        mes = QMessageBox.information(self,
                                      'Просмотр элемента',
                                      item.text(),
                                      QMessageBox.Ok, QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wind = Window()
    wind.show()
    sys.exit(app.exec())
