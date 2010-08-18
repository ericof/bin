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
pt_origem = 'News Item'
pt_destino = 'Blog Entry'

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
site_properties = getattr(site.portal_properties, 'site_properties')
if site_properties.getProperty('enable_link_integrity_checks', False):
    site_properties.manage_changeProperties(enable_link_integrity_checks=False)
    
results = ct.searchResults(portal_type=pt_origem)

for b in results:
    item = b.getObject()
    migrator = InplaceCMFItemMigrator(item)
    migrator.dst_portal_type = pt_destino
    migrator.migrate()

if site_properties.getProperty('enable_link_integrity_checks', False):
    site_properties.manage_changeProperties(enable_link_integrity_checks=True)

# Realiza o commit da transacao
transaction.commit()
print 'Commit da transacao'

# Sincroniza a base de dados
app._p_jar.sync()
print 'Sincroniza ZEO'
print 'Finalizado as ',
print datetime.now().isoformat()

