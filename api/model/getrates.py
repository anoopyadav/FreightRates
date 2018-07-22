from api.model.request import Request


class GetRatesRequest(Request):
    def __init__(self, values):
        super().__init__(values)
        values = dict((k.lower(), v) for k, v in values.items())
        self.origin_code = values['origin'] if 'origin' in values.keys() else ''
        self.destination_code = values['destination'] if 'destination' in values.keys() else ''

    def __repr__(self):
        return 'PostRatesRequest(date_from={0}, date_to={1}, origin={2}, destination={3})'.format(
            self.date_from, self.date_to, self.origin_code, self.destination_code
        )
