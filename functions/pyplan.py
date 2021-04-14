from __future__ import print_function
import pickle
import os
from os import path
import subprocess
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dict_hash import sha256
import sys
from prettytable import PrettyTable
from datetime import datetime
import glob


def plan(kurse, meine_klasse):

    file = glob.glob("res/vplan/*.pdf")
    file = (file[::-1])[0]

    x = subprocess.check_output('pdfgrep  -i " " %s | grep -v "Landesgymnasium" | grep -v "Schwäbisch" | grep -v "Standard" | grep -v "(Raum)"' % (file), shell=True, text=True)
    x = x.split("\n")

    file = file.split("/")[len(file.split("/"))-1]
    file = file.split(".pdf")[0]
    plan_datum = str(file)[8:10] + "." + str(file)[5:7] + "." + str(file)[0:4]

    for line in range(0,len(x)):
        if not x[line]:
            x.pop(line)
    for i in range(0,len(x)):
        try:
            if x[i][0] == " ":
                x[i-1] += " " + ' '.join(x[i].split())
                x.pop(i)
        except:
            pass
    for i in range(0,len(x)):
        if x[i][3] != " ":
            x[i] = x[i][0:2] + "  " + x[i][3]+x[i][5]+x[i][7] + " " + x[i][8:len(x[i])]
        if x[i][6] == " " and x[i][7] != " ":
            x[i] = x[i][0:6] + x[i][7] + x[i][9] + x[i][10] + "  " + x[i][11:len(x[i])]
    datum = []
    stunde = []
    art = []
    klasse = []
    lehrer = []
    kurs = []
    raum = []
    kommentar = []
    for line in x:
        orig = line
        appended = False
        if len(line.lstrip(' '))+25 < len(line):
            appended = True
        datum.append(line[0:2])
        stunde.append(line[4:9].replace(" ",""))
        art.append(line[12:24].replace(" ",""))
        line=line[25:]
        klasse.append(line.split(" ")[0])
        line=line[len(line.split(" ")[0]):]
        line=line.lstrip(' ')
        lehrer.append(line.split(" ")[0])
        line=line[len(line.split(" ")[0]):]
        line=line.lstrip(' ')
        kurs.append(line[0:8].replace(" ",""))
        line=line[8:]
        if line[3:8].replace(" ","") == "":
            raum.append("")
            line=line.lstrip(' ')
        else:
            line=line.lstrip(' ')
            raum.append(line.split(" ")[0])
            line=line[len(line.split(" ")[0]):]
            line=line.lstrip(' ')
        if not appended:
            kommentar.append(line)
        else:
            kommentar[len(kommentar)-1]+=orig.lstrip(" ")
            kommentar.append(" ")
    for i in range(0,len(datum)):
        if kommentar[i] == "":
            kommentar[i] = "---"
        kommentar[i] = kommentar[i].replace("+ ","+")
        kommentar[i] = kommentar[i].replace(" +","+")
        kommentar[i] = kommentar[i].replace("+"," + ")

    pt = PrettyTable()

    pt.field_names = ["Datum", "Stunde", "Art", "Klasse", "Lehrer" ,"Kurs" ,"Raum" ,"Kommentar"]
    for i in range(0,len(datum)):
        condition = False
        for x in kurse:
            if str(x) in str(kommentar[i]):
                condition = True
        if meine_klasse in klasse[i] and (kurs[i] in kurse or condition):
            pt.add_row([datum[i],stunde[i],art[i],klasse[i],lehrer[i],kurs[i],raum[i],kommentar[i]])

    pt.align = "l"

    return (str(pt),plan_datum)

def fetch():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        raise Exception

    service = build('gmail', 'v1', credentials=creds)
    id = None

    result = service.users().messages().list(maxResults=5, userId='me', labelIds=['Label_9200074680711448170']).execute()
    messages = result.get('messages')

    for msg in messages:

        if os.path.exists("res/vplan/%s" % sha256(msg)):
            return True

        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            payload = txt['payload']
            header = payload['headers']

            for part in txt['payload'].get('parts', ''):
                if part['filename'] and "ertret" in part['filename']:

                    att_id=part['body']['attachmentId']
                    att=service.users().messages().attachments().get(userId='me', messageId=msg['id'],id=att_id).execute()
                    data=att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    
                    with open("res/vplan/%s.pdf" % (datetime.now().strftime("%Y.%m.%d.%H.%M")), 'wb') as f:
                        f.write(file_data)
                        f.close()
                    with open("res/vplan/%s" % sha256(msg), "w") as f:
                        f.write(" ")
                        f.close()
                        return False
                else:
                    continue
        except Exception as e:
            print(e)
            pass

def auth():
    with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)