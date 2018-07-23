import json
import requests
from decimal import Decimal
from flask import jsonify
from api.controller.requesthandler import RequestHandler
from api.controller.Helpers import querieshelper, resultshelper
from api.model.postrates import PostRatesRequest
from api.model.postratescurrency import PostRatesCurrencyRequest


class PostRequestHandler(RequestHandler):
    def __init__(self, app, db):
        super().__init__(app, db)

    def handle_submit_rates(self, request):
        request = PostRatesRequest(request.values)

        if not self.verify_post_parameters(request):
            return self.create_bad_response('Bad Request')

        check_codes_sql = querieshelper.check_ports_query(request)
        cursor = self.db.cursor()

        cursor.execute(check_codes_sql)
        if not resultshelper.both_ports_in_db(cursor.fetchall()):
            return 'Supplied port codes are not supported'

        insert_price_sql = querieshelper.post_rates_query(request)
        cursor.execute(insert_price_sql)
        self.db.commit()
        return self.create_good_response(jsonify('Submitted'))

    def handle_submit_rates_with_currency(self, request):
        request = PostRatesCurrencyRequest(request.values)

        if not self.verify_post_currency_parameters(request):
            return self.create_bad_response('Bad Request')

        check_codes_sql = querieshelper.check_ports_query(request)
        cursor = self.db.cursor()

        cursor.execute(check_codes_sql)
        if not resultshelper.both_ports_in_db(cursor.fetchall()):
            return self.create_bad_response('Supplied port codes are not supported')

        # obtain latest currency information
        currency_rates = self.get_latest_currency_rates()

        if not self.is_valid_currency(request.currency_code, currency_rates):
            return self.create_bad_response("No information available for supplied \
                                    \currency")

        request.price = self.convert_to_usd(request.price,
                                            request.currency_code,
                                            currency_rates)

        insert_price_sql = querieshelper.post_rates_query(request)
        cursor.execute(insert_price_sql)
        self.db.commit()
        return self.create_good_response(jsonify('Submitted'))

    @staticmethod
    def verify_post_parameters(request):
        return request.date_to != '' and request.date_from != '' and\
            request.origin_code != '' and request.destination_code != '' \
            and request.origin_code != request.destination_code \
            and request.price is not None

    @staticmethod
    def verify_post_currency_parameters(request):
        return request.date_to != '' and request.date_from != '' and \
            request.origin_code != '' and request.destination_code != '' \
            and request.origin_code != request.destination_code \
            and request.price is not None and request.currency_code != ''

    @staticmethod
    def get_latest_currency_rates():
        payload = {'app_id': '00f48ee0b04b45b7b57d988bf3aaff3d'}
        currency_rates_json = requests.get(
            'https://openexchangerates.org/api/latest.json', payload)
        return json.loads(currency_rates_json.content.decode())['rates']

    @staticmethod
    def convert_to_usd(value, currency, currency_rates):
        return value / Decimal(currency_rates[currency])

    @staticmethod
    def is_valid_currency(currency_code, currency_rates):
        return currency_code in currency_rates.keys()

