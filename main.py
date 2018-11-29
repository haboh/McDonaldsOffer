import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QPushButton, QPlainTextEdit, QLineEdit
from PyQt5.QtCore import Qt


WIDTH = 300
HEIGHT_OF_UNIT = 40
COUNT_SIZE = 50

class Unit:
    def __init__(self, display, name, price,):
        self.name = name
        self.price = price
        self.display = display
        self.descreption = name + ' - ' + str(self.price) + ' руб.'
        self.check = QCheckBox(self.descreption, self.display)
        self.offered = False
        self.check.stateChanged.connect(self.change_state)
        self.check.resize(WIDTH - COUNT_SIZE, HEIGHT_OF_UNIT)
        self.size = QLineEdit(self.display)
        self.size.setEnabled(False)
        self.size.resize(COUNT_SIZE, HEIGHT_OF_UNIT)
        self.size.setText('1')

    def change_state(self, state):
        self.offered = state == Qt.Checked
        self.size.setEnabled(self.offered)

    def move(self, x, y):
        self.check.move(x, y)
        self.size.move(x + WIDTH - COUNT_SIZE, y)

    def get_text(self):
        if self.offered:
            return self.descreption
        else:
            return ''

    def get_size(self):
        try:
            self.count = max(int(self.size.text()), 1)
        except ValueError:
            exit()
        return self.count


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, WIDTH, HEIGHT_OF_UNIT * len(products) + 50)
        self.setWindowTitle('Заказ в McDonalds')
        self.list_of_units = []
        x, y = 0, 0
        for product in products:
            self.list_of_units.append(Unit(self, product[0], product[1]))
            self.list_of_units[-1].move(x, y)
            y += HEIGHT_OF_UNIT
        self.main_button = QPushButton('Заказать', self)
        self.main_button.move(x, y + 5)
        self.main_button.clicked.connect(self.print_check)
        self.receipt = QPlainTextEdit(self)
        self.receipt.setVisible(False)
        self.receipt.resize(WIDTH, HEIGHT_OF_UNIT * len(products) + 50)

    def print_check(self):
        # self.main_button.deleteLater()
        self.main_button.setVisible(False)
        for product in self.list_of_units:
            product.check.setVisible(False)
        self.receipt.setVisible(True)
        text = "==================Чек===================\n"
        total = 0
        for product in self.list_of_units:
            if product.offered:
                pos = product.get_size()
                text += product.get_text() + " x " + str(pos) + '\n'
                total += product.price * pos
        text += '========================================' + "\n"
        text += 'Итого: ' + str(total) + ' руб.'
        self.receipt.setPlainText(text)


if __name__ == '__main__':
    #Список всех позиций
    products = [
        ('Биг Мак', 137),
        ('Макчикен', 105),
        ('Чизбургер', 50),
        ('Салат Цезарь', 278),
        ('Фиш Ролл', 168),
        ('Биг Тейсти', 252),
        ('Гамбургер', 48),
    ]
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
