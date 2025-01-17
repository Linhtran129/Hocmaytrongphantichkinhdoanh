from PyQt6.QtWidgets import QMessageBox, QMainWindow

from Sales_management.UI.MainProgramMainWindowExt import MainProgramMainWindowExt
#from PyQt6.QtWidgets.QWidget import setWindowTitle

from Sales_management.UI.login_main_window import Ui_MainWindow


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.pushButton_Dangnhap.clicked.connect(self.xuly_dangnhap)

    def xuly_dangnhap(self):
        username = self.username.text()
        password = self.password.text()
        #giả lập đăng nhập (hôm sau truy vấn thật trong csdl)
        if username == "admin" and password =="123":
            self.MainWindow.hide()
            self.MainWindow = QMainWindow()
            self.myui = MainProgramMainWindowExt()
            self.myui.setupUi(self.MainWindow)
            self.myui.showWindow()
        else:
            self.msg=QMessageBox()
            self.msg.setWindowTitle("Login thất bại")
            self.msg.setText("Bạn đăng nhập thất bại. \nKiểm tra lại thông tin.")
            self.msg.setIcon(QMessageBox.Icon.Critical)
            self.msg.show()
