import calendar
import datetime


def unixts():
    return calendar.timegm(datetime.datetime.utcnow().timetuple())
