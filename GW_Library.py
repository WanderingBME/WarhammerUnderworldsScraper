import json
import os.path
import pickle
import requests


class Card:
    id = -1
    title = ''
    set = ''
    warband = ''
    type = ''
    image = ''

    def __init__(self, card):
        self.id = card['id']
        self.title = card['title']
        self.set = card['set']
        self.warband = card['warband']
        self.type = card['type']
        self.image = card['image']

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return self.title


class Objective(Card):
    def __init__(self, card):
        if card['type'] != 'objective':
            raise ValueError('Objective instantiated with non-objective card')
        Card.__init__(self, card)


class Ploy(Card):
    def __init__(self, card):
        if card['type'] != 'ploy':
            raise ValueError('Objective instantiated with non-objective card')
        Card.__init__(self, card)

class Gambit(Card):
    def __init__(self, card):
        if card['type'] != 'gambit spell':
            raise ValueError('Objective instantiated with non-objective card')
        Card.__init__(self, card)


class Upgrade(Card):
    def __init__(self, card):
        if card['type'] != 'upgrade':
            raise ValueError('Objective instantiated with non-objective card')
        Card.__init__(self, card)


class Character(Card):
    def __init__(self, card):
        if card['type'] != 'character':
            raise ValueError('Objective instantiated with non-objective card')
        Card.__init__(self, card)


class Library:
    library_file = 'library.pickle'
    library = {}
    warbands = {}
    sets = {}

    def __init__(self, reload=False):
        if not reload and os.path.exists(self.library_file):
            with open(self.library_file, 'rb')as f:
                self.library = pickle.load(f)
        else:
            response = requests.get('https://warhammerunderworlds.com/wp-json/wp/v2/cards/?ver=13&per_page=1000')
            cards = json.loads(response.text)
            response = requests.get('https://warhammerunderworlds.com/wp-json/wp/v2/warbands/?ver=10&per_page=100')
            warbands = {w['id']: w['name'] for w in json.loads(response.text)}
            response = requests.get('https://warhammerunderworlds.com/wp-json/wp/v2/sets/?ver=12&per_page=100')
            sets = {s['id']: s['name'] for s in json.loads(response.text)}
            response = requests.get('https://warhammerunderworlds.com/wp-json/wp/v2/card_types/?ver=11&per_page=100')
            types = {t['id']: t['name'] for t in json.loads(response.text)}

            card_objects = {'objective': Objective, 'ploy': Ploy, 'upgrade': Upgrade, 'gambit spell': Gambit}
            for card in cards:
                card_id = card['id']
                card_title = card['title']
                card_warbands = [warbands[w].replace('’', '\'') for w in card['warbands']]
                card_sets = [sets[s] for s in card['sets']]
                card_types = [types[t] for t in card['card_types']]
                card_image = card['acf']['card_image']['url']
                card_dict = {'id': int(card_id), 'title': card_title, 'type': card_types[0].lower(), 'set': card_sets[0],
                             'warband': card_warbands[0], 'image': card_image}
                self.library[int(card_id)] = card_objects[card_dict['type']](card_dict)

        self.warbands = list(set(self.library[c]['warband'] for c in self.library))
        self.sets = list(set(self.library[c]['set'] for c in self.library))
