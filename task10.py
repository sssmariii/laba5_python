import sys
import argparse
import textwrap
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

UI_PATH = Path(__file__).parent / "task10.ui"

def format_text_block(frame_height: int, frame_width: int, file_name: str) -> str:
    """
    Читает текстовый файл, переносит строки по ширине и оборачивает в рамку.
    """
    try:
        
        with open(file_name, 'r', encoding='utf-8-sig') as f:
            text = f.read()
    except Exception as e:
        # Если возникла ошибка, возвращаем её текст
        return str(e)

    # Ширина внутренней части (минус 2 символа для боковых границ "|")
    inner_width = frame_width - 2 
    
    wrapped_lines = []
    # Разбиваем текст на строки и обрабатываем каждую
    for line in text.split('\n'):
        # Если строка пустая, добавляем пустую строку
        if not line.strip():
            wrapped_lines.append("")
            continue
            
        # textwrap.wrap разбивает длинную строку на несколько коротких, не разрывая слова
        wrapped = textwrap.wrap(line, width=inner_width)
        if not wrapped:
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(wrapped)
            
    # Берем только те строки, которые влезают в высоту (минус 2 строки для верхней и нижней границы)
    max_content_lines = frame_height - 2
    content_lines = wrapped_lines[:max_content_lines]
    
    # Формируем рамку
    horizontal_line = "+" + "-" * inner_width + "+"
    
    result = [horizontal_line]
    for line in content_lines:
        # Дополняем строку пробелами справа до нужной ширины
        result.append("|" + line.ljust(inner_width) + "|")
    
    # Если текста меньше, чем высота рамки, добавляем пустые строки
    while len(result) < (frame_height - 1):
        result.append("|" + " " * inner_width + "|")
        
    result.append(horizontal_line)
    
    return "\n".join(result)


class Task10Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        
        self.file_path = ""
        
        self.btn_file.clicked.connect(self.select_file)
        self.btn_run.clicked.connect(self.run_format)

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Выберите текстовый файл", "", "Text files (*.txt)")
        if path:
            self.file_path = path
            self.text_output.setPlainText(f"Выбран файл: {path}")

    def run_format(self):
        if not self.file_path:
            self.text_output.setPlainText("ОШИБКА: Сначала выберите файл!")
            return
            
        width = self.spin_width.value()
        height = self.spin_height.value()
        
        result = format_text_block(height, width, self.file_path)
        self.text_output.setPlainText(result)


if __name__ == "__main__":
    # Проверка: если программа запущена из терминала с аргументами
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(exit_on_error=False)
        parser.add_argument("--frame-height", type=int, required=True)
        parser.add_argument("--frame-width", type=int, required=True)
        parser.add_argument("filename")
        
        try:
            args = parser.parse_args()
            print(format_text_block(args.frame_height, args.frame_width, args.filename))
        except Exception as e:
            print(f"Ошибка аргументов: {e}")
    else:
        # Иначе запускаем GUI
        app = QApplication(sys.argv)
        window = Task10Window()
        window.show()
        sys.exit(app.exec())