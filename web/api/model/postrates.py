from decimal import Decimal


class PostRatesRequest:
    def __init__(self, values):
        # case-insensitive indices
        values = dict((k.lower(), v) for k, v in values.items())

        self.date_from = values['date_from'] if 'date_from' in values.keys() else ''
        self.date_to = values['date_to'] if 'date_to' in values.keys() else ''
        self.origin_code = values['origin_code'] if 'origin_code' in values.keys() else ''
        self.destination_code = values['destination_code'] if 'destination_code' in values.keys() else ''
        self.price = Decimal(values['price'].strip(' "')) if self.is_number(values['price']) else None

    def __repr__(self):
        return 'PostRatesRequest(date_from={0}, date_to={1}, origin={2}, destination={3}, rate={4})'.format(
            self.date_from, self.date_to, self.origin_code, self.destination_code, self.price
        )

    @staticmethod
    def is_number(numeric_string):
        try:
            float(numeric_string)
            return True
        except ValueError:
            return False



