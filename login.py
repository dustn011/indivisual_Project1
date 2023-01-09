import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# ui 클래스
form_class = uic.loadUiType("ui/main.ui")[0]


# 클래스 선언
class Bcorn(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 로그인 버튼을 클릭하면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.btn_login.clicked.connect(self.checkLogin)
        # 비밀번호 입력 라인에디터에서 엔터키 누르면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.led_PW.returnPressed.connect(self.checkLogin)

    # DB에서 ID, PW 정보 가져와서 입력한 ID, PW와 대조하기
    def checkLogin(self):
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bcorn = Bcorn()
    bcorn.show()
    app.exec_()
