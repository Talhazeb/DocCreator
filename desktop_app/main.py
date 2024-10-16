import sys
from PyQt5.QtWidgets import QApplication
from desktop_app.ui.main_window import MainWindow
from desktop_app.config.config_manager import ConfigManager

def main():
    app = QApplication(sys.argv)
    config = ConfigManager('config.ini')
    main_window = MainWindow(config)
    main_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()