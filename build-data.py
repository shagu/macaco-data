#!/usr/bin/env python3
import json, re

# load JSON files
print("Loading JSON Input Files...")

with open("AllPrintings.json", "r") as f:
  all_printings = json.loads(f.read())

with open("AllPrices.json", "r") as f:
  all_prices = json.loads(f.read())

# prepare fallback language lookup table
print("Preparing Locale Lookup Table...")
locales = {}

for set_id in all_printings["data"].keys():
  for card in all_printings["data"][set_id]["cards"]:
    # build card locales
    if not card["name"] in locales:
      locales[card["name"]] = { }

    # english
    locales[card["name"]]["English"] = {
      'name': card.get('name'),
      'type': card.get('type'),
      'text': card.get('text'),
      'mult': card.get('multiverseId'),
    }

    # multi languages
    for locale in card['foreignData']:
      locales[card["name"]][locale["language"]] = {
        'name': locale.get('name'),
        'type': locale.get('type'),
        'text': locale.get('text'),
        'mult': locale.get('multiverseId'),
      }

# build macaco-metadata
print("Building Macaco Metadata...")
metadata = {}

for set_id in all_printings["data"].keys():
  for card in all_printings["data"][set_id]["cards"]:
    # create set if not existing
    if not set_id in metadata:
      metadata[set_id] = {}

    # remove non-numbers
    number = re.sub('\D', '', card["number"])

    if not number in metadata[set_id]:
      metadata[set_id][number] = { }

    # read price data
    prices = [ 0, 0 ]

    try:
      # read cardkingdom data as price baseline
      for date in all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["normal"]:
        prices[0] = all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["normal"][date]

      for date in all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["foil"]:
        prices[1] = all_prices["data"][card["uuid"]]["paper"]["cardkingdom"]["buylist"]["foil"][date]

      # overwrite with cardmarket where possible
      for date in all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["normal"]:
        prices[0] = all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["normal"][date]

      for date in all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["foil"]:
        prices[1] = all_prices["data"][card["uuid"]]["paper"]["cardmarket"]["retail"]["foil"][date]
    except:
      pass

    # read/write basic card data
    metacard = metadata[set_id][number]
    metacard['artist'] = card.get('artist')
    metacard['color'] = card.get('color')
    metacard['identity'] = card.get('colorIdentity')
    metacard['cmc'] = card.get('convertedManaCost')
    metacard['mana'] = card.get('manaCost')
    metacard['rarity'] = card.get('rarity')
    metacard['power'] = card.get('power')
    metacard['toughness'] = card.get('toughness')
    metacard['scryfall'] = card.get('scryfallId')
    metacard['uuid'] = card.get('uuid')
    metacard["prices"] = prices

    # write locales
    #   first write fallback data from locale-cache, then
    #   replace with actual card locales if there are any.
    metacard["locales"] = {}

    # load fallback locales
    for locale in locales.get(card['name'], {}):
      metacard["locales"][locale] = locales[card['name']][locale]

    # obtain english card locales
    metacard["locales"]["English"] = {
      'name': card.get('name'),
      'type': card.get('type'),
      'text': card.get('text'),
      'mult': card['identifiers'].get('multiverseId'),
    }

    # obtain other card locales
    for locale in card['foreignData']:
      metacard["locales"][locale["language"]] = {
        'name': locale.get('name'),
        'type': locale.get('type'),
        'text': locale.get('text'),
        'mult': locale.get('multiverseId'),
      }

with open("macaco-database.json", "w") as outfile:
  json.dump(metadata, outfile)
