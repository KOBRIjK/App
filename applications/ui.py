# applications/ui.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle


class TaskCard(BoxLayout):
    """Карточка задачи"""

    def __init__(self, task_data, show_accept=True, show_complete=False,
                 on_accept=None, on_view=None, on_complete=None, **kwargs):
        super().__init__(**kwargs)
        self.task_data = task_data
        self.on_accept = on_accept
        self.on_view = on_view
        self.on_complete = on_complete

        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(105)
        self.padding = dp(8)
        self.spacing = dp(4)

        # Фон карточки
        with self.canvas.before:
            status = task_data.get('status', 'new')
            if status == 'completed':
                Color(0.8, 0.9, 0.8, 1)
            elif status == 'assigned':
                Color(0.9, 0.9, 0.7, 1)
            else:
                Color(0.95, 0.95, 0.95, 1)

            self.bg_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8), ]
            )

        self.bind(pos=self._update_bg, size=self._update_bg)

        # Заголовок
        title_row = BoxLayout(size_hint_y=None, height=dp(25))
        title_label = Label(
            text=task_data['title'][:30] + ('...' if len(task_data['title']) > 30 else ''),
            color=(0.2, 0.2, 0.2, 1),
            font_size='15sp',
            bold=True,
            halign='left',
            size_hint_x=0.7
        )
        title_label.bind(size=title_label.setter('text_size'))

        dept_label = Label(
            text=task_data['department'][:15],
            color=(0.4, 0.4, 0.4, 1),
            font_size='13sp',
            size_hint_x=0.3,
            halign='right'
        )
        dept_label.bind(size=dept_label.setter('text_size'))

        title_row.add_widget(title_label)
        title_row.add_widget(dept_label)
        self.add_widget(title_row)

        # Описание
        desc_text = task_data['description']
        if len(desc_text) > 60:
            desc_text = desc_text[:57] + '...'

        desc_label = Label(
            text=desc_text,
            color=(0.4, 0.4, 0.4, 1),
            font_size='13sp',
            size_hint_y=None,
            height=dp(35),
            halign='left'
        )
        desc_label.bind(size=desc_label.setter('text_size'))
        self.add_widget(desc_label)

        # Информация и кнопки
        info_row = BoxLayout(size_hint_y=None, height=dp(30), spacing=dp(5))

        # Дни
        days_label = Label(
            text=f"📅 {task_data['days']} дн.",
            color=(0.3, 0.3, 0.3, 1),
            font_size='12sp',
            size_hint_x=0.4
        )
        info_row.add_widget(days_label)

        # Кнопки
        buttons_layout = BoxLayout(size_hint_x=0.6, spacing=dp(3))

        # Кнопка "Подробнее"
        view_btn = Button(
            text='👁',
            size_hint_x=0.3,
            background_color=(0.3, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='12sp'
        )
        view_btn.bind(on_press=lambda x: self._on_view())
        buttons_layout.add_widget(view_btn)

        # Кнопка "Принять" или "Завершить"
        if show_accept:
            accept_btn = Button(
                text='✅',
                size_hint_x=0.3,
                background_color=(0.4, 0.7, 0.4, 1),
                color=(1, 1, 1, 1),
                font_size='12sp'
            )
            accept_btn.bind(on_press=lambda x: self._on_accept())
            buttons_layout.add_widget(accept_btn)
        elif show_complete:
            complete_btn = Button(
                text='🏁',
                size_hint_x=0.3,
                background_color=(0.8, 0.4, 0.4, 1),
                color=(1, 1, 1, 1),
                font_size='12sp'
            )
            complete_btn.bind(on_press=lambda x: self._on_complete())
            buttons_layout.add_widget(complete_btn)

        # Заполнитель
        buttons_layout.add_widget(Label())

        info_row.add_widget(buttons_layout)
        self.add_widget(info_row)

    def _update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def _on_view(self):
        if self.on_view:
            self.on_view(self.task_data['id'])

    def _on_accept(self):
        if self.on_accept:
            self.on_accept(self.task_data['id'])

    def _on_complete(self):
        if self.on_complete:
            self.on_complete(self.task_data['id'])