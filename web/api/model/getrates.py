class GetRatesRequest:
    def __init__(self, values):
        # case-insensitive indices
        values = dict((k.lower(), v) for k, v in values.items())

        self.date_from = values['date_from']
        self.date_to = values['date_to']
        self.origin = values['origin']
        self.destination = values['destination']

    def __repr__(self):
        return 'PostRatesRequest(date_from={0}, date_to={1}, origin={2}, destination={3})'.format(
            self.date_from, self.date_to, self.origin, self.destination
        )
