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
from Products.contentmigration.archetypes import ATItemMigrator
from Products.CMFPlone.utils import normalizeString
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping

#for patching
from Products.kupu.plone.html2captioned import *


# Configuracoes
portal_id = 'pessoal'
user_id = 'admin'

def convert(self, data, idata, filename=None, **kwargs):
    """convert the data, store the result in idata and return that
    optional argument filename may give the original file name of received data
    additional arguments given to engine's convert, convertTo or __call__ are
    passed back to the transform
    
    The object on which the translation was invoked is available as context
    (default: None)
    """
    from zope.app.component.hooks import getSite
    context = kwargs.get('context', None)
    at_tool = None
    site = getSite()
    template = site.portal_skins.kupu_plone.kupu_captioned_image
    
    at_tool = site.archetype_tool
    rc = at_tool.reference_catalog

    if context is not None and at_tool is not None:
        def replaceImage(match):
            tag = match.group('pat0') or match.group('pat1')
            attrs = ATTR_PATTERN.match(tag)
            atag = match.group('atag0') or match.group('atag1')
            src = attrs.group('src')
            subtarget = None
            m = SRC_TAIL.match(tag, attrs.end('src'))
            if m is not None:
                srctail = m.group(1)
            else:
                srctail = None
            if src is not None:
                d = attrs.groupdict()
                target = self.resolveuid(context, rc, src)
                if target is not None:
                    d['class'] = attrs.group('class')
                    d['originalwidth'] = attrs.group('width')
                    d['originalalt'] = attrs.group('alt')
                    d['url_path'] = target.absolute_url_path()
                    d['caption'] = newline_to_br(html_quote(target.Description()))
                    d['image'] = d['fullimage'] = target
                    d['tag'] = None
                    d['isfullsize'] = True
                    d['width'] = target.width
                    if srctail:
                        if isinstance(srctail, unicode):
                            srctail =srctail.encode('utf8') # restrictedTraverse doesn't accept unicode
                        try:
                            subtarget = target.restrictedTraverse(srctail)
                        except:
                            subtarget = getattr(target, srctail, None)
                        if subtarget is not None:
                            d['image'] = subtarget

                        if srctail.startswith('image_'):
                            d['tag'] = target.getField('image').tag(target, scale=srctail[6:])
                        elif subtarget:
                            d['tag'] = subtarget.tag()

                    if d['tag'] is None:
                        d['tag'] = target.tag()

                    if subtarget is not None:
                        d['isfullsize'] = subtarget.width == target.width and subtarget.height == target.height
                        d['width'] = subtarget.width

                    # strings that may contain non-ascii characters need to be decoded to unicode
                    for key in ('caption', 'tag'):
                        if isinstance(d[key], str):
                            d[key] = d[key].decode('utf8', 'replace')

                    if atag is not None: # Must preserve original link, don't overwrite with a link to the image
                        d['isfullsize'] = True
                        d['tag'] = "%s%s</a>" % (atag, d['tag'])

                    result = template(**d)
                    if isinstance(result, str):
                        result = result.decode('utf8')

                    return result

            return match.group(0) # No change

        if isinstance(data, str):
            # Transform for end user output should avoid erroring
            # if it can, so use 'replace' on decode.
            data = data.decode('utf8', 'replace')
        html = IMAGE_PATTERN.sub(replaceImage, data)

        # Replace urls that use UIDs with human friendly urls.
        def replaceUids(match):
            tag = match.group('tag')
            uid = match.group('uid')
            target = self.resolveuid(context, rc, uid)
            if target is not None:
                if getattr(aq_base(target), 'getRemoteUrl', None) is not None:
                    url = target.getRemoteUrl()
                else:
                    url = target.absolute_url_path()
                return tag + url
            return match.group(0)

        html = UID_PATTERN.sub(replaceUids, html)
        if isinstance(html, unicode):
            html = html.encode('utf8') # Indexing requires a string result.
        idata.setData(html)
        return idata

    # No context to use for replacements, so don't bother trying.
    idata.setData(data)
    return idata

# Patching
setattr(HTMLToCaptioned,'convert',convert)

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

def migrateContent(site,source,destination,destinationMeta):
    ct = site.portal_catalog    
    results = ct.searchResults(portal_type=source)
    for b in results:
        item = b.getObject()
        migrator = ATItemMigrator(item)
        migrator.dst_portal_type = destination
        migrator.dst_meta_type = destinationMeta
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
pt_origem = 'Blog Entry'
pt_destino = 'News Item'
mt_destino = 'ATNewsItem'
migrateContent(site,source=pt_origem,destination=pt_destino,destinationMeta=mt_destino)

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

# E para finalizar, limpamos o custom
site.portal_skins.custom.manage_delObjects(site.portal_skins.custom.objectIds())

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
