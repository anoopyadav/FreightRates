class RequestHandler:
    def __init__(self, app, db):
        self.db = db
        self.app = app
        self.STATUS_CODE_OK = 200
        self.STATUS_CODE_ERROR = 400

    def create_response(self, body, status_code):
        return self.app.response_class(
            response=body,
            status=status_code,
            mimetype='application/json'
        )

    def create_good_response(self, message):
        return self.create_response(message, self.STATUS_CODE_OK)

    def create_bad_response(self, message):
        return self.create_response(message, self.STATUS_CODE_ERROR)
