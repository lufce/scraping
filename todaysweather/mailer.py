# 181201  ver0.1  作り始め。
#                 とりあえずメールを送信できるようになった。
#TODO: 例外処理。


import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import os

FROM_ADDRESS = os.environ['FROM_ADDRESS']
MY_PASSWORD  = os.environ['hotmail_pass']
TO_ADDRESS   = os.environ['TO_ADDRESS']
SUBJECT      = "天気予報 from Raspberry Pi"

CHARSET      = "ISO-2022-JP"

def create_message(sbj, body):
    msg = MIMEText(body, 'plain', CHARSET)
    msg['Subject'] = sbj
    #msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    #msg['Date'] = formatdate(localtime = True)
    
    return msg
    
def send(from_adr, to_adr, msg):
    smtpobj = smtplib.SMTP('smtp.live.com', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(FROM_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_adr, to_adr, msg.as_string())
    smtpobj.close()
    
def mailing(body):
    msg = create_message(SUBJECT, body)
    send(FROM_ADDRESS,TO_ADDRESS, msg)
    