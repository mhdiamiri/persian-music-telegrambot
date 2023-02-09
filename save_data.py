import datetime

def save_data(user, search):
    try:
        f = open(str(user), 'a')
    except:
        f = open(str(user), 'w')
        
    dt = datetime.datetime.now()
    
    line = str(dt) + ', '+ search+ "\n"
    
    f.write(line)
    
    f.close()