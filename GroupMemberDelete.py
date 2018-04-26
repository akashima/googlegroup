# coding: utf-8

from __future__ import print_function
import httplib2
import os
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import json

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/groupssettings-python-quickstart.json
SCOPES = {'https://www.googleapis.com/auth/admin.directory.group.member', 'https://www.googleapis.com/auth/admin.directory.group.readonly'}
CLIENT_SECRET_FILE = 'json.txt'
APPLICATION_NAME = 'Groups Settings API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'groupmemberdelete.csv')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Admin SDK Directory API.

    Creates a Google Admin SDK API service object and outputs a list of first
    10 users in the domain.
    """

    # 削除するメールアドレスの一覧をlist化
    mailscsv = open('./deletemail.csv')
    mails = mailscsv.read()
    mailscsv.close()
    mailLists = mails.replace('\r', '').replace('\n', ',').split(',')

    # 削除するグループのファイル出力先
    outputList = []
    for mail in mailLists:
        if not mail:
            break
        today = datetime.datetime.today()
        outputfilename = str(mail) + '_delete_' + str(today.year) + str(today.month) + str(today.day) + str(today.hour) + str(today.minute) + '.csv'
        csv = open(outputfilename, 'w')
        outputList.append(outputfilename)
        csv.close()

    # 除外リストの読み込みとlist化
    excludescsv = open('./excludes.csv')
    excludes = excludescsv.read()
    excludescsv.close()
    excludeslist = excludes.replace('\r', '').replace('\n', ',').split(',')

    # credential(認証処理)
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    # Google Groupsのlist取得
    results = service.groups().list(customer='my_customer').execute()
    groups = results.get('groups', [])
    shallowGroups = groups[:]

    # 除外listを元にGoogle Groupsのlistを編集
    print('exclude list')
    for group in shallowGroups:
        for exclude in excludeslist:
            if not exclude:
                break
            if group['email'] == exclude:
                print(group['email'])
                groups.remove(group)
                break

    # Google Groupsのlistを元にユーザ削除処理
    if not groups:
        print('No groups in the domain.')
    else:
        print('[start]:It execute delete of ' + str(mailLists) + '.')
        print('delete group member:')
        for mail in mailLists:
            if not mail:
                break
            indexNo = mailLists.index(mail)
            outputfilename = outputList[indexNo]
            for group in groups:
                results = service.members().list(groupKey=group['email']).execute()
                members = results.get('members', [])
                for member in members:
                    if member['email'] == mail:
                        print(group['email'] + ' delete ' + mail )
                        csv = open(outputfilename, 'a')
                        csv.write(group['email'] + '\r\n')
                        csv.close()
                        service.members().delete(groupKey=group['email'], memberKey=mail).execute()
        print('[end]:It executed delete of ' + str(mailLists) + '.')

if __name__ == '__main__':
    main()
