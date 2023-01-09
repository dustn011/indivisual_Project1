import pymysql
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

        # ID, PW란에 아무것도 입력 안했으면 어떤 걸 적어야 하는지 가이드 라인을 보여줌
        self.led_ID.setPlaceholderText('ID')
        self.led_PW.setPlaceholderText('Password')

        # 로그인 버튼을 클릭하면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.btn_login.clicked.connect(self.checkLogin)
        # 비밀번호 입력 라인에디터에서 엔터키 누르면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.led_PW.returnPressed.connect(self.checkLogin)

        self.btn_logout.clicked.connect(self.logout)

    # 메인 화면에서 로그아웃버튼을 누르면 로그인 창으로 되돌아옴
    def logout(self):
        self.HRD_Widget.setCurrentIndex(0)

    # DB에서 ID, PW 정보 가져와서 입력한 ID, PW와 대조하기
    def checkLogin(self):
        checking_id = self.led_ID.text()
        checking_pw = self.led_PW.text()

        # DB 연결하기
        src_db = pymysql.connect(host='127.0.0.1', user='root', password='DUstn123!', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 회원정보의 ID가 checking_id이고 PW는 checking_pw인 사람의 정보를 가져오고 싶어
        sql = f"SELECT * FROM `b-corn`.student_data WHERE (아이디 = '{checking_id}') AND (비밀번호 = '{checking_pw}')"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)

        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        self.account = cur_corn.fetchall()      # 로그인 하는 account 계정 정보 저장
        # DB 닫아주기
        src_db.close()

        # 로그인, 비밀번호 틀렸을 시
        if not bool(self.account):
            self.reject_login()     # 로그인 거절 함수 실행
        else:
            self.accept_login()     # 로그인 허용 함수 실행

    # 로그인 성공 시 실행하는 함수
    def accept_login(self):
        print('로그인 성공')
        # 위젯의 1페이지로 넘어감
        self.HRD_Widget.setCurrentIndex(1)
        # 아이디, 비밀번호 입력한 라인에디터 박스 초기화
        self.led_ID.clear()
        self.led_PW.clear()
        
    # 로그인 실패 시 실행하는 함수
    def reject_login(self):
        # 입력 실패 안내 문구 출력함
        QMessageBox.information(self, '입력 오류', '아이디나 비밀번호가 틀리셨습니다\n다시 입력해주세요')
        # 아이디, 비밀번호 입력한 라인에디터 박스 초기화(다시써)
        self.led_ID.clear()
        self.led_PW.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bcorn = Bcorn()
    bcorn.show()
    app.exec_()
