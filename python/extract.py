#!/usr/bin/env python

# Import Psyco if available
try:
    import psyco
    psyco.full()
except ImportError:
    pass

from dbfpy.dbf import Dbf
from constants.extensions import CSV

import sys
import parser

straatnm_dbf = sys.argv[1] + 'straatnm.dbf'
huisnr_dbf = sys.argv[1] + 'huisnr.dbf'
pkancode_dbf = sys.argv[1] + 'pkancode.dbf'
gemnm_dbf = sys.argv[1] + 'gemnm.dbf'
gem_dbf = sys.argv[1] + 'gem.dbf'
tobjhnr_dbf = sys.argv[1] + 'tobjhnr.dbf'
terrobj_dbf = sys.argv[1] + 'terrobj.dbf'

postal_code = 0
if(len(sys.argv) > 2):
    postal_code = int(sys.argv[2])

print 'Filtering on postalcode: ' + str(postal_code)

# parse & index pkancode
huisnr_dic = dict()

print 'Extracting pkancode'
db = Dbf()
db.openFile(pkancode_dbf, readOnly = 1)
record_count = db.recordCount()

for i in range(0, record_count):
    rec = db[i]
    
    if(i % (record_count / 50) is 0 and not i is 0):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    huisnr_id = rec['HUISNRID']
    pkancode = rec['PKANCODE']

    if(pkancode == postal_code or postal_code is 0):
        huisnr_dic[huisnr_id] = dict()
        huisnr_dic[huisnr_id]['PKANCODE'] = pkancode

print ''

# parse & index tobjhnr
print 'Extracting tobjhnr'
terrobj_to_huirnr_id = dict()
db = Dbf()
db.openFile(tobjhnr_dbf, readOnly = 1)
record_count = db.recordCount()

for i in range(0, record_count):
    rec = db[i]
    
    if((i) % (record_count / 50) is 0 and not i is 0):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    huisnr_id = rec['HUISNRID']
    if(huisnr_id in huisnr_dic):
        terrobj_to_huirnr_id[rec['TERROBJID']] = huisnr_id

print ''

# parse & index terrobj
print 'Extracting terrobj'
db = Dbf()
db.openFile(terrobj_dbf, readOnly = 1)
record_count = db.recordCount()

for i in range(0, record_count):
    rec = db[i]
    
    if((i) % (record_count / 50) is 0 and not i is 0):
        sys.stdout.write('.')
        sys.stdout.flush()
    
    terrobj_id = rec['ID']
    if(terrobj_id in terrobj_to_huirnr_id):
        huisnr_id = terrobj_to_huirnr_id[terrobj_id]
        huisnr_dic[huisnr_id]['X'] = rec['X']
        huisnr_dic[huisnr_id]['Y'] = rec['Y']
print ''

# parse & index huisnr
print 'Extracting huisnr'
db = Dbf()
db.openFile(huisnr_dbf, readOnly = 1)
record_count = db.recordCount()

for i in range(0, record_count):
    rec = db[i]
    
    if((i) % (record_count / 50) is 0 and not i is 0):
        sys.stdout.write('.')
        sys.stdout.flush()

    huisnr_id = rec['ID']
    if(huisnr_id in huisnr_dic):
        huisnr_dic[huisnr_id]['STRAATNMID'] = rec['STRAATNMID']
        huisnr_dic[huisnr_id]['HUISNR'] = rec['HUISNR']

print ''

# parse & index straatnm
print 'Extracting straatnm:'
db = Dbf()
db.openFile(straatnm_dbf, readOnly = 1)
record_count = db.recordCount()

fields = [ 'STRAATNM', 'TAALCODE', 'NISGEMCODE', 'STRAATNM2', 'TAALCODE2' ]
straatnm_dic = parser.recordsD(db, 0, record_count, fields, 'ID')

db.close()
print ''

# index per ID and extract lanuages.
straatnm_lang_dic = dict()

for(straatnm_id, straatnm_fields) in straatnm_dic.items():
    straatnm_lang_dic[straatnm_id] = dict()
    straatnm_lang_dic[straatnm_id]['NISGEMCODE'] = straatnm_fields['NISGEMCODE']
    straatnm_lang_dic[straatnm_id]['NAME_NL'] = ''
    straatnm_lang_dic[straatnm_id]['NAME_FR'] = ''
    straatnm_lang_dic[straatnm_id]['NAME_DE'] = ''
    
    if(len(straatnm_fields['TAALCODE']) > 0):
        straatnm_lang_dic[straatnm_id]['NAME_' + straatnm_fields['TAALCODE'].upper()] = straatnm_fields['STRAATNM']
    if(len(straatnm_fields['TAALCODE2']) > 0):
        straatnm_lang_dic[straatnm_id]['NAME_' + straatnm_fields['TAALCODE2'].upper()] = straatnm_fields['STRAATNM2']

del straatnm_dic

for (huisnr_id, huisnr_fields) in huisnr_dic.items():
    straatnm_id = huisnr_fields['STRAATNMID']

    huisnr_fields['NISGEMCODE'] = straatnm_lang_dic[straatnm_id]['NISGEMCODE']
    huisnr_fields['STREET_NL'] = straatnm_lang_dic[straatnm_id]['NAME_NL']
    huisnr_fields['STREET_FR'] = straatnm_lang_dic[straatnm_id]['NAME_FR']
    huisnr_fields['STREET_DE'] = straatnm_lang_dic[straatnm_id]['NAME_DE']

# parse & index gem
print 'Extracting gem:'
db = Dbf()
db.openFile(gem_dbf, readOnly = 1)
record_count = db.recordCount()

fields = [ 'NISGEMCODE']
gem_dic = parser.recordsD(db, 0, record_count, fields, 'ID')

db.close()
print ''

# parse & index gemnm
print 'Extracting gemnm:'
db = Dbf()
db.openFile(gemnm_dbf, readOnly = 1)
record_count = db.recordCount()

fields = [ 'GEMID', 'TAALCODE', 'GEMNM' ]
gemnm_dic = parser.recordsD(db, 0, record_count, fields, 'ID')

db.close()
print ''

# index per NISGEMCODE and extract languages.
gemnm_lang_dic = dict()

for (gemnm_id, gemnm_fields) in gemnm_dic.items():
    gem_id = gemnm_fields['GEMID']
    niscode = gem_dic[gem_id]['NISGEMCODE']
    if(not niscode in gemnm_lang_dic):
        gemnm_lang_dic[niscode] = dict()
        gemnm_lang_dic[niscode]['NAME_NL'] = ''
        gemnm_lang_dic[niscode]['NAME_FR'] = ''
        gemnm_lang_dic[niscode]['NAME_DE'] = ''
    
    lang_field_name = 'NAME_' + gemnm_fields['TAALCODE'].upper()
    
    gemnm_lang_dic[niscode][lang_field_name] = gemnm_fields['GEMNM']

del gemnm_dic
del gem_dic



for (huisnr_id, huisnr_fields) in huisnr_dic.items():
    niscode = huisnr_fields['NISGEMCODE']
        
    huisnr_fields['COMMUNE_NL'] = gemnm_lang_dic[niscode]['NAME_NL']
    huisnr_fields['COMMUNE_FR'] = gemnm_lang_dic[niscode]['NAME_FR']
    huisnr_fields['COMMUNE_DE'] = gemnm_lang_dic[niscode]['NAME_DE']

for (huisnr_id, huisnr_fields) in huisnr_dic.items():
    print huisnr_fields