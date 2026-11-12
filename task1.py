import os
import sys
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

UI_PATH = Path(__file__).parent / "task1.ui"


UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

def human_size(size: int) -> str:
    """
    Перевод байт в человекочитаемый формат.
    Переход через 1024, округление через round.
    """
    value = float(size)
    unit_index = 0
    while value >= 1024 and unit_index < len(UNITS) - 1:
        value /= 1024
        unit_index += 1
    
    return f"{round(value)}{UNITS[unit_index]}"

def get_files_info() -> str:
    """
    Берет файлы из текущей папки.
    Возвращает строку с размерами только файлов.
    """
    # Получаем текущую рабочую директорию
    current_dir = os.getcwd()
    
    try:
        items = os.listdir(current_dir)
    except Exception as e:
        return f"Ошибка чтения папки: {e}"

    result_lines = []
    
    # Перебираем все элементы в папке
    for name in sorted(items):
        full_path = os.path.join(current_dir, name)
        
        # Нужны только файлы, каталоги пропускаем
        if os.path.isfile(full_path):
            size_bytes = os.path.getsize(full_path)
            h_size = human_size(size_bytes)
            result_lines.append(f"{name} {h_size}")
            
    return "\n".join(result_lines)


class Task1Window(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загружаем UI из Дизайнера
        uic.loadUi(UI_PATH, self)
        
        # Подключаем кнопку к функции
        self.btn_run.clicked.connect(self.on_run_clicked)

    def on_run_clicked(self):
        # Получаем текст и выводим в поле
        result = get_files_info()
        self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task1Window()
    window.show()
    sys.exit(app.exec())