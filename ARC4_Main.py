#ARC4 암호화를 진행한 소스
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import ARC4_Testing
import timeit

FILES = []
keytext = bytes('KEY00000', 'utf-8')  # KEY len is longer than 8bytes
myCipher = ARC4_Testing.myARC4(keytext)

# 시간을 측정합니다.
start = timeit.default_timer()

# ARC4 암호화.
for i in range(1, 101):
    stream = 'dummyFile\\' + str(i) + '.txt'  # Make a file stream name
    fp = open(stream, "r")  # file open
    s = fp.read()  # save the string
    fp.close()  # close file stream

    encrypted = myCipher.enc(bytes(s, "utf-8"))

    stream = 'crypto\\' + str(i) + '.bin'
    fp = open(stream, 'wb')
    FILES.append(stream)
    fp.write(encrypted)
    fp.close()

# # 암호화 한 값을 다시 복호화 합니다.
# for i in range(1, 101):
#     stream = 'crypto\\' + str(i) + '.bin'
#     fp = open(stream, "rb")
#     encrypted = bytes(fp.read())
#     fp.close()
#
#     decrypted = myCipher.dec(encrypted)
#     decrypted = decrypted.decode("utf-8")
#
#     stream = 'deCrypto\\' + str(i) + '.txt'
#     fp = open(stream, 'w')
#     fp.write(decrypted)
#     fp.close()
#
# # 암호화 시간을 출력합니다.
# stop = timeit.default_timer()
# print(float(stop - start))

# 구글 API 연동 및 파일 전송
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

