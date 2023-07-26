import sys
import threading
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QMessageBox
from selenium import webdriver
from time import sleep
import math


class ChromeDriverThread(threading.Thread):
    def __init__(self, stop_event, thread):
        super().__init__()
        self.stop_event = stop_event
        self.thread = thread

    def run(self):
        num_worker = self.thread
        cols = 10
        x = (num_worker % cols) * 510
        y = math.floor(num_worker / cols) * 810

        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)

        options = webdriver.ChromeOptions()
        options.add_argument("--force-device-scale-factor=0.375")
        driver = webdriver.Chrome(options=options)
        driver.set_window_rect(x, y, 200, 800)

        driver.get("https://www.youtube.com/")

        sleep(3)
        while not self.stop_event.is_set():
            sleep(1)
            driver.execute_script("window.scrollBy(0, 100);")

        driver.quit()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Multithreaded Chrome Driver")
        self.setGeometry(100, 100, 400, 200)

        self.start_button = QPushButton("Start", self)
        self.start_button.setGeometry(100, 50, 100, 50)
        self.start_button.clicked.connect(self.start_thread)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.setGeometry(200, 50, 100, 50)
        self.stop_button.clicked.connect(self.stop_thread)
        self.stop_button.setEnabled(False)

        self.stop_event = threading.Event()
        self.chrome_threads = []

    def start_thread(self):
        num_thread = 5
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.stop_event.clear()  # Đảm bảo flag stop_event là chưa được set
        self.chrome_threads = [
            ChromeDriverThread(self.stop_event, i) for i in range(num_thread)
        ]

        for thread in self.chrome_threads:
            sleep(3)
            thread.start()

    def stop_thread(self):
        result = QMessageBox.question(
            self,
            "Xác nhận dừng",
            "Bạn có chắc chắn muốn dừng không.Điều này có thể gây mất mát dữ liệu?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if result == QMessageBox.StandardButton.Yes:
            self.stop_event.set()  # Set flag stop_event để tất cả các luồng biết dừng
            for thread in self.chrome_threads:
                thread.join()

            self.stop_button.setEnabled(False)
            self.start_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
