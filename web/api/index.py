from flask import Flask, request, g
import os
if 'local' in os.environ:
    from web.api.controller import DbHelper
    from web.api.controller.Helpers import QueriesHelper
    from web.api.model.getrates import GetRatesRequest
    from web.api.model.postrates import PostRatesRequest
    from web.api.controller.Helpers import resultshelper
    port = 5001
else:
    from controller import DbHelper
    from controller.Helpers import QueriesHelper
    from model.getrates import GetRatesRequest
    from model.postrates import PostRatesRequest
    from controller.Helpers import resultshelper
    port = 5000
app = Flask(__name__)


def connect_db():
    return DbHelper.connect_db()


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

    sql = QueriesHelper.get_rates_query(get_rates_request)
    cursor = g.db.cursor()

    cursor.execute(sql)
    results = resultshelper.format_get_rates(cursor, get_rates_request.date_from, get_rates_request.date_to)
    return results


@app.route('/rates_null')
def get_average_rates_null():
    get_rates_request = GetRatesRequest(request.args)

    if not verify_get_parameters(get_rates_request):
        return 'Bad Request'

    sql = QueriesHelper.get_rates_query_null(get_rates_request)
    cursor = g.db.cursor()

    cursor.execute(sql)
    results = resultshelper.format_get_rates_null(cursor, get_rates_request.date_from, get_rates_request.date_to)
    return results


@app.route('/submit_rate', methods=['POST'])
def submit_rate():
    post_rates_request = PostRatesRequest(request.values)

    if not verify_post_parameters(post_rates_request):
        return 'Bad Request'

    check_codes_sql = QueriesHelper.check_ports_query(post_rates_request)
    cursor = g.db.cursor()

    cursor.execute(check_codes_sql)
    if not resultshelper.both_ports_in_db(cursor.fetchall()):
        return 'Supplied codes are not supported'

    insert_price_sql = QueriesHelper.post_rates_query(post_rates_request)
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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
