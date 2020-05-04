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


approveScreen = Screen(
    'Подтверждение ассистентом',
    'screens/12.jpg'
)

cancelScreen = Screen(
    'Отмена покупки',
    'screens/10.jpg',
    [
        (commands.cancel, approveScreen),
    ]
)

addItemScreen = Screen(
    'Добавление товаров',
    'screens/3.jpg',
    [
        (commands.addItem, None),
        (commands.cancel, cancelScreen)
    ]
)

startScreen = Screen(
    'Начальный экран',
    'screens/1.jpg',
    [
        (commands.start, addItemScreen)
    ]
)


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


if __name__ == '__main__':
    from time import sleep
    view = View()
    sleep(2)
    view.set_screen(addItemScreen)
    sleep(2)
    view.destroy()
