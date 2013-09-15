import sys

def header(db, output):
    if(not db.isOpen() or output.closed):
        pass
        # TODO: Exception
    
    header = ""
    for field_name in db.fieldNames():
        header += field_name + ","
    
    output.write(header[:-1] + "\n")

def headerF(db, output, fields):
    if(not db.isOpen() or output.closed):
        pass
    # TODO: Exception
    
    header = ""
    for field_name in db.fieldNames():
        if(field_name in fields):
            header += field_name + ","
    
    output.write(header[:-1] + "\n")


def records(db, output, offset, records):
    if(not db.isOpen() or output.closed):
        pass
        # TODO: Exception
    
    for i in range(offset, offset + records):
        rec = db[i]
        
        rec_str = ""
        for fldName in db.fieldNames():
            rec_str += str(rec[fldName]) + ','
            
        output.write(rec_str[:-1] + "\n")

def recordsF(db, output, offset, records, fields):
    if(not db.isOpen() or output.closed):
        pass
    # TODO: Exception
    
    for i in range(offset, offset + records):
        rec = db[i]
        
        rec_str = ""
        for fldName in db.fieldNames():
            if(fldName in fields):
                rec_str += str(rec[fldName]) + ','
        
        output.write(rec_str[:-1] + "\n")

def recordsD(db, offset, records, fields, index_field):
    
    result = dict()
    
    for i in range(offset, offset + records):
        rec = db[i]
        
        if((i - offset) % (records / 50) is 0 and not i is offset):
            sys.stdout.write('.')
            sys.stdout.flush()
        
        record_dic = dict()
        result[rec[index_field]] = record_dic
        
        for fldName in db.fieldNames():
            if(fldName in fields):
                record_dic[fldName] = rec[fldName]
    return result

def recordsDF(db, offset, records, fields, index_field, filter):
    
    result = dict()
    
    for i in range(offset, offset + records):
        rec = db[i]
        
        if((i - offset) % (records / 50) is 0 and not i is offset):
            sys.stdout.write('.')
            sys.stdout.flush()
        
        include = ('true' == 'true')
        if(not filter is None):
            for fldName in db.fieldNames():
                if(fldName in filter):
                    include = include and (rec[fldName] in filter[fldName])
                
        if(include):
            record_dic = dict()
            result[rec[index_field]] = record_dic
        
            for fldName in db.fieldNames():
                if(fldName in fields):
                    record_dic[fldName] = rec[fldName]
    return result

