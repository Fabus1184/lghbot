from __future__ import print_function
import pickle
import os
import base64
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dict_hash import sha256
from datetime import datetime
import glob
from PIL import Image, ImageDraw, ImageFont
from pandas import DataFrame

from tabula import read_pdf
from tabulate import tabulate

_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
_FIELDS = ["Datum", "Stunde", "Art", "Klasse", "Lehrer", "Kurs", "Raum", "Kommentar"]


def plan(kurse, meine_klasse):
    file = glob.glob("res/vplan/*.pdf")
    file.sort()
    file = (file[::-1])[0]

    df = DataFrame(read_pdf(file, pages="all", output_format="dataframe")[0])
    df = df[(df["Art"] != "ht")]

    for x in df.index[df["Tag"].isnull()].tolist():
        for k in df.columns.values:
            if str(df.loc[x, k]) != "nan":
                df.loc[x - 1, k] = df.loc[x - 1, k] + df.loc[x, k]
                df = df.drop(x)

    f = tabulate(df, tablefmt="fancy_grid", headers=_FIELDS, showindex=False).split("\n")
    f = [x for x in f if (any([k in x for k in kurse]) and meine_klasse in x) or (f.index(x) in (0, 1, 2, len(f) - 1))]

    image = Image.new("RGB", (1920, 1080), (0x36, 0x39, 0x3f))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("/usr/share/fonts/ubuntu-font-family/UbuntuMono-R.ttf", 30)
    [draw.text((10, (f.index(x) + 1) * 30), x, (0xC5, 0xD6, 0xD0), font=font) for x in f]
    img_resized = image.resize((1920, 1080), Image.ANTIALIAS)

    return img_resized, file.split(".pdf")[0]


def fetch():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        raise Exception

    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().list(maxResults=5, userId='me',
                                             labelIds=['Label_9200074680711448170']).execute()
    messages = result.get('messages')

    for msg in messages:

        if os.path.exists("res/vplan/%s" % sha256(msg)):
            return True

        txt = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            for part in txt['payload'].get('parts', ''):
                if part['filename'] and "ertret" in part['filename']:

                    att_id = part['body']['attachmentId']
                    att = service.users().messages().attachments().get(userId='me', messageId=msg['id'],
                                                                       id=att_id).execute()
                    data = att['data']
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
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', _SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
