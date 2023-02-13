#!/usr/bin/env python3
import json

# load JSON files
print("Loading JSON Input Files...")

with open("AllPrintings.json", "r") as f:
  all_printings = json.loads(f.read())

with open("AllPrices.json", "r") as f:
  all_prices = json.loads(f.read())

# prepare card locale lookup table
print("Building Locale Lookup JSON...")
locales = {}

for set_id in all_printings["data"].keys():
  for card in all_printings["data"][set_id]["cards"]:
    # prepare card locale table
    if not card["name"] in locales:
      locales[card["name"]] = {}

    lcard = locales[card["name"]]

    # english
    language = "English"

    if not language in lcard:
      lcard[language] = { "name": [], "text": [], "type": [], "flavor": [] }

    if not card.get('name') in lcard[language]["name"]:
      lcard[language]["name"].append(card.get('name'))

    if not card.get('type') in lcard[language]["type"]:
      lcard[language]["type"].append(card.get('type'))

    if not card.get('text') in lcard[language]["text"]:
      lcard[language]["text"].append(card.get('text'))

    if not card.get('flavorText') in lcard[language]["flavor"]:
      lcard[language]["flavor"].append(card.get('flavorText'))

    # other locales
    for card in card['foreignData']:
      language = card["language"]

      if not language in lcard:
        lcard[language] = { "name": [], "text": [], "type": [], "flavor": [] }

      if not card.get('name') in lcard[language]["name"]:
        lcard[language]["name"].append(card.get('name'))

      if not card.get('type') in lcard[language]["type"]:
        lcard[language]["type"].append(card.get('type'))

      if not card.get('text') in lcard[language]["text"]:
        lcard[language]["text"].append(card.get('text'))

      if not card.get('flavorText') in lcard[language]["flavor"]:
        lcard[language]["flavor"].append(card.get('flavorText'))

# build macaco-metadata
print("Building Card Metadata JSON...")
metadata = {}

for set_id in all_printings["data"].keys():
  for card in all_printings["data"][set_id]["cards"]:
    # make all card numbers uppercase
    number = card["number"].upper()

    # create set if not existing
    if not set_id in metadata:
      metadata[set_id] = {}

    if not number in metadata[set_id]:
      metadata[set_id][number] = {}

    # read price data
    prices = [ 0, 0, 0, 0 ]

    try:
      # obtain cardkingdom card prices [normal]
      for date in all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["normal"]:
        prices[0] = all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["normal"][date]
    except:
      pass

    try:
      # obtain cardkingdom card prices [foil]
      for date in all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["foil"]:
        prices[1] = all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["foil"][date]
    except:
      pass

    try:
      # obtain cardmarket card prices [normal]
      for date in all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["normal"]:
        prices[2] = all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["normal"][date]
    except:
      pass

    try:
      # obtain cardmarket card prices [foil]
      for date in all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["foil"]:
        prices[3] = all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["foil"][date]
    except:
      pass

    # read/write basic card data
    mcard = metadata[set_id][number]
    mcard["name"] = card.get('name')
    mcard['artist'] = card.get('artist')
    mcard['color'] = card.get('colors')
    mcard['identity'] = card.get('colorIdentity')
    mcard['cmc'] = card.get('convertedManaCost')
    mcard['mana'] = card.get('manaCost')
    mcard['rarity'] = card.get('rarity')
    mcard['power'] = card.get('power')
    mcard['toughness'] = card.get('toughness')
    mcard['scryfall'] = card["identifiers"].get('scryfallId')
    mcard['uuid'] = card.get('uuid')
    mcard["prices"] = prices

    # write locales
    mcard["locales"] = {}
    locale = locales[card['name']]

    # add all possible fallback language data
    for language in locale:
      mcard["locales"][language] = {}
      mcard["locales"][language]["name"] = 0
      mcard["locales"][language]["text"] = 0
      mcard["locales"][language]["type"] = 0
      mcard["locales"][language]["flavor"] = 0
      mcard["locales"][language]["multiverse"] = 0

    language = "English"
    locale_entry = locale[language]

    # set english locale to the appropriate index
    mcard["locales"][language] = {}
    mcard["locales"][language]["name"] = locale_entry["name"].index(card.get("name")) or 0
    mcard["locales"][language]["text"] = locale_entry["text"].index(card.get("text")) or 0
    mcard["locales"][language]["type"] = locale_entry["type"].index(card.get("type")) or 0
    mcard["locales"][language]["flavor"] = locale_entry["flavor"].index(card.get("flavorText")) or 0
    mcard["locales"][language]["multiverse"] = int(card['identifiers'].get('multiverseId') or 0)

    # set foreign locale to the appropriate index
    for card in card['foreignData']:
      language = card.get("language")
      locale_entry = locale[language]

      mcard["locales"][language] = {}
      mcard["locales"][language]["name"] = locale_entry["name"].index(card.get("name")) or 0
      mcard["locales"][language]["text"] = locale_entry["text"].index(card.get("text")) or 0
      mcard["locales"][language]["type"] = locale_entry["type"].index(card.get("type")) or 0
      mcard["locales"][language]["flavor"] = locale_entry["flavor"].index(card.get("flavorText")) or 0
      mcard["locales"][language]["multiverse"] = int(card.get('multiverseId') or 0)

with open("macaco-locales.json", "w", encoding='utf8') as outfile:
  json.dump(locales, outfile, ensure_ascii=False)

with open("macaco-data.json", "w", encoding='utf8') as outfile:
  json.dump(metadata, outfile, ensure_ascii=False)
