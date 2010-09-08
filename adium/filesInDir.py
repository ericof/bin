#-*- coding:utf-8 -*-
import os
import sys
import adiumConverter
import adiumBuddies
from mailbox import Maildir
from email.mime.text import MIMEText


def listFiles(dir):
    files = []
    for dirname, dirnames, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith('.xml'):
                path = dirname.split('/')
#                print path[-3],path[-2],filename
                files.append(os.path.join(dirname, filename))
    return files



if __name__ == '__main__':
    if len(sys.argv) == 2:
        path = sys.argv[1]
        sys.stderr = open('/dev/null','w')
        files = listFiles('%s/Logs/' % path)
        buddies = adiumBuddies.Buddies('%s' % path)
        logs = {}
        counter = 0
        baseDir = Maildir('./MAILDIR/',None)
        for file in files:
            try:
                log = adiumConverter.Log(file,buddies)
            except:
                #Erro de xml
                continue
            dirName = ('%s@%s' % (log.service,log.friend)).replace('@','_')
            try:
                maildir = baseDir.get_folder(dirName)
            except:
                maildir = baseDir.add_folder(dirName)
                
            messages = log.process()
            key = (log.service,log.account,log.friend)
            
            if not key in logs:
                logs[key] = {'alias':log.friendAlias,
                             'messages':[]}
            if len(messages):
                #logs[key]['messages'].append(messages)
                counter += len(messages)
                for msg in messages:
                    maildir.add(msg)
                maildir.flush()
                print counter
            baseDir.flush()

        
        
    
