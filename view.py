import commands


class Screen:
    def __init__(self, name, commands=None):
        if commands is None:
            commands = []
        self.name = name
        self.commands = commands


approveScreen = Screen('Подтверждение ассистентом')

cancelScreen = Screen('Отмена покупки', [
    (commands.cancel, approveScreen),
])

addItemScreen = Screen('Добавление товаров', [
    (commands.addItem, None),
    (commands.cancel, cancelScreen),
])

startScreen = Screen('Начальный экран', [
    (commands.start, addItemScreen)
])


class View:
    def __init__(self):
        self.screen = startScreen

    def set_screen(self, screen):
        if screen is not None:
            self.screen = screen
            print('Screen changed to "{}"'.format(screen.name))