#DES 암호화를 진행한 소스
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import DES_Testing
import timeit

keytext = 'KEY00000'
ivtext = '1234'
msg = 'python'

FILES = []
myCipher = DES_Testing.myDES(keytext, ivtext)

# 시간을 측정합니다.
start = timeit.default_timer()

# DES 암호화
for i in range(1, 101):
    stream = 'dummyFile\\' + str(i) + '.txt'  # Make a file stream name
    fp = open(stream, "r")  # file open
    msg = fp.read()  # save the string
    fp.close()  # close file stream

    ciphered = myCipher.enc(msg)
    stream = 'crypto\\' + str(i) + '.bin'
    fp = open(stream, 'wb')
    FILES.append(stream)
    fp.write(ciphered)
    fp.close()

# 복호화
# for i in range(1, 101):
#     stream = 'crypto\\' + str(i) + '.bin'
#     fp = open(stream, "rb")
#     encrypted = bytes(fp.read())
#     fp.close()
#
#     deciphered = myCipher.dec(encrypted)
#     deciphered = deciphered.decode("utf-8")
#
#     index = deciphered.find('0')
#
#     if index != -1:
#         deciphered = deciphered[:index]
#
#     stream = 'test\\deCrypto\\' + str(i) + '.txt'
#     fp = open(stream, 'w')
#     fp.write(deciphered)
#     fp.close()

# 구글 API 연결 및 데이터 전송
try :
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drivze.file'
store = file.Storage('storage.json')
creds = store.get()

if not creds or creds.invalid:
    print("make new storage data file ")
    flow = client.flow_from_clientsecrets('client_secret_drive.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow, store)

DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

for file_title in FILES :
    file_name = file_title
    metadata = {'name': file_name,
                'mimeType': None}

    res = DRIVE.files().create(body=metadata, media_body=file_name).execute()
    if res:
        print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))
stop = timeit.default_timer()
print(float(stop - start))