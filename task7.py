import sys
import shlex
import argparse
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

UI_PATH = Path(__file__).parent / "task7.ui"

def parse_args_from_string(arg_string: str) -> str:
    """
    Эмулирует работу argparse с командной строкой, 
    но берет аргументы из переданной строки.
    """
    # Создаем парсер 
    parser = argparse.ArgumentParser()
    parser.add_argument("items", nargs="*")
    
    try:
        # shlex.split разбивает строку по пробелам, игнорируя лишние
        args_list = shlex.split(arg_string)
    except ValueError:
        args_list = arg_string.split()
        
    # Парсим аргументы (передаем список, а не sys.argv)
    args = parser.parse_args(args_list)
    
    # Формируем результат
    if not args.items:
        return "no args"
    else:
        # Каждый аргумент с новой строки
        return "\n".join(args.items)


class Task7Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        
        # Подключаем кнопку
        self.btn_run.clicked.connect(self.on_run_clicked)

    def on_run_clicked(self):
        # Берем текст из поля ввода
        arg_str = self.line_args.text()
        
        # Получаем результат
        result = parse_args_from_string(arg_str)
        
        # Выводим
        self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task7Window()
    window.show()
    sys.exit(app.exec())