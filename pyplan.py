#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import pickle
import os
from os import path
import subprocess
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys

#kurse = ["2rel2","2s2","3ch1","2inf1","5M2","3d1","2geo1","3e2","5Ph1","2mu1","5Wi1","2g2"]
#kurse = sys.argv[1].split("")
kurse = str(sys.argv[1]).replace("\"","").split(",")
meine_klasse = sys.argv[2]

'''with open("log","a") as f:
    f.write(sys.argv[1]+":"+sys.argv[2])
    for x in kurse:
        f.write(x+"_")
'''
#print("-"+str(meine_klasse)+"-")
#kurse = ["3bio1"]
#meine_klasse="11"


# If modifying these scopes, delete the file token.pickle.

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def prettyprint():

    from prettytable import PrettyTable
    pt = PrettyTable()
    # = subprocess.run(['pdfgrep', "-i", ' ' ,"plan.pdf"],stdout=subprocess.PIPE)
    x = subprocess.check_output('pdfgrep  -i " " plan.pdf | grep -v "Landesgymnasium" | grep -v "Schwäbisch" | grep -v "Standard" | grep -v "(Raum)"', shell=True, text=True)

    #pdfgrep  -i " " plan.pdf | grep -v "Landesgymnasium" | grep -v "Schwäbisch" | grep -v "Standard" | grep -v "(Raum)"

    #x = x.stdout.decode("utf-8").split("\n")

    x = x.split("\n")

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


    pt.field_names = ["Datum", "Stunde", "Art", "Klasse", "Lehrer" ,"Kurs" ,"Raum" ,"Kommentar"]
    for i in range(0,len(datum)):
        #DEBUG
        #print(kommentar[i])
#        if kurs[i] in kurse and klasse[i] == meine_klasse:
        #if meine_klasse in klasse[i] and (kurs[i] in kurse or kurs[i] in kommentar[i]):
        condition = False
        for x in kurse:
            if str(x) in str(kommentar[i]):
                condition = True
        if meine_klasse in klasse[i] and (kurs[i] in kurse or condition): #or condition): #or [ele for ele in kurse if(ele in kommentar[i])] ):
            pt.add_row([datum[i],stunde[i],art[i],klasse[i],lehrer[i],kurs[i],raum[i],kommentar[i]])

    pt.align = "l"
    print(pt)
    #with open("plan.txt","w+") as f:
    #    f.write(str(pt))
    #f.close()

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = \
                InstalledAppFlow.from_client_secrets_file('credentials.json'
                    , SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    id = None

    result = service.users().messages().list(maxResults=100, userId='me').execute()
    messages = result.get('messages')

    for msg in messages:
        txt = service.users().messages().get(userId='me', id=msg['id']).execute()

        try:
            payload = txt['payload']
            header = payload['headers']

            for d in header:
                if d['name'] == "Subject" and "Vertretung" in d['value']:
                    id = (msg['id'])
                    message = service.users().messages().get(userId='me',id=id).execute()
                    for part in message['payload'].get('parts', ''):
                        if part['filename'] and "ertret" in part['filename']:
                            att_id=part['body']['attachmentId']
                            att=service.users().messages().attachments().get(userId='me', messageId=id,id=att_id).execute()
                            data=att['data']
                        else:
                            continue
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = "plan.pdf"
                    with open(path, 'wb') as f:
                        f.write(file_data)

                    raise SystemExit

        except SystemExit:

            prettyprint()

            sys.exit(0)
        except :
            pass




if __name__ == '__main__':
    main()
