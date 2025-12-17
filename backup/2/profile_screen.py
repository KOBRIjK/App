from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from datetime import datetime
import re

from screens.color_block import ColorBlock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../logining'))
from logining.logining_database import Database


class LoginPopup(Popup):
    def __init__(self, on_login_success, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Авторизация'
        self.size_hint = (0.8, 0.6)
        self.on_login_success = on_login_success

        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        # Email
        layout.add_widget(Label(text='Email:'))
        self.email_input = TextInput(
            multiline=False,
            hint_text='Введите email'
        )
        layout.add_widget(self.email_input)

        # Пароль
        layout.add_widget(Label(text='Пароль:'))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            hint_text='Введите пароль'
        )
        layout.add_widget(self.password_input)

        # Кнопки
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

        login_btn = Button(
            text='Войти',
            background_color=(0.2, 0.6, 1, 1)
        )
        login_btn.bind(on_press=self.login)

        register_btn = Button(
            text='Регистрация',
            background_color=(0.4, 0.8, 0.4, 1)
        )
        register_btn.bind(on_press=self.show_register)

        button_layout.add_widget(login_btn)
        button_layout.add_widget(register_btn)
        layout.add_widget(button_layout)

        self.content = layout
        self.db = Database()

    def login(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()

        if not email or not password:
            self.show_error('Заполните все поля')
            return

        user = self.db.authenticate_user(email, password)
        if user:
            self.dismiss()
            self.on_login_success(user)
        else:
            self.show_error('Неверный email или пароль')

    def show_register(self, instance):
        RegisterPopup(self.db, self.on_login_success).open()

    def show_error(self, message):
        error_popup = Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        error_popup.open()


class RegisterPopup(Popup):
    def __init__(self, db, on_login_success, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Регистрация'
        self.size_hint = (0.85, 0.8)
        self.db = db
        self.on_login_success = on_login_success

        scroll = ScrollView()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        # Email
        layout.add_widget(Label(text='Email*:'))
        self.email_input = TextInput(
            multiline=False,
            hint_text='example@mail.com',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.email_input)

        # Пароль
        layout.add_widget(Label(text='Пароль*:'))
        self.password_input = TextInput(
            multiline=False,
            password=True,
            hint_text='Не менее 6 символов',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.password_input)

        # Подтверждение пароля
        layout.add_widget(Label(text='Подтвердите пароль*:'))
        self.confirm_password_input = TextInput(
            multiline=False,
            password=True,
            hint_text='Повторите пароль',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.confirm_password_input)

        # Имя
        layout.add_widget(Label(text='Имя:'))
        self.first_name_input = TextInput(
            multiline=False,
            hint_text='Иван',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.first_name_input)

        # Фамилия
        layout.add_widget(Label(text='Фамилия:'))
        self.last_name_input = TextInput(
            multiline=False,
            hint_text='Иванов',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.last_name_input)

        # Отчество
        layout.add_widget(Label(text='Отчество:'))
        self.middle_name_input = TextInput(
            multiline=False,
            hint_text='Иванович',
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.middle_name_input)

        # Кнопка регистрации
        register_btn = Button(
            text='Зарегистрироваться',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        register_btn.bind(on_press=self.register)
        layout.add_widget(register_btn)

        scroll.add_widget(layout)
        self.content = scroll

    def register(self, instance):
        email = self.email_input.text.strip()
        password = self.password_input.text.strip()
        confirm_password = self.confirm_password_input.text.strip()
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        middle_name = self.middle_name_input.text.strip()

        # Валидация
        if not email or not password:
            self.show_error('Заполните обязательные поля')
            return

        if len(password) < 6:
            self.show_error('Пароль должен быть не менее 6 символов')
            return

        if password != confirm_password:
            self.show_error('Пароли не совпадают')
            return

        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            self.show_error('Неверный формат email')
            return

        # Проверка существования пользователя
        if self.db.get_user_by_email(email):
            self.show_error('Пользователь с таким email уже существует')
            return

        # Создание пользователя
        uid = self.db.create_user(email, password, first_name, last_name, middle_name)
        if uid:
            user = self.db.get_user_by_uid(uid)
            self.dismiss()
            self.on_login_success(user)
        else:
            self.show_error('Ошибка при регистрации')

    def show_error(self, message):
        error_popup = Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        error_popup.open()


class ProfileScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "profile"
        self.db = Database()
        self.current_user = None

        # ОСНОВНОЙ ЛЕЙАУТ - только ColorBlock
        self.color_block = ColorBlock(color=(0, 0, 0, 0.9))
        self.add_widget(self.color_block)

        # Контейнер для контента (будет поверх ColorBlock)
        self.content_container = BoxLayout(orientation='vertical')
        # Изначально скрываем контейнер
        self.content_container.opacity = 0
        self.add_widget(self.content_container)

    def on_enter(self, *args):
        """Вызывается при переходе на этот экран"""
        super().on_enter(*args)

        # Если пользователь не авторизован, показываем попап
        if not self.current_user:
            self.show_login_popup()
        else:
            # Если уже авторизован, загружаем профиль
            self.load_profile_form()

    def on_leave(self, *args):
        """Вызывается при уходе с экрана"""
        super().on_leave(*args)
        # Не закрываем базу данных здесь, чтобы сохранить сессию

    def show_login_popup(self):
        """Показать попап авторизации"""
        # Очищаем контейнер
        self.content_container.clear_widgets()

        # Показываем только черный фон и попап
        login_popup = LoginPopup(self.on_login_success)
        login_popup.open()

    def on_login_success(self, user):
        """Обработка успешной авторизации"""
        self.current_user = user
        self.load_profile_form()

    def load_profile_form(self):
        """Загрузка формы профиля"""
        # Очищаем контейнер
        self.content_container.clear_widgets()

        # Делаем контейнер видимым
        self.content_container.opacity = 1

        scroll = ScrollView()
        form_layout = BoxLayout(orientation='vertical', spacing=15, padding=20, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))

        # Заголовок
        title = Label(
            text=f'Профиль пользователя\nUID: {self.current_user["uid"]}',
            size_hint_y=None,
            height=60,
            halign='center',
            font_size='20sp',
            bold=True
        )
        title.bind(size=title.setter('text_size'))
        form_layout.add_widget(title)

        # Email (только для отображения)
        form_layout.add_widget(Label(text='Email:', size_hint_y=None, height=30))
        email_label = Label(
            text=self.current_user['email'],
            size_hint_y=None,
            height=40,
            color=(0.8, 0.8, 0.8, 1)
        )
        email_label.bind(size=email_label.setter('text_size'))
        form_layout.add_widget(email_label)

        # Имя
        form_layout.add_widget(Label(text='Имя:', size_hint_y=None, height=30))
        self.first_name_input = TextInput(
            text=self.current_user.get('first_name', '') or '',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.first_name_input)

        # Фамилия
        form_layout.add_widget(Label(text='Фамилия:', size_hint_y=None, height=30))
        self.last_name_input = TextInput(
            text=self.current_user.get('last_name', '') or '',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.last_name_input)

        # Отчество
        form_layout.add_widget(Label(text='Отчество:', size_hint_y=None, height=30))
        self.middle_name_input = TextInput(
            text=self.current_user.get('middle_name', '') or '',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.middle_name_input)

        # Дата рождения
        form_layout.add_widget(Label(text='Дата рождения (ДД.ММ.ГГГГ):', size_hint_y=None, height=30))
        birth_date = self.current_user.get('birth_date')
        display_birth_date = ''  # Значение по умолчанию пустая строка

        if birth_date:  # Проверяем, что birth_date не None
            try:
                # Конвертируем из формата SQLite в отображаемый формат
                dt = datetime.strptime(birth_date, '%Y-%m-%d')
                display_birth_date = dt.strftime('%d.%m.%Y')
            except (ValueError, TypeError):
                display_birth_date = ''  # Если ошибка - пустая строка

        self.birth_date_input = TextInput(
            text=display_birth_date,  # Используем переменную с обработанным значением
            multiline=False,
            hint_text='01.01.1990',
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.birth_date_input)

        # Отдел
        form_layout.add_widget(Label(text='Отдел:', size_hint_y=None, height=30))
        self.department_spinner = Spinner(
            text=self.current_user.get('department', 'Не выбран') or 'Не выбран',
            values=('Не выбран', 'IT-отдел', 'Юридический отдел', 'HR-отдел'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.department_spinner)

        # Кнопка сохранения
        save_btn = Button(
            text='Сохранить изменения',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 1, 1)
        )
        save_btn.bind(on_press=self.save_profile)
        form_layout.add_widget(save_btn)

        # Кнопка выхода
        logout_btn = Button(
            text='Выйти',
            size_hint_y=None,
            height=50,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        logout_btn.bind(on_press=self.logout)
        form_layout.add_widget(logout_btn)

        scroll.add_widget(form_layout)
        self.content_container.add_widget(scroll)

    def save_profile(self, instance):
        """Сохранение профиля"""
        first_name = self.first_name_input.text.strip()
        last_name = self.last_name_input.text.strip()
        middle_name = self.middle_name_input.text.strip()
        birth_date = self.birth_date_input.text.strip()
        department = self.department_spinner.text

        # Валидация даты рождения
        formatted_birth_date = ''
        if birth_date:
            try:
                # Парсим в формате ДД.ММ.ГГГГ
                dt = datetime.strptime(birth_date, '%d.%m.%Y')
                formatted_birth_date = dt.strftime('%Y-%m-%d')  # Формат для SQLite
            except ValueError:
                self.show_message('Ошибка', 'Неверный формат даты. Используйте ДД.ММ.ГГГГ')
                return

        # Сохранение в базу данных
        success = self.db.update_user_profile(
            self.current_user['uid'],
            first_name,
            last_name,
            middle_name,
            formatted_birth_date,
            department if department != 'Не выбран' else ''
        )

        if success:
            # Обновляем данные текущего пользователя
            self.current_user = self.db.get_user_by_uid(self.current_user['uid'])
            self.show_message('Успех', 'Данные успешно сохранены')
        else:
            self.show_message('Ошибка', 'Не удалось сохранить данные')

    def logout(self, instance):
        """Выход из профиля"""
        self.current_user = None
        self.content_container.clear_widgets()
        self.show_login_popup()

    def show_message(self, title, message):
        """Показать сообщение"""
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.6, 0.3)
        )
        popup.open()