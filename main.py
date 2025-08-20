import random
import tkinter as tk
from tkinter import ttk, messagebox

#Генератор рецептов

recipes = {
    "завтрак": {
        "Овсяноблин с сыром и ветчиной":
            ["Овсяные хлопья", "Яйцо", "Сыр", "Ветчина"],
        "Смузи зеленый":
            ["Шпинат", "Банан", "Йогурт", "Мед"],
        "Тост с авокадо и яйцом-пашот":
            ["Хлеб", "Авокадо", "Яйцо", "Специи"],
        "Гранола с йогуртом":
            ["Гранола", "Йогурт", "Ягоды", "Мед"],
        "Яичница в авокадо":
            ["Авокадо", "Яйцо", "Специи", "Зелень"]
    },
    "обед": {
        "Куриный суп с лапшой":
            ["Курица", "Лапша", "Морковь", "Лук"],
        "Салат Цезарь":
            ["Курина", "Салат", "Сухарики", "Соус Цезарь"],
        "Гречневая лапша с овощами":
            ["Гречневая лапша", "Перец", "Морковь", "Соус соевый"],
        "Куриные котлеты с пюре":
            ["Фарш куриный", "Картофель", "Лук", "Яйцо"],
        "Овощной рататуй":
            ["Кабачок", "Баклажан", "Помидор", "Перец"]
    },
    "ужин": {
        "Лосось с овощами на пару":
            ["Лосось", "Брокколи", "Морковь", "Лимон"],
        "Тыквенный крем-суп":
            ["Тыква", "Сливки", "Имбирь", "Гренки"],
        "Творожная запеканка":
            ["Творог", "Яйцо", "Манка", "Изюм"],
        "Омлет с грибами":
            ["Яйца", "Шампиньоны", "Сыр", "Зелень"],
        "Салат с тунцом":
            ["Тунец консервированный", "Яйцо", "Огурец", "Кукуруза"]
    }
}

"""Кастомный класс для создания кнопок с закругленными углами"""
class RoundedButton(tk.Canvas):
    def __init__(self, master=None, text="", radius=25, bg="#2E86AB", fg="white",
                 font=("Arial", 12, "bold"), command=None, width=120, height=40, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.font = font
        self.text = text
        self.width = width
        self.height = height
        # Привязка обработчиков событий
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

        self.draw_button()

    def draw_button(self):
        self.delete("all")
        # Рисуем закругленный прямоугольник
        self.create_rectangle(
            (self.radius, 0, self.width - self.radius, self.height),
            fill=self.bg, outline=self.bg
        )
        self.create_rectangle(
            (0, self.radius, self.width, self.height - self.radius),
            fill=self.bg, outline=self.bg
        )
        # Рисуем закругленные углы
        self.create_oval(
            (0, 0, self.radius * 2, self.radius * 2),
            fill=self.bg, outline=self.bg
        )
        self.create_oval(
            (self.width - self.radius * 2, 0, self.width, self.radius * 2),
            fill=self.bg, outline=self.bg
        )
        self.create_oval(
            (0, self.height - self.radius * 2, self.radius * 2, self.height),
            fill=self.bg, outline=self.bg
        )
        self.create_oval(
            (self.width - self.radius * 2, self.height - self.radius * 2, self.width, self.height),
            fill=self.bg, outline=self.bg
        )
        # Добавляем текст на кнопку
        self.create_text(
            self.width // 2,
            self.height // 2,
            text=self.text,
            fill=self.fg,
            font=self.font
        )

    def _on_click(self, event):
        """Обработчик клика по кнопке"""
        if self.command:
            self.command()

    def _on_enter(self, event):
        """Обработчик наведения курсора на кнопку (эффект hover)"""
        self.config(cursor="hand2")
        lighter_bg = self.lighten_color(self.bg)
        self.bg = lighter_bg
        self.draw_button()

    def _on_leave(self, event):
        """Обработчик отведения курсора с кнопки"""
        self.config(cursor="")
        darker_bg = self.darken_color(self.bg)
        self.bg = darker_bg
        self.draw_button()

    def lighten_color(self, color):
        """Осветление цвета для эффекта hover"""
        if color == "#2E86AB": return "#3FA0C9"
        if color == "#A23B72": return "#C44D8A"
        return color

    def darken_color(self, color):
        """Затемнение цвета для эффекта hover"""
        if color == "#3FA0C9": return "#2E86AB"
        if color == "#C44D8A": return "#A23B72"
        return color


def generate_recipe():
    """Основная функция генерации случайного рецепта"""
    selected_meal = meal_var.get()
    # Проверка выбора приема пищи
    if not selected_meal:
        messagebox.showwarning("Внимание", "Выберите прием пищи!")
        return

    if selected_meal not in recipes:
        messagebox.showerror("Ошибка", "Неверный прием пищи!")
        return
    # Выбор случайного блюда и его ингредиентов
    dish, ingredients = random.choice(list(recipes[selected_meal].items()))

    # Очищаем предыдущие результаты
    for widget in result_frame.winfo_children():
        widget.destroy()

    # Создаем контейнер для отображения рецепта
    result_container = tk.Frame(result_frame, bg="#FFFFFF", bd=2, relief=tk.GROOVE)
    result_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    # Заголовок рецепта
    tk.Label(result_container, text="🍽️ ВАШ РЕЦЕПТ",
             font=("Arial", 14, "bold"), fg="#2E86AB", bg="#FFFFFF").pack(pady=(15, 5))

    # Прием пищи
    tk.Label(result_container, text=f"Прием пищи: {selected_meal.upper()}",
             font=("Arial", 11, "bold"), fg="#A23B72", bg="#FFFFFF").pack(pady=2)

    # Разделитель
    ttk.Separator(result_container, orient='horizontal').pack(fill='x', padx=20, pady=8)

    # Название блюда
    tk.Label(result_container, text=dish,
             font=("Arial", 14, "bold"), fg="#F18F01", bg="#FFFFFF",
             wraplength=400, justify="center").pack(pady=5)

    # Ингредиенты
    ingredients_frame = tk.Frame(result_container, bg="#FFFFFF")
    ingredients_frame.pack(pady=8)

    tk.Label(ingredients_frame, text="🔎 Главные ингредиенты:",
             font=("Arial", 11, "bold"), fg="#2E86AB", bg="#FFFFFF").pack(pady=(0, 5))

    for ingredient in ingredients[:3]:
        tk.Label(ingredients_frame, text=f"• {ingredient}",
                 font=("Arial", 10), fg="#333333", bg="#FFFFFF").pack(pady=1)

    # Кнопка для генерации нового рецепта
    RoundedButton(result_container, text="🎲 Новый рецепт", command=generate_recipe,
                  bg="#2E86AB", fg="white", font=("Arial", 10, "bold"),
                  width=140, height=35).pack(pady=15)


def random_meal():
    """Функция для случайного выбора приема пищи и генерации рецепта"""
    meal_var.set(random.choice(list(recipes.keys())))
    generate_recipe()


# Создаем главное окно
root = tk.Tk()
root.title("🍳 Генератор рецептов")
root.geometry("500x700")
root.configure(bg="#F8F9FA")
root.resizable(False, False)

# Главный фрейм
main_frame = tk.Frame(root, bg="#F8F9FA", padx=20, pady=15)
main_frame.pack(fill=tk.BOTH, expand=True)

# Заголовок
header_frame = tk.Frame(main_frame, bg="#F8F9FA")
header_frame.pack(pady=(0, 15))

tk.Label(header_frame, text="🍳 ЧТО ПРИГОТОВИТЬ?",
         font=("Arial", 18, "bold"), fg="#2E86AB", bg="#F8F9FA").pack()

# Выбор приема пищи
selection_frame = tk.Frame(main_frame, bg="#F8F9FA")
selection_frame.pack(pady=15)

tk.Label(selection_frame, text="Выберите прием пищи:",
         font=("Arial", 11, "bold"), fg="#333333", bg="#F8F9FA").pack(pady=(0, 8))

meal_var = tk.StringVar()
meal_combobox = ttk.Combobox(selection_frame, textvariable=meal_var,
                             values=list(recipes.keys()),
                             font=("Arial", 10), state="readonly",
                             width=18, height=8)
meal_combobox.pack(pady=5)
meal_combobox.set("завтрак")

# Кнопки
button_frame = tk.Frame(main_frame, bg="#F8F9FA")
button_frame.pack(pady=15)

# Кнопки одинаковой ширины (под самую длинную надпись)
RoundedButton(button_frame, text="🍽️ Сгенерировать", command=generate_recipe,
              bg="#2E86AB", fg="white", font=("Arial", 10, "bold"),
              width=160, height=38).pack(side=tk.LEFT, padx=8)

RoundedButton(button_frame, text="🎲 Случайно", command=random_meal,
              bg="#A23B72", fg="white", font=("Arial", 10, "bold"),
              width=160, height=38).pack(side=tk.LEFT, padx=8)

# Разделитель
ttk.Separator(main_frame, orient='horizontal').pack(fill='x', pady=15)

# Фрейм для результатов
result_frame = tk.Frame(main_frame, bg="#F8F9FA", height=280)  # Уменьшил высоту
result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
result_frame.pack_propagate(False)

# Запускаем приложение
root.mainloop()
