from api.controller.Helpers import querieshelper, resultshelper
from api.controller.requesthandler import RequestHandler
from api.model.getrates import GetRatesRequest
from api.model.getrequesttype import GetRequestType


class GetRequestHandler(RequestHandler):
    def __init__(self, app, db):
        super().__init__(app, db)

    def handle_get_rates(self, get_request, request_type):
        get_rates_request = GetRatesRequest(get_request.args)

        if not self.verify_get_parameters(get_rates_request):
            return self.create_bad_response('Bad Request')

        if request_type is GetRequestType.GetRequest:
            sql = querieshelper.get_rates_query(get_rates_request)
        elif request_type is GetRequestType.GetRequestNull:
            sql = querieshelper.get_rates_query_null(get_rates_request)

        cursor = self.db.cursor()

        cursor.execute(sql)
        results = resultshelper.format_get_rates(
            cursor, get_rates_request.date_from, get_rates_request.date_to)
        return self.create_good_response(results)

    def verify_get_parameters(self, request):
        return request.date_to != '' and request.date_from != '' and \
            request.origin_code != '' and request.destination_code != '' \
            and request.origin_code != request.destination_code
