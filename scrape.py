import shutil

import requests

import GW_Library

import json
import xml.etree.ElementTree as ET


class DeckEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, GW_Library.Card):
            return o.__dict__
        return json.dumps(o)


if __name__ == '__main__':
    gw_library = GW_Library.Library()
    with open('library.json', 'w') as f:
        json.dump(gw_library.library, f, cls=DeckEncoder)

    root = ET.Element("cards")
    for card in gw_library.library:
        node = ET.SubElement(root, "card")
        node.set("id", str(gw_library.library[card].id))
        node.set("title", str(gw_library.library[card].title))
        node.set("set", str(gw_library.library[card].set))
        node.set("warband", str(gw_library.library[card].warband))
        node.set("type", str(gw_library.library[card].type))
        node.set("image", str(gw_library.library[card].image))

        with open('images/c' + str(card) + ".png", 'wb') as f:
            url = gw_library.library[card].image
            response = requests.get(url, stream=True)
            shutil.copyfileobj(response.raw, f)
