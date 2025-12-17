from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty


class BottomPanel(BoxLayout):
    button_size = NumericProperty(50)  # Добавляем свойство

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(size=self.update_button_size)
        # Сразу вызываем обновление
        self.update_button_size()

    def update_button_size(self, *args):
        if self.width > 0:  # Проверяем, что размер установлен
            available_width = self.width - (self.spacing * 3) - (self.padding[0] + self.padding[2])
            self.button_size = max(available_width / 4, 40)


class MainLayout(BoxLayout):
    pass


class MyApp(App):
    def build(self):
        return MainLayout()


if __name__ == '__main__':
    MyApp().run()