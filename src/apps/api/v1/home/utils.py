from datetime import datetime



def get_beginning_day():
    date = datetime.now()
    beginning_day = date.replace(second=0, microsecond=0, minute=0, hour=0)
    
    return int(beginning_day.timestamp())

def get_ending_day():
    unix_day = 86400
    beginning_day = get_beginning_day()
    
    return beginning_day + unix_day