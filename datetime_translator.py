import dateutil.parser
from datetime import datetime as dt
from datetime import timezone

def handle_plural(amount, units):
    if amount == 1:
        return('1 ' + units)
    else:
        return(str(amount) + ' ' + units + 's')

def translate(datetime):
    now = dt.now(timezone.utc)
    time = dateutil.parser.isoparse(datetime)

    difference = now - time
    days = difference.days
    hours = difference.seconds // 3600
    minutes = (difference.seconds // 60) % 60

    if days > 0:
        return(handle_plural(days, 'day'))
    elif hours > 0:
        return(handle_plural(hours, 'hour'))
    else:
        return(handle_plural(minutes, 'minute'))
