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

        # 등록 일정 보는 위젯 페이지로 설정(임시)
        self.HRD_Widget.setCurrentIndex(2)

        # 학생 리스트 보여주세요~
        self.show_student()

    # (나중에 추가할 기능 선택한 날짜의)학생 리스트를 나열
    def show_student(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 회원정보의 학생 이름 리스트만 모두 가져오고 싶어
        sql = f"SELECT 이름 FROM `b-corn`.student_data WHERE (아이디 = '{checking_id}') AND (비밀번호 = '{checking_pw}')"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)

        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        self.account = cur_corn.fetchall()  # 로그인 하는 account 계정 정보 저장
        # DB 닫아주기
        src_db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bcorn = Bcorn()
    bcorn.show()
    app.exec_()
