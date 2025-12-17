# send/ui_components.py
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

class BaseLabel(Label):
    """Базовый класс для всех меток"""
    def __init__(self, **kwargs):
        defaults = {
            'color': get_color_from_hex('#FFFFFF'),
            'size_hint': (1, None),
            'height': dp(30)
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class TitleLabel(BaseLabel):
    """Заголовок экрана"""
    def __init__(self, **kwargs):
        defaults = {
            'font_size': '24sp',
            'bold': True,
            'height': dp(40)
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class FieldLabel(BaseLabel):
    """Метка для полей ввода"""
    def __init__(self, **kwargs):
        defaults = {
            'font_size': '16sp',
            'height': dp(25)
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class BaseTextInput(TextInput):
    """Базовый класс для полей ввода"""
    def __init__(self, **kwargs):
        defaults = {
            'multiline': False,
            'size_hint': (1, None),
            'height': dp(45),
            'background_color': (1, 1, 1, 0.9),
            'foreground_color': (0, 0, 0, 1),
            'padding': dp(10),
            'background_normal': '',
            'background_active': '',
            'write_tab': False
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class MultilineTextInput(BaseTextInput):
    """Многострочное поле ввода"""
    def __init__(self, **kwargs):
        defaults = {
            'multiline': True,
            'height': dp(120)
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class DepartmentSpinner(Spinner):
    """Спиннер для выбора отдела"""
    def __init__(self, **kwargs):
        defaults = {
            'text': 'Выберите отдел',
            'values': ('IT-отдел', 'Юридический отдел', 'HR-отдел'),
            'size_hint': (1, None),
            'height': dp(45),
            'background_color': (1, 1, 1, 1),
            'color': (0, 0, 0, 1)
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class SubmitButton(Button):
    """Кнопка отправки"""
    def __init__(self, **kwargs):
        defaults = {
            'size_hint': (1, None),
            'height': dp(50),
            'background_color': (0.4, 0.6, 0.2, 1),
            'color': get_color_from_hex('#FFFFFF'),
            'font_size': '18sp',
            'bold': True
        }
        defaults.update(kwargs)
        super().__init__(**defaults)

class StatusLabel(BaseLabel):
    """Метка статуса"""
    def __init__(self, **kwargs):
        defaults = {
            'font_size': '14sp',
            'height': dp(0),
            'opacity': 0
        }
        defaults.update(kwargs)
        super().__init__(**defaults)