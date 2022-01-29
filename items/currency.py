class Currency:
    """ Class for currency items
    """

    def __init__(self, data):
        self.name = data['currencyTypeName']
        self.details = data['detailsId']
        self.chaos_value = data['chaosEquivalent']