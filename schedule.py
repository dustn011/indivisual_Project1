import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QTime, QDate

# ui 클래스
form_class = uic.loadUiType("ui/main.ui")[0]


# 클래스 선언
class Bcorn(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 등록 일정 보는 위젯 페이지로 설정(임시)
        self.HRD_Widget.setCurrentIndex(3)

        # 일정 작성자 리스트 보여주는 함수 실행
        self.show_scheduleWriter()

        # 일정추가 버튼 누르면 함수 실행
        self.btn_addSchedule.clicked.connect(self.method_addSchedule)

    # 일정 추가하는 메소드
    def method_addSchedule(self):
        print(self.led_addSchedule.text())
        # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
        date = QDate.currentDate()
        # 쿼리문으로 전달할 날짜 데이터 문자열로 저장
        nowDate = date.toString('yyMMdd')
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 오늘 날짜와 로그인한 사람의 학생번호, 입실시간을 DB에 넣고싶어
        sql = f"INSERT INTO test_attandance(날짜, 번호, 입실시간) VALUES({nowDate}, {student_num}, {nowTime})"


        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()


    # (나중에 추가할 기능 선택한 날짜의)일정 작성자 리스트를 나열
    def show_scheduleWriter(self):
        pass
        # # self.list_scheduleWriter
        # # DB 연결하기
        # src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        # cur_corn = src_db.cursor()
        #
        # # 회원정보의 학생 이름 리스트만 모두 가져오고 싶어
        # sql = f"SELECT 이름 FROM `b-corn`.student_data WHERE (아이디 = '{checking_id}') AND (비밀번호 = '{checking_pw}')"
        #
        # # execute 메서드로 db에 sql 문장 전송
        # cur_corn.execute(sql)
        #
        # # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        # self.account = cur_corn.fetchall()  # 로그인 하는 account 계정 정보 저장
        # # DB 닫아주기
        # src_db.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bcorn = Bcorn()
    bcorn.show()
    app.exec_()
