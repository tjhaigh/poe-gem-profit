class Gem():
    """
    Base class for gems
    """

    _alt_quals = ['divergent', 'anomalous', 'phantasmal']
    profit = 0

    def __init__(self, data):
        """ Constructor
            Expects a dict of data to build from
        """

        self.name = data['name']
        self.details = data['detailsId']
        self.chaos_value = data['chaosValue']
        self.exalted_value = data['exaltedValue']
        self.count = data['count']

        self._process_variant(data['variant'])
        
        self.is_awakened = True if 'awakened' in self.details else False
        self.is_alt_quality = any((True for x in self._alt_quals if x in self.details))
        self.is_double_corrupted = self._check_double_corrupted()


    def _process_variant(self, variant):
        """ Set vals based on the 'variant' string
            this gives us gem level, quality, and corruption

            EG: '21/20c' is level 21, 20qual, and corrupted
        """
        
        # first check for corruption then remove the c to process gem level and qual
        if variant[-1] == 'c':
            self.corrupted = True
            variant = variant[:-1]
        else:
            self.corrupted = False

        if '/' in variant:
            x = variant.split('/')
            self.level = int(x[0])
            self.quality = int(x[1])
        else:
            self.quality = 0
            self.level = int(variant)


    def _check_double_corrupted(self):
        """ Checks for possible double corruptions:

            possibilities are:
                21/23q
                vaal+21 lv
                vaal+23q
                6/23q for awakened

        """
        
        if self.level == 21 and self.quality > 20:
            return True
        elif 'vaal' in self.details and (self.level == 21 or self.quality > 20):
            return True
        elif 'awakened' in self.details and (self.level == 6 and self.quality > 20):
            return True
        else:
            return False