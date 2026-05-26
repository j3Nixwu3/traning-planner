import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=5, pady=5)
        self.type_entry = ttk.Combobox(self.root, values=["Кардио", "Силовая", "Йога", "Растяжка"])
        self.type_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("Дата", "Тип", "Длительность"), show="headings")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Тип", text="Тип")
        self.tree.heading("Длительность", text="Длительность (мин)")
        self.tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=5, column=0, padx=5, pady=5)
        self.filter_type = ttk.Combobox(self.root, values=["Все", "Кардио", "Силовая", "Йога", "Растяжка"])
        self.filter_type.set("Все")
        self.filter_type.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Фильтр по дате (ДД.ММ.ГГГГ):").grid(row=6, column=0, padx=5, pady=5)
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=0, pady=10)
        tk.Button(self.root, text="Сбросить фильтр", command=self.reset_filter).grid(row=7, column=1, pady=10)

    def add_training(self):
        date_str = self.date_entry.get()
        training_type = self.type_entry.get()
        duration_str = self.duration_entry.get()

        # Проверка даты
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ДД.ММ.ГГГГ")
            return

        # Проверка длительности
        try:
            duration = int(duration_str)
            if duration <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return

        if not training_type:
            messagebox.showerror("Ошибка", "Выберите тип тренировки")
            return

        # Добавление в таблицу
        self.trainings.append({
            "date": date_str,
            "type": training_type,
            "duration": duration
        })
        self.update_table()
        self.save_data()

        # Очистка полей
        self.date_entry.delete(0, tk.END)
        self.type_entry.set("")
        self.duration_entry.delete(0, tk.END)

    def apply_filter(self):
        filter_type = self.filter_type.get()
        filter_date = self.filter_date.get()

        filtered = self.trainings

        if filter_type != "Все":
            filtered = [t for t in filtered if t["type"] == filter_type]
        if filter_date:
            try:
                datetime.strptime(filter_date, "%d.%m.%Y")
                filtered = [t for t in filtered if t["date"] == filter_date]
            except ValueError:
                    messagebox.showerror("Ошибка", "Неверный формат даты фильтра")
                    return

        self.update_table(filtered)

    def reset_filter(self):
        self.filter_type.set("Все")
        self.filter_date.delete(0, tk.END)
        self.update_table()

    def save_data(self):
        with open("trainings.json", "w", encoding="utf-8") as f:
            json.dump(self.trainings, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("trainings.json", "r", encoding="utf-8") as f:
                self.trainings = json.load(f)
        except FileNotFoundError:
            self.trainings = []

    def update_table(self, data=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        target_data = data if data is not None else self.trainings
        for training in target_data:
            self.tree.insert("", "end", values=(training["date"], training["type"], training["duration"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
