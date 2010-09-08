#-*- coding:utf-8 -*-
import sys
import os
from BeautifulSoup import BeautifulStoneSoup

PROTOCOLS = {
             'prpl-bigbrownchunx-facebookim':'Facebook',
             'prpl-bigbrownchunx-skype':'Skype',
             'prpl-msn':'MSN',
             'prpl-msn_pecan':'MSN',
             'prpl-icq':'ICQ',
             'prpl-yahoo':'Yahoo!',
             'prpl-irc':'IRC',
             'prpl-jabber':['GTalk','Facebook','Jabber'],
            }
SUBPROTOCOLS = {
                u'prpl-jabber':{
                              '@chat.facebook.com':'Facebook',
                              '@gmail.com':'GTalk',
                              }
               }

def _service(protocol, account):
   ''' Return a service name based on protocol and account'''
   protocol = str(protocol)
   account = str(account)
   service = PROTOCOLS.get(protocol,'Other')
   if isinstance(service,list):
       if protocol in SUBPROTOCOLS:
           for k,v in SUBPROTOCOLS[protocol].items():
               if (account.find(k) > 0):
                   service = v
           if isinstance(service,list):
               service = 'GTalk'
       else:
           service = 'GTalk'
   return service

class Buddies:
    def __init__(self,path=''):
        if path:
            file = '%s/libpurple/blist.xml' % path
        else:
            file = 'blist.xml'
        blist = open(file).read().decode('utf-8')
        data = BeautifulStoneSoup(blist)
        buddiesTags = data.blist.findAll('buddy')
        buddies = [Buddy(ele) for ele in buddiesTags]
        accounts = set([(b['proto'],b['account']) for b in buddiesTags])
        self.services = [_service(p,a) for p,a in accounts]
        self._buddies = dict([((b.service,b.account.replace('/Adium',''),b.name),b) for b in buddies])

    def getBuddy(self,service,account,id):
        ''' Return a buddy
        '''
        return self._buddies.get((service,account,id))
        
class Buddy(object):
    ''' A Buddy
    '''
    def __init__(self,ele):
        self.ele = ele
        self.attrs = dict(ele.attrs)
        self.account = self.attrs.get(u'account',u'').encode('utf-8')
        self.protocol = self.attrs.get(u'proto',u'').encode('utf-8')
        self.service = _service(self.protocol,self.account).encode('utf-8')
        self.name = self._getName().encode('utf-8')
        self.alias = self._getAlias().encode('utf-8')
    
    def _getName(self):
        ''' Return the name for this Buddy
        '''
        name = ''
        ele = self.ele
        nameTag = ele.find('name')
        if nameTag:
            name = nameTag.string
        # Fix Facebook ids
        if self.service == 'Facebook' and name.find('@')<0:
            name = '-%s@chat.facebook.com' % name
        return name
    
    def _getAlias(self):
        ''' Find the alias for this Buddy
        '''
        alias = servernick = ''
        ele = self.ele
        aliasTag = ele.find('alias')
        settings = ele.findAll('setting')
        if settings:
            servernick = [s.string for s in settings if s.get('name')=='servernick']
        if aliasTag:
            alias = aliasTag.string
        elif servernick:
            alias = servernick[0]
        return alias

if __name__ == '__main__':
    
    buddies = Buddies() 
    import pdb;pdb.set_trace()
    print buddies