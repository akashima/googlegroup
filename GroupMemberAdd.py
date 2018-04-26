# coding: utf-8

from __future__ import print_function
import httplib2
import os

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
                                   'groupmemberadd.csv')

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

    mailscsv = open('./addmail.csv')
    mails = mailscsv.read()
    mailscsv.close()
    mailLists = mails.replace('\r', '').replace('\n', ',').split(',')
    print(mailLists)

    targetscsv = open('./addgroup.csv')
    targets = targetscsv.read()
    targetscsv.close()
    targetLists = targets.replace('\r', '').replace('\n', ',').split(',')

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('admin', 'directory_v1', http=http)

    results = service.groups().list(customer='my_customer').execute()
    groups = results.get('groups', [])

    if not groups:
        print('No groups in the domain.')
    else:
        print('[start]:It execute add of ' + str(mailLists) + '.')
        print('add group member:')
        for mail in mailLists:
            if not mail:
                break
            for group in groups:
                for targetList in targetLists:
                    if group['email'] == targetList:
                        print(group['email'] + ' add ' + mail)
                        dictionary = {'email':mail, 'role':'MEMBER'}
                        service.members().insert(groupKey=group['email'], body=dictionary).execute()
        print('[end]:It executed add of ' + str(mailLists) + '.')

if __name__ == '__main__':
    main()
