from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
# import sqlite3
import mysql.connector
import sys
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont
import random
# import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from passlib.hash import sha256_crypt

ui_path = "src/"
icon_path = "src/icon.png"


class sendMail():

    def send(self, to, subject, main_text):
        message = MIMEMultipart()
        message["From"] = "Login by sensoyg"
        message["To"] = to
        message["Subject"] = subject
        message_body = MIMEText(main_text, "plain")
        message.attach(message_body)
        self.mail.sendmail(message["From"], message["To"], message.as_string())
        print("Mail successfully sent...")

    def connect(self):
        self.mail = smtplib.SMTP("smtp.gmail.com", 587)
        self.mail.ehlo()
        self.mail.starttls()
        self.mail.login("youremail@mail.com", "youremailPassword")

class connection():

    def __init__(self):
        self.con = mysql.connector.connect(host="127.0.0.1", port="3306", user="root", passwd="", database="login")
        self.cursor = self.con.cursor()
        self.cursor.execute("create table if not exists users (id TEXT, name TEXT, surname TEXT, email TEXT, password TEXT)")
        self.con.commit()


class temp_id():
    def setTemp(self, temp):
        self.temp_hesap = temp

    def getTemp(self):
        return self.temp_hesap

    def setEmail(self, mail):
        self.temp_mail = mail

    def getEmail(self):
        return self.temp_mail


class Enter(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.con = connection()
        self.setStyleSheet("background-color: #13bfc9;")
        sorgu = "select * from users"
        self.con.cursor.execute(sorgu)
        self.query_out = self.con.cursor.fetchall()

    def init_ui(self):

        self.register_button = QtWidgets.QPushButton("Register")
        self.login_button = QtWidgets.QPushButton("Login")

        self.register_button.clicked.connect(self.click)
        self.login_button.clicked.connect(self.click2)

        self.label = QtWidgets.QLabel("Login")

        self.label.setFont(QFont("Arial", 12))
        self.login_button.setFixedSize(200, 70)
        self.register_button.setFixedSize(200, 70)
        self.setGeometry(640, 300, 640, 450)
        self.login_button.setStyleSheet("background-color: solid white;")
        self.register_button.setStyleSheet("background-color: solid white;")

        self.h_box = QtWidgets.QHBoxLayout()

        self.v_box = QtWidgets.QVBoxLayout()

        self.h2_box = QtWidgets.QHBoxLayout()

        self.h2_box.addStretch()
        self.h2_box.addWidget(self.label)
        self.h2_box.addStretch()

        self.v_box.addLayout(self.h2_box)
        self.v_box.addLayout(self.h_box)
        self.h_box.addWidget(self.register_button)
        self.h_box.addStretch()
        self.h_box.addWidget(self.login_button)
        self.setLayout(self.v_box)

    def click(self):
        stacked_widget.setCurrentIndex(1)

    def click2(self):
        if(len(self.query_out) == 0):
            self.user_dont_exists = '<p style="font-size:13pt; color: white;"><b>There is no one user found in database<br>You are redirecting to register page...<b/></p>'
            Register().msgbox.about(self, "Error!", self.user_dont_exists)
            stacked_widget.setCurrentIndex(1)
        else:
            stacked_widget.setCurrentIndex(2)


class Register(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.sendMail = mail1.send
        loadUi("{}register.ui".format(ui_path), self)
        self.main_page_button.clicked.connect(self.main_page_click)
        self.con = connection()
        self.main_func()

    def main_page_click(self):
        self.name_area.setText("")
        self.surname_area.setText("")
        self.email_area.setText("")
        self.password_area.setText("")
        self.repassword_area.setText("")
        stacked_widget.setCurrentIndex(0)

    def make_id(self):
        no = random.randint(0, 90000) + 10000
        query = "select * from users where id = %s"
        self.con.cursor.execute(query, (no,))
        nos = self.con.cursor.fetchall()
        if(len(nos) == 0):
            return no
        else:
            return make_id()

    def check_email(self, email):
        query = "select * from users where email = %s"
        self.con.cursor.execute(query, (email,))
        is_there = self.con.cursor.fetchall()
        if(len(is_there) == 0):
            return False
        else:
            return True

    def main_func(self):

        self.password_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repassword_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.register_button.clicked.connect(self.register_clicked)
        self.msgbox = QMessageBox()
        self.name_blank = '<p style="font-size:13pt; color: white;"><b>Name area cannot be blank!<b/></p>'
        self.nurname_blank = '<p style="font-size:13pt; color: white;"><b>Surname area cannot be blank!<b/></p>'
        self.password_blank = '<p style="font-size:13pt; color: white;"><b>Password area cannot be blank!<b/></p>'
        self.repassword_blank = '<p style="font-size:13pt; color: white;"><b>Re-Password area cannot be blank!<b/></p>'

    def register_clicked(self):

        if(self.name_area.text() == ""):
            self.msgbox.about(self, "Error!", self.name_blank)

        if(self.surname_area.text() == ""):
            self.msgbox.about(self, "Error!", self.surname_blank)

        if(self.password_area.text() == ""):
            self.msgbox.about(self, "Error!", self.password_blank)

        if(self.repassword_area.text() == ""):
            self.msgbox.about(self, "Error!", self.repassword_blank)

        if(not self.name_area.text() == "" and not self.surname_area.text() == "" and not self.password_area.text() == "" and not self.repassword_area.text() == ""):

            if(not self.email_area.text().find("@") == -1 and not self.email_area.text().find(".com") == -1):

                if(not self.check_email(self.email_area.text())):

                    if(self.password_area.text() == self.password_area.text()):
                        self.last_id = self.make_id()
                        self.registered = '<p style="font-size:13pt; color: white;"><b>You are successfully registered.<br> Your id : {}<br> You are redirecting to login page...<b/></p>'.format(self.last_id)
                        self.msgbox.about(self, "Registered", self.registered)
                        query = "insert into users (id, name, surname, email, password) values (%s,%s,%s,%s,%s)"
                        self.enc_password = sha256_crypt.hash(self.password_area.text())
                        self.con.cursor.execute(query, (self.last_id, self.name_area.text(), self.surname_area.text(), self.email_area.text(), self.enc_password))
                        self.con.con.commit()
                        self.main_text = "You are successfully registered\nYour id : {}".format(self.last_id)
                        self.sendMail(self.email_area.text(), "Successfully Registered", self.main_text)
                        self.name_area.setText("")
                        self.surname_area.setText("")
                        self.email_area.setText("")
                        self.password_area.setText("")
                        self.repassword_area.setText("")
                        stacked_widget.setCurrentIndex(2)
                    else:
                        self.passworddontmatch = """<p style = font-size:13pt; color: white;"><b>Password's don't match...<b/></p>"""
                        self.msgbox.about(self, "Error!", self.passworddontmatch)
                else:
                    self.email_using = '<p style="font-size:13pt; color: white;"><b>This E-Mail address already exists...<b/></p>'
                    self.msgbox.about(self, "Error!", self.email_using)
            else:
                self.email_not_valid = '<p style="font-size:13pt; color: white;"><b>This E-Mail address is not valid...<b/></p>'
                self.msgbox.about(self, "Error!", self.email_not_valid)


class Login(QtWidgets.QDialog):
    def __init__(self):
        self.con = connection()
        self.cursor = self.con.cursor
        super().__init__()
        self.sendmail = mail1.send
        loadUi("{}login.ui".format(ui_path), self)
        self.login_button.clicked.connect(self.click)
        self.password_button.clicked.connect(self.password_click)
        self.password_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.main_page_button.clicked.connect(self.main_page_click)
        self.id_button.clicked.connect(self.id_click)
        self.id_area.setMaxLength(5)
        self.main_page_button.clicked.connect(self.main_page_click)

    def main_page_click(self):
        stacked_widget.setCurrentIndex(0)

    def password_click(self):
        stacked_widget.setCurrentIndex(3)

    def id_click(self):
        stacked_widget.setCurrentIndex(4)

    def click(self):
        if(self.id_area.text() == ""):
            self.id_blank = '<p style="font-size:13pt; color: white;"><b>ID area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.id_blank)

        if(self.password_area.text() == ""):
            self.id_blank = '<p style="font-size:13pt; color: white;"><b>Password area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.id_blank)

        if(not self.id_area.text() == "" and not self.password_area.text() == ""):

            query = "select * from users where id = %s"
            self.con.cursor.execute(query,(self.id_area.text(),))
            self.result = self.con.cursor.fetchall()
            if(len(self.result) == 0):
                self.user_not_found = '<p style="font-size:13pt; color: white;"><b>User not found!<b/></p>'
                Register().msgbox.about(self, "Error!", self.user_not_found)
            else:
                query = "select password from users where id = %s"
                self.con.cursor.execute(query, (self.id_area.text(),))
                self.enc_password = self.con.cursor.fetchall()
                if(not sha256_crypt.verify(self.password_area.text(), self.enc_password[0][0])):
                    self.wrong_password = '<p style="font-size:13pt; color: white;"><b>Wrong Password!<b/></p>'
                    Register().msgbox.about(self, "Error!", self.wrong_password)
                    self.entry_detected = "An attempt was made to log into your account."
                    self.sendmail(self.email_print_out[0][0], "Log In Attempt", self.entry_detected)
                else:
                    self.logged_in = '<p style="font-size:13pt; color: white;"><b>you are successfully logged in!<b/></p>'
                    Register().msgbox.about(self, "Logged In!", self.logged_in)
                    query = "select email from users where id = %s"
                    self.con.cursor.execute(query, (self.id_area.text(),))
                    self.email_print_out = self.con.cursor.fetchall()
                    self.entry_detected = "Entry detected on your account..."
                    self.sendmail(self.email_print_out[0][0], "Entry Detected On Your Account", self.entry_detected)
                    self.id_area.setText("")
                    self.password_area.setText("")

                
# Old log in algorithm
            # query = "select * from users where id = %s and password = %s"
            # self.con.cursor.execute(query, (self.id_area.text(), self.password_area.text()))
            # control = self.con.cursor.fetchall()

            # if(len(control) == 0):
            #     self.user_not_found = '<p style="font-size:13pt; color: white;"><b>User not found!<b/></p>'
            #     Register().msgbox.about(self, "Error!", self.user_not_found)

            # else:
            #     self.logged_in = '<p style="font-size:13pt; color: white;"><b>you are successfully logged in!<b/></p>'
            #     Register().msgbox.about(self, "Logged In!", self.logged_in)
            #     query = "select email from users where id = %s"
            #     self.con.cursor.execute(query, (self.id_area.text(),))
            #     self.email_print_out = self.con.cursor.fetchall()
            #     self.entry_detected = "Entry detected on your account..."
            #     self.sendmail(self.email_print_out[0][0], "Entry Detected On Your Account", self.entry_detected)
            #     self.id_area.setText("")
            #     self.password_area.setText("")


class forgotPassword(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.sendmail = mail1.send
        loadUi("{}forgot_password.ui".format(ui_path), self)
        self.inputDialog = QtWidgets.QInputDialog
        self.inputDialog.setStyleSheet(self, "QDialog{background-color: #79360A;}" "QInputDialog {background-color: #79360A;};")
        self.id_area.setMaxLength(5)
        self.verification_area.setMaxLength(8)
        self.con = connection()
        self.refresh_button.clicked.connect(self.refresh_click)
        self.forgot_password_button.clicked.connect(self.click)
        self.verification_code.setText(str(self.captcha()))
        self.main_page_button.clicked.connect(self.main_page_click)

    def main_page_click(self):
        stacked_widget.setCurrentIndex(2)

    def click(self):
        if(self.verification_area.text == ""):
            self.verification_area_blank = '<p style="font-size:13pt; color: white;"><b>Verification area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.verification_area_blank)

        if(self.id_area.text() == ""):
            self.id_area_blank = '<p style="font-size:13pt; color: white;"><b>ID area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.id_area_blank)

        if(self.email_area.text() == ""):
            self.email_area_blank = '<p style="font-size:13pt; color: white;"><b>E-Mail area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.email_area_blank)

        if(not self.verification_area.text() == "" and not self.id_area.text() == "" and not self.email_area.text() == ""):
            if(not self.verification_code.text() == self.verification_area.text()):
                self.verification_dont_match = """<p style="font-size:13pt; color: white;"><b>Verification codes don't match...<b/></p>"""
                Register().msgbox.about(self, "Error!", self.verification_dont_match)

            else:
                if(not self.email_area.text().find("@") == -1 and not self.email_area.text().find(".com") == -1):
                    query = "select name from users where id = %s and email = %s"
                    self.con.cursor.execute(query, (self.id_area.text(), self.email_area.text()))
                    self.out = self.con.cursor.fetchall()

                    if(len(self.out) == 0):
                        self.user_dont_exists = """<p style="font-size:13pt; color: white;"><b>User don't exists...<b/></p>"""
                        Register().msgbox.about(self, "Hata!", self.user_dont_exists)
                    else:
                        self.temp_captcha = self.captcha()
                        self.main_text = "The code for reset password is as below.\n                 {}".format(self.temp_captcha)
                        self.sendmail(self.email_area.text(), "Reset Password", self.main_text)
                        self.mail_coming_code = '<p style="font-size:13pt; color: white;"><b>Enter the code sent your E-Mail<b/></p>'
                        self.input_text, self.isOk = self.inputDialog.getText(self, "Veirfication Code", self.mail_gelen_kod)

                        if(self.isOk):
                            if(str(self.temp_captcha) == self.input_text):
                                temp1.setTemp(self.id_area.text())
                                temp1.setEmail(self.email_area.text())
                                stacked_widget.setCurrentIndex(5)
                            else:
                                self.verification_code_wrong = '<p style="font-size:13pt; color: white;"><b>You entered wrong verification code...<b/></p>'
                                Register().msgbox.about(self, "Error!", self.verification_code_wrong)

                        self.verification_code.setText(str(self.captcha()))
                        self.verification_area.setText("")
                        self.id_area.setText("")
                        self.email_area.setText("")

                else:
                    self.not_valid_email = '<p style="font-size:13pt; color: white;"><b>This E-Mail is not valid<b/></p>'
                    Register().msgbox.about(self, "Error!", self.not_valid_email)

    def refresh_click(self):
        self.verification_code.setText(str(self.captcha()))

    def captcha(self):
        number = random.randint(0, 90000000) + 10000000
        return number


class forgotId(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.sendmail = mail1.send
        loadUi("{}forgot_id.ui".format(ui_path), self)
        self.verification_code.setText(str(self.captcha()))
        self.refresh_button.clicked.connect(self.refresh_click)
        self.forgot_id_button.clicked.connect(self.click)
        self.con = connection()
        self.password_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verification_area.setMaxLength(8)
        self.main_page_button.clicked.connect(self.main_page_click)

    def captcha(self):
        number = random.randint(0, 90000000) + 10000000
        return number

    def refresh_click(self):
        self.verification_code.setText(str(self.captcha()))

    def main_page_click(self):
        stacked_widget.setCurrentIndex(2)

    def click(self):

        if(self.password_area.text() == ""):
            self.password_blank = '<p style="font-size:13pt; color: white;"><b>Password area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.password_blank)

        if(self.email_area.text() == ""):
            self.email_blank = '<p style="font-size:13pt; color: white;"><b>E-Mail area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.email_blank)

        if(self.verification_area.text() == ""):
            self.verification_blank = '<p style="font-size:13pt; color: white;"><b>verification area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.verification_blank)

        if(not self.password_area.text() == "" and not self.email_area.text() == "" and not self.verification_area.text() == ""):
            if(self.verification_code.text() == self.verification_area.text()):

                if(not self.email_area.text().find("@") == -1 and not self.email_area.text().find(".com")):
                    query = "select id from users where email = %s"
                    self.con.cursor.execute(query, (self.email_area.text(),))
                    self.control = self.con.cursor.fetchall()
                    if(len(self.control) == 0):
                        self.user_not_found = '<p style="font-size:13pt; color: white;"><b>User not found...<b/></p>'
                        Register().msgbox.about(self, "Error!", self.user_not_found)
                    else:
                        query = "select password from users where email = %s"
                        self.con.cursor.execute(query, (self.email_area.text(),))
                        self.result = self.con.cursor.fetchall()
                        if(not sha256_crypt.verify(self.password_area.text(), self.result[0][0])):
                            self.wrong_password = '<p style="font-size:13pt; color: white;"><b>Wrong Password...<b/></p>'
                            Register().msgbox.about(self, "Error!", self.wrong_password)
                        else:
                            self.main_text = "The id for login to system is as below:\n                 {}".format(self.control[0][0])
                            try:
                                self.sendmail(self.email_area.text(), "Forgot ID", self.main_text)
                                self.mail_sent = '<p style="font-size:13pt; color: white;"><b>Your id is sent to your E-Mail address<b/></p>'
                                Register().msgbox.about(self, "Mail Sent!", self.mail_sent)
                                stacked_widget.setCurrentIndex(2)
                                self.verification_code.setText(str(self.captcha()))
                                self.password_area.setText("")
                                self.verification_area.setText("")
                                self.email_area.setText("")

                            except:
                                self.an_error_mail = '<p style="font-size:13pt; color: white;"><b>An error occured<b/></p>'
                                Register().msgbox.about(self, "Error!", self.an_error_mail)
                        

                    # if(len(self.control) == 0):
                    #     self.user_not_found = '<p style="font-size:13pt; color: white;"><b>User not found...<b/></p>'
                    #     Register().msgbox.about(self, "Error!", self.user_not_found)
                    # else:
                    #     self.main_text = "The id for login to system is as below:\n                 {}".format(self.control[0][0])
                    #     try:
                    #         self.sendmail(self.email_area.text(), "Forgot ID", self.main_text)
                    #         self.mail_sent = '<p style="font-size:13pt; color: white;"><b>Your id is sent to your E-Mail address<b/></p>'
                    #         Register().msgbox.about(self, "Mail Sent!", self.mail_sent)
                    #         stacked_widget.setCurrentIndex(2)
                    #         self.verification_code.setText(str(self.captcha()))
                    #         self.password_area.setText("")
                    #         self.verification_area.setText("")
                    #         self.email_area.setText("")

                    #     except:
                    #         self.an_error_mail = '<p style="font-size:13pt; color: white;"><b>An error occured<b/></p>'
                    #         Register().msgbox.about(self, "Error!", self.an_error_mail)
                else:
                    self.not_valid_email = '<p style="font-size:13pt; color: white;"><b>This E-Mail is not valid<b/></p>'
                    Register().msgbox.about(self, "Error!", self.not_valid_email)
            else:
                self.verification_dont_match = """<p style="font-size:13pt; color: white;"><b>Verifications don't match...<b/></p>"""
                Register().msgbox.about(self, "Hata!", self.dogrulama_uyusmuyor)


class resetPassword(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.sendmail = mail1.send
        loadUi("{}reset_password.ui".format(ui_path), self)
        self.new_password_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.new_repassword_area.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verification_code.setText(str(forgotId().captcha()))
        self.con = connection()
        self.verification_area.setMaxLength(8)
        self.forgot_password_button.clicked.connect(self.click)
        self.refresh_button.clicked.connect(self.refresh_click)

    def refresh_click(self):
        self.dogrulama_kodu.setText(str(forgotId().captcha()))

    def click(self):
        if(self.new_password_area.text() == ""):
            self.password_area_blank = '<p style="font-size:13pt; color: white;"><b>verification_area!<b/></p>'
            Register().msgbox.about(self, "Error!", self.password_area_blanks)

        if(self.new_password_area.text() == ""):
            self.yeni_sifre_tekrar_alani_bos = '<p style="font-size:13pt; color: white;"><b>New password area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.yeni_sifre_tekrar_alani_bos)

        if(self.verification_area.text() == ""):
            self.verification_area_blank = '<p style="font-size:13pt; color: white;"><b>Verification area cannot be blank!<b/></p>'
            Register().msgbox.about(self, "Error!", self.verification_area_blank)

        if(not self.verification_area.text() == "" and not self.new_password_area.text() == "" and not self.new_repassword_area.text() == ""):

            if(self.new_password_area.text() == self.new_repassword_area.text()):
                query = "update users set password = %s where id = %s"
                self.enc_new_password = sha256_crypt.hash(self.new_password_area.text())
                self.con.cursor.execute(query, (self.enc_new_password, temp1.getTemp()))
                self.con.commit()
                self.password_changed = '<p style="font-size:13pt; color: white;"><b>Password successfully changed...<b/></p>'
                self.password_changed_mail = "Your password is successfully changed."
                Register().msgbox.about(self, "Password Changed!", self.password_changed)
                self.sendmail(temp1.getEmail(), "Password Successfully Changed", self.password_changed_mail)
                stacked_widget.setCurrentIndex(2)
            else:
                self.password_dont_match = """<p style="font-size:13pt; color: white;"><b>Passwords don't match...<b/></p>"""
                Register().msgbox.about(self, "Error!", self.password_dont_match)


if __name__ == '__main__':
    temp1 = temp_id()
    mail1 = sendMail()
    mail1.connect()
    app = QtWidgets.QApplication(sys.argv)
    main = Enter()
    forgotid = forgotId()
    register = Register()
    login = Login()
    forgotpassword = forgotPassword()
    resetpassword = resetPassword()
    stacked_widget = QtWidgets.QStackedWidget()

    stacked_widget.addWidget(main)
    stacked_widget.addWidget(register)
    stacked_widget.addWidget(login)
    stacked_widget.addWidget(forgotpassword)
    stacked_widget.addWidget(forgotid)
    stacked_widget.addWidget(resetpassword)

    stacked_widget.setWindowTitle("Login With Python")
    stacked_widget.setWindowIcon(QtGui.QIcon(icon_path))
    stacked_widget.setFixedSize(640, 450)
    stacked_widget.show()

    trayIcon = QtWidgets.QSystemTrayIcon(QtGui.QIcon(icon_path), parent=app)
    trayIcon.setToolTip("Login by sensoyg working...")
    trayIcon.show()
    sys.exit(app.exec_())
