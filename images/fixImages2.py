#-*- coding:utf-8 -*-
import os
import datetime
from hachoir_parser import createParser
from hachoir_metadata.jpeg import JpegMetadata
from hachoir_core.error import error, HACHOIR_ERRORS
from hachoir_core.endian import endian_name
from hachoir_metadata.metadata_item import (
    Data, MIN_PRIORITY, MAX_PRIORITY, QUALITY_NORMAL)

from hachoir_metadata.metadata import extractors
def extractMetadata(parser, quality=QUALITY_NORMAL):
    """
    Create a Metadata class from a parser. Returns None if no metadata
    extractor does exist for the parser class.
    """
    try:
        extractor = extractors[parser.__class__]
    except KeyError:
        return None
    metadata = extractor(quality)
    
    try:
        metadata.register(Data("keywords", 998, u"Keywords", type=unicode))
        metadata.extract(parser)
    except HACHOIR_ERRORS, err:
        error("Error during metadata extraction: %s" % unicode(err))
    if metadata:
        metadata.mime_type = parser.mime_type
        metadata.endian = endian_name[parser.endian]
    return metadata
        

quality = 1.0

IPTC_KEY_NEW = JpegMetadata.IPTC_KEY
IPTC_KEY_NEW[25] = "keywords"
IPTC_KEY_NEW[5] = "filename"
JpegMetadata.IPTC_KEY = IPTC_KEY_NEW

path_sou = '/Users/erico/Pictures/tmp/'
path_des = '/Users/erico/Pictures/Repositorio/'
fotos_sou = os.listdir(path_sou)
fotos_des = os.listdir(path_des)

source = []
destination = []

for foto in fotos_sou:
    tmpSou = 0
    tmpDes = 0
    filename_sou = '%s%s' % (path_sou,foto)
    parser_sou = createParser(unicode(filename_sou))
    metadata_sou = extractMetadata(parser_sou, quality)
    
    filename_des = '%s%s' % (path_des,foto)
    parser_des = createParser(unicode(filename_des))
    metadata_des = extractMetadata(parser_des, quality)
    
    
    if not metadata_sou:
        tmpDes += 10
        title_sou = ''
        latitude_sou = ''
        keywords_sou = []
    else:
        title_sou = metadata_sou.getValues('title')
        latitude_sou = metadata_sou.getValues('latitude')
        keywords_sou = metadata_sou.getValues('keywords')

    print keywords_sou
    if not metadata_des:
        tmpSou += 10
        title_des = ''
        latitude_des = ''
        keywords_des = []
    else:
        title_des = metadata_des.getValues('title')
        latitude_des = metadata_des.getValues('latitude')
        keywords_des = metadata_des.getValues('keywords')
    
    if title_sou:
        tmpSou += 1
    else:
        tmpDes += 1
    
    if latitude_sou:
        tmpSou += 1
    else:
        tmpDes += 1
    
    if len(keywords_sou)>len(keywords_des):
        tmpSou +=1
    
    if tmpSou > tmpDes:
        source.append(foto)
        os.rename(filename_sou,filename_des)
    else:
        destination.append(foto)
    
print len(source)
print len(destination)

print source
print destination