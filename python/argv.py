from constants.extensions import DBF, CSV

def input(argv):
    file_name = argv[1].strip() 
    
    # Add extension if missing
    pos = file_name.lower().find(DBF)
    if(pos == -1):
        file_name += DBF
    
    return file_name 

def output(argv):
    file_name = argv[2].strip()
    
    # Remove extension if found
    pos = file_name.lower().find(CSV)
    if(pos != -1):
        file_name = file_name[:pos]
        
    return file_name
    
def page_size(argv):
    size = 0
    if (len(argv) > 3):
       size = int(argv[3])
    
    return int(size)
