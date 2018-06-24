from flask import Flask, request, g
import os
import requests
import json
from decimal import Decimal
if 'local' in os.environ:
    from web.api.controller import dbhelper
    from web.api.controller.Helpers import querieshelper
    from web.api.model.getrates import GetRatesRequest
    from web.api.model.postrates import PostRatesRequest
    from web.api.model.postratescurrency import PostRatesCurrencyRequest
    from web.api.controller.Helpers import resultshelper
    port = 5001
else:
    from controller import DbHelper
    from controller.Helpers import QueriesHelper
    from model.getrates import GetRatesRequest
    from model.postrates import PostRatesRequest
    from model.postratescurrency import PostRatesCurrencyRequest
    from controller.Helpers import resultshelper
    port = 5000
app = Flask(__name__)


def connect_db():
    return dbhelper.connect_db()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/rates')
def get_average_rates():
    get_rates_request = GetRatesRequest(request.args)

    if not verify_get_parameters(get_rates_request):
        return 'Bad Request'

    sql = querieshelper.get_rates_query(get_rates_request)
    cursor = g.db.cursor()

    cursor.execute(sql)
    results = resultshelper.format_get_rates(cursor, get_rates_request.date_from, get_rates_request.date_to)
    return results


@app.route('/rates_null')
def get_average_rates_null():
    get_rates_request = GetRatesRequest(request.args)

    if not verify_get_parameters(get_rates_request):
        return 'Bad Request'

    sql = querieshelper.get_rates_query_null(get_rates_request)
    cursor = g.db.cursor()

    cursor.execute(sql)
    results = resultshelper.format_get_rates_null(cursor, get_rates_request.date_from, get_rates_request.date_to)
    return results


@app.route('/submit_rate', methods=['POST'])
def submit_rate():
    post_rates_request = PostRatesRequest(request.values)

    if not verify_post_parameters(post_rates_request):
        return 'Bad Request'

    check_codes_sql = querieshelper.check_ports_query(post_rates_request)
    cursor = g.db.cursor()

    cursor.execute(check_codes_sql)
    if not resultshelper.both_ports_in_db(cursor.fetchall()):
        return 'Supplied port codes are not supported'

    insert_price_sql = querieshelper.post_rates_query(post_rates_request)
    cursor.execute(insert_price_sql)
    g.db.commit()
    return 'Submitted'


@app.route('/submit_rate_currency', methods=['POST'])
def submit_rate_with_currency():
    post_rates_currency_request = PostRatesCurrencyRequest(request.values)

    if not verify_post_currency_parameters(post_rates_currency_request):
        return 'Bad Request'

    check_codes_sql = querieshelper.check_ports_query(post_rates_currency_request)
    cursor = g.db.cursor()

    cursor.execute(check_codes_sql)
    if not resultshelper.both_ports_in_db(cursor.fetchall()):
        return 'Supplied port codes are not supported'

    # obtain latest currency information
    currency_rates = get_latest_currency_rates()

    if not is_valid_currency(post_rates_currency_request.currency_code, currency_rates):
        return 'No information available for supplied currency'

    post_rates_currency_request.price = convert_to_usd(post_rates_currency_request.price,
                                                       post_rates_currency_request.currency_code,
                                                       currency_rates)

    insert_price_sql = querieshelper.post_rates_query(post_rates_currency_request)
    cursor.execute(insert_price_sql)
    g.db.commit()
    return 'Submitted'


def verify_get_parameters(get_rates_request):
    return get_rates_request.date_to != '' and get_rates_request.date_from != '' and get_rates_request.origin != '' and \
           get_rates_request.destination != ''


def verify_post_parameters(post_rates_request):
    return post_rates_request.date_to != '' and post_rates_request.date_from != '' and\
           post_rates_request.origin_code != '' and post_rates_request.destination_code != ''\
           and post_rates_request.price is not None


def verify_post_currency_parameters(post_rates_request):
    return post_rates_request.date_to != '' and post_rates_request.date_from != '' and\
           post_rates_request.origin_code != '' and post_rates_request.destination_code != ''\
           and post_rates_request.price is not None and post_rates_request.currency_code != ''


def get_latest_currency_rates():
    payload = {'app_id': '00f48ee0b04b45b7b57d988bf3aaff3d'}
    currency_rates_json = requests.get('https://openexchangerates.org/api/latest.json', payload)
    return json.loads(currency_rates_json.content.decode())['rates']


def convert_to_usd(value, currency, currency_rates):
    return value / Decimal(currency_rates[currency])


def is_valid_currency(currency_code, currency_rates):
    return currency_code in currency_rates.keys()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
