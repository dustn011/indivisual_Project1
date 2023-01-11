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

        # 학생, 교수 ID, PW란에 아무것도 입력 안했으면 어떤 걸 적어야 하는지 가이드 라인을 보여줌
        self.led_studentID.setPlaceholderText('ID')
        self.led_studentPW.setPlaceholderText('Password')
        self.led_professorID.setPlaceholderText('ID')
        self.led_professorPW.setPlaceholderText('Password')

        # 학생 로그인 버튼을 클릭하면 checkStudentLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.btn_studentLogin.clicked.connect(self.checkStudentLogin)
        # 학생 비밀번호 입력 라인에디터에서 엔터키 누르면 checkStudentLogin 함수 실행. 로그인 확인 후 승인 or 거절
        self.led_studentPW.returnPressed.connect(self.checkStudentLogin)

        # 로그아웃 버튼 누르면 로그아웃 하고 로그인 페이지로 돌아감
        self.btn_Logout1.clicked.connect(self.student_logout)   # 교수 위젯 로그아웃
        self.btn_Logout2.clicked.connect(self.student_logout)   # 학생 위젯 로그아웃
        self.btn_Logout3.clicked.connect(self.student_logout)   # 일정 위젯에서 로그아웃

        # self.studentORprofessor_widget.

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

        # ---------------- 일정 위젯 ----------------
        # 일정 보기 버튼 누르면 일정위젯으로 이동하는 메소드 실행
        self.btn_showChalendar.clicked.connect(self.move_scheduleWidget)
        # 일정 추가 버튼 누르면 DB에 일정 추가해주는 메소드 실행
        self.btn_addSchedule.clicked.connect(self.method_addSchedule)
        # 일정 삭제 버튼 누르면 DB의 일정 삭제해주는 메소드 실행
        self.btn_deleteSchedule.clicked.connect(self.method_deleteSchedule)

        # 캘린더 선택하면 선택한 날짜에 있는 일정 보여주는 메소드 실행
        self.cw_schedule.clicked.connect(self.method_showSchedule)

    # ---------------- 일정 메서드 ----------------
    # 일정 위젯으로 이동하는 메서드
    def move_scheduleWidget(self):
        self.HRD_Widget.setCurrentIndex(3)

    # 일정 삭제하는 메소드
    def method_deleteSchedule(self):
        print()
        pass

    # 일정 추가하는 메소드
    def method_addSchedule(self):
        # 쿼리문으로 전달할 일정 데이터 문자열로 저장 test_addNo1Schedule
        schedule = self.led_addSchedule.text()

        # 일정 안적으면 일정 추가 못함
        if not bool(schedule):
            QMessageBox.information(self, '공백 오류', '일정을 입력해주세요')
        # 일정 적어야 일정 추가 기닁 돌아감
        else:
            # 캘린더에서 선택한 날짜 가져와서 date 변수에 넣어주기
            selectDay = self.cw_schedule.selectedDate().toString('yyMMdd')

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 오늘 날짜와 로그인한 사람의 이름, 일정내용을 DB에 넣고싶어
            sql = f"INSERT INTO schedule_test VALUES('{selectDay}', '{self.account[1]}', '{schedule}')"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()

            # DB 닫아주기
            src_db.close()
            print(f'"{schedule}"을 일정에 넣었습니다')

            # 사용자에게 입력 완료했다고 알려주는 메세지 박스 출력
            QMessageBox.information(self, '입력 완료', '일정 입력하셨습니다')

            # 입력하고 나서 라인에디트 지워주기
            self.led_addSchedule.clear()

            # 입력한 일정 보여주기
            self.method_showSchedule()

    # 선택한 날짜의 일정을 보여주는 메소드
    def method_showSchedule(self):

        self.list_scheduleWriter.clear()        # 작성한 리스트 위젯 지워주기
        self.lbw_dailySchedule.clear()          # 작성한 리스트 위젯 지워주기
        self.tb_selectDate.clear()              # 작성한 선택날짜 텍스트브라우저 지워주기

        # 선택한 날짜 yyMMdd 형식으로 저장
        selectDay = self.cw_schedule.selectedDate().toString('yyMMdd')

        # DB 열기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 선택한 날짜의 일정(작성자)을 가져오고 싶어
        sql = f"SELECT 작성자, 일정 FROM schedule_test WHERE 날짜 = {selectDay}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        schedule_data = cur_corn.fetchall()  # 오늘 로그인한 사람의 출석 상황 정보 저장(2중튜플)
        # DB 닫아주기
        src_db.close()

        print(schedule_data)

        self.tb_selectDate.setText(self.cw_schedule.selectedDate().toString('yy년MM월dd일'))
        # 작성자 리스트 위젯에 넣기
        for i in schedule_data:
            self.list_scheduleWriter.addItem(i[0])

        # 일정 내용 리스트 위젯에 넣기
        for i in schedule_data:
            self.lbw_dailySchedule.addItem(i[1])

    # ---------------- 출석 메서드 ----------------
    # 출석 상태 확인 메서드(로그인 후 실행)
    def check_attandance(self):
        #오늘 날짜 구하기
        date = QDate.currentDate()
        nowdate = date.toString('yyMMdd')

        # DB를 열고 오늘 접속한 회원의 출석상태 확인
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 오늘 로그인한 사람의 출석 상황을 보고싶어
        sql = f"SELECT * FROM test_attandance WHERE 번호 = {self.account[0]} AND 날짜 = {nowdate}"

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

    # 입실 버튼 누르면 실행되는 메서드(지각인지 아닌지 확인하기)
    def method_present(self):
        # 입실 체크 메세지 출력 Yes 누르면 입실됨
        check = QMessageBox.question(self, '입실', '입실 하겠습니까?', QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if check == QMessageBox.Yes:
            # 현재 시간 QTime.current로 가져와서 time 변수에 넣어주기
            time = QTime.currentTime()
            # 현재 날짜 QDate.current로 가져와서 date 변수에 넣어주기
            date = QDate.currentDate()
            # 입실 완료 메세지
            QMessageBox.information(self, '입실 완료', '입실 하셨습니다')

            # 외출, 퇴실 버튼 있는 위젯으로 이동
            self.schedule_btnWidget.setCurrentIndex(1)

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
            sql = f"INSERT INTO test_attandance(날짜, 번호, 입실시간)" \
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
            sql = f"UPDATE test_attandance SET 외출시간 = {nowTime} WHERE (날짜 = {nowDate}) AND (번호 = {student_num})"

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

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 복귀 시간을 그 사람이 입실한 날짜와 학생번호가 일치하는 row에 업데이트 하고 싶어
            sql = f"UPDATE test_attandance SET 복귀시간 = {nowTime} WHERE (날짜 = {nowDate}) AND (번호 = {student_num})"

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

            # DB 연결하기
            src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
            # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
            cur_corn = src_db.cursor()

            # 퇴실 시간을 그 사람이 입실한 날짜와 학생번호가 일치하는 row에 업데이트 하고, 출석했으면 대문자 O를 넣고 싶어
            sql = f"UPDATE test_attandance SET 퇴실시간 = {nowTime}, 출결 = '출석' WHERE (날짜 = {nowDate}) AND (번호 = {student_num})"

            # execute 메서드로 db에 sql 문장 전송
            cur_corn.execute(sql)
            # 쿼리문 실행!
            src_db.commit()
            # DB 닫아주기
            src_db.close()

    # 지각이면 지각 데이터 카운트 추가 메서드
    def method_lateCount(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 현재 로그인 한 사람의 지각 카운트를 추가하고 싶어
        sql = f"UPDATE student_test SET 지각 = {self.account[-2]} + 1 WHERE 번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()

    # 조퇴면 조퇴 데이터 카운트 추가 메서드
    def method_earlyLeaveCount(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 현재 로그인 한 사람의 조퇴 카운트를 추가하고 싶어
        sql = f"UPDATE student_test SET 조퇴 = {self.account[-3]} + 1 WHERE 번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()

    # 외출하면 외출 데이터 카운트 추가 메서드
    def method_goingoutCount(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 현재 로그인 한 사람의 외출 카운트를 추가하고 싶어
        sql = f"UPDATE student_test SET 외출 = {self.account[-2]} + 1 WHERE 번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()

    # 결석하면 결석 데이터 카운트 추가 메서드
    def method_absentCount(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 현재 로그인 한 사람의 결석 카운트를 추가하고 싶어
        sql = f"UPDATE student_test SET 결석 = {self.account[-1]} + 1 WHERE 번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()

    # 출석하면 출석 데이터 카운트 추가 메서드
    def method_attandanceCount(self):
        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 현재 로그인 한 사람의 출석 카운트를 추가하고 싶어
        sql = f"UPDATE student_test SET 출석 = {self.account[-5]} + 1 WHERE 번호 = {self.account[0]}"

        # execute 메서드로 db에 sql 문장 전송
        cur_corn.execute(sql)
        # 쿼리문 실행!
        src_db.commit()
        # DB 닫아주기
        src_db.close()

    # 출석 상태 하단에 보여주기 메서드
    def show_attandance(self):
        attandance = str(self.account[-5])
        late = str(self.account[-4])
        earlyLeave = str(self.account[-3])
        goingout = str(self.account[-2])
        absent = str(self.account[-1])

        self.circle_attandance.setText(attandance)
        self.circle_late.setText(late)
        self.circle_earlyLeave.setText(earlyLeave)
        self.circle_goingout.setText(goingout)
        self.circle_absent.setText(absent)

    # ---------------- 로그인 메서드 ----------------
    # 메인 화면에서 로그아웃버튼을 누르면 로그인 창으로 되돌아옴
    def student_logout(self):
        self.HRD_Widget.setCurrentIndex(0)
        self.schedule_btnWidget.setCurrentIndex(0)
        # 입실 퇴실 시간 ui에서 지우기
        self.time_present.clear()
        self.time_leave.clear()
        self.time_goingout.clear()
        self.time_return.clear()

    # DB에서 ID, PW 정보 가져와서 입력한 ID, PW와 대조하기(학생)
    def checkStudentLogin(self):
        checking_id = self.led_studentID.text()
        checking_pw = self.led_studentPW.text()

        # DB 연결하기
        src_db = pymysql.connect(host='10.10.21.102', user='local', password='0000', db='b-corn', charset='utf8')
        # DB와 상호작용하기 위해 연결해주는 cursor 객체 만듬
        cur_corn = src_db.cursor()

        # 회원정보의 ID가 checking_id이고 PW는 checking_pw인 사람의 정보를 학생용 데이터에서 찾고 싶어
        student_sql = f"SELECT * FROM student_test WHERE (아이디 = '{checking_id}') AND (비밀번호 = '{checking_pw}')"      # test용 임시 데이터 만듬(수정 할 것)
        # execute 메서드로 db에 student_sql 문장 전송
        cur_corn.execute(student_sql)
        # 전체 나열 함수, 레코드를 배열(튜플) 형식으로 저장해준다(fetch : 나열하다 정렬하다)
        student_account = cur_corn.fetchall()      # 로그인 하는 account 계정 정보 저장(2중튜플)

        # DB 닫아주기
        src_db.close()

        # 로그인, 비밀번호 틀렸을 시 student_account에는 빈 튜플만 저장됨
        if not bool(student_account):
            self.reject_studentLogin()     # 로그인 거절 함수 실행
            print('로그인 실패')
        else:
            self.account = student_account[0]  # 2중 튜플이 아닌 일반 1중 튜플로 학생 회원 정보 저장
            self.accept_studentLogin()     # 로그인 허용 함수 실행

    # 로그인 성공 시 실행하는 함수(학생)
    def accept_studentLogin(self):
        print('로그인 성공')
        # 위젯의 2페이지로 넘어감
        self.HRD_Widget.setCurrentIndex(2)
        # 아이디, 비밀번호 입력한 라인에디터 박스 초기화
        self.led_studentID.clear()
        self.led_studentPW.clear()

        print(self.account)

        # 출석 상태에 따라서 어떤 출색 위젯을 먼저 보이게 할 지 설정
        self.check_attandance()
        # 하단 출석상태 출력 실험 실행
        self.show_attandance()

    # 로그인 실패 시 실행하는 함수(학생)
    def reject_studentLogin(self):
        # 입력 실패 안내 문구 출력함
        QMessageBox.information(self, '입력 오류', '아이디나 비밀번호가 틀리셨습니다\n다시 입력해주세요')
        # 아이디, 비밀번호 입력한 라인에디터 박스 초기화(다시써)
        self.led_studentID.clear()
        self.led_studentPW.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bcorn = Bcorn()
    bcorn.show()
    app.exec_()
