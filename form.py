import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import psycopg2

class MainInterface:
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

        self.button_complex_query = tk.Button(root, text="Отчет", command=self.show_complex_query_window)
        # Создание и заполнение выпадающего списка таблиц
        self.tables_label = tk.Label(root, text="Выберите таблицу:")
        self.tables_combobox = ttk.Combobox(root, values=self.get_table_names())
        self.tables_combobox.bind("<<ComboboxSelected>>", self.load_table_data)

        # Создание Treeview для отображения данных таблицы
        self.tree = ttk.Treeview(root)
        self.tree.grid(row=1, column=0, columnspan=4, pady=10)

        # Кнопка для обновления данных
        self.button_refresh = tk.Button(root, text="Обновить", command=self.load_table_data)
        self.button_refresh.grid(row=2, column=0, padx=5)

        # Кнопки для управления данными
        self.button_frame = tk.Frame(root)
        self.button_frame.grid(row=2, column=1, columnspan=3, pady=10)

        self.button_view = tk.Button(self.button_frame, text="Просмотр", command=self.view_data)
        self.button_add = tk.Button(self.button_frame, text="Добавить", command=self.add_data)
        self.button_update = tk.Button(self.button_frame, text="Изменить", command=self.update_data)
        self.button_delete = tk.Button(self.button_frame, text="Удалить", command=self.delete_data)

        # Расположение элементов на форме
        self.tables_label.grid(row=0, column=0, padx=10, pady=10)
        self.tables_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.button_view.grid(row=0, column=2, padx=5)
        self.button_add.grid(row=0, column=3, padx=5)
        self.button_update.grid(row=0, column=4, padx=5)
        self.button_delete.grid(row=0, column=5, padx=5)
        self.button_complex_query.grid(row=2, column=7, padx=5)

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

            if data:
                # Загрузка данных в Treeview только если есть данные
                columns = [column[0] for column in self.cursor.description]
                self.tree["columns"] = columns
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
            columns = [column[0] for column in self.cursor.description]
            new_data = simpledialog.askstring("Добавление данных", f"Введите данные через запятую ({', '.join(columns)}):")
            if new_data:
                try:
                    self.cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join(['%s']*len(new_data.split(',')))})", tuple(new_data.split(',')))
                    self.connection.commit()
                    self.load_table_data()  # Обновляем данные после добавления
                    messagebox.showinfo("Успех", "Новая запись успешно добавлена")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

    def update_data(self):
        table_name = self.tables_combobox.get()
        if table_name:
            data = self.get_data_from_tree()
            if data:
                # Получаем список столбцов
                columns = [column[0] for column in self.cursor.description]

                # Здесь должен быть ваш код для открытия диалогового окна с формой для ввода новых данных
                # Вам нужно получить новые значения для каждого столбца

                # Пример использования simpledialog для получения новых значений
                new_values = []
                for column in columns:
                    new_value = simpledialog.askstring("Изменение данных", f"Введите новое значение для {column}:")
                    if new_value is not None:
                        new_values.append(new_value)

                # Ваш код для обновления данных в базе данных
                if new_values:
                    update_query = f"UPDATE {table_name} SET {', '.join([f'{column}=%s' for column in columns])} WHERE {columns[0]}=%s"
                    self.cursor.execute(update_query, tuple(new_values + [data[0]]))
                    self.connection.commit()
                    self.load_table_data()  # Обновляем данные после изменения
                    messagebox.showinfo("Успех", "Запись успешно изменена")
            else:
                messagebox.showinfo("Изменение данных", "Выберите запись для изменения")

    def delete_data(self):
        table_name = self.tables_combobox.get()
        if table_name:
            data = self.get_data_from_tree()
            if data:
                column_name = simpledialog.askstring("Удаление данных",
                                                     "Введите название столбца, по которому удалять:")
                if column_name:
                    try:
                        self.cursor.execute(f"DELETE FROM {table_name} WHERE {column_name}=%s", (data[0],))
                        self.connection.commit()
                        self.load_table_data()  # Обновляем данные после удаления
                        messagebox.showinfo("Успех", "Запись успешно удалена")
                    except Exception as e:
                        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            else:
                messagebox.showinfo("Удаление данных", "Выберите запись для удаления")

    def show_complex_query_window(self):
        # Создание нового окна для ввода сложного запроса
        complex_query_window = tk.Toplevel(self.root)
        complex_query_window.title("Отчет")

        # Многострочное текстовое поле для ввода SQL-запроса
        query_text = scrolledtext.ScrolledText(complex_query_window, wrap=tk.WORD, width=40, height=10)
        query_text.grid(row=0, column=0, padx=10, pady=10)

        # Выпадающий список с выбором запроса
        query_options = [
            "Запрос 1",
            "Запрос 2",
            "Запрос 3",
            "Запрос 4",
            "Запрос 5",
            "Запрос 6"
        ]
        query_combobox = ttk.Combobox(complex_query_window, values=query_options)
        query_combobox.set("Выберите запрос")
        query_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Кнопка для выполнения сложного запроса
        execute_button = tk.Button(complex_query_window, text="Выполнить отчет",
                                   command=lambda: self.execute_complex_query(query_combobox.get(), query_text.get("1.0", tk.END)))
        execute_button.grid(row=1, column=0, columnspan=2, pady=10)

    def execute_complex_query(self, selected_query, query):
        try:
            # Выполнение выбранного запроса
            if selected_query == "Запрос 1":
                result = self.query1()
            elif selected_query == "Запрос 2":
                result = self.query2()
            elif selected_query == "Запрос 3":
                result = self.query3()
            elif selected_query == "Запрос 4":
                result = self.query4()
            elif selected_query == "Запрос 5":
                result = self.query5()
            elif selected_query == "Запрос 6":
                result = self.query6()
            else:
                result = None

            # Отображение результата запроса (пример)
            messagebox.showinfo("Результат запроса", f"Результат: {result}")
        except Exception as e:
            messagebox.showerror("Ошибка выполнения запроса", f"Произошла ошибка: {e}")

    # Примеры методов для выполнения конкретных запросов
    def query1(self):
        self.cursor.execute('''
        SELECT r.title, pl.price, pl.expenses, (pl.price + pl.expenses) AS total_cost
        FROM price_list pl
        JOIN rate r ON pl.id_rate = r.id_rate
        ''')
        return self.cursor.fetchall()

    def query2(self):
        self.cursor.execute('''
        SELECT c.full_name, s.*
        FROM subscribe s
        JOIN client c ON s.id_client = c.id_client
        JOIN rate r ON s.id_rate = r.id_rate
        WHERE c.status = 'Active';
        ''')
        return self.cursor.fetchone()

    def query3(self):
        self.cursor.execute('''
        SELECT r.title, pl.price
        FROM price_list pl
        JOIN rate r ON pl.id_rate = r.id_rate
        WHERE pl.price = (SELECT MAX(price) FROM price_list);
        ''')
        return self.cursor.fetchall()

    def query4(self):
        self.cursor.execute('''
        SELECT c.*
        FROM client c
        JOIN subscribe s ON c.id_client = s.id_client
        JOIN rate r ON s.id_rate = r.id_rate
        JOIN price_list p ON r.id_rate = p.id_rate
        WHERE p.expenses > (SELECT AVG(expenses) FROM price_list);
        ''')
        return self.cursor.fetchall()

    def query5(self):
        self.cursor.execute('''
        SELECT e.type_equipment, COUNT(c.id_client) AS client_count
        FROM equipment e
        LEFT JOIN rate r ON e.id_equipment = r.id_equipment
        LEFT JOIN subscribe s ON r.id_rate = s.id_rate
        LEFT JOIN client c ON s.id_client = c.id_client
        GROUP BY e.type_equipment;
        ''')
        return self.cursor.fetchall()

    def query6(self):
        self.cursor.execute('''
        SELECT e.type_equipment, SUM(e.price) AS total_price
        FROM equipment e
        GROUP BY e.type_equipment;
        ''')
        return self.cursor.fetchall()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()
