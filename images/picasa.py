#-*- coding:utf-8 -*-
import gdata.photos.service
import gdata.media
import gdata.geo

# Configuracoes
gd_client = gdata.photos.service.PhotosService()
gd_client.email = 'pa2.macunaima@gmail.com'
gd_client.password = 'foobar'
gd_client.source = 'batchUpdate'
gd_client.ProgrammaticLogin()

username = 'pa2.macunaima'
keywords = 'Vereda da Salvação, Macunaíma, PA2, Macunaima'

albums = gd_client.GetUserFeed(user=username)
for album in albums.entry:
  if not 'Vereda' in album.title.text:
      continue
  print 'title: %s, number of photos: %s, id: %s' % (album.title.text,
      album.numphotos.text, album.gphoto_id.text)
  photos = gd_client.GetFeed(
    '/data/feed/api/user/%s/albumid/%s?kind=photo' % (
        username, album.gphoto_id.text))
  i = 0
  for photo in photos.entry:
     if not 'Vereda' in photo.title.text:
        photo.title.text = 'Vereda da Salvação (%s)' % photo.title.text
     #photo.summary.text = ''
     if not photo.media:
       photo.media = gdata.media.Group()
     if not photo.media.keywords:
       photo.media.keywords = gdata.media.Keywords()
     photo.media.keywords.text = keywords
     updated_entry = gd_client.UpdatePhotoMetadata(photo)
     i +=1