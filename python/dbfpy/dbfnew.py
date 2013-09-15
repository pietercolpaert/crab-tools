#!/usr/bin/python

'''\
modul to create a dbf file

added by Hans Fiby June 2000


Example Usage:
  see test at the end

This module cannot handle Memo-fields, they are special.
Maybe I will add that sometime.

'''


class dbf_new:
    debug=None
    def __init__(self):
        self.fields=[]
        return None
    def add_field(self,name,typ,len,dec=0):
        self.fields.append([name,typ,len,dec])
    def write(self,filename):
        dbfh=DbfHeader()
        dbfh.setCurrentDate()
        for f in self.fields:
            if f[1]== 'N':
                dbf_f=DbfNumericFieldDef()
                dbf_f.decimalCount =f[3]
            elif f[1]== 'L':
                dbf_f=DbfLogicalFieldDef()
                dbf_f.decimalCount =0
            elif f[1]== 'D':
                dbf_f=DbfDateFieldDef()
                dbf_f.decimalCount =0
                # force length = 8
                f[2]=8
            else:
                dbf_f=DbfCharacterFieldDef()
                dbf_f.decimalCount =0
            dbf_f.length=f[2]
            dbf_f.name=f[0]
            dbfh.addFieldDef(dbf_f)
            dbfh.recordLength = dbfh.recordLength+dbf_f.length
        dbfh.recordLength = dbfh.recordLength+1
        dbfh.headerLength = 32+(32*len(dbfh.fieldNames))+1
        dbfStream = open(filename,"wb")
        dbfh.writeOn(dbfStream)
        dbfStream.close()
        
        
if (__name__=='__main__'):
    ''' test dbf_new '''
    # create a new DBF-File 
    from dbf import *
    dbfn=dbf_new()
    dbfn.add_field("name",'C',80)
    dbfn.add_field("price",'N',10,2)
    dbfn.add_field("date",'D',8)
    dbfn.write("tst.dbf")
    # test new dbf
    print "*** created tst.dbf: ***"
    dbft = Dbf()
    dbft.openFile('tst.dbf', readOnly=0)
    dbft.reportOn()
    # add a record
    rec=DbfRecord(dbft)
    rec['name']='something'
    rec['price']=10.5
    rec['date']=(2000,1,12)
    rec.store()
    # add another record
    rec=DbfRecord(dbft)
    rec['name']='foo and bar'
    rec['price']=12234
    rec['date']=(1992,7,15)
    rec.store()
    
    # show the records
    print "*** inserted 2 records into tst.dbf: ***"
    dbft.reportOn()
    for i1 in range(len(dbft)):
        rec = dbft[i1]
        for fldName in dbft.fieldNames():
            print '%s:\t %s'%(fldName, rec[fldName])
        print
    dbft.close()

   
