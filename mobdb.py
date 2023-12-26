import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

class DatabaseForm:
    def __init__(self, root):
        self.root = root
        self.root.title("kursovaya")

        # Подключение к PostgreSQL
        self.connection = psycopg2.connect(
            database="kursach",
            user="postgres",
            password="20133102es",
            host="localhost",
            port="5432"
        )
        self.cursor = self.connection.cursor()

        # Создание и заполнение выпадающего списка таблиц
        self.tables_label = tk.Label(root, text="Выберите таблицу:")
        self.tables_combobox = ttk.Combobox(root, values=self.get_table_names())
        self.tables_combobox.bind("<<ComboboxSelected>>", self.load_table_data)

        # Создание Treeview для отображения данных таблицы
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ()
        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Кнопки для управления данными
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        self.button_view = tk.Button(self.button_frame, text="Просмотр", command=self.view_data)
        self.button_add = tk.Button(self.button_frame, text="Добавить", command=self.add_data)
        self.button_delete = tk.Button(self.button_frame, text="Удалить", command=self.delete_data)

        # Расположение элементов на форме
        self.tables_label.grid(row=0, column=0, padx=10, pady=10)
        self.tables_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.button_view.grid(row=0, column=2, padx=5)
        self.button_add.grid(row=0, column=3, padx=5)
        self.button_delete.grid(row=0, column=4, padx=5)

    def get_table_names(self):
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name")
        return [table[0] for table in self.cursor.fetchall()]

    def load_table_data(self, event=None):
        table_name = self.tables_combobox.get()
        if table_name:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            data = self.cursor.fetchall()

            # Очистка предыдущих записей в Treeview
            self.tree.delete(*self.tree.get_children())

            # Загрузка данных в Treeview
            columns = [column[0] for column in self.cursor.description]
            self.tree["columns"] = columns
            self.tree.heading("#0", text="ID")
            for col in columns:
                self.tree.heading(col, text=col.capitalize())
                self.tree.column(col, anchor=tk.CENTER, width=100)

            for row in data:
                self.tree.insert("", tk.END, values=row)

    def get_data_from_tree(self):
        # Получение выделенной строки из Treeview
        selected_item = self.tree.selection()
        if selected_item:
            return self.tree.item(selected_item, "values")
        return None

    def view_data(self):
        self.load_table_data()

    def add_data(self):
        table_name = self.tables_combobox.get()
        if table_name:
            data = self.get_data_from_tree()
            if data:
                messagebox.showinfo("Добавление данных", "Для добавления новой записи, нажмите 'Обновить'")
            else:
                messagebox.showinfo("Добавление данных", "Для добавления новой записи, воспользуйтесь 'Обновить'")

    def delete_data(self):
        table_name = self.tables_combobox.get()
        if table_name:
            data = self.get_data_from_tree()
            if data:
                try:
                    self.cursor.execute(f"DELETE FROM {table_name} WHERE {"columns"[0]}=%s", (data[0],))
                    self.connection.commit()
                    self.load_table_data()  # Обновляем данные после удаления
                    messagebox.showinfo("Успех", "Запись успешно удалена")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            else:
                messagebox.showinfo("Удаление данных", "Выберите запись для удаления")

if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseForm(root)
    root.mainloop()


