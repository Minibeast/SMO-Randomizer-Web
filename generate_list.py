from settings import Settings
from global_vars import *


def allow_moon(moon : int, settings : Settings) -> int:
    for x in settings.overrides:
        if x['moon'] == moon:
            return x['override']
    return None


def get_all_moons(min : int, max : int, prerequisite : int, settings : Settings) -> list:
    output = []
    i = min
    while i < max:
        override_check = allow_moon(MOONS[i]['id'], settings)
        if override_check is None:
            if (MOONS[i]["moonPrerequisites"] is None or MOONS[i]["moonPrerequisites"][0]["id"] <= prerequisite) and (
                        MOONS[i]["moonTypes"] is None or MOONS[i]["moonTypes"][0]["name"] != "Warp Painting") and (
                        MOONS[i]["isPostGame"] is not True) and (MOONS[i]["requiresRevisit"] is not True) and (
                        MOONS[i]["isStoryMoon"] is not True) and (MOONS[i]["moonTypes"] is None or (
                        MOONS[i]["moonTypes"][0]["name"] != "Hint Art" and MOONS[i]["moonTypes"][0]["name"] != "Tourist")):
                trait = ""
                if MOONS[i]["id"] in COIN_MOONS:
                    trait += " [100 Coins] "
                if MOONS[i]["id"] in DEEP_WOODS:
                    trait += " [Deep Woods] "
                if MOONS[i]["id"] in PURPLE_MOONS:
                    trait += " [Outfit Moon] "
                if MOONS[i]["id"] == 339:
                    trait += " [500 Coins] "
                output.append({"name": MOONS[i]['name'], "id": MOONS[i]['id'], "trait": trait})
        elif override_check is True:
            if (MOONS[i]["moonPrerequisites"] is None or MOONS[i]["moonPrerequisites"][0]["id"] <= prerequisite):
                trait = ""
                if MOONS[i]["id"] in COIN_MOONS:
                    trait += " [100 Coins] "
                if MOONS[i]["id"] in DEEP_WOODS:
                    trait += " [Deep Woods] "
                if MOONS[i]["id"] in PURPLE_MOONS:
                    trait += " [Outfit Moon] "
                if MOONS[i]["id"] == 339:
                    trait += " [500 Coins] "
                output.append({"name": MOONS[i]['name'], "id": MOONS[i]['id'], "trait": trait})

        i += 1
    return output


def get_moon_json(settings : Settings) -> list:
    output = []
    output.append({"set": "Cascade|1", "moons": get_all_moons(135, 174, 137, settings), "transition_moon": None})
    output.append({"set": "Sand|1", "moons": get_all_moons(175, 263, 177, settings), "transition_moon": MOONS[177]['name']})
    output.append({"set": "Sand|2", "moons": get_all_moons(175, 263, 178, settings), "transition_moon": MOONS[178]['name']})
    output.append({"set": "Sand|3", "moons": get_all_moons(175, 263, 179, settings), "transition_moon": None})
    output.append({"set": "Lake|1", "moons": get_all_moons(264, 305, 0, settings), "transition_moon": MOONS[264]['name']})
    output.append({"set": "Lake|2", "moons": get_all_moons(264, 305, 265, settings), "transition_moon": None})
    output.append({"set": "Wooded|1", "moons": get_all_moons(306, 381, 307, settings), "transition_moon": MOONS[307]['name']})
    output.append({"set": "Wooded|2", "moons": get_all_moons(306, 381, 308, settings), "transition_moon": MOONS[309]['name']})
    output.append({"set": "Wooded|3", "moons": get_all_moons(306, 381, 310, settings), "transition_moon": None})
    output.append({"set": "Lost|1", "moons": get_all_moons(391, 425, 0, settings), "transition_moon": None})
    output.append({"set": "Metro|1", "moons": get_all_moons(426, 506, 428, settings), "transition_moon": MOONS[432]['name']})
    output.append({"set": "Metro|2", "moons": get_all_moons(426, 506, 433, settings), "transition_moon": None})
    output.append({"set": "Snow|1", "moons": get_all_moons(507, 561, 0, settings), "transition_moon": MOONS[511]['name']})
    output.append({"set": "Snow|2", "moons": get_all_moons(507, 561, 512, settings), "transition_moon": None})
    output.append({"set": "Seaside|1", "moons": get_all_moons(562, 632, 0, settings), "transition_moon": MOONS[566]['name']})
    output.append({"set": "Seaside|2", "moons": get_all_moons(562, 632, 567, settings), "transition_moon": None})
    output.append({"set": "Luncheon|1", "moons": get_all_moons(633, 700, 635, settings), "transition_moon": MOONS[635]['name']})
    output.append({"set": "Luncheon|2", "moons": get_all_moons(633, 700, 637, settings), "transition_moon": MOONS[637]['name']})
    output.append({"set": "Luncheon|3", "moons": get_all_moons(633, 700, 638, settings), "transition_moon": None})
    output.append({"set": "Bowsers|1", "moons": get_all_moons(711, 772, 715, settings), "transition_moon": None})
    return output
