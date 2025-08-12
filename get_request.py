import json
import requests
import os


if not os.path.exists("card_results"):
    os.mkdir("card_results")
else:
    os.chdir("card_results")


api_uri = "https://api.scryfall.com/"

def get_card_count_by_set(set_code):

    headers = {
        "Accept": "text/plain",
    }
    result=requests.get(f'{api_uri}sets/{set_code}', headers=headers)
    return result.json()["card_count"]


def get_all_cards_by_set(set_code, card_count):

    page_count = card_count // 175 + 1

    params = {
        "q": f"set:{set_code}",
        "games": "paper"
    }
    headers = {
        "Accept": "application/json",
    }

    cards = []

    for page_no in range(1, page_count):
        params["page"] = str(page_no)
        result = requests.get(f'{api_uri}cards/search', params=params, headers=headers)
        jlist = json.loads(result.text)
        cards.extend(jlist["data"])
    return cards


def result_to_card_names(result):
    return [card["name"] for card in result]


sc = input("Enter set code: ")
card_list = get_all_cards_by_set(sc, get_card_count_by_set(sc))

f = open(f"{sc}_cards.txt", "w")
f.write("\n".join(result_to_card_names(card_list)))
f.close()

