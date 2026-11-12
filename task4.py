import os
import sys
import shutil
from pathlib import Path
from datetime import datetime
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

UI_PATH = Path(__file__).parent / "task4.ui"

def make_reserve_arc(source, dest):
    """Архивирует папку source в папку dest с датой и временем в имени."""
    if not os.path.isdir(source):
        return "Ошибка: Исходный путь не является папкой."

    if not os.path.exists(dest):
        try:
            os.makedirs(dest)
        except Exception as e:
            return f"Ошибка при создании папки назначения: {e}"

    # Дата и время до секунды
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Имя исходной папки
    source_name = os.path.basename(os.path.normpath(source))
    
    # Имя архива без .zip
    archive_name = f"{source_name}_{current_time}"
    archive_path_no_ext = os.path.join(dest, archive_name)
    
    try:
        # Создаем zip-архив
        archive_path = shutil.make_archive(archive_path_no_ext, 'zip', source)
        return f"Архив создан:\n{archive_path}"
    except Exception as e:
        return f"ОШИБКА при создании архива: {e}"


class Task4Window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_PATH, self)
        
        # Подключаем кнопки
        self.btn_src.clicked.connect(self.select_source)
        self.btn_dest.clicked.connect(self.select_dest)
        self.btn_run.clicked.connect(self.run_archive)

    def select_source(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для архивации")
        if path:
            self.text_output.setPlainText(f"Исходная папка: {path}")

    def select_dest(self):
        path = QFileDialog.getExistingDirectory(self, "Выберите папку, куда сохранить архив")
        if path:
            # Дописываем в конец текста
            current_text = self.text_output.toPlainText()
            self.text_output.setPlainText(f"{current_text}\nПапка назначения: {path}")

    def run_archive(self):
        # Берем текст из поля вывода, чтобы найти пути
        text = self.text_output.toPlainText()
        
        source_path = ""
        dest_path = ""
        
        # Ищем строки с путями
        for line in text.split('\n'):
            if "Исходная папка:" in line:
                source_path = line.replace("Исходная папка:", "").strip()
            if "Папка назначения:" in line:
                dest_path = line.replace("Папка назначения:", "").strip()
                
        if not source_path or not dest_path:
            self.text_output.setPlainText("ОШИБКА: Сначала выберите ИСХОДНУЮ папку и ПАПКУ НАЗНАЧЕНИЯ!")
            return
            
        
        self.text_output.setPlainText("Архивация... Пожалуйста, подождите.")
        QApplication.processEvents() # Обновляем интерфейс
        
        # Вызываем функцию
        result = make_reserve_arc(source_path, dest_path)
        
        self.text_output.setPlainText(result)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Task4Window()
    window.show()
    sys.exit(app.exec())