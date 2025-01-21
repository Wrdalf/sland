import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import pandas as pd
from app.profile_manager import ProfileManager
from app.api_client import APIClient
from app.yml_generator import YMLGenerator

class App:
    def __init__(self):
        # Инициализация приложения
        self.profile_manager = ProfileManager()  # Управление профилями
        self.root = tk.Tk()  # Создание основного окна
        self.root.title("Sima-Land Профили")  # Установка заголовка окна
        self.yml_generator = YMLGenerator()  # Генератор YML-файлов
        self.setup_ui()  # Настройка пользовательского интерфейса

    def setup_ui(self):
        # Основной фрейм интерфейса
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)

        # Список профилей
        self.profiles_listbox = tk.Listbox(frame, height=10, width=50)
        self.profiles_listbox.pack(side=tk.LEFT, padx=(0, 10))

        # Прокрутка для списка профилей
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.profiles_listbox.yview)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.profiles_listbox.config(yscrollcommand=scrollbar.set)

        # Кнопки управления профилями
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        tk.Button(buttons_frame, text="Добавить профиль", command=self.add_profile).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Удалить профиль", command=self.delete_profile).pack(side=tk.LEFT, padx=5)
        tk.Button(buttons_frame, text="Загрузить Excel", command=self.load_excel_file).pack(side=tk.LEFT, padx=5)

        # Поле ввода номера заказа
        order_frame = tk.Frame(self.root)
        order_frame.pack(pady=10)

        tk.Label(order_frame, text="Введите номер заказа:").pack(side=tk.LEFT, padx=5)
        self.order_id_entry = tk.Entry(order_frame)
        self.order_id_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка выполнения заказа
        tk.Button(order_frame, text="Выполнить", command=self.execute_order).pack(side=tk.LEFT, padx=5)

        # Обработчик клавиши Enter
        self.root.bind("<Return>", lambda event: self.execute_order())

        # Обновление списка профилей при запуске
        self.update_profiles_list()

    def update_profiles_list(self):
        # Очистить текущий список профилей
        self.profiles_listbox.delete(0, tk.END)
        for profile in self.profile_manager.profiles:
            self.profiles_listbox.insert(tk.END, profile)

    def add_profile(self):
        # Инструкция для пользователя о добавлении профиля
        instruction = (
            "Для добавления профиля вам нужно получить x-api-token в личном кабинете Sima-Land.\n"
            "Перейдите по адресу: https://www.sima-land.ru/cabinet/token/ и скопируйте ваш токен."
        )
        messagebox.showinfo("Инструкция", instruction)

        # Ввод названия профиля
        name = simpledialog.askstring("Добавить профиль", "Введите название профиля:")
        if not name:
            return

        # Ввод API-ключа
        api_key = simpledialog.askstring("Добавить профиль", "Введите x-api-token:")
        if not api_key:
            return

        # Сохранение профиля
        self.profile_manager.add_profile(name, api_key)
        self.update_profiles_list()

    def delete_profile(self):
        # Удаление выбранного профиля
        selected = self.profiles_listbox.curselection()
        if not selected:
            messagebox.showwarning("Удаление профиля", "Выберите профиль для удаления.")
            return

        profile_name = self.profiles_listbox.get(selected[0])
        if messagebox.askyesno("Удаление профиля", f"Вы уверены, что хотите удалить профиль '{profile_name}'?"):
            self.profile_manager.delete_profile(profile_name)
            self.update_profiles_list()

    def execute_order(self):
        # Выполнение заказа
        selected = self.profiles_listbox.curselection()
        if not selected:
            messagebox.showwarning("Выполнение заказа", "Выберите профиль перед выполнением.")
            return

        profile_name = self.profiles_listbox.get(selected[0])
        api_key = self.profile_manager.profiles[profile_name]["api_key"]
        api_client = APIClient(api_key)

        try:
            # Проверка корректности номера заказа
            order_id = int(self.order_id_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Номер заказа должен быть числом.")
            return

        try:
            # Получение товаров из заказа
            items = api_client.get_order_items(order_id)
            if not items:
                messagebox.showinfo("Результат", "Товары не найдены в заказе.")
                return

            # Создание YML-файла
            self.yml_generator.create_yml_file(order_id, items, api_client)
            messagebox.showinfo("Результат", f"YML-файл для заказа {order_id} создан.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def load_excel_file(self):
        # Загрузка Excel-файла
        file_path = filedialog.askopenfilename(title="Выберите Excel файл", filetypes=[("Excel Files", "*.xlsx *.xls")])
        if not file_path:
            return

        try:
            # Чтение данных из Excel
            data = pd.read_excel(file_path)
            self.map_excel_columns(data)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {e}")

    def map_excel_columns(self, data):
        # Окно сопоставления столбцов
        column_window = tk.Toplevel(self.root)
        column_window.title("Сопоставление столбцов")

        # Инструкция для пользователя
        instruction = (
            "Инструкция: Загрузите файл с не более чем тремя столбцами: 'Артикул', 'Название', 'Штрихкод'.\n"
            "Если столбец не нужен, выберите 'Не добавлять'."
        )
        tk.Label(column_window, text=instruction, wraplength=400, justify="left").pack(pady=10)

        # Показать первые 10 строк данных
        frame = tk.Frame(column_window)
        frame.pack()

        tree = ttk.Treeview(frame, columns=list(data.columns), show="headings")
        for col in data.columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for _, row in data.head(10).iterrows():
            tree.insert("", tk.END, values=list(row))

        tree.pack()

        # Настройка выбора категорий столбцов
        column_labels = ["Не добавлять", "Артикул", "Название", "Штрихкод"]
        column_mapping = {}

        selection_frame = tk.Frame(column_window)
        selection_frame.pack(pady=10)

        for idx, col in enumerate(data.columns):
            tk.Label(selection_frame, text=f"Столбец {idx + 1}").pack(side=tk.LEFT, padx=5)

            combobox = ttk.Combobox(selection_frame, values=column_labels, state="readonly")
            combobox.current(0)  # Установить "Не добавлять" по умолчанию
            combobox.pack(side=tk.LEFT, padx=5)

            column_mapping[col] = combobox

        def submit_mapping():
            # Сопоставленные данные
            mapped_data = {
                "Артикул": None,
                "Название": None,
                "Штрихкод": None
            }

            for col, combobox in column_mapping.items():
                selected = combobox.get()
                if selected != "Не добавлять":
                    mapped_data[selected] = data[col]

            # Проверка обязательных данных
            if mapped_data["Артикул"] is None or mapped_data["Штрихкод"] is None:
                messagebox.showwarning("Ошибка", "Необходимо выбрать хотя бы 'Артикул' и 'Штрихкод'.")
                return

            if mapped_data["Артикул"].empty or mapped_data["Штрихкод"].empty:
                messagebox.showwarning("Ошибка", "Столбцы 'Артикул' и 'Штрихкод' не должны быть пустыми.")
                return

            # Создание YML-файла
            self.yml_generator.create_yml_file_from_excel(mapped_data)
            messagebox.showinfo("Успех", "YML-файл успешно создан.")
            column_window.destroy()

        tk.Button(column_window, text="Создать YML", command=submit_mapping).pack(pady=10)

    def run(self):
        # Запуск основного цикла приложения
        self.root.mainloop()
