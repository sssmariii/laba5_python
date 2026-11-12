import os
import sys
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

UI_PATH = Path(__file__).parent / "task3.ui"

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

def human_size(size: int) -> str:
    """Перевод байт в человекочитаемый формат."""
    value = float(size)
    unit_index = 0
    while value >= 1024 and unit_index < len(UNITS) - 1:
        value /= 1024
        unit_index += 1
    return f"{round(value)}{UNITS[unit_index]}"

def get_top_10_items(root_path: str) -> str:
    """
    Считает размеры папок и файлов, возвращает общий ТОП-10.
    """
    if not os.path.exists(root_path) or not os.path.isdir(root_path):
        return "Указанный путь не является папкой."

    # Словарь: {полный_путь: (имя, размер)}
    items_sizes = {}

    for dirpath, dirnames, filenames in os.walk(root_path):
        # 1. Добавляем в словарь папки 
        if dirpath != root_path:
            items_sizes[dirpath] = [os.path.basename(dirpath), 0]
        
        # 2. Добавляем файлы и считаем их размер
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.isfile(fp):
                try:
                    size = os.path.getsize(fp)
                except OSError:
                    size = 0
                items_sizes[fp] = [f, size]

    # 3. Сортируем пути по длине (снизу вверх), чтобы правильно просуммировать размеры папок
    sorted_paths = sorted(items_sizes.keys(), key=lambda x: len(x), reverse=True)
    
    for path in sorted_paths:
        if path == root_path:
            continue
        
        parent = os.path.dirname(path)
        # Если у нас есть родительская папка в словаре, прибавляем к ее размеру текущий
        if parent in items_sizes:
            items_sizes[parent][1] += items_sizes[path][1]

    # 4. Сортировка по размеру (по убыванию) и берем первые 10
    top_10 = sorted(items_sizes.values(), key=lambda x: x[1], reverse=True)[:10]

    # 5. строка вывода 
    result_lines = []
    for name, size in top_10:
        result_lines.append(f"{name} - {human_size(size)}")

    return "\n".join(result_lines)


class Task3Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.btn_select.clicked.connect(self.on_select_clicked)

    def on_select_clicked(self):
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "Выберите папку для анализа",
            ""
        )
        
        if folder_path:
            self.text_output.setPlainText("Идет подсчет размеров, подождите...")
            QApplication.processEvents() 
            
            result = get_top_10_items(folder_path)
            self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task3Window()
    window.show()
    sys.exit(app.exec())