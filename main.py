import os
import mysql.connector
import smtplib, ssl
from twilio.rest import Client

mydb = mysql.connector.connect(host="localhost", user="root", password="shivaraj06",database="shivaraj")
smtp_server = "smtp.gmail.com"
port = 587
sender_email = "your_mail"
email_password = 'password'
context = ssl.create_default_context()
botNumber ='+16316023183'
account_sid = 'ACa547e176f30e3f22342b8f998a5cf7bc'
auth_token = '00ffb49b2d8827cf6dabbd26860e7d6e'
client = Client(account_sid, auth_token)

def fetchData():
    mycursor = mydb.cursor()
    mycursor.execute("select * from student_data where s_attendance < 75 or s_marks < 29")
    for i in mycursor:
        student_name = i[1]
        recNo = i[2]
        recMail = i[3]
        attendace = i[4]
        internals = i[5]
        action(student_name, recNo, recMail, attendace, internals)

def send_mail(sender_email,recMail,mail_msg,email_password):
    try:
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() 
        server.starttls(context=context) 
        server.ehlo() 
        server.login(sender_email, email_password)
        server.sendmail(sender_email, recMail, mail_msg)

    except Exception as e:
        print(e)
    finally:
        server.quit()

def sendMsg(msg,botNumber,recNo):
    message = client.messages.create(body=msg ,from_= botNumber ,to=recNo)
    call = client.calls.create(to=recNo ,from_= botNumber, url="https://handler.twilio.com/twiml/EHb8a33d13e6e1b3d12bc9f955c3c378c7")
    print(message.sid)
    print(message.cid)

    

def action(student_name, recNo, recMail, attendace, internals):
    if internals < 29 and attendace < 75:
        cnum = 75 - attendace
        x = int(cnum * 0.5)
        num = 29 - internals
        txtmsg = "Dear Parent, ", student_name, " performance is very low as compared to the average criteria. Your wards internals and attendance are ", internals," & " ,attendace, " Which is below the required criteria and need ", str(x), " attendance and ", str(num), " internals . We kindly request you to look into the issue. For more details contact the HOD."
        msg = ""
        for i in txtmsg:
            msg = msg+i
        sendMsg(msg, botNumber,recNo)
        send_mail(sender_email, recMail, msg, email_password) 
    elif internals < 29:
        num = 29 - internals
        txtmsg = "Dear Parent, ",student_name, " current internal's are low. Your ward's internals marks are ", str(internals), " Which is less than the required criteria i.e  29  and still need to have " , str(num), " more marks to attempt exams. We kindly request you to look into the issue. For more details contact the HOD."
        msg =""
        for i in txtmsg:
            msg = msg+i
        sendMsg(msg, botNumber,recNo)
        send_mail(sender_email, recMail, msg, email_password) 
    elif attendace < 75:
        cnum = 75 - attendace
        x = int(cnum * 0.5)
        txtmsg = "Dear Parent, ",student_name, " current attendance's is low. Your ward's attendance is ", str(attendace), " Which is less than the required criteria i.e  75  and still need to attend " , str(x), " more days to attempt exams. We kindly request you to look into the issue. For more details contact the HOD."
        msg =""
        for i in txtmsg:
            msg = msg+i
        sendMsg(msg, botNumber,recNo)
        send_mail(sender_email, recMail, msg, email_password) 
    print(student_name, recNo, recMail, attendace, internals)

fetchData()