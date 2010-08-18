#-*- coding:utf-8 -*-
import os
import datetime
from hachoir_parser import createParser
from hachoir_metadata import extractMetadata
quality = 1.0

path = '/Users/erico/Pictures/tmp/'
fotos = os.listdir(path)

def newName(filename):
    
    parser = createParser(unicode(filename))
    metadata = extractMetadata(parser, quality)
    if metadata.getValues('creation_date'):
        name = metadata.getValues('creation_date')[0].strftime('%Y%m%d%H%M%S')
    else:
        name = datetime.datetime.fromtimestamp(os.stat(filename).st_ctime).strftime('%Y%m%d%H%M%S')
    return name


for foto in fotos:
    name = foto.split('.')
    if len(name)==1 or (name[-1].lower() not in ['jpg','jpeg','png']):
        continue
    filename = '%s/%s' % (path,foto)
    new_name = '%s/%s' % (path,newName(filename))
    if new_name == ('%s/' % path):
        continue
    name_collision = True
    i = 1
    while name_collision:
        new_name = '%s%02d' % (new_name,i)
        name_collision = os.access('%s.jpg' % new_name,os.F_OK)
        if name_collision:
            new_name = new_name[:-2]
            i+=1
    
    os.rename(filename,'%s.jpg' % new_name)
    print new_name
