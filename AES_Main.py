#AES 암호화를 진행한 소스
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import AES_Testing
import timeit

FILES = []
cipherinstance = AES_Testing.AESCipher('KEY00000')

# 시간을 측정합니다.
start = timeit.default_timer()

# AES 암호화
# 제작한 암호화 클래스를 이용해 cipherinstance 객체를 만들면서, 암호화키를 넣습니다.
for i in range(1, 101):
    stream = 'dummyFile\\' + str(i) + '.txt'  # Make a file stream name
    fp = open(stream)  # file open
    s = fp.read()  # save the string
    fp.close()

    encrypted = cipherinstance.encrypt(s)
    stream = 'crypto\\' + str(i) + '.txt'
    fp = open(stream, 'w')
    FILES.append(stream);
    fp.write(encrypted)
    fp.close()

    # # 암호화 한 값을 다시 복호화 합니다.
    # decrypted = cipherinstance.decrypt(encrypted)
    # stream = 'deCrypto\\' + str(i) + '.txt'
    # fp = open(stream, 'w')
    # fp.write(decrypted)


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
# 총 시간 출력
stop = timeit.default_timer()
print(float(stop - start))
