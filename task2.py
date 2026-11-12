import os
import sys
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
import zipfile

UI_PATH = Path(__file__).parent / "task2.ui"

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

def human_size(size: int) -> str:
    """Перевод байт в человекочитаемый формат."""
    value = float(size)
    unit_index = 0
    while value >= 1024 and unit_index < len(UNITS) - 1:
        value /= 1024
        unit_index += 1
    return f"{round(value)}{UNITS[unit_index]}"


def get_zip_structure(zip_path: str) -> str:
    """
    Читает zip-архив и возвращает его файловую структуру 
    с отступами, папками и размерами файлов.
    """
    if not os.path.exists(zip_path):
        return "Файл не найден."

    result_lines = []
    seen_dirs = set()  # Множество, чтобы не выводить одну и ту же папку дважды
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            info_list = z.infolist()
            
            if not info_list:
                return ""  # Если архив пустой — ничего не выводим

            for item in info_list:
                filepath = item.filename
                

                # Разбиваем путь на части 
                parts = filepath.strip('/').split('/')
                
                # 1. Выводим все папки по пути (если еще не выводили)
                for i in range(len(parts) - 1):
                    dir_path = "/".join(parts[:i+1])
                    if dir_path not in seen_dirs:
                        seen_dirs.add(dir_path)
                        indent = "  " * i
                        result_lines.append(f"{indent}{parts[i]}")
                
                # 2. Если это файл (не заканчивается на /), выводим его с размером
                if not filepath.endswith('/'):
                    level = len(parts) - 1
                    indent = "  " * level
                    name_only = parts[-1]
                    size = item.file_size
                    result_lines.append(f"{indent}{name_only} {human_size(size)}")
                
    except zipfile.BadZipFile:
        return "Ошибка: Это не zip-архив или он поврежден."
    except Exception as e:
        return f"Произошла ошибка: {e}"
        
    return "\n".join(result_lines)


class Task2Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        
        # Подключаем кнопку к выбору файла
        self.btn_open.clicked.connect(self.on_open_clicked)

    def on_open_clicked(self):
        # Открываем окно выбора файла 
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите zip-архив", 
            "", 
            "Zip files (*.zip)"
        )
        
        # Если пользователь выбрал файл
        if file_path:
            result = get_zip_structure(file_path)
            self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task2Window()
    window.show()
    sys.exit(app.exec())