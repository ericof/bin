#! -*- coding: UTF-8 -*-
from datetime import datetime
import mimetypes
import transaction
from zope.app.component.hooks import setHooks, setSite
from Testing.makerequest import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from os.path import join
from Products.contentmigration.inplace import InplaceCMFItemMigrator
from Products.CMFPlone.utils import normalizeString

# Configuracoes
portal_id = 'foobar'
user_id = 'foobar'

# Inicia o processo
print 'Iniciado as ',
print datetime.now().isoformat()

# Usamos o makerequest para criar um request fake para este ambiente
app = makerequest(app)

# Pegamos o portal Plone
portal = portal_id 
site = app[portal] 

# Definimos qual e o site, algumas ferramentas precisam disso, como o FSS
setSite(site)

# Ate este momento estamos como usuario anonimo.
# usando o newSecurityManager nos damos as credenciais do usuario admin
newSecurityManager(None, app.acl_users.getUserById(user_id))

ct = site.portal_catalog
    
results = ct.searchResults()

for brain in results:
    o = brain.getObject()
    o.setLanguage('pt-br')

# Realiza o commit da transacao
transaction.commit()
print 'Commit da transacao'

# Sincroniza a base de dados
app._p_jar.sync()
print 'Sincroniza ZEO'
print 'Finalizado as ',
print datetime.now().isoformat()

