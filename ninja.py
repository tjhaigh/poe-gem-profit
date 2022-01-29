# This handles all the interaction with the poe ninja api

import requests
import json
from items import Gem, Currency

class Ninja:
    """
    Makes requests to various 
    """
    _ninja_base_url_item = 'https://poe.ninja/api/data/itemoverview'
    _ninja_base_url_currency = 'https://poe.ninja/api/data/currencyoverview'
    _valid_leagues = ['Standard', 'Scourge']

    def __init__(self, league='Standard'):
        self.league = league

    @property
    def league(self):
        return self._league
    
    @league.setter
    def league(self, league):
        if league.capitalize() in self._valid_leagues:
            self._league = league.capitalize()
        else:
            raise ValueError('League name: ' + league + ' is not a member of valid leagues')


    def _make_request(self, url, item_type):
        """ Makes a request to the ninja api and returns json output

        Args:
            url (str): The url to search request on (it's different for items and currency)
            item_type (str): The type of search to be made

        Returns: Json response from poe ninja or empty string on failed request
        """

        params = {'league': self.league, 'type': item_type}
        r = requests.get(url, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return ''


    def get_skill_gems(self):
        """ Return a list of Gems

        """

        items = self._make_request(self._ninja_base_url_item, 'SkillGem')

        gems = []
        for item in items['lines']:
            gems.append(Gem(item))


        return gems

    def get_currency(self):
        """ Return a list of Currency
        """

        items = self._make_request(self._ninja_base_url_currency, 'Currency')

        currency = []
        for item in items['lines']:
            currency.append(Currency(item))

        return currency
