import sys
import time
import threading
from pathlib import Path
from datetime import datetime
import schedule
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import pyqtSignal

UI_PATH = Path(__file__).parent / "task5.ui"

class Task5Window(QMainWindow):
    # Для безопасного вывода текста из фонового потока в GUI
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        
        # Подключаем сигнал к текстовому полю
        self.log_signal.connect(self.append_text)
        
        # Подключаем кнопки
        self.btn_start.clicked.connect(self.start_timer)
        self.btn_test.clicked.connect(self.test_now)
        
        self.is_running = False

    def append_text(self, text):
        """Добавляет текст в конец поля вывода"""
        current = self.text_output.toPlainText()
        if current:
            self.text_output.setPlainText(current + "\n" + text)
        else:
            self.text_output.setPlainText(text)

    def print_ku(self):
        """Функция, которая печатает 'Ку' нужное количество раз"""
        now = datetime.now()
        hour = now.hour
        
        # Переводим 24-часовой формат в 12-часовой для определения количества
        # Например: 13:00 -> 1 раз, 14:00 -> 2 раза, 0:00 -> 12 раз
        count = hour % 12
        if count == 0:
            count = 12
            
        # Выводим в консоль 
        for _ in range(count):
            print("Ку")
            
        # Выводим в окно программы
        time_str = now.strftime("%H:%M:%S")
        self.log_signal.emit(f"[{time_str}] Сработал таймер! Напечатано 'Ку' {count} раз(а).")

    def test_now(self):
        """Кнопка для ручной проверки (имитация срабатывания таймера)"""
        self.print_ku()

    def start_timer(self):
        if self.is_running:
            return
            
        self.is_running = True
        self.btn_start.setEnabled(False)
        self.append_text("Таймер запущен! Ждем 00 минут каждого часа...")
        
        # Настройка schedule: каждый час в 00 минут
        schedule.every().hour.at(":00").do(self.print_ku)
        
        # Запускаю фоновый поток, чтобы не вешать интерфейс
        thread = threading.Thread(target=self.run_schedule, daemon=True)
        thread.start()

    def run_schedule(self):
        """Бесконечный цикл проверки расписания"""
        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task5Window()
    window.show()
    sys.exit(app.exec())