import requests
import json
import time
import hashlib
import random
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


msg_from = 'sender@example.com'
smtp = 'smtp.example.com'
passwd = 'password_of_sender@example.com'
msg_to = 'recv@example.com'
IMEI = 'change_with_your_imei'
API_ROOT = 'http://client3.aipao.me/api/'

# Generate a string contain 10 char
table = ''
for i in range(10):
    table += chr(random.randint(ord('a'), ord('z')))


def sendMsg(content):
    msg = MIMEMultipart()
    msg.attach(MIMEText(content, 'plain', 'utf-8'))
    msg['Subject'] = content
    msg['From'] = msg_from
    s = smtplib.SMTP_SSL(smtp, 465)
    s.login(msg_from, passwd)
    s.sendmail(msg_from, msg_to, msg.as_string())


def MD5(str):
    return hashlib.md5(str.encode()).hexdigest()


def encrypt(str):
    result = ''
    for i in str:
        result += table[ord(i) - ord('0')]
    return result


def run(IMEI):
    if IMEI is None:
        if len(sys.argv) > 1:
            # Get IMEI from console arguments
            IMEI = sys.argv[1]
        else:
            # If IMEI is neither defined in file nor passed through
            # command arguments, it will get from the console
            IMEI = str(input("[!]ERROR: No Valid IMEI, Please Input Your IMEI: "))
        if len(IMEI) != 32:
            exit("[!]ERROR: IMEI Format Error!")

        if len(sys.argv) > 2 and sys.argv[2].upper() == 'Y':
            pass
        else:
            print("Your IMEI Code:", IMEI)
            sure = str(input("Sure?(Y/n)"))
            if sure.upper == 'Y' :
                pass
            else:
                exit("User Aborted.")
    print("[+]DEBUG: IMEI=" + IMEI)
    tokenHeaders = \
        {
            'version': '2.40',
            'Host': 'client3.aipao.me',
            'Connection': 'Keep-Alive'
        }
    tokenUrl = API_ROOT + 'token/QM_Users/Login_AndroidSchool?IMEICode=' + IMEI
    print("[*]DEBUG: tokenUrl=" + tokenUrl)
    tokenRequests = requests.get(tokenUrl, headers=tokenHeaders)
    tokenJson = json.loads(tokenRequests.content.decode('utf8', 'ignore'))
    state = tokenJson['Success']
    if not state:
        print("[!]ERROR: IMEI Invalid.")
        sendMsg('IMEI已过期！')
        exit("[+]INFO: User Aborted.")
    else:
        print("[+]OK: Login Success.")
    token = tokenJson['Data']['Token']
    print("[*]DEBUG: token=" + token)
    userId = str(tokenJson['Data']['UserId'])
    nonce = str(random.randint(100000, 10000000))
    timespan = str(time.time()).replace('.', '')[:13]
    sign = MD5(token + nonce + timespan + userId).upper()
    getSchoolUrl = API_ROOT + token + '/QM_Users/GS'
    print("[*]DEBUG: getSchoolUrl=" + getSchoolUrl)
    schoolHeaders = \
        {
            'nonce': nonce,
            'timespan': timespan,
            'sign': sign,
            'version': '2.14',
            'Accept': None,
            'User-Agent': None,
            'Accept-Encoding': None,
            'Connection': 'Keep-Alive'
        }
    getSchoolRequests = requests.get(getSchoolUrl, headers=schoolHeaders, data={})
    getSchoolJson = json.loads(getSchoolRequests.content.decode('utf8', 'ignore'))
    Lengths = getSchoolJson['Data']['SchoolRun']['Lengths']
    print('[+]INFO:',
          getSchoolJson['Data']['User']['UserID'],
          getSchoolJson['Data']['User']['NickName'],
          getSchoolJson['Data']['User']['UserName'],
          getSchoolJson['Data']['User']['Sex'])
    print('[+]INFO:',
          getSchoolJson['Data']['SchoolRun']['Sex'],
          getSchoolJson['Data']['SchoolRun']['SchoolId'],
          getSchoolJson['Data']['SchoolRun']['SchoolName'],
          getSchoolJson['Data']['SchoolRun']['MinSpeed'],
          getSchoolJson['Data']['SchoolRun']['MaxSpeed'],
          getSchoolJson['Data']['SchoolRun']['Lengths'])
    startRunningUrl = API_ROOT + token + '/QM_Runs/SRS?S1=30.534736&S2=114.367788&S3=' + str(Lengths)
    print("[*]DEBUG: startRunningUrl=" + startRunningUrl)
    startRunningRequests = requests.get(startRunningUrl, headers=schoolHeaders, data={})
    startRunningJson = json.loads(startRunningRequests.content.decode('utf8', 'ignore'))

    # Generate running data randomly
    RunTime = str(random.randint(720, 1000))  # seconds
    RunDist = str(Lengths + random.randint(0, 3))  # meters
    RunStep = str(random.randint(1300, 1600))  # steps
    StartT = time.time()
    for i in range(int(RunTime)):
        time.sleep(0.1)
        print("[+]INFO: Current Minutes: %d Running Progress: %.2f%%\r" %
              (i / 60, i * 100.0 / int(RunTime)), end='')
    print("")
    print("Running Seconds:", time.time() - StartT)
    RunId = startRunningJson['Data']['RunId']

    # End running
    endUrl = API_ROOT + token + '/QM_Runs/ES?S1=' + RunId + '&S4=' + \
             encrypt(RunTime) + '&S5=' + encrypt(RunDist) + \
             '&S6=&S7=1&S8=' + table + '&S9=' + encrypt(RunStep)
    print("[*]DEBUG: endUrl=" + endUrl)
    endRequests = requests.get(endUrl, headers=schoolHeaders)
    endJson = json.loads(endRequests.content.decode('utf8', 'ignore'))
    print("----------------------")
    print("Time:", RunTime)
    print("Distance:", RunDist)
    print("Steps:", RunStep)
    print("----------------------")
    if (endJson['Success']):
        sendMsg('跑步成功！')
        print("[+]OK:", endJson['Data'])
    else:
        sendMsg('跑步失败！')
        print("[!]Fail:", endJson['Data'])


if __name__ == '__main__':
    run(IMEI)