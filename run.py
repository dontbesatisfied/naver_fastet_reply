import os
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import *
import sys
import constant
from app import Process
from datetime import datetime

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
# form_class = uic.loadUiType(os.getcwd() + "/app.ui")[0]
form_class = uic.loadUiType("./app.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.naver_pw_edt.setEchoMode(QLineEdit.Password)
        self.start_btn.clicked.connect(self.clicked_start)
        self.set_dir.clicked.connect(self.clicked_set_dir)
        self.dateTimeEdit.setMinimumDateTime(QtCore.QDateTime.currentDateTime())
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

    def clicked_start(self):
        try:
            if self.check_input():
                Process().run()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Error")
                msg.setInformativeText('입력을 다시 확인하세요')
                msg.setWindowTitle("Error")
                msg.exec_()
        except Exception as e:
            raise Exception(e)

    def check_input(self):
        try:
            id = self.naver_id_edt.text()
            pw = self.naver_pw_edt.text()
            blog_id = self.blog_id_edt.text()
            reply_content = self.reply_content_edt.text()
            interval = self.interval_box.value()
            gecko_path = self.dir_edt.text()

            if id and pw and blog_id and reply_content and interval and gecko_path:
                constant.NAVER_ID = id
                constant.NAVER_PW = pw
                constant.BLOG_ID = blog_id
                constant.REPLY_CONTENT = reply_content
                constant.INTERVAL_SEC = interval
                constant.GECKO_DRIVER_PATH = gecko_path
                constant.MAX_DATETIME = self.dateTimeEdit.dateTime().toPyDateTime()
                return True
            else:
                return False

        except Exception as e:
            raise Exception(e)

    def clicked_set_dir(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Open file', os.getcwd(),
                                               "All Files(*)")
            self.dir_edt.setText(path[0])
        except Exception as e:
            raise Exception(e)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()

    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
