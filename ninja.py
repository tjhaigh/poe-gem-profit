# This handles all the interaction with the poe ninja api

import requests

class Ninja:
    """
    Makes requests to various 
    """
    _ninja_base_url = 'https://poe.ninja/api/data/itemoverview'
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


    def _make_request(self, item_type):
        """ Makes a request to the ninja api and returns json output

        Args:
            Type (str): The type of search to be made

        Returns: Json response from poe ninja or empty string on failed request
        """

        params = {'league': self.league, 'type': item_type}
        r = requests.get(self._ninja_base_url, params=params)
        if r.status_code == requests.codes.ok:
            return r.json()
        else:
            return ''

    def get_skill_gems(self):
        return self._make_request('SkillGem')
