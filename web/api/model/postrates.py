from decimal import Decimal
from datetime import datetime
import os
if 'local' in os.environ:
    from web.api.model.request import Request
else:
    from model.request import Request


class PostRatesRequest(Request):
    def __init__(self, values):
        super().__init__(values)
        # case-insensitive indices
        values = dict((k.lower(), v) for k, v in values.items())
        self.price = Decimal(values['price'].strip(' "')) if self.is_number(values['price']) else None

    def __repr__(self):
        return 'PostRatesRequest(date_from={0}, date_to={1}, origin={2}, destination={3}, rate={4})'.format(
            self.date_from, self.date_to, self.origin_code, self.destination_code, self.price
        )
