#-*- coding:utf-8 -*-
from BeautifulSoup import BeautifulStoneSoup
import os
import sys
from email.mime.text import MIMEText
import time
from hashlib import md5

PROTOCOLS = {
             u'Facebook':'Facebook',
             u'MSN':'MSN',
             u'Twitter':'Twitter',
             u'Yahoo!':'Yahoo',
             u'IRC':'IRC',
             u'Skype':'Skype',
             u'GTalk':'GTalk',
             u'Jabber':['Jabber','Facebook'],
            }
            
SUBPROTOCOLS = {
                u'Jabber':{
                              '@chat.facebook.com':'Facebook',
                              '@gmail.com':'GTalk',
                              }
               }

def _service(protocol, account):
   ''' Return a service name based on protocol and account'''
   service = PROTOCOLS.get(protocol,'Other')
   if isinstance(service,list):
       if protocol in SUBPROTOCOLS:
           for k,v in SUBPROTOCOLS.items():
               if (account.find(k) > 0):
                   service = v
       else:
           service = 'GTalk'
   return service

class Log(object):
    def __init__(self,file,buddies):
        logFile = open(file)
        logPath = logFile.name.split('/')
        self.subject = logPath[-1][:-4]
        self.log = BeautifulStoneSoup(logFile.read())
        self.account = '%s' % self.log.chat['account']
        self.service = _service('%s' % self.log.chat['service'],self.account)
        self.accountCode = logPath[-4]
        self.friend = self._getFriendName(logPath[-3])
        self.lastMsgId=''
        buddy = buddies.getBuddy(self.service,self.account,self.friend)
        self.friendAlias = (buddy and buddy.alias) or ''
    
    def _getFriendName(self,name):
        ''' Return the name for this Buddy
        '''
        # Fix Facebook ids
        if self.service == 'Facebook' and name.find('@')<0:
            name = '-%s@chat.facebook.com' % name
        return name
        
    def process(self):
        messages = []
        for ele in self.log.chat.findAll(['event','message']):
            if ele.name=='event':
                ele = Event(ele)
            elif ele.name=='message':
                ele = Message(ele)
                msg = MIMEText(str(ele.text),'rfc822','utf-8')
                date = ele.time
                alias = ele.alias
                alias = '%s' % (ele.alias or self.friend)
                friend = '%s <%s>' % (alias,self.friend)
                me = self.accountCode
                msg['Message-ID'] = md5('%s%s%s'% (date, self.accountCode, self.friend)).hexdigest()
                msg['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S " + date[-6:].replace(':',''),
                                             time.strptime(date[:-6],'%Y-%m-%dT%H:%M:%S'))
                msg['Subject'] = self.subject
                msg['From'] = (ele.sender == self.account) and me or friend 
                msg['To'] = (ele.sender == self.account) and friend or me
                
                if self.lastMsgId:
                    msg['In-Reply-To'] = self.lastMsgId
                self.lastMsgId = msg['Message-ID']
#                print '(%s)' % ele.time ,ele.alias,ele.sender,':',ele.text
                messages.append(msg)
        return messages

class Event(object):
    def __init__(self,ele):
        print >> sys.stderr, ele.name, ele.attrs
        self.ele = ele
        self.attrs = ele.attrs
        self.sender = ele['sender']
        self.type = ele['type']

class Message(object):
    def __init__(self,ele):
        print >> sys.stderr, ele.name, ele.attrs
        self.ele = ele
        self.attrs = ele.attrs
        self.sender = ele.get('sender') 
        self.alias = ele.get('alias',self.sender)
        self.time = ele.get('time')
        self.raw = ele.find(text=True) or ''
        try:
            self.text = BeautifulStoneSoup(self.raw,convertEntities=BeautifulStoneSoup.XML_ENTITIES)
        except:
            import pdb;pdb.set_trace()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file = sys.argv[1]
    else: # Get Testing Log
        file = os.listdir('testlogs')[0]
        file = os.path.join('testlogs',file)

    # Redirect debugging
    #sys.stderr = open('/dev/null','w')

    log = Log(file)
    messages = log.process()