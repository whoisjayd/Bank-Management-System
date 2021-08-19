try:
    import get_pip
    import os
    import random
    import secrets
    import smtplib
    import subprocess
    import sys
    from datetime import date, datetime
    from email.message import EmailMessage
    from time import sleep
except Exception as Error:
    print(Error)


def package_installer(package_name):
    return subprocess.call([sys.executable, "-m", "pip", "install", package_name])


try:
    import mysql.connector
    from tabulate import tabulate
except Exception as e:
    print(e)
    try:
        import pip

        package_installer("mysql-connector-python")
        package_installer("tabulate")
    except Exception as e:
        print(e)
        get_pip.main()
        try:
            import pip

            package_installer("mysql-connector-python")
            package_installer("tabulate")
        except Exception as e:
            print(e)


def log_the_task(USER_BANK_ID, USER_ACCOUNT_ID, NAME, EMAIL, PREV_AMOUNT, NEW_BAL, TASK_PERFORMED,
                 TIMESTAMP=datetime.now().strftime('%I:%M:%S %p  %Y/%m/%d')):
    query_execute = f"INSERT INTO LOGS (USER_BANK_ID,USER_ACCOUNT_ID,NAME,EMAIL,PREV_AMOUNT,NEW_BAL,TASK_PERFORMED,TIMESTAMP) VALUES('{USER_BANK_ID}','{USER_ACCOUNT_ID}','{NAME}','{EMAIL}','{PREV_AMOUNT}','{NEW_BAL}','{TASK_PERFORMED}','{TIMESTAMP}')"
    sql_query(query_execute, "execute")


def call_the_name(y):
    clear()
    a = "\t\t"
    for i in y:
        a += i + " "
    print("=" * (len(a) + 32))
    print(str(a).upper())
    print("=" * (len(a) + 32))


def database_creation():
    conn = mysql.connector.connect(user='root', password='', host='127.0.0.1')
    cursor = conn.cursor()
    sql = "CREATE DATABASE IF NOT EXISTS BANK"
    cursor.execute(sql)
    conn.close()


def welcome():
    clear()

    def table_creation():
        call_the_name("TABLE CREATION PROCEDURE")
        print("\t\tCreating database.. ")
        database_creation()
        sleep(2)
        print("\t\tCreating tables ..")
        table_1 = """CREATE TABLE IF NOT EXISTS USERS(ID INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT,NAME CHAR(20) NOT NULL,EMAIL_ID VARCHAR(40) NOT NULL UNIQUE,DOB VARCHAR(100) NOT NULL,PASSWORD INT(20) NOT NULL,PHONE_NUMBER BIGINT(255) NOT NULL,AADHAAR_NUMBER VARCHAR(50) NOT NULL UNIQUE,GENDER CHAR(20) NOT NULL,REGISTERED_TIMESTAMP VARCHAR(100) NOT NULL )"""
        sql_query(table_1, "execute")
        table_2 = """CREATE TABLE IF NOT EXISTS ACCOUNT_DETAILS(TABLE_ID INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT,ID INT(255) NOT NULL,EMAIL_ID VARCHAR(40) NOT NULL UNIQUE,PASSWORD INT(20) NOT NULL,ACCOUNT_BALANCE BIGINT(255) NOT NULL, ACCOUNT_TYPE CHAR(20) NOT NULL,ACCOUNT_REGISTERED_TIMESTAMP VARCHAR(100))"""
        sql_query(table_2, "execute")
        table_3 = """CREATE TABLE IF NOT EXISTS ADMINS(ID INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT,NAME CHAR(20) NOT NULL,EMAIL VARCHAR(20) NOT NULL UNIQUE,PASSWORD INT(30) NOT NULL)"""
        sql_query(table_3, "execute")
        table_4 = """CREATE TABLE IF NOT EXISTS LOGS(LOG_ID INT(255) NOT NULL PRIMARY KEY AUTO_INCREMENT,USER_BANK_ID INT(255) NOT NULL,USER_ACCOUNT_ID INT(255) NOT NULL,NAME CHAR(20) NOT NULL,EMAIL VARCHAR(20) NOT NULL,PREV_AMOUNT INT(255) NOT NULL,NEW_BAL CHAR(255) DEFAULT 'NOT UPDATED',TASK_PERFORMED TINYTEXT NOT NULL,TIMESTAMP TINYTEXT NOT NULL)"""
        sql_query(table_4, "execute")
        sleep(10)
        print("\t\tBoth Database Tables have been created..")
        print(
            """
                    1. Database :
                        > BANK
                    2. Tables  :
                        > USERS
                        > ACCOUNT_DETAILS
                        > ADMINS
                        > LOGS""")
        sleep(8)

    call_the_name("WELCOME TO URMI BANKING ")

    print("You will find a file named 'secrets.py' ")
    print(
        "Open it and update that file to the credentials,Instructions and helpful links are shared in secrets.py  ...")
    print("\n" * 4)
    input("Press enter to move ahead...")
    table_creation()
    sleep(2)
    print("\t\tCongratulations ! You are ready to go to use this program.")
    sleep(2)
    clear()
    print("\t\tPlease wait initialising program...")
    sleep(2)
    print("\t\tConnecting to the server...")
    sleep(4)
    print("\t\tFinished initialisation...")
    sleep(2)
    clear()
    interface_director()


def sending_otp_to_user(user_email_id_to_send, Function, FUNCTION_TO_DO_IF_CORRECT=False):
    call_the_name("OTP VERIFICATION PROCEDURE")
    send_otp = str(email_verification(user_email_id_to_send, "User"))
    enter_otp = input(f"Please enter otp sent to {user_email_id_to_send}  : ")
    while enter_otp != send_otp:

        print(
            f"The otp entered is not same to which we sent to {user_email_id_to_send}")
        print(
            """Do you want us to send the otp again to
               1. similar email
               2. you want to change email""")
        your_choice = input("Choice [1-2] : ")
        if your_choice == "1":
            call_the_name("OTP VERIFICATION PROCEDURE")
            send_otp = str(email_verification(user_email_id_to_send, "User"))
            enter_otp = input(
                f"Please enter otp sent to {user_email_id_to_send} : ")
        else:
            clear()
            user_register_protocol()

    if enter_otp == send_otp:
        if FUNCTION_TO_DO_IF_CORRECT is not False:
            clear()
            print("Email successfully verified you can now proceed ahead.")
            sleep(5)
            Function(user_email_id_to_send)
        else:
            clear()
            print("Email successfully verified you can now proceed ahead.")
            sleep(5)
            Function()


def raise_error(function_name_to_call=None):
    clear()
    print("We found some error.")
    print("Please wait running the program again.")
    print("Make sure to do as directed...")
    sleep(5)
    clear()
    if function_name_to_call is not None:
        function_name_to_call()


def sql_query(query, function, password="", dbname="bank"):
    db = mysql.connector.connect(
        host="localhost", user="root", password=password, database=dbname)
    try:
        cursor = db.cursor()
        if function == "execute":
            cursor.execute(query)
            db.commit()
            db.close()
        elif function == "extract":
            cursor.execute(query)
            return cursor.fetchall()
    except Exception as error:

        clear()
        print(error)
        print("Error in sql_query")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")


def message_content_send(email, r_name, r_email, main_otp):
    msg_content = EmailMessage()
    msg_content['Subject'] = f'Your otp for Urmi Bank is {main_otp}'
    msg_content['From'] = email
    msg_content['To'] = r_email
    msg_content.set_content(
        """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xmlns:o="urn:schemas-microsoft-com:office:office" style="font-family:'merriweather sans', 'helvetica neue', helvetica, arial, sans-serif"><head><meta charset="UTF-8"><meta name="x-apple-disable-message-reformatting"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta content="telephone=no" 
        name="format-detection"><title>VerificationMain</title> <!--[if (mso 16)]><style type="text/css">     a {text-decoration: none;}     </style><![endif]--> <!--[if gte mso 9]><style>sup { font-size: 100% !important; }</style><![endif]--> <!--[if gte mso 9]><xml> <o:OfficeDocumentSettings> <o:AllowPNG></o:AllowPNG> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml><![endif]--> <!--[if !mso]><!-- --><link href="https://fonts.googleapis.com/css?family=Merriweather:400,
        400i,700,700i" rel="stylesheet"><link href="https://fonts.googleapis.com/css?family=Merriweather+Sans:400,400i,700,700i" rel="stylesheet"><link href="https://fonts.googleapis.com/css2?family=Montserrat&display=swap" rel="stylesheet"> <!--<![endif]--><style type="text/css">.rollover div {	font-size:0;}#outlook a {	padding:0;}.es-button {	mso-style-priority:100!important;	text-decoration:none!important;}a[x-apple-data-detectors] {	color:inherit!important;	
        text-decoration:none!important;	font-size:inherit!important;	font-family:inherit!important;	font-weight:inherit!important;	line-height:inherit!important;}.es-desk-hidden {	display:none;	float:left;	overflow:hidden;	width:0;	max-height:0;	line-height:0;	mso-hide:all;}[data-ogsb] .es-button {	border-width:0!important;	padding:10px 30px 10px 30px!important;}</style></head> <body style="width:100%;font-family:'merriweather sans', 'helvetica neue', helvetica, arial, 
        sans-serif;-webkit-text-size-adjust:100%;-ms-text-size-adjust:100%;padding:0;Margin:0"><div class="es-wrapper-color" style="background-color:#C8ABAB"> <!--[if gte mso 9]><v:background xmlns:v="urn:schemas-microsoft-com:vml" fill="t"> <v:fill type="tile" src="https://lwgjqe.stripocdn.email/content/guids/CABINET_f17b7d3e2c12d21089d2b900057266f6/images/85441627530954154.jpg" color="#c8abab"></v:fill> </v:background><![endif]--><table class="es-wrapper" width="100%" cellspacing="0" 
        cellpadding="0" background="https://lwgjqe.stripocdn.email/content/guids/CABINET_f17b7d3e2c12d21089d2b900057266f6/images/85441627530954154.jpg" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;padding:0;Margin:0;width:100%;height:100%;background-image:url(https://lwgjqe.stripocdn.email/content/guids/CABINET_f17b7d3e2c12d21089d2b900057266f6/images/85441627530954154.jpg);background-repeat:no-repeat;background-position:left top"><tr 
        class="gmail-fix" height="0"><td style="padding:0;Margin:0"><table cellpadding="0" cellspacing="0" border="0" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;width:760px"><tr><td cellpadding="0" cellspacing="0" border="0" height="0" style="padding:0;Margin:0;line-height:1px;min-width:760px"><img src="https://lwgjqe.stripocdn.email/content/guids/CABINET_837dc1d79e3a5eca5eb1609bfe9fd374/images/41521605538834349.png" width="760" 
        height="1" style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic;max-height:0px;min-height:0px;min-width:760px;width:760px" alt></td> </tr></table></td> </tr><tr><td valign="top" style="padding:0;Margin:0"><table cellpadding="0" cellspacing="0" class="es-content" align="center" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;table-layout:fixed !important;width:100%"><tr><td align="center" 
        style="padding:0;Margin:0"><table bgcolor="#ffffff" class="es-content-body" align="center" cellpadding="0" cellspacing="0" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px;background-color:#FFFFFF;background-repeat:no-repeat;width:760px;background-image:url(https://lwgjqe.stripocdn.email/content/guids/CABINET_f17b7d3e2c12d21089d2b900057266f6/images/33381627296428601.png);background-position:left top" 
        background="https://lwgjqe.stripocdn.email/content/guids/CABINET_f17b7d3e2c12d21089d2b900057266f6/images/33381627296428601.png"><tr><td align="left" style="padding:0;Margin:0"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" valign="top" style="padding:0;Margin:0;width:760px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" 
        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" style="padding:0;Margin:0;padding-bottom:5px;padding-left:10px;padding-top:15px;font-size:0px"><img src="https://img.icons8.com/bubbles/2x/fa314a/gmail.png" alt style="display:block;border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic" width="114"></td> </tr><tr><td align="center" style="padding:0;Margin:0"><h1 
        style="Margin:0;line-height:46px;mso-line-height-rule:exactly;font-family:'merriweather sans', 'helvetica neue', helvetica, arial, sans-serif;font-size:38px;font-style:normal;font-weight:normal;color:#000000;margin-bottom:42px;text-align:center"><strong>OTP VERIFICATION</strong></h1></td></tr></table></td></tr></table></td> </tr><tr><td align="left" style="padding:0;Margin:0;padding-left:20px;padding-right:20px"><table cellpadding="0" cellspacing="0" width="100%" 
        style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" valign="top" style="padding:0;Margin:0;width:720px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" style="padding:0;Margin:0"><p 
        style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:montserrat, sans-serif;line-height:27px;margin-bottom:12px;color:#000000;font-size:18px">Hi, """ + r_name + """<br>Your otp for email :<br>""" + r_email + """<br>is&nbsp;</p></td> 
                                </tr><tr><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'merriweather sans', 'helvetica neue', helvetica, arial, sans-serif;line-height:42px;margin-bottom:12px;color:#333333;font-size:28px"><strong>""" + main_otp + """</strong></p></td></tr></table></td></tr></table></td> </tr><tr><td align="left" 
                                style="Margin:0;padding-top:25px;padding-left:35px;padding-right:35px;padding-bottom:40px"><table cellpadding="0" cellspacing="0" width="100%" style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" valign="top" style="padding:0;Margin:0;width:690px"><table cellpadding="0" cellspacing="0" width="100%" role="presentation" 
                                style="mso-table-lspace:0pt;mso-table-rspace:0pt;border-collapse:collapse;border-spacing:0px"><tr><td align="center" style="padding:0;Margin:0"><p style="Margin:0;-webkit-text-size-adjust:none;-ms-text-size-adjust:none;mso-line-height-rule:exactly;font-family:'merriweather sans', 'helvetica neue', helvetica, arial, sans-serif;line-height:18px;margin-bottom:12px;color:#333333;font-size:12px"><strong>CONTACT:</strong><br><strong><font face="merriweather sans, 
                                helvetica neue, helvetica, arial, sans-serif" style="font-size:12px">""" + email + """</font></strong><br><strong><font style="font-size:12px">Urmi School</font></strong><br><font style="font-size:12px"><strong>&nbsp;Mysql Project</strong></font><br><br><br>If you receive this&nbsp;<strong>mail&nbsp;</strong>without using this&nbsp;<strong>program&nbsp;</strong>,sorry for that as the user using this program might have entered&nbsp;<strong>wrong mail</strong>.</p> 
                                </td></tr></table></td></tr></table></td></tr></table></td></tr></table></td></tr></table></div></body></html>
                                """, subtype='html')
    return msg_content


def email_verification(receiver_email, receiver_name):
    try:
        sender_email = secrets.email()
        sender_email_password = secrets.email_password()

        def otp():
            main_otp = ""
            for _ in range(4):
                otp_1 = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
                main_otp += str(otp_1[0])
            return main_otp

        otp_is = otp()
        msg = message_content_send(
            sender_email, receiver_name, receiver_email, otp_is)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_email_password)
            smtp.send_message(msg)
        return otp_is
    except:
        clear()
        print("Error in email_verification")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(interface_director)


def clear(number_of_lines=50):
    for _ in range(number_of_lines):
        print("\n")


def login_interface():
    clear()
    print("=" * 30)
    print("\t  L O G I N")
    print("=" * 30)
    print(
        """
    1. User Interface
    2. Admin Interface""")
    print("_" * 30)
    return input("""Choice [1 or 2] : """)


def interface_director():
    try:
        login = login_interface()
        if login == "1":
            user_main_interface_director()
        elif login == "2":
            admin_main_interface_director()
    except:
        clear()
        print("Error in interface_director")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(interface_director)


"""USER INTERFACE FUNCTIONS STARTS FROM HERE"""


def user_main_interface():
    clear()
    try:
        call_the_name("user interface")
        print(
            """
        1. Login
        2. Register
        3. Delete
        4. Update
        5. Quit""")
        print("_" * 30)
        return input("""Choice [1 or 2 or 3 or 4 or 5] : """)
    except:
        clear()
        print("Error in user_main_interface")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_main_interface_director)


def user_main_interface_director():
    clear()
    try:
        user_inter = user_main_interface()
        if user_inter == "1":
            user_login_protocol()
        elif user_inter == "2":
            user_register_protocol()
        elif user_inter == "3":
            user_delete_protocol()
        elif user_inter == "4":
            user_update_protocol()
        elif user_inter == "5":
            clear()
            interface_director()
    except:
        clear()
        print("Error in user_main_interface_director")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_main_interface_director)


def user_login_protocol():
    clear()
    try:
        call_the_name("LOGIN PAGE")
        user_email = input("Please type your registered email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email not in user_email_fetch_list:
            print(
                "Seems email is not registered you can not login without registering .")
            sleep(5)
            user_main_interface_director()
        else:
            user_id = int(input("Please enter user id : "))
            user_password = int(input("Please type your password: "))
            user_auth_query = f"SELECT EMAIL_ID,PASSWORD,NAME FROM USERS WHERE ID={user_id}"
            user_auth_execute = sql_query(user_auth_query, "extract")
            if user_auth_execute[0][0] == user_email and user_auth_execute[0][1] == user_password:
                clear()
                print(f"Successfully logged in as {user_auth_execute[0][2]}")
                sleep(2)
                clear()
                print(f"Welcome {user_auth_execute[0][2]}")
                print("Redirecting to your user choices page .")
                log_the_task(user_id, 0, user_auth_execute[0][2], user_email, 0, 0, f"USER LOGIN SUCCESSFULLY")
                sleep(5)
                account_main_interface_director()
            else:
                print("Invalid Credentials")
                user_login_protocol()
    except:
        clear()
        print("Error in user_login_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_login_protocol)


def user_update_process_start_choices():
    clear()
    call_the_name("UPDATE CHOICES PAGE")
    try:
        print(
            """
        1.Username
        2.Email
        3.Date Of Birth
        4.Password
        5.PhoneNumber
        6.Aadhaar Number
        7.Gender""")
        print("Choose only that you want to update.")
        print("Please give in format of 1,2,3,4,5,6")

        return input("Please enter you choices: ").split(",")
    except:
        clear()
        print("Error in user_update_process_start_choices")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_update_process_start)


def convertor_list_to_sql_string(changes_to_made):
    try:
        converted = ""
        for i in range(len(changes_to_made)):
            converted += changes_to_made[i]
            if i < len(changes_to_made) - 1:
                converted += ","
        return converted
    except:
        clear()
        print("Error in convertor_list_to_sql_string")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")


def user_update_process_start():
    clear()
    try:
        call_the_name("UPDATE PROCEDURE")
        change = []
        list_of_changes = user_update_process_start_choices()
        list_of_changes.append(" ")
        sleep(3)
        clear()
        dictionary = {"1": "NAME", "2": "EMAIL_ID", "3": " DOB", "4": "PASSWORD", "5": "PHONE_NUMBER",
                      "6": "AADHAAR_NUMBER", "7": "GENDER", " ": " "}
        if str(dictionary[list_of_changes[0]]) == "NAME":
            user_name = input("Please enter your new name : ")
            change.append(
                str(dictionary[list_of_changes[0]]) + "='" + str(user_name) + "'")
            list_of_changes.remove("1")

        if str(dictionary[list_of_changes[0]]) == "EMAIL_ID":
            user_email = input("Please enter your new email: ")
            change.append(
                str(dictionary[list_of_changes[0]]) + "='" + str(user_email) + "'")
            list_of_changes.remove("2")

        if str(dictionary[list_of_changes[0]]) == "DOB":
            user_dob = int(input("Please type your new Date of birth: "))
            change.append(
                str(dictionary[list_of_changes[0]]) + "='" + str(user_dob) + "'")
            list_of_changes.remove("3")

        if str(dictionary[list_of_changes[0]]) == "PASSWORD":
            user_password = int(input("Please type your new password: "))
            while len(str(user_password)) < 4 or len(str(user_password)) > 18:
                print("Range for password is 4-18 and that must be integer value.")
                user_password = int(input("Please type your new password: "))
            change.append(
                str(
                    dictionary[list_of_changes[0]]) + "='" + str(user_password) + "'")
            list_of_changes.remove("4")

        if str(dictionary[list_of_changes[0]]) == "PHONE_NUMBER":
            user_phone = input("Please type your phone new number: ")
            while len(user_phone) != 10:
                print("Please  enter valid phone number.")
                user_phone = input("Please type your new phone number: ")
            change.append(
                str(dictionary[list_of_changes[0]]) + "='" + str(user_phone) + "'")
            list_of_changes.remove("5")

        if str(dictionary[list_of_changes[0]]) == "AADHAAR_NUMBER":
            user_aadhaar = input("Please enter your new aadhaar number: ")
            while len(user_aadhaar) != 14:
                print(
                    "Please enter valid aadhaar.It should be in 'xxxx-xxxx-xxxx' format")
                user_aadhaar = input("Please enter your new aadhaar number: ")
            change.append(
                str(
                    dictionary[list_of_changes[0]]) + "='" + str(user_aadhaar) + "'")
            list_of_changes.remove("6")

        if str(dictionary[list_of_changes[0]]) == "GENDER":
            user_gender = input("Please enter your gender: ")
            change.append(
                str(dictionary[list_of_changes[0]]) + "='" + str(user_gender) + "'")
            list_of_changes.remove("7")

        return convertor_list_to_sql_string(change)
    except:
        clear()
        print("Error in user_update_process_start")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_update_process_start)


def user_update_process(user_email_id):
    clear()
    try:
        call_the_name("UPDATE AUTHENTICATION")
        user_password = int(input("Please type your password: "))
        user_auth_query = f"SELECT PASSWORD,NAME,ID FROM USERS WHERE EMAIL_ID='{user_email_id}'"
        user_auth_execute = sql_query(user_auth_query, "extract")
        if user_auth_execute[0][0] == user_password:
            print(
                f"Successfully authenticated as {user_auth_execute[0][1]}")
            print("Update process starting in few seconds")
            sleep(5)
            clear()
            change_is_given = user_update_process_start()
            sleep(1)
            clear()
            print("Okay wait processing your changes and updating it.")
            query_for_update = f"UPDATE USERS SET {change_is_given} WHERE EMAIL_ID='{user_email_id}'"
            sql_query(query_for_update, "execute")
            sleep(1)
            log_the_task(user_auth_execute[0][2], 0, user_auth_execute[0][1], user_email_id, 0, 0,
                         f"USER DETAILS UPDATED SUCCESSFULLY")
            print("Successfully updated your details.")
            print("Wait going to user choices.")
            sleep(4)
            clear()
            user_main_interface_director()
    except:
        clear()
        print("Error in user_update_process")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")


def user_update_protocol():
    clear()
    try:
        call_the_name("UPDATE EMAIL AUTHENTICATION")
        user_email = input("Please type your registered email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email not in user_email_fetch_list:
            print(
                "Seems email is not registered you can not login without registering .")
            sleep(5)
            user_main_interface_director()

        else:
            sending_otp_to_user(
                user_email, user_update_process, True)
    except:
        clear()
        print("Error in user_update_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_update_protocol)


def user_register_process(email):
    clear()
    try:
        call_the_name("REGISTRATION PAGE")
        user_email = email
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        while user_email in user_email_fetch_list:
            print("Duplicate Entry For Your Email ID ")
            user_email = input("Please enter email address: ")
            user_email_fetch = sql_query(user_email_fetch_query, "extract")
            user_email_fetch_list = [i[0] for i in user_email_fetch]
        user_name = input("Please enter your name : ")
        user_dob = input("Please enter your Date of birth: ")
        user_password = int(input("Please type your password: "))
        while len(str(user_password)) < 4 or len(str(user_password)) > 18:
            print("Range for password is 4-18 and that must be integer value.")
            user_password = int(input("Please type your password: "))
        user_phone = input("Please type your phone number: ")
        while len(user_phone) != 10:
            print("Please  enter valid phone number.")
            user_phone = input("Please type your phone number: ")
        user_aadhaar = input("Please enter your aadhaar number: ")
        while len(user_aadhaar) != 14:
            print("Please enter valid aadhaar.It should be in 'xxxx-xxxx-xxxx' format")
            user_aadhaar = input("Please enter your aadhaar number: ")
        user_gender = input("Please enter your gender: ")
        user_auth_query = f"INSERT INTO USERS (NAME, EMAIL_ID,DOB,PASSWORD,PHONE_NUMBER,AADHAAR_NUMBER,GENDER,REGISTERED_TIMESTAMP) VALUES('{user_name}', '{user_email}','{user_dob}', '{user_password}','{user_phone}', '{user_aadhaar}','{user_gender}', '{datetime.now().strftime('%I:%M:%S %p  %Y/%m/%d')}')"
        sql_query(user_auth_query, "execute")
        auth_selection_query = f"SELECT ID FROM USERS WHERE EMAIL_ID='{user_email}'"
        auth_selection_execute = sql_query(
            auth_selection_query, "extract")
        print(
            f"Successfully registered as {user_name} having email {user_email} and password {user_password}")
        print(f"Your user id is {auth_selection_execute[0][0]}")
        print("Remember this user id it will be used in the user confirmation.")
        print("Redirecting to your user choices page.")
        log_the_task(auth_selection_execute[0][0], 0, user_name, user_email, 0, 0, f"USER REGISTRATION SUCCESSFULLY")
        sleep(5)
        account_main_interface_director()
    except:
        clear()
        print("Error in user_register_process")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_register_process)


def user_register_protocol():
    clear()
    try:
        call_the_name("REGISTRATION AUTH PROTOCOL")
        print("We will send otp to the email you provide below so make sure you enter valid email id.")
        user_email_id = input("Please type your email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email_id in user_email_fetch_list:
            print(
                "Seems email is already registered you can not register again with same email.")
            sleep(5)
            user_main_interface_director()
        else:
            sending_otp_to_user(
                user_email_id, user_register_process, True)
    except:
        clear()
        print("Error in user_register_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_register_protocol)


def user_delete_process(user_email):
    clear()
    try:
        call_the_name("DELETE CONFORMATION FROM USER")
        print(
            f"""
            Make sure this will delete all accounts associated with your email id.
    
            Are you sure you want to delete?
    
            1. Delete all accounts associated with {user_email}
            2. Quit deletion process""")
        confirmation = input("Choice [1-2] : ")
        if confirmation == "1":
            user_bank_id = input("Please enter your user bank id: ")
            user_password = int(input("Please type your password: "))
            user_auth_query = f"SELECT PASSWORD,NAME FROM USERS WHERE EMAIL_ID='{user_email}'"
            user_auth_execute = sql_query(user_auth_query, "extract")
            if user_auth_execute[0][0] == user_password:
                print("Deleting all accounts associated with your email id...")
                print(
                    f"Deleting all accounts associated with name {user_auth_execute[0][1]}")
                delete_query_from_bank = f"DELETE FROM USERS WHERE ID={user_bank_id}"
                delete_query_from_accounts = f"DELETE FROM ACCOUNT_DETAILS WHERE ID={user_bank_id}"
                sql_query(delete_query_from_accounts, "execute")
                sql_query(delete_query_from_bank, "execute")
                print("Deleted all accounts associated with your email id...")
                print("Logging you out...")
                log_the_task(user_bank_id, 0, user_auth_execute[0][1], user_email, 0, 0, f"USER DELETED SUCCESSFULLY")
                sleep(5)
                interface_director()

        else:
            user_main_interface_director()
    except:
        clear()
        print("Error in user_delete_process")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_delete_process)


def user_delete_protocol():
    clear()
    try:
        call_the_name("EMAIL VERIFICATION PAGE")

        print("We will send otp to the email you provide below so make sure you enter valid email id.")
        user_email_id = input(
            "Please type your email address of your account that you want to delete: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email_id not in user_email_fetch_list:
            print(
                "Seems email is already deleted you can not delete the email that does not exist in the database.")
            sleep(5)
            interface_director()
        else:
            sending_otp_to_user(
                user_email_id, user_delete_process, True)
    except:
        clear()
        print("Error in user_delete_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_delete_protocol)


"""USER INTERFACE FUNCTIONS ENDS FROM HERE"""

"""ACCOUNT INTERFACE FUNCTIONS STARTS FROM HERE"""


def choices_main_interface():
    clear()
    try:
        call_the_name("USER ACCOUNT INTERFACE")
        print(
            """
        1. Deposit
        2. Withdraw
        3. Transfer
        4. Quit
        """)
        print("_" * 30)
        return input("""Choice [1 or 2 or 3 or 4 or 5] : """)

    except:
        clear()
        print("Error in choices_main_interface")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choices_main_interface_director)


def choices_main_interface_director():
    clear()
    try:
        user_acc_inter = choices_main_interface()
        if user_acc_inter == "1":
            choice_deposit()
        elif user_acc_inter == "2":
            choice_withdraw_protocol()
        elif user_acc_inter == "3":
            choice_transfer_protocol()
        elif user_acc_inter == "4":
            clear()
            account_main_interface_director()
    except:
        clear()
        print("Error in choices_main_interface_director")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choices_main_interface_director)


def choice_deposit():
    clear()
    call_the_name("MONEY DEPOSIT PAGE")
    try:
        bank_id = int(input("Please enter bank account id: "))
        bank_password = input("Please enter bank password: ")
        extract_query_perform = f"SELECT ID,PASSWORD,ACCOUNT_BALANCE,EMAIL_ID FROM ACCOUNT_DETAILS WHERE TABLE_ID={bank_id}"
        extract_query = sql_query(extract_query_perform, "extract")
        if extract_query[0][2] > 5000 and str(extract_query[0][1]) == bank_password:
            dep_money = int(
                input("Hi user please specify amount to deposit: "))
            updated_bal = int(dep_money) + int(extract_query[0][2])
            update_query = f"UPDATE ACCOUNT_DETAILS SET ACCOUNT_BALANCE='{updated_bal}' WHERE TABLE_ID={bank_id}"
            sql_query(update_query, "execute")
            sleep(5)
            clear()
            log_the_task(extract_query_perform[0][0], bank_id, "User", extract_query_perform[0][3],
                         extract_query[0][2], updated_bal, f"MONEY DEPOSITED SUCCESSFULLY")
            print(
                f"Account balance of account having id {bank_id} successfully updated")
            print(
                f"Earlier it was {extract_query[0][2]} , After depositing {dep_money} you have {updated_bal} in your bank account.")
            sleep(5)
            clear()
            choices_main_interface_director()
        elif extract_query[0][2] < 5000 or str(extract_query[0][1]) != bank_password:
            clear()
            print("You are not eligible to deposit money .")
            sleep(3)
            print("Closing connection to bank")
            sleep(5)
            clear()
            choices_main_interface_director()
    except:
        clear()
        print("Error in choice_deposit")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choice_deposit)


def choice_withdraw_processor():
    clear()
    try:
        call_the_name("MONEY WITHDRAW PAGE ")
        bank_id = input("Please enter your user bank id: ")
        user_password = int(input("Please type your password: "))

        extract_query_perform = f"SELECT ID,PASSWORD,ACCOUNT_BALANCE,EMAIL_ID FROM ACCOUNT_DETAILS WHERE TABLE_ID={bank_id}"
        extract_query = sql_query(extract_query_perform, "extract")
        if extract_query[0][2] > 5000 and str(extract_query[0][1]) == str(user_password):
            with_money = int(
                input("Hi user please specify amount to withdraw: "))
            updated_bal = int(extract_query[0][2]) - int(with_money)
            if updated_bal < 0 and updated_bal < 5000:
                print("You have insufficient money to withdraw...")
                print("Please deposit money to withdraw money..")
                print("Redirecting to your account choices page.")
                sleep(5)
                clear()
                choices_main_interface_director()
            elif updated_bal > 0 and updated_bal > 5000:
                update_query = f"UPDATE ACCOUNT_DETAILS SET ACCOUNT_BALANCE='{updated_bal}' WHERE TABLE_ID={bank_id}"
                sql_query(update_query, "execute")
                sleep(5)
                clear()

                print(
                    f"Account balance of account having id {bank_id} successfully updated")
                print(
                    f"Earlier it was {extract_query[0][2]} , After withdrawing {with_money} you have {updated_bal} in your bank account.")
                sleep(5)
                log_the_task(extract_query_perform[0][0], bank_id, "User", extract_query_perform[0][3],
                             extract_query[0][2], updated_bal, f"MONEY WITHDRAWN SUCCESSFULLY")
                choices_main_interface_director()
        elif extract_query[0][2] < 5000 or str(extract_query[0][1]) != user_password:
            clear()
            print("You are not eligible to withdraw money .")
            sleep(3)
            print("Closing connection to bank")
            sleep(5)
            clear()
            choices_main_interface_director()
    except:
        clear()
        print("Error in choice_withdraw_processor")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choice_withdraw_processor)


def choice_withdraw_protocol():
    clear()
    call_the_name("WITHDRAW AUTH PAGE")
    try:
        print("We will send otp to the email you provide below so make sure you enter valid email id.")
        user_email_id = input(
            "Please type your email address : ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM ACCOUNT_DETAILS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email_id not in user_email_fetch_list:
            print(
                "Seems email is not registered you can not withdraw from the account that does not exist in the database.")
            sleep(5)
            interface_director()
        else:
            sending_otp_to_user(
                user_email_id, choice_withdraw_processor, False)
    except:
        clear()
        print("Error in choice_withdraw_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choice_withdraw_protocol)


def choice_transfer_processor():
    clear()
    try:
        call_the_name("TRANSFER PROTOCOL PAGE")
        user_bank_id = int(
            input("Enter your user bank id from which you want to transfer money: "))
        user_get_bank_id = int(
            input("Enter the bank id of whom you want to transfer money : "))
        amount_to_transfer = int(
            input("Enter the amount you want to transfer :"))
        user_password = input("Enter you bank password to confirm transfer: ")

        user_query = f"SELECT PASSWORD,ACCOUNT_BALANCE,EMAIL_ID,ID FROM ACCOUNT_DETAILS WHERE TABLE_ID={user_bank_id}"
        user_extracted_data = sql_query(user_query, "extract")
        user_get_query = f"SELECT ACCOUNT_BALANCE,EMAIL_ID,ID FROM ACCOUNT_DETAILS WHERE TABLE_ID={user_get_bank_id}"
        user_get_extracted_data = sql_query(user_get_query, "extract")
        user_updated_bal = int(
            user_extracted_data[0][1]) - int(amount_to_transfer)
        user_get_updated_bal = int(
            user_get_extracted_data[0][0]) + int(amount_to_transfer)
        if str(user_extracted_data[0][0]) == str(user_password) and user_extracted_data[0][1] > 5000 and user_updated_bal > 2000:
            print(
                f"Transferring money to  account having id {user_get_bank_id} from your account having id {user_bank_id}")
            user_update_query = f"UPDATE ACCOUNT_DETAILS SET ACCOUNT_BALANCE='{user_updated_bal}' WHERE TABLE_ID={user_bank_id}"
            user_get_update_query = f"UPDATE ACCOUNT_DETAILS SET ACCOUNT_BALANCE='{user_get_updated_bal}' WHERE TABLE_ID={user_get_bank_id}"
            sql_query(user_update_query, "execute")
            sql_query(user_get_update_query, "execute")
            print(
                f"Your balance after transferring {amount_to_transfer} is {user_updated_bal}")
            print("Successfully transferred money !!")
            log_the_task(user_query[0][3], user_bank_id, "User", user_query[0][2], user_query[0][1], user_updated_bal,
                         f"MONEY TRANSFERRED SUCCESSFULLY TO {user_get_bank_id}")
            log_the_task(user_get_query[0][2], user_get_bank_id, "User", user_get_query[0][1], user_get_query[0][0],
                         user_get_updated_bal, f"MONEY RECEIVED SUCCESSFULLY FROM {user_bank_id}")
            sleep(5)
            choices_main_interface_director()
        else:
            print("Invalid Credentials or Insufficient balance..")
            choice_transfer_processor()
    except:
        clear()
        print("Error in choice_transfer_processor")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choice_transfer_processor)


def choice_transfer_protocol():
    clear()
    call_the_name("TRANSFER PAGE AUTHENTICATION")
    try:
        print("We will send otp to the email you provide below so make sure you enter valid email id.")
        user_email_id = input(
            "Please type your email address that you have registered: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email_id not in user_email_fetch_list:
            print(
                "Seems email is already deleted you can not delete the email that does not exist in the database.")
            sleep(5)
            interface_director()
        else:
            sending_otp_to_user(
                user_email_id, choice_transfer_processor, False)
    except:
        clear()
        print("Error in choice_transfer_protocol")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(choice_transfer_protocol)


def account_main_interface():
    clear()
    try:
        call_the_name("USER ACCOUNT INTERFACE")
        print(
            """
        1. Login
        2. Register
        3. Delete
        4. Quit""")
        print("_" * 30)
        return input("""Choice [1 or 2 or 3 or 4] : """)
    except:
        clear()
        print("Error in account_main_interface")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(account_main_interface_director)


def account_main_interface_director():
    clear()
    try:
        user_acc_inter = account_main_interface()
        if user_acc_inter == "1":
            account_user_login()
        elif user_acc_inter == "2":
            account_user_register()
        elif user_acc_inter == "3":
            user_account_delete()
        elif user_acc_inter == "4":
            clear()
            interface_director()
    except:
        clear()
        print("Error in account_main_interface_director")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(account_main_interface_director)


def user_account_delete():
    clear()
    try:
        call_the_name("USER ACCOUNT DELETE")
        user_email = input("Please type your registered email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email not in user_email_fetch_list:
            print(
                "Seems email is not registered you can not delete without registering .")
            sleep(5)
            user_main_interface_director()
        else:
            print(
                f"""
                    Make sure this will delete all accounts associated with your email id.

                    Are you sure you want to delete?

                    1. Delete  account associated with {user_email}
                    2. Quit deletion process""")
            confirmation = input("Choice [1-2] : ")
            if confirmation == 1:
                print("Email Id : ", user_email)
                user_id = int(input("Please enter bank id that you want to : "))
                user_password = int(input("Please type bank password: "))
                user_auth_query = f"SELECT EMAIL_ID,PASSWORD,ID,ACCOUNT_BALANCE FROM ACCOUNT_DETAILS WHERE TABLE_ID={user_id}"
                user_auth_execute = sql_query(user_auth_query, "extract")
                if user_auth_execute[0][0] == user_email and user_auth_execute[0][1] == user_password:
                    print(
                        f"Deleting your account having Bank id : '{user_id}' and Name : {user_auth_execute[0][2]}")
                    delete_query = f"DELETE FROM ACCOUNT_DETAILS WHERE TABLE_ID={user_id}"
                    sql_query(delete_query, "execute")
                    print("Account deleted successfully.")
                    sleep(5)
                    log_the_task(user_auth_execute[0][2], user_id, "User", user_auth_execute[0][0],
                                 user_auth_execute[0][3], user_auth_execute[0][3], f"BANK ACCOUNT DELETED SUCCESSFULLY")
                    clear()
                    account_main_interface_director()

                else:
                    print("Invalid Credentials")
                    user_account_delete()
            else:
                account_main_interface_director()
    except:
        clear()
        print("Error in user_account_delete")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(user_account_delete)


def account_user_login():
    clear()
    try:
        call_the_name("USER LOGIN PAGE")
        user_email = input("Please type your registered email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM ACCOUNT_DETAILS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email not in user_email_fetch_list:
            print(
                "Seems email is not registered you can not login without registering .")
            sleep(5)
            user_main_interface_director()
        else:
            user_id = int(input("Please enter bank id : "))
            user_password = int(input("Please type bank password: "))
            user_auth_query = f"SELECT EMAIL_ID,PASSWORD,ID,ACCOUNT_BALANCE FROM ACCOUNT_DETAILS WHERE TABLE_ID={user_id}"
            user_auth_execute = sql_query(user_auth_query, "extract")
            if user_auth_execute[0][0] == user_email and user_auth_execute[0][1] == user_password:
                clear()
                print(
                    f"Successfully logged in to bank account ")
                sleep(2)
                print(f"Welcome User !")
                print("Redirecting to your user choices page .")
                sleep(5)
                log_the_task(user_auth_execute[0][2], user_id, "User", user_auth_execute[0][0], user_auth_execute[0][3],
                             user_auth_execute[0][3], f"BANK ACCOUNT LOGIN IN SUCCESSFULLY")
                choices_main_interface_director()
            else:
                print("Invalid Credentials")
                account_user_login()
    except:
        clear()
        print("Error in account_user_login")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(account_user_login)


def account_user_register_process(user_email):
    clear()
    try:
        call_the_name("USER REGISTRATION PAGE")
        print("=" * 50)
        print("\t  A C C O U N T  R E G I S T E R  I N T E R F A C E")
        print("=" * 50)
        user_password = int(input("Please type your password: "))
        while len(str(user_password)) < 4 or len(str(user_password)) > 18:
            print("Range for password is 4-18 and that must be integer value.")
            user_password = int(input("Please type your password: "))
        user_acc_type = input("Please type your account type : ")
        user_start_bal = int(input("Please enter you starting balance: "))
        user_bank_id = int(input("Please enter your bank id :"))

        query = f"INSERT INTO ACCOUNT_DETAILS (ID,EMAIL_ID,PASSWORD,ACCOUNT_TYPE,ACCOUNT_BALANCE,ACCOUNT_REGISTERED_TIMESTAMP) VALUES ({user_bank_id},'{user_email}','{user_password}','{user_acc_type}','{user_start_bal}','{datetime.now().strftime('%I:%M:%S %p  %Y/%m/%d')}')"
        sql_query(query, "execute")
        print("Account Successfully registered..")
        auth_selection_query = f"SELECT TABLE_ID FROM ACCOUNT_DETAILS WHERE PASSWORD='{user_password}'"
        auth_selection_execute = sql_query(
            auth_selection_query, "extract")
        print(
            f"Successfully registered  bank account having email {user_email}")
        print(f"Your user bank id is {auth_selection_execute[0][0]}")

        print("Remember this bank id it will be used in the bank account confirmation.")
        print("Redirecting to your user choices page.")
        sleep(5)
        log_the_task(auth_selection_execute[0][0], user_bank_id, "User", user_email, user_start_bal, user_start_bal,
                     f"BANK ACCOUNT REGISTERED SUCCESSFULLY")
        choices_main_interface_director()
    except:
        clear()
        print("Error in account_user_register_process")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(account_user_register_process)


def account_user_register():
    clear()
    try:
        call_the_name("USER ACCOUNT AUTH PAGE")
        print("We will send otp to the email you provide below so make sure you enter valid email id.")
        user_email_id = input("Please type your email address: ")
        user_email_fetch_query = "SELECT EMAIL_ID FROM USERS"
        user_email_fetch = sql_query(user_email_fetch_query, "extract")
        user_email_fetch_list = [i[0] for i in user_email_fetch]

        if user_email_id not in user_email_fetch_list:
            print(
                "Seems email is already registered you can not register again with same email.")
            sleep(5)
            user_main_interface_director()
        else:
            sending_otp_to_user(
                user_email_id, account_user_register_process, True)
    except:
        clear()
        print("Error in account_user_register")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(account_user_register)


"""ACCOUNT INTERFACE FUNCTIONS ENDS FROM HERE"""


def admin_main_interface():
    clear()
    try:
        call_the_name("ADMIN INTERFACE PAGE")
        print(
            """
        1. Login
        2. Register
        3. Delete
        4. Quit""")
        print("_" * 30)
        return input("""Choice [1 or 2 or 3 or 4] : """)
    except:
        clear()
        print("Error in admin_main_interface")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(admin_main_interface_director)


"""ADMIN INTERFACE FUNCTIONS STARTS FROM HERE"""


def admin_main_interface_director():
    clear()
    try:
        admin_inter = admin_main_interface()
        print(admin_inter)
        if admin_inter == "1":
            admin_login()
        elif admin_inter == "2":
            admin_register()
        elif admin_inter == "3":
            admin_delete()
        elif admin_inter == "4":
            clear()
            interface_director()
    except:
        clear()
        print("Error in admin_main_interface_director")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(admin_main_interface_director)


def admin_login():
    clear()
    try:
        call_the_name("ADMIN LOGIN PAGE")
        admin_id = int(input("Please enter admin id : "))
        admin_email = input("Please type your registered email address: ")
        admin_password = int(input("Please type your password: "))
        auth_query = f"SELECT EMAIL,PASSWORD,NAME FROM ADMINS WHERE ID={admin_id}"
        auth_execute = sql_query(auth_query, "extract")
        if auth_execute[0][0] == admin_email and auth_execute[0][1] == admin_password:
            clear()
            print(f"Successfully logged in as {auth_execute[0][2]}")
            sleep(2)
            print(f"Welcome {auth_execute[0][2]}")
            print("Redirecting to your admin choices page .")
            sleep(5)
            log_the_task(admin_id, 0, f"ADMIN {auth_execute[0][2]}", admin_email, 0, 0, f"ADMIN LOGIN IN SUCCESSFULLY")
            timewise_report()
        else:
            print("Invalid Credentials")
            admin_login()
    except:
        clear()
        print("Error in admin_login")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(admin_login)


def admin_register():
    clear()
    try:
        call_the_name("ADMIN REGISTRATION PAGE")
        admin_name = input("Please enter your name: ")
        admin_email = input("Please type your email address: ")
        admin_password = int(input("Please type your password: "))
        auth_query = f"INSERT INTO ADMINS (NAME,EMAIL,PASSWORD) VALUES('{admin_name}','{admin_email}',{admin_password})"
        sql_query(auth_query, "execute")
        auth_selection_query = f"SELECT ID FROM ADMINS WHERE EMAIL='{admin_email}'"
        auth_selection_execute = sql_query(
            auth_selection_query, "extract")[0][0]
        print(
            f"Successfully registered as {admin_name} having email {admin_email} and password {admin_password}")
        print(f"Your admin id is {auth_selection_execute}")
        print("Remember this admin id it will be used in the admin confirmation.")
        print("Redirecting to your admin choices page.")
        sleep(5)  # Remember to add redirection to admin choices
        timewise_report()
        log_the_task(auth_selection_execute, 0, f"ADMIN {admin_name}", admin_email, 0, 0,
                     f"ADMIN REGISTERED SUCCESSFULLY")
    except:
        clear()
        print("Error in admin_register")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(admin_register)


def admin_delete():
    clear()
    try:
        call_the_name("ADMIN DELETION PAGE")
        admin_to_delete_id = int(input("Please enter admin id : "))
        admin_email = input("Please type your registered email address: ")
        admin_password = int(input("Please type your password: "))
        auth_query = f"SELECT EMAIL,PASSWORD,NAME FROM ADMINS WHERE ID={admin_to_delete_id}"
        auth_execute = sql_query(auth_query, "extract")
        if auth_execute[0][0] == admin_email and auth_execute[0][1] == admin_password:
            clear()
            print(f"Successfully delete admin having details:")
            print(
                f"""
            ID: {admin_to_delete_id}
            Email: {auth_execute[0][0]}
            Name : {auth_execute[0][2]}""")
            sleep(7)
            interface_director()
            log_the_task(admin_to_delete_id, 0, f"ADMIN {auth_execute[0][2]}", admin_email, 0, 0,
                         f"ADMIN DELETED SUCCESSFULLY")
        else:
            print("Invalid Credentials")
            admin_delete()
    except:
        clear()
        print("Error in admin_delete")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(admin_delete)


"""ADMIN INTERFACE Functions ENDS FROM HERE"""


def admin_choicer():
    clear()
    try:
        call_the_name("ADMIN CHOICES PAGE")
        print(
            """
        1. Daily Report
        2. Monthly Report
        3. Yearly Report
        4. Money Deposit Report
        5. Money Withdraw Report
        6. Money Transfer Report
        7. Money Received Report
        8. Registered Accounts Information
        9. Login Accounts Information
        10. Deleted Accounts Information
        11. All Logs
        12. Specify Report
        13. Details Updated
        """)
        return input("\tEnter your choice 1 to 13 : ")
    except:
        clear()
        print("Error in admin_choicer")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
Exception Type:{exc_type}
File Name:{file_name}
Error Occurred Line Number: {exc_tb.tb_lineno}""")

        sleep(5)
        raise_error(timewise_report)


def timewise_report():
    clear()
    try:
        enter = ""
        while enter != "q":
            perform = admin_choicer()
            to = {"1": ["Daily Report", datetime.now().strftime('%d')],
                  "2": ["Monthly Report", datetime.now().strftime('/%m/')],
                  "3": ["Yearly Report", datetime.now().strftime(' %Y/')],
                  "4": ["Money Deposit Report", "DEPOSITED"],
                  "5": ["Money Withdraw Report", "WITHDRAWN"],
                  "6": ["Money Transfer Report", "TRANSFERRED"],
                  "7": ["Money Received Report", "RECEIVED"],
                  "8": ["Registered Accounts Information", "REGISTERED "],
                  "9": ["Login Accounts Information", "LOGIN"],
                  "10": ["Deleted Accounts Information", "DELETED"],
                  "11": ["All Logs"],
                  "12": ["Specify Report"],
                  "13": ["Details Updated", "UPDATED"]}
            set_to = to[str(perform)]
            header = ["SR NO:", "BANK ID", "ACCOUNT ID", "User Name", "EMAIL ID", "PREVIOUS BALANCE", "UPDATED BALANCE",
                      "TASK PERFORMED", "TIMESTAMP"]
            if set_to[0] == "Daily Report":
                clear()
                call_the_name(set_to[0])
                query = f"SELECT * FROM LOGS WHERE TIMESTAMP LIKE '%{set_to[1]}'"
                extracted_data = sql_query(query, "extract")
                print(tabulate(extracted_data, header, tablefmt='fancy_grid'))
            elif set_to[0] in ["Monthly Report", "Yearly Report"]:
                clear()
                call_the_name(set_to[0])
                query = f"SELECT * FROM LOGS WHERE TIMESTAMP LIKE '%{set_to[1]}%'"
                extracted_data = sql_query(query, "extract")
                print(tabulate(extracted_data, header, tablefmt='fancy_grid'))
            elif set_to[0] in ["Money Deposit Report", "Money Withdraw Report", "Money Transfer Report",
                               "Money Received Report", "Registered Accounts Information", "Login Accounts Information",
                               "Deleted Accounts Information", "Details Updated"]:
                clear()
                call_the_name(set_to[0])
                query = f"SELECT * FROM LOGS WHERE TASK_PERFORMED LIKE '%{set_to[1]}%'"
                extracted_data = sql_query(query, "extract")
                print(tabulate(extracted_data, header, tablefmt='fancy_grid'))
            elif set_to[0] == "All Logs":
                clear()
                call_the_name(set_to[0])
                query = f"SELECT * FROM LOGS"
                extracted_data = sql_query(query, "extract")
                print(tabulate(extracted_data, header, tablefmt='fancy_grid'))
            elif set_to[0] == "Specify Report":
                user_id = input("Which user you want to fetch specify it's User ID :")
                bank_id = input("Which bank you want to fetch of the user id mentioned above specify it's Bank Id'")
                taskPerformed = input(
                    """Which Task you want to fetch
                    1. UPDATED
                    2. DEPOSITED
                    3. WITHDRAWN
                    4. TRANSFERRED
                    5. RECEIVED
                    6. REGISTERED
                    8. DELETED
                    9. LOGIN
                    10. All
            (Take care of whitespace while typing)
            Write sentence not number given in-front of it ===>""").upper()
                print("You can only specify month or year or day ")
                print("""Like for:-
                day--> /1
                month--> /12/
                year--> 2021/""")
                timestamp = input(
                    "Enter the timestamp [Press enter to use today's timestamp or to get all type 'all' ] :").casefold()
                query = f"SELECT * FROM LOGS WHERE USER_BANK_ID={user_id} AND USER_ACCOUNT_ID={bank_id} AND TASK_PERFORMED='{taskPerformed}' AND TIMESTAMP LIKE '%{timestamp}%'"
                if taskPerformed == "ALL":
                    query = f"SELECT * FROM LOGS WHERE USER_BANK_ID={user_id} AND USER_ACCOUNT_ID={bank_id} AND TIMESTAMP LIKE '%{timestamp}%'"
                if timestamp == "":
                    timestamp = datetime.now().strftime('%d')
                if timestamp == "all":
                    query = f"SELECT * FROM LOGS WHERE USER_BANK_ID={user_id} AND USER_ACCOUNT_ID={bank_id} AND TASK_PERFORMED LIKE '%{taskPerformed}%'"
                if timestamp == "all" and taskPerformed == "ALL":
                    query = f"SELECT * FROM LOGS WHERE USER_BANK_ID={user_id} AND USER_ACCOUNT_ID={bank_id}"
                extracted_data = sql_query(query, "extract")
                call_the_name("ADMIN SPECIFIC REPORT")
                print(tabulate(extracted_data, header, tablefmt='fancy_grid'))

            enter = input("Q to quit  Enter to continue: ").casefold()
        interface_director()
    except:
        clear()
        print("Error in timewise_report")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(f"""
        Exception Type:{exc_type}
        File Name:{file_name}
        Error Occurred Line Number: {exc_tb.tb_lineno}""")
        sleep(5)
        raise_error(timewise_report)


user_main_interface_director()
