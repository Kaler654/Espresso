import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
import sqlite3


class Coffee(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)
        self.initUI()

    def initUI(self):
        self.load_table()
        self.pushButton.clicked.connect(self.call_add_form)
        self.pushButton_2.clicked.connect(self.call_change_form)

    def get_coffee(self):
        """Получение всех фильмов и их параметров из БД"""
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        con.close()
        return result

    def load_table(self):
        """Отображение БД в QTableWidget"""
        films = self.get_coffee()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Тип",
                                                    "Описание вкуса", "Цена", "Объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(films):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def call_add_form(self):
        """Вызов формы для заполнения параметров нового фильма"""
        self.form = FormAddFilm(self.tableWidget)
        self.form.show()

    def call_change_form(self):
        """Изменение информации о фильме"""
        try:
            item_row = self.tableWidget.selectedItems()[0].row()
            self.label.setText("")
            film_info = [self.tableWidget.item(item_row, 0).text(),
                         self.tableWidget.item(item_row, 1).text(),
                         self.tableWidget.item(item_row, 2).text(),
                         self.tableWidget.item(item_row, 3).text(),
                         self.tableWidget.item(item_row, 4).text(),
                         self.tableWidget.item(item_row, 5).text(),
                         self.tableWidget.item(item_row, 6).text()]
            self.form_change_element = FormChangeFilm(film_info, self.tableWidget)
            self.form_change_element.show()
        except IndexError:
            self.label.setText("Фильм для редактирования не выделен")


class FormAddFilm(QMainWindow):
    def __init__(self, tableWidget):
        super().__init__()
        uic.loadUi("Form_add_element.ui", self)
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        con.close()
        self.comboBox.addItems(["молотый", "в зернах"])
        self.initUI(tableWidget)

    def initUI(self, tableWidget):
        self.pushButton.clicked.connect(self.add_element_to_bd)
        self.tableWidget = tableWidget

    def add_element_to_bd(self):
        """Добавление эелемента в БД"""
        title = self.lineEdit.text()
        roasting = self.lineEdit_2.text()
        coffee_type = self.comboBox.currentText()
        taste_desc = self.lineEdit_3.text()
        price = self.lineEdit_4.text()
        pack_vol = self.lineEdit_5.text()
        try:
            if int(price) > 0:
                con = sqlite3.connect("coffee.sqlite")
                cur = con.cursor()
                coffee_id = cur.execute(f"""SELECT id from coffee""").fetchall()[-1][0] + 1
                cur.execute(
                    f"""INSERT INTO coffee(id,title,roasting,coffee_type,taste_desc,price,pack_vol) 
                        VALUES({coffee_id},'{title}',{roasting},'{coffee_type}',
                        {taste_desc},{price},{pack_vol})""")
                con.commit()
                con.close()
                self.load_table_coffee()
                self.close()
            else:
                self.label_5.setText("Неверно заполнена форма")
        except ValueError:
            self.label_5.setText("Неверно заполнена форма")

    def load_table_coffee(self):
        """Отображение БД в QTableWidget"""
        films = self.get_films()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Тип",
                                                    "Описание вкуса", "Цена", "Объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(films):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def get_films(self):
        """Получение нужных фильмов из БД"""
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        con.close()
        return result


class FormChangeFilm(QMainWindow):
    def __init__(self, item_info, tableWidget):
        super().__init__()
        uic.loadUi("Form_change_element.ui", self)
        self.initUI(item_info, tableWidget)

    def initUI(self, item_info, tableWidget):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute("""SELECT * FROM coffee""").fetchall()
        con.close()
        self.comboBox.addItems(["молотый", "в зернах"])
        self.pushButton.clicked.connect(self.change_element_bd_and_table)
        self.item_info = item_info
        self.tableWidget = tableWidget
        self.show_film_param()

    def change_element_bd_and_table(self):
        title = self.lineEdit.text()
        roasting = self.lineEdit_2.text()
        coffee_type = self.comboBox.currentText()
        taste_desc = self.lineEdit_3.text()
        price = self.lineEdit_4.text()
        pack_vol = self.lineEdit_5.text()
        try:
            if int(price) > 0:
                con = sqlite3.connect("coffee.sqlite")
                cur = con.cursor()
                cur.execute(f"""UPDATE coffee
                        SET title = '{title}',
                            roasting = {roasting},
                            coffee_type = '{coffee_type}',
                            taste_desc = {taste_desc},
                            price = {price},
                            pack_vol = {pack_vol}
                        WHERE id = {self.last_id}""")
                con.commit()
                con.close()
                self.load_table_films()
                self.close()
            else:
                self.label_5.setText("Неверно заполнена форма")
        except ValueError:
            self.label_5.setText("Неверно заполнена форма")

    def show_film_param(self):
        """Заполнение параметров фильма"""
        self.last_id = self.item_info[0]
        self.last_title = self.item_info[1]
        self.last_roasting = self.item_info[2]
        self.last_coffee_type = self.item_info[3]
        self.last_taste_desc = self.item_info[4]
        self.last_price = self.item_info[5]
        self.last_pack_vol = self.item_info[6]
        self.lineEdit.setText(self.last_title)
        self.lineEdit_2.setText(self.last_roasting)
        self.comboBox.setCurrentText(self.last_coffee_type)
        self.lineEdit_3.setText(self.last_taste_desc)
        self.lineEdit_4.setText(self.last_price)
        self.lineEdit_5.setText(self.last_pack_vol)

    def get_data(self):
        """Получение всех фильмов и их параметров из БД"""
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM coffee""").fetchall()
        con.close()
        return result

    def load_table_films(self):
        """Отображение БД в QTableWidget"""
        films = self.get_data()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название сорта", "Степень обжарки", "Тип",
                                                    "Описание вкуса", "Цена", "Объем упаковки"])
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(films):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Coffee()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
