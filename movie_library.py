import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Настройки ---
DATA_FILE = "movies.json"

# --- Класс приложения ---
class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []

        # Создание виджетов
        self.create_widgets()
        self.load_movies()
        self.update_table()

    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Название").grid(row=0, column=0, padx=5, pady=5)
        self.entry_title = tk.Entry(self.root)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Жанр").grid(row=1, column=0, padx=5, pady=5)
        self.entry_genre = tk.Entry(self.root)
        self.entry_genre.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Год выпуска").grid(row=2, column=0, padx=5, pady=5)
        self.entry_year = tk.Entry(self.root)
        self.entry_year.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Рейтинг (0-10)").grid(row=3, column=0, padx=5, pady=5)
        self.entry_rating = tk.Entry(self.root)
        self.entry_rating.grid(row=3, column=1, padx=5, pady=5)

        # Кнопка добавления
        self.btn_add = tk.Button(self.root, text="Добавить фильм", command=self.add_movie)
        self.btn_add.grid(row=4, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(self.root, columns=("title", "genre", "year", "rating"), show='headings')
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Фильтрация
        tk.Label(self.root, text="Фильтр по жанру").grid(row=6, column=0, padx=5)
        self.combo_genre = ttk.Combobox(self.root, values=["Все"] + sorted({m['genre'] for m in self.movies}))
        self.combo_genre.current(0)
        self.combo_genre.grid(row=6, column=1, padx=5)

        tk.Label(self.root, text="Фильтр по году").grid(row=7, column=0, padx=5)
        self.entry_filter_year = tk.Entry(self.root)
        self.entry_filter_year.grid(row=7, column=1, padx=5)

        self.btn_filter = tk.Button(self.root, text="Применить фильтр", command=self.apply_filter)
        self.btn_filter.grid(row=8, column=0, columnspan=2, pady=10)

    # --- Логика приложения ---
    def add_movie(self):
        title = self.entry_title.get().strip()
        genre = self.entry_genre.get().strip()
        year = self.entry_year.get().strip()
        rating = self.entry_rating.get().strip()

        # Валидация
        if not title or not genre or not year or not rating:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены.")
            return

        if not year.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return

        if not (rating.replace('.', '', 1).isdigit()):
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом.")
            return

        rating_num = float(rating)
        if not (0 <= rating_num <= 10):
            messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10.")
            return

        # Добавление фильма
        movie = {"title": title, "genre": genre.title(), "year": int(year), "rating": rating_num}
        
          
    def apply_filter(self):
        genre_filter = self.combo_genre.get()
        year_filter = self.entry_filter_year.get().strip()
        filtered_movies = self.movies.copy()

        if genre_filter != "Все":
            filtered_movies = [m for m in filtered_movies if m['genre'] == genre_filter]

        if year_filter.isdigit():
            filtered_movies = [m for m in filtered_movies if m['year'] == int(year_filter)]

            self.update_table(filtered_movies)

    def update_table(self, data=None):
        for i in self.tree.get_children():
            self.tree.delete(i)
        if data is None:
            data = self.movies
        for m in data:
            self.tree.insert("", "end", values=(m['title'], m['genre'], m['year'], m['rating']))

    def save_movies(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    def load_movies(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                try:
                    self.movies = json.load(f)
                except json.JSONDecodeError:
                    self.movies = []
        else:
            self.movies = []

    # --- Обработка закрытия окна ---
    def on_closing(self):
        self.save_movies()
        self.root.destroy()

# --- Запуск приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()