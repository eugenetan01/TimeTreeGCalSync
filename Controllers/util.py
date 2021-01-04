import iso8601
import pytz

def dateTimeConverter(dateStr):
    _date_obj=iso8601.parse_date(dateStr)
    _date_utc=_date_obj.astimezone(pytz.utc)
    _date_utc_zformat=_date_utc.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    return _date_utc_zformat