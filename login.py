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

        # ---------------- 로그인 위젯 ----------------
        # 처음 보이는 페이지는 로그인 페이지로 설정
        self.HRD_Widget.setCurrentIndex(0)

        # ID, PW란에 아무것도 입력 안했으면 어떤 걸 적어야 하는지 가이드 라인을 보여줌
        self.led_ID.setPlaceholderText('ID')
        self.led_PW.setPlaceholderText('Password')

        # 로그인 버튼을 클릭하면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.btn_login.clicked.connect(self.checkLogin)
        # 비밀번호 입력 라인에디터에서 엔터키 누르면 checkLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.led_PW.returnPressed.connect(self.checkLogin)

        # 로그아웃 버튼 누르면 로그아웃 하고 로그인 페이지로 돌아감
        self.btn_logout.clicked.connect(self.logout)

        # ---------------- 출석 위젯 ----------------

        # 입실 버튼 누르면 메소드 실행(출석 체크 시작)
        self.btn_present.clicked.connect(self.method_present)

        # 외출 버튼 누르면 메소드 실행
        self.btn_goingout.clicked.connect(self.method_goingout)

        # 복귀 버튼 누르면 메소드 실행
        self.btn_return.clicked.connect(self.method_return)

        # 퇴실 버튼 누르면 메소드 실행(출석 체크 완료)
        self.btn_leave1.clicked.connect(self.method_leave)
        self.btn_leave2.clicked.connect(self.method_leave)

    # ---------------- 출석 메서드 ----------------
    # 출석 상태 확인 메서드(로그인 후 실행)
    def check_attandance(self):
        # DB를 열고 오늘 접속한 회원의 출석상태 확인
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 오늘 로그인한 사람의 출석 상황을 보고싶어
        sql = f"SELECT * FROM test_attandance WHERE 학생번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        attandance = cur_corn.fetchall()      # 오늘 로그인한 사람의 출석 상황 정보 저장(2중튜플)
        # DB 닫아주기
        src_db.close()
        # print(str(attandance[0][-1])) print(attandance)
        if bool(attandance):
            # 입실한 상태이면 외출 / 퇴실 위젯이 뜨게 함
            if bool(attandance[0][-4]):
                self.schedule_btnWidget.setCurrentIndex(1)  # 외출 / 퇴실 위젯은 인덱스 1번
                self.time_present.setText(f'입실 | {attandance[0][-4]}')
            # 외출한 상태이면 복귀 위젯이 뜨게 함
            if bool(attandance[0][-3]):
                self.schedule_btnWidget.setCurrentIndex(2)      # 복귀 위젯은 인덱스 2번
                self.time_goingout.setText(f'외출 | {attandance[0][-3]}')
            # 복귀한 상태이면 퇴실 위젯이 뜨게 함
            if bool(attandance[0][-2]):
                self.schedule_btnWidget.setCurrentIndex(3)      # 퇴실 위젯은 인덱스 3번
                self.time_return.setText(f'복귀 | {attandance[0][-2]}')
            # 퇴실 했으면 출석 완료 위젯이 뜨게 함
            if bool(attandance[0][-1]):
                self.schedule_btnWidget.setCurrentIndex(4)  # 출석 완료 위젯은 인덱스 4번
                self.time_leave.setText(f'퇴실 | {attandance[0][-1]}')
        # 입실 하지 않은 상태일 때 입실 위젯 뜨게 함
        else:
            self.schedule_btnWidget.setCurrentIndex(0)      # 입실 위젯은 인덱스 0번

    # 입실 버튼 누르면 실행되는 메서드
    def method_present(self):
        # 입실 체크 메세지 출력 Yes 누르면 입실됨
        check = QMessageBox.question(self, '입실', '입실 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if check == QMessageBox.Yes:
            # 입실 완료 메세지
            QMessageBox.information(self, '입실 완료', '입실 하셨습니다')
            # 외출, 퇴실 버튼 있는 위젯으로 이동
            self.schedule_btnWidget.setCurrentIndex(1)

            # 현재 시간 QTime.current로 가져와서 time 변수에 넣어주기
            time = QTime.currentTime()
            # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
            date = QDate.currentDate()

            # 입실 | **:** 형태로 입실 시간 time_present 텍스트 브라우저에 넣어주기
            self.time_present.setText(time.toString('입실 | hh:mm:ss'))

            # 쿼리문으로 전달할 날짜 데이터 문자열로 저장
            nowDate = date.toString('yyMMdd')
            # 쿼리문으로 전달할 학생 번호 저장
            student_num = str(self.account[0])
            # 쿼리문으로 전달할 입실 시간 데이터 문자열로 저장
            nowTime = time.toString('hhmmss')

            # 지금 로그인 한 사람의 정보 가져오기
            # print(self.account)
            # print(type(student_name), nowTime, nowDate)

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 오늘 날짜와 로그인한 사람의 학생번호, 입실시간을 DB에 넣고싶어
            sql = f"INSERT INTO test_attandance(날짜, 학생번호, 입실시간)" \
                  f"VALUES({nowDate}, {student_num}, {nowTime})"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()
            # DB 닫아주기
            src_db.close()

    # 외출 버튼 누르면 실행되는 메서드
    def method_goingout(self):
        check = QMessageBox.question(self, '외출', '외출 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if check == QMessageBox.Yes:
            QMessageBox.information(self, '외출', '시간 안에 복귀해주세요')
            # 복귀 버튼 있는 위젯으로 이동
            self.schedule_btnWidget.setCurrentIndex(2)

            # 외출 시간 텍스트 브라우저에 적음
            time = QTime.currentTime()  # 현재 시간 QTime.current로 가져와서 time 변수에 넣어주기
            # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
            date = QDate.currentDate()

            # 외출 | **:** 형태로 입실 시간 time_present 텍스트 브라우저에 넣어주기
            self.time_goingout.setText(time.toString('외출 | hh:mm:ss'))

            # 쿼리문으로 전달할 날짜 데이터 문자열로 저장
            nowDate = date.toString('yyMMdd')
            # 쿼리문으로 전달할 학생 번호 저장
            student_num = str(self.account[0])
            # 쿼리문으로 전달할 외출 시간 데이터 문자열로 저장
            nowTime = time.toString('hhmmss')

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 외출 시간을 그 사람이 입실한 날짜와 학생번호가 일치하는 row에 업데이트 하고 싶어
            sql = f"UPDATE test_attandance SET 외출시간 = {nowTime} WHERE (날짜 = {nowDate}) AND (학생번호 = {student_num})"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()
            # DB 닫아주기
            src_db.close()

    # 복귀 버튼 누르면 실행되는 메서드
    def method_return(self):
        check = QMessageBox.question(self, '복귀', '복귀 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if check == QMessageBox.Yes:
            QMessageBox.information(self, '복귀 완료', '복귀 하셨습니다')
            # 퇴실 버튼 있는 위젯으로 이동
            self.schedule_btnWidget.setCurrentIndex(3)

            # 복귀 시간 텍스트 브라우저에 적음
            time = QTime.currentTime()  # 현재 시간 QTime.current로 가져와서 time 변수에 넣어주기
            # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
            date = QDate.currentDate()

            # 복귀 | **:** 형태로 복귀 시간 time_present 텍스트 브라우저에 넣어주기
            self.time_return.setText(time.toString('복귀 | hh:mm:ss'))

            # 쿼리문으로 전달할 날짜 데이터 문자열로 저장
            nowDate = date.toString('yyMMdd')
            # 쿼리문으로 전달할 학생 번호 저장
            student_num = str(self.account[0])
            # 쿼리문으로 전달할 외출 시간 데이터 문자열로 저장
            nowTime = time.toString('hhmmss')

            # 지금 로그인 한 사람의 정보 가져오기
            # print(self.account)
            print(type(student_num), nowTime, nowDate)

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 복귀 시간을 그 사람이 입실한 날짜와 학생번호가 일치하는 row에 업데이트 하고 싶어
            sql = f"UPDATE test_attandance SET 복귀시간 = {nowTime} WHERE (날짜 = {nowDate}) AND (학생번호 = {student_num})"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()
            # DB 닫아주기
            src_db.close()

    # 퇴실 버튼 누르면 실행되는 메서드
    def method_leave(self):
        check = QMessageBox.question(self, '퇴실', '퇴실 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if check == QMessageBox.Yes:
            QMessageBox.information(self, '퇴실 완료', '퇴실 하셨습니다')
            # 출석 체크 완료 위젯으로 이동
            self.schedule_btnWidget.setCurrentIndex(4)

            # 퇴실 시간 텍스트 브라우저에 적음
            time = QTime.currentTime()      # 현재 시간 QTime.current로 가져와서 time 변수에 넣어주기
            # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
            date = QDate.currentDate()

            # 퇴실 | **:** 형태로 입실 시간 time_present 텍스트 브라우저에 넣어주기
            self.time_leave.setText(time.toString('퇴실 | hh:mm:ss'))

            # 쿼리문으로 전달할 날짜 데이터 문자열로 저장
            nowDate = date.toString('yyMMdd')
            # 쿼리문으로 전달할 학생 번호 저장
            student_num = str(self.account[0])
            # 쿼리문으로 전달할 외출 시간 데이터 문자열로 저장
            nowTime = time.toString('hhmmss')

            # 지금 로그인 한 사람의 정보 가져오기
            # print(self.account)
            print(type(student_num), nowTime, nowDate)

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 퇴실 시간을 그 사람이 입실한 날짜와 학생번호가 일치하는 row에 업데이트 하고 싶어
            sql = f"UPDATE test_attandance SET 퇴실시간 = {nowTime}, 출석 = 'O'  WHERE (날짜 = {nowDate}) AND (학생번호 = {student_num})"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()
            # DB 닫아주기
            src_db.close()

    # ---------------- 로그인 메서드 ----------------
    # 메인 화면에서 로그아웃버튼을 누르면 로그인 창으로 되돌아옴
    def logout(self):
        self.HRD_Widget.setCurrentIndex(0)
        self.schedule_btnWidget.setCurrentIndex(0)
        # 입실 퇴실 시간 ui에서 지우기
        self.time_present.clear()
        self.time_leave.clear()
        self.time_goingout.clear()
        self.time_return.clear()

    # DB에서 ID, PW 정보 가져와서 입력한 ID, PW와 대조하기
    def checkLogin(self):
        checking_id = self.led_ID.text()
        checking_pw = self.led_PW.text()

        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 회원정보의 ID가 checking_id이고 PW는 checking_pw인 사람의 정보를 가져오고 싶어
        sql = f"SELECT * FROM student_test WHERE (아이디 = '{checking_id}') AND (비밀번호 = '{checking_pw}')"              # test용 임시 데이터 만듬(수정 할 것)

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)

        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        account = cur_corn.fetchall()      # 로그인 하는 account 계정 정보 저장(2중튜플)
        self.account = account[0]       # 2중 튜플이 아닌 일반 1중 튜플로 회원 정보 저장

        # DB 닫아주기
        src_db.close()

        # 로그인, 비밀번호 틀렸을 시 self.account에는 빈 튜플만 저장됨
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

        # 출석 상태에 따라서 어떤 출색 위젯을 먼저 보이게 할 지 설정
        self.check_attandance()

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
