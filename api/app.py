from flask import Flask, request, g
from api.controller.Helpers import dbhelper
from api.model.getrequesttype import GetRequestType
from api.controller.getrequesthandler import GetRequestHandler
from api.controller.postrequesthandler import PostRequestHandler


app = Flask(__name__)

if __name__ == "__main__":
    app.run()


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
    handler = GetRequestHandler(app, g.db)
    return handler.handle_get_rates(request, GetRequestType.GetRequest)


@app.route('/rates_null')
def get_average_rates_null():
    handler = GetRequestHandler(app, g.db)
    return handler.handle_get_rates(request, GetRequestType.GetRequestNull)


@app.route('/submit_rate', methods=['POST'])
def submit_rate():
    handler = PostRequestHandler(app, g.db)
    return handler.handle_submit_rates(request)


@app.route('/submit_rate_currency', methods=['POST'])
def submit_rate_with_currency():
    handler = PostRequestHandler(app, g.db)
    return handler.handle_submit_rates_with_currency(request)
