import tkinter as tk
from tkinter import simpledialog
from app.gui import App

class AppV2(App):
    def __init__(self):
        super().__init__()
        self.setup_custom_ui()

    def setup_custom_ui(self):
        """
        Добавляет кастомные кнопки для управления профилями.
        """
        add_profile_button = tk.Button(self.root, text="Добавить профиль", command=self.prompt_add_profile)
        add_profile_button.pack(pady=5)

    def prompt_add_profile(self):
        """
        Открывает диалоговые окна для ввода данных профиля и добавляет профиль.
        """
        profile_name = simpledialog.askstring("Добавить профиль", "Введите имя профиля:")
        if profile_name:
            token = simpledialog.askstring("Добавить профиль", "Введите токен профиля:")
            if token:
                self.add_profile(profile_name, token)

    def add_profile(self, profile_name, token):
        """
        Добавление профиля с проверкой токена.
        Если токен не начинается с "bearer", то добавляется префикс "bearer ".
        """
        if not token.lower().startswith("bearer"):
            token = f"bearer {token}"
        
        # Добавление профиля в менеджер профилей
        self.profile_manager.add_profile(profile_name, token)
        
        # Обновление интерфейса
        self.update_profiles_listbox()

    def update_profiles_listbox(self):
        """
        Обновляет список профилей в интерфейсе.
        """
        self.profiles_listbox.delete(0, tk.END)
        for profile in self.profile_manager.get_all_profiles():
            self.profiles_listbox.insert(tk.END, profile)

if __name__ == "__main__":
    app = AppV2()
    app.run()
