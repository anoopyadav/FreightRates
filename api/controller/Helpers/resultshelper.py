from datetime import date, datetime, timedelta
from decimal import Decimal
import json


def json_serial(obj):
    # custom serializer for objects
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, Decimal):
        return str(round(obj, 2))
    raise TypeError("Type %s not serializable" % type(obj))


def format_get_rates(cursor, begin, end):
    results = [dict((cursor.description[i][0], value)
                    for i, value in enumerate(row))
               for row in cursor.fetchall()
               ]
    results = fill_in_the_blanks(results, begin, end)

    return json.dumps(results, default=json_serial)


def both_ports_in_db(results):
    return results[0][0] == 2


def fill_in_the_blanks(results, begin, end):
    missing_days = set(get_date_range(begin, end)) - set([row['day'].isoformat() for row in results])
    for day in missing_days:
        results.append({'day': datetime.strptime(day, '%Y-%m-%d').date(), 'average_price': 'null'})

    return sorted(results, key=lambda k: k['day'])


def get_date_range(begin, end):
    # need date objects here
    begin = datetime.strptime(begin, '%Y-%m-%d').date()
    end = datetime.strptime(end, '%Y-%m-%d').date()
    return [(end - timedelta(days=x)).isoformat() for x in range(0, end.day - begin.day + 1)]