from datetime import datetime

def get_current_date():

    return datetime.now().strftime("%d %B %Y")


def get_current_time():

    return datetime.now().strftime("%I:%M %p")