import sys
import shlex
import argparse
from pathlib import Path
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

UI_PATH = Path(__file__).parent / "task8.ui"

def calculate_sum(text_from_input: str) -> str:
    # Создаем парсер. Отключаем авто-выход при ошибках, чтобы поймать их самим
    parser = argparse.ArgumentParser(exit_on_error=False)
    
    # Добавляем позиционные аргументы типа int (целые числа)
    parser.add_argument("nums", nargs="*", type=int)
    
    # Разбиваем строку на список слов
    words = shlex.split(text_from_input)
    
    try:
        # Парсим аргументы
        args = parser.parse_args(words)
        
        # Проверки по условию
        if len(args.nums) == 0:
            return "NO PARAMS"
        elif len(args.nums) == 1:
            return "TOO FEW PARAMS"
        elif len(args.nums) > 2:
            return "TOO MANY PARAMS"
        else:
            # Если ровно два числа — считаем сумму
            return str(args.nums[0] + args.nums[1])
            
    except Exception as e:
        # Если ввели буквы вместо чисел, выводим имя класса исключения
        return type(e).__name__


class Task8Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        self.btn_run.clicked.connect(self.on_run_clicked)

    def on_run_clicked(self):
        text = self.line_args.text()
        result = calculate_sum(text)
        self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task8Window()
    window.show()
    sys.exit(app.exec())