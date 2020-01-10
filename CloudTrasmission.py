#암호화 없이 데이터를 전송을 위한 소스
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import timeit

# 시간을 측정합니다.
start = timeit.default_timer()

FILES = []
#더미 파일 이름 받기
for i in range(1, 101):
    stream = 'dummyFile\\' + str(i) + '.txt'
    FILES.append(stream)
# 클라우드 데이터 전송
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
                'mimeType': None
                }

    res = DRIVE.files().create(body=metadata, media_body=file_name).execute()
    if res:
        print('Uploaded "%s" (%s)' % (file_name, res['mimeType']))

stop = timeit.default_timer()
print(float(stop - start))