from gui.gui import BibliotecaApp

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    ex = BibliotecaApp()
    ex.show()
    sys.exit(app.exec_())
