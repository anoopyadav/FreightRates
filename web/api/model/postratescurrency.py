import os
if 'local' in os.environ:
    from web.api.model.postrates import PostRatesRequest
else:
    from model.postrates import PostRatesRequest


class PostRatesCurrencyRequest(PostRatesRequest):
    def __init__(self, values):
        super().__init__(values)
        # case-insensitive indices
        values = dict((k.lower(), v) for k, v in values.items())
        self.currency_code = str.upper(values['currency_code']) if 'currency_code' in values.keys() else ''

    def __repr__(self):
        return 'PostRatesRequest(date_from={0}, date_to={1}, origin={2}, destination={3}, rate={4},' \
               ' currency{5})'.format(
                self.date_from, self.date_to, self.origin_code, self.destination_code, self.price, self.currency_code
                )
