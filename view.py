import cv2
import commands
from threading import Thread


class Screen:
    def __init__(self, name, image, commands=None):
        if commands is None:
            commands = []

        self.name = name
        self.image = image
        self.commands = commands

    def add_commands(self, commands):
        self.commands = commands



approveScreen = Screen(
    'Подтверждение ассистентом',
    'screens/12.jpg'
)

cancelScreen = Screen(
    'Отмена покупки',
    'screens/10.jpg'
)

addItemScreen = Screen(
    'Добавление товаров',
    'screens/3.jpg'
)

startScreen = Screen(
    'Начальный экран',
    'screens/1.jpg'
)

addWeightItemScreen = Screen(
    'Товар на вес',
    'screens/6.jpg'
)

addReadyMealItemScreen = Screen(
    'Выбор товара',
    'screens/8.jpg'
)

addBagScreen = Screen(
    'Добавление пакетов',
    'screens/11.jpg'
)

conclusionScreen = Screen(
    'Подытог',
    'screens/13.jpg'
)

loyaltyScreen = Screen(
    'Выбор скидки',
    'screens/14.jpg'
)

paymentScreen = Screen(
    'Итого к оплате',
    'screens/2.jpg'
)

paymentBankScreen = Screen(
    'Итого к оплате',
    'screens/15.jpg'
)

paymentСanselScreen = Screen(
    'Итого к оплате',
    'screens/26.jpg'
)

cancelScreen.add_commands([
    (commands.cancel, addItemScreen),
    (commands.changeTopper, approveScreen),
    (commands.cancel.expand(['да']), approveScreen),
    (commands.cancel.expand(['нет']), addItemScreen),
    (commands.returnAddItem, addItemScreen)
])

addItemScreen.add_commands([
    (commands.addItem, None),
    (commands.deletePosition, None),
    (commands.deleteAll, None),
    (commands.payment, addBagScreen),
    (commands.subTotal, addBagScreen),
    (commands.cancel, cancelScreen)
])

startScreen.add_commands([
    (commands.start, addItemScreen)
])

addWeightItemScreen.add_commands([
    (commands.addItem, None),
    (commands.cancel, addItemScreen)
])

addReadyMealItemScreen.add_commands([
    (commands.addItem, None),
    (commands.cancel, addItemScreen)
])

addBagScreen.add_commands([
    (commands.addItem, None),
    (commands.cancel, conclusionScreen),
    (commands.subTotal, conclusionScreen)
])

conclusionScreen.add_commands([
    (commands.addLoyalty, loyaltyScreen),
    (commands.payment, paymentScreen),
    (commands.returnAddItem, addItemScreen),
    (commands.sellingMode, addItemScreen),
    (commands.cancel, cancelScreen)
])

loyaltyScreen.add_commands([
    (commands.cancel, conclusionScreen)
])

paymentScreen.add_commands([
    (commands.deleteTransaction, conclusionScreen),
    (commands.payment, paymentBankScreen),
    (commands.cancel, cancelScreen),
    (commands.changeTopper, approveScreen)
])

paymentСanselScreen.add_commands([
    (commands.deleteTransaction, conclusionScreen),
    (commands.payment, paymentBankScreen),
    (commands.cancel, cancelScreen),
    (commands.changeTopper, approveScreen)
])


class View:
    def __init__(self):
        self.screen = startScreen
        self.im = cv2.imread(self.screen.image)
        self._loop = True
        self._changed = True
        Thread(target=self._show_image).start()

    def _show_image(self):
        while self._loop:
            if self._changed:
                self.im = cv2.imread(self.screen.image)
                self._changed = False
            cv2.imshow('view', self.im)
            cv2.waitKey(1000)

    def set_screen(self, screen):
        if screen is not None:
            self.screen = screen
            self._changed = True
            print('Screen changed to "{}"'.format(screen.name))

    def destroy(self):
        self._loop = False