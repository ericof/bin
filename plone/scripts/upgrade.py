#! -*- coding: UTF-8 -*-
from datetime import datetime
import mimetypes
import transaction
from zope.app.component.hooks import setHooks, setSite
from Testing.makerequest import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from os.path import join
from collective.contentlicensing.utilities.interfaces import  IContentLicensingUtility
from collective.contentlicensing.utilities.utils import ContentLicensingUtility
from Products.contentmigration.inplace import InplaceCMFItemMigrator
from Products.CMFPlone.utils import normalizeString
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

# Configuracoes
portal_id = 'foobar'
user_id = 'foobar'

def walker(obj):
    print '/'.join(obj.getPhysicalPath()),obj.Type(),obj.__class__
    try:
        objIds = obj.objectIds()
    except AttributeError:
        objIds = []
    
    for oId in objIds:
        walker(obj[oId])

def removeComponents(sm,searchStr):
    
    adapters = sm.utilities._adapters
    for x in adapters[0].keys():
        if x.__module__.find(searchStr) != -1:
          print "deleting %s" % x
          del adapters[0][x]
    sm.utilities._adapters = adapters
    
    subscribers = sm.utilities._subscribers
    for x in subscribers[0].keys():
        if x.__module__.find(searchStr) != -1:
          print "deleting %s" % x
          del subscribers[0][x]
    sm.utilities._subscribers = subscribers
    
    provided = sm.utilities._provided
    for x in provided.keys():
        if x.__module__.find(searchStr) != -1:
          print "deleting %s" % x
          del provided[x]
    sm.utilities._provided = provided

def removeObjects(site,portal_types=[]):
    ct = site.portal_catalog    
    results = ct.searchResults(portal_type=portal_types)
    for b in results:
        item = b.getObject()
        parent = item.aq_parent
        parent.manage_delObjects([item.getId(),])

def migrateContent(site,source,destination):
    ct = site.portal_catalog    
    results = ct.searchResults(portal_type=source)
    for b in results:
        item = b.getObject()
        migrator = InplaceCMFItemMigrator(item)
        migrator.dst_portal_type = destination
        migrator.migrate()
    

def setDefaultLanguage(site,language='pt-br'):
    ct = site.portal_catalog
    results = ct.searchResults()
    for brain in results:
        o = brain.getObject()
        o.setLanguage(language)
    

def uninstallProducts(site,products=[]):
    qi = site.portal_quickinstaller
    for product in products:
        try:
            qi.uninstallProducts([product,])
        except AttributeError:
            pass

def removePortlets(context):
    column = getUtility(IPortletManager, name=u'plone.leftcolumn', context=context)
    manager = getMultiAdapter((context, column,), IPortletAssignmentMapping)
    column2 = getUtility(IPortletManager, name=u'plone.rightcolumn', context=context)
    manager2 = getMultiAdapter((context, column2,), IPortletAssignmentMapping)
    for key in manager.keys():
        del(manager[key])
    for key in manager2.keys():
        del(manager2[key])


# Inicia o processo
print 'Iniciado as ',
print datetime.now().isoformat()

# Usamos o makerequest para criar um request fake para este ambiente
app = makerequest(app)

# Pegamos o portal Plone
portal = portal_id 
site = app[portal] 
sm = site.getSiteManager()

# Definimos qual e o site, algumas ferramentas precisam disso, como o FSS
setSite(site)

# Ate este momento estamos como usuario anonimo.
# usando o newSecurityManager nos damos as credenciais do usuario admin
newSecurityManager(None, app.acl_users.getUserById(user_id))
walker(site)

site_properties = getattr(site.portal_properties, 'site_properties')
if site_properties.getProperty('enable_link_integrity_checks', False):
    site_properties.manage_changeProperties(enable_link_integrity_checks=False)

# Upgrade Plone
migration = site.portal_migration
migration.upgrade()

# Migra clases
pt_origem = 'News Item'
pt_destino = 'Blog Entry'
migrateContent(site,source=pt_origem,destination=pt_destino)

# Ajusta idioma para pt-BR
language = 'pt-br'
setDefaultLanguage(site,language)

# Remove portlets
removePortlets(site)
removePortlets(site.blog)

# Remove tipos nao usados
portal_types = ['PlonePopoll','ContentPanels',]
removeObjects(site,portal_types)

products = ['PlonePopoll','beyondskins.erico.site2009','CacheSetup',
            'CMFContentPanels', 'Products.CMFSquidTool',
            'collective.plonetruegallery','CMFSquidTool',
            'Products.PlonePopoll','PlonePopoll',
            'collective.js.jquery','collective.js.jqueryui',
            'collective.contentlicensing','collective.easyslider',
            'sc.social.bookmarks','Products.Scrawl','Scrawl']

# Remove componentes
componentes = ['collective.contentlicensing',
               'collective.easyslider',
               'collective.plonetruegallery'] + products
for componente in componentes:
    removeComponents(sm,componente)

try:
    util_obj = sm.getUtility(IContentLicensingUtility)
    sm.unregisterUtility(provided=IContentLicensingUtility)
    del util_obj
    sm.utilities.unsubscribe((), IContentLicensingUtility)
    del sm.utilities.__dict__['_provided'][IContentLicensingUtility]
    del sm.utilities._subscribers[0][IContentLicensingUtility]
except:
    print 'Error deleting Utility'


# Desinstala produtos
uninstallProducts(site,products)

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

print 'Walker:'
walker(site)
