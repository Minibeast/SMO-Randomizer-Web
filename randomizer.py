import random
from settings import Settings
from global_vars import *
from generate_list import get_moon_json


def rand(min : int, max : int) -> int:
    return random.randint(min, max)


def randomize(min : int, max : int) -> str:
    value = rand(min, max)
    return MOONS[value]


def allow_moon(moon : int, settings : Settings) -> int:
    for x in settings.overrides:
        if x['moon'] == moon:
            return x['override']
    return None


def generatestory(min : int, max : int, collectedMoons : list) -> str:
    while True:
        value = rand(min, max)
        if MOONS[value]["id"] not in collectedMoons:
            collectedMoons.append(MOONS[value]["id"])
            return {"name": MOONS[value]["name"], "trait": " [Story] "}


def generate(min : int, max : int, prerequisite : int, amount : int, collectedMoons : list, settings : Settings) -> list:
    i = 0
    return_list = []
    while i < amount:
        x = randomize(min, max)
        override_check = allow_moon(x['id'], settings)
        if override_check is None:
            if (x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite) and (
                    x["moonTypes"] is None or x["moonTypes"][0]["name"] != "Warp Painting") and (
                    x["isPostGame"] is not True) and (x["requiresRevisit"] is not True) and (
                    x["isStoryMoon"] is not True) and (x["moonTypes"] is None or (
                    x["moonTypes"][0]["name"] != "Hint Art" and x["moonTypes"][0]["name"] != "Tourist")) and (
                    x["id"] not in collectedMoons):
                trait = ""
                if x["id"] in COIN_MOONS:
                    trait += " [100 Coins] "
                if x["id"] in DEEP_WOODS:
                    trait += " [Deep Woods] "
                if x["id"] in PURPLE_MOONS:
                    trait += " [Outfit Moon] "
                if x["id"] == 339:
                    trait += " [500 Coins] "
                return_list.append({"name": x['name'], "trait": trait})
                collectedMoons.append(x["id"])
                i += 1
        elif override_check is True:
            if (x["moonPrerequisites"] is None or x["moonPrerequisites"][0]["id"] <= prerequisite) and (
                        x["id"] not in collectedMoons):
                    trait = ""
                    if x["id"] in COIN_MOONS:
                        trait += " [100 Coins] "
                    if x["id"] in DEEP_WOODS:
                        trait += " [Deep Woods] "
                    if x["id"] in PURPLE_MOONS:
                        trait += " [Outfit Moon] "
                    if x["id"] == 339:
                        trait += " [500 Coins] "
                    return_list.append({"name": x['name'], "trait": trait})
                    collectedMoons.append(x["id"])
                    i += 1
    return return_list


def talkatoo(seed : int, settings : Settings) -> dict:
    random.seed(seed)
    output = get_moon_json(settings)
    for x in output:
        random.shuffle(x['moons'])
    return output


def generate_page(seed : int, settings : Settings) -> list:
    random.seed(seed)
    bowserSprinkle = settings.bowser_sprinkle
    peaceSkips = settings.peace_skips
    output = []
    collectedmoons = []

    # Cascade
    if settings.fms:
        cascade_moon_list = [{"name": MOONS[136]["name"], "trait": " [Story] "}] + generate(135, 174, 137, 2, collectedmoons, settings)
    else:
        cascade_moon_list = [{"name": MOONS[135]["name"], "trait": " [Story] "}, {"name": MOONS[136]["name"], "trait": " [Story] "}] + generate(135, 174, 137, 1, collectedmoons, settings)

    output.append({"kingdom": "Cascade", "moons": cascade_moon_list})
    #

    # Sand
    moonCount = 0
    sand_moon_list = []

    local = rand(0, 16)
    moonCount += local

    sand_moon_list += generate(175, 263, 0, local, collectedmoons, settings)
    
    if not peaceSkips:
        if moonCount < 16:
            sand_moon_list.append({"name": MOONS[175]["name"], "trait": " [Story] "})
            moonCount += 1

            local = rand(0, 16 - moonCount)
            moonCount += local

            sand_moon_list += generate(175, 263, 176, local, collectedmoons, settings)
            if moonCount < 16:
                sand_moon_list.append({"name": MOONS[176]["name"], "trait": " [Story] "})
                moonCount += 1

                local = rand(0, 16 - moonCount)
                moonCount += local

                sand_moon_list += generate(175, 263, 177, local, collectedmoons, settings)

                if moonCount < 14:
                    sand_moon_list.append({"name": MOONS[177]["name"], "trait": " [Story] "})
                    moonCount += 3

                    local = rand(0, 16 - moonCount)
                    moonCount += local

                    sand_moon_list += generate(175, 263, 178, local, collectedmoons, settings)

                    if moonCount < 14:
                        sand_moon_list.append({"name": MOONS[178]["name"], "trait": " [Story] "})
                        moonCount += 3

                        sand_moon_list += generate(175, 263, 179, 16 - moonCount, collectedmoons, settings)
                    elif 16 > moonCount >= 14:
                        sand_moon_list += generate(175, 263, 177, 16 - moonCount, collectedmoons, settings)

                elif 16 > moonCount >= 14:
                    sand_moon_list += generate(175, 263, 177, 16 - moonCount, collectedmoons, settings)
    else:
        if moonCount < 14:
            sand_moon_list.append({"name": MOONS[177]["name"], "trait": " [Story] "})
            moonCount += 3

            local = rand(0, 16 - moonCount)
            moonCount += local

            sand_moon_list += generate(175, 263, 178, local, collectedmoons, settings)

            if moonCount < 14:
                sand_moon_list.append({"name": MOONS[178]["name"], "trait": " [Story] "})
                moonCount += 3

                sand_moon_list += generate(175, 263, 179, 16 - moonCount, collectedmoons, settings)
            elif 16 > moonCount >= 14:
                sand_moon_list += generate(175, 263, 177, 16 - moonCount, collectedmoons, settings)

        elif 16 > moonCount >= 14:
            sand_moon_list += generate(175, 263, 177, 16 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Sand", "moons": sand_moon_list})
    #

    # Lake
    moonCount = 0
    lake_moon_list = []

    local = rand(0, 8)
    moonCount += local

    lake_moon_list += generate(264, 305, 0, local, collectedmoons, settings)

    if moonCount < 6:
        lake_moon_list.append({"name": MOONS[264]["name"], "trait": " [Story] "})
        moonCount += 3

        lake_moon_list += generate(264, 305, 265, 8 - moonCount, collectedmoons, settings)
    elif 8 > moonCount >= 6:
        lake_moon_list += generate(264, 305, 0, 8 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Lake", "moons": lake_moon_list})
    #
    
    # Wooded
    moonCount = 0
    wooded_moon_list = []

    local = rand(0, 16)
    moonCount += local

    wooded_moon_list += generate(306, 381, 0, local, collectedmoons, settings)

    if moonCount < 16:
        wooded_moon_list.append({"name": MOONS[306]["name"], "trait": " [Story] "})
        moonCount += 1

        local = rand(0, 16 - moonCount)
        moonCount += local

        wooded_moon_list += generate(306, 381, 307, local, collectedmoons, settings)

        if moonCount < 14:
            wooded_moon_list.append({"name": MOONS[307]["name"], "trait": " [Story] "})
            moonCount += 3

            local = rand(0, 16 - moonCount)
            moonCount += local

            wooded_moon_list += generate(306, 381, 308, local, collectedmoons, settings)

            if moonCount < 16:
                wooded_moon_list.append({"name": MOONS[308]["name"], "trait": " [Story] "})
                moonCount += 1

                local = rand(0, 16 - moonCount)
                moonCount += local

                wooded_moon_list += generate(306, 381, 309, local, collectedmoons, settings)

                if moonCount < 14:
                    wooded_moon_list.append({"name": MOONS[309]["name"], "trait": " [Story] "})
                    moonCount += 3

                    wooded_moon_list += generate(306, 381, 310, 16 - moonCount, collectedmoons, settings)
                elif 16 > moonCount >= 14:
                    wooded_moon_list += generate(306, 381, 309, 16 - moonCount, collectedmoons, settings)
        elif 16 > moonCount >= 14:
            wooded_moon_list += generate(306, 381, 307, 16 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Wooded", "moons": wooded_moon_list})
    #

    # Lost
    output.append({"kingdom": "Lost", "moons": generate(391, 425, 0, 10, collectedmoons, settings)})
    #

    # Metro
    moonCount = 3
    metro_moon_list = [{"name": MOONS[426]["name"], "trait": " [Story] "}]

    local = rand(0, 20 - moonCount)
    moonCount += local

    metro_moon_list += generate(426, 506, 427, local, collectedmoons, settings)

    if moonCount < 20:
        metro_moon_list.append(generatestory(427, 430, collectedmoons))
        moonCount += 1

        local = rand(0, 20 - moonCount)
        moonCount += local

        metro_moon_list += generate(426, 506, 427, local, collectedmoons, settings)

        if moonCount < 20:
            story = generatestory(427, 430, collectedmoons)
            metro_moon_list.append(story)
            moonCount += 1

            local = rand(0, 20 - moonCount)
            moonCount += local

            metro_moon_list += generate(426, 506, 427, local, collectedmoons, settings)

            if moonCount < 20:
                story = generatestory(427, 430, collectedmoons)
                metro_moon_list.append(story)
                moonCount += 1

                local = rand(0, 20 - moonCount)
                moonCount += local

                metro_moon_list += generate(426, 506, 427, local, collectedmoons, settings)

                if moonCount < 20:
                    story = generatestory(427, 430, collectedmoons)
                    metro_moon_list.append(story)
                    moonCount += 1

                    local = rand(0, 20 - moonCount)
                    moonCount += local

                    metro_moon_list += generate(426, 506, 428, local, collectedmoons, settings)

                    if moonCount < 20:
                        metro_moon_list.append({"name": MOONS[431]["name"], "trait": " [Story] "})
                        moonCount += 1

                        local = rand(0, 20 - moonCount)
                        moonCount += local

                        metro_moon_list += generate(426, 506, 432, local, collectedmoons, settings)

                        if moonCount < 18:
                            metro_moon_list.append({"name": MOONS[432]["name"], "trait": " [Story] "})
                            moonCount += 3

                            metro_moon_list += generate(426, 506, 433, 20 - moonCount, collectedmoons, settings)
                        elif 20 > moonCount >= 18:
                            metro_moon_list += generate(426, 506, 432, 20 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Metro", "moons": metro_moon_list})
    #

    # Snow
    moonCount = 0
    snow_moon_list = []

    local = rand(0, 10)
    moonCount += local

    snow_moon_list += generate(507, 561, 0, local, collectedmoons, settings)

    if not peaceSkips:
        if moonCount < 10:
            story = generatestory(507, 510, collectedmoons)
            snow_moon_list.append(story)
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            snow_moon_list += generate(507, 561, 0, local, collectedmoons, settings)

            if moonCount < 10:
                story = generatestory(507, 510, collectedmoons)
                snow_moon_list.append(story)
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                snow_moon_list += generate(507, 561, 0, local, collectedmoons, settings)

                if moonCount < 10:
                    story = generatestory(507, 510, collectedmoons)
                    snow_moon_list.append(story)
                    moonCount += 1

                    local = rand(0, 10 - moonCount)
                    moonCount += local

                    snow_moon_list += generate(507, 561, 0, local, collectedmoons, settings)

                    if moonCount < 10:
                        story = generatestory(507, 510, collectedmoons)
                        snow_moon_list.append(story)
                        moonCount += 1

                        local = rand(0, 10 - moonCount)
                        moonCount += local

                        snow_moon_list += generate(507, 561, 0, local, collectedmoons, settings)

                        if moonCount < 8:
                            snow_moon_list.append({"name": MOONS[511]["name"], "trait": " [Story] "})
                            moonCount += 3

                            snow_moon_list += generate(507, 561, 512, 10 - moonCount, collectedmoons, settings)
                        elif 10 > moonCount >= 8:
                            snow_moon_list += generate(507, 561, 0, 10 - moonCount, collectedmoons, settings)
    else:
        if moonCount < 8:
            snow_moon_list.append({"name": MOONS[511]["name"], "trait": " [Story] "})
            moonCount += 3

            snow_moon_list += generate(507, 561, 512, 10 - moonCount, collectedmoons, settings)
        elif 10 > moonCount >= 8:
            snow_moon_list += generate(507, 561, 0, 10 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Snow", "moons": snow_moon_list})
    #
    
    # Seaside
    moonCount = 0
    seaside_moon_list = []

    local = rand(0, 10)
    moonCount += local

    seaside_moon_list += generate(562, 632, 0, local, collectedmoons, settings)

    if moonCount < 10:
        story = generatestory(562, 565, collectedmoons)
        seaside_moon_list.append(story)
        moonCount += 1

        local = rand(0, 10 - moonCount)
        moonCount += local

        seaside_moon_list += generate(562, 632, 0, local, collectedmoons, settings)

        if moonCount < 10:
            story = generatestory(562, 565, collectedmoons)
            seaside_moon_list.append(story)
            moonCount += 1

            local = rand(0, 10 - moonCount)
            moonCount += local

            seaside_moon_list += generate(562, 632, 0, local, collectedmoons, settings)

            if moonCount < 10:
                story = generatestory(562, 565, collectedmoons)
                seaside_moon_list.append(story)
                moonCount += 1

                local = rand(0, 10 - moonCount)
                moonCount += local

                seaside_moon_list += generate(562, 632, 0, local, collectedmoons, settings)

                if moonCount < 10:
                    story = generatestory(562, 565, collectedmoons)
                    seaside_moon_list.append(story)
                    moonCount += 1

                    local = rand(0, 10 - moonCount)
                    moonCount += local

                    seaside_moon_list += generate(562, 632, 0, local, collectedmoons, settings)

                    if moonCount < 8:
                        seaside_moon_list.append({"name": MOONS[566]["name"], "trait": " [Story] "})
                        moonCount += 3

                        seaside_moon_list += generate(562, 632, 567, 10 - moonCount, collectedmoons, settings)
                    elif 10 > moonCount >= 8:
                        seaside_moon_list += generate(562, 632, 0, 10 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Seaside", "moons": seaside_moon_list})
    #

    # Luncheon
    moonCount = 1
    luncheon_moon_list = [{"name": MOONS[633]["name"], "trait": " [Story] "}]

    local = rand(0, 15)
    moonCount += local

    luncheon_moon_list += generate(633, 700, 634, local, collectedmoons, settings)

    if moonCount < 18:
        luncheon_moon_list.append({"name": MOONS[634]["name"], "trait": " [Story] "})
        moonCount += 1

        local = rand(0, 18 - moonCount)
        moonCount += local

        luncheon_moon_list += generate(633, 700, 635, local, collectedmoons, settings)

        if moonCount < 16:
            luncheon_moon_list.append({"name": MOONS[635]["name"], "trait": " [Story] "})
            moonCount += 3

            local = rand(0, 18 - moonCount)
            moonCount += local

            luncheon_moon_list += generate(633, 700, 636, local, collectedmoons, settings)

            if moonCount < 18:
                luncheon_moon_list.append({"name": MOONS[636]["name"], "trait": " [Story] "})
                moonCount += 1

                local = rand(0, 18 - moonCount)
                moonCount += local

                luncheon_moon_list += generate(633, 700, 637, local, collectedmoons, settings)

                if moonCount < 16:
                    luncheon_moon_list.append({"name": MOONS[637]["name"], "trait": " [Story] "})
                    moonCount += 3

                    luncheon_moon_list += generate(633, 700, 638, 18 - moonCount, collectedmoons, settings)

                elif 18 > moonCount >= 16:
                    luncheon_moon_list += generate(633, 700, 637, 18 - moonCount, collectedmoons, settings)
        elif 18 > moonCount >= 16:
            luncheon_moon_list += generate(633, 700, 635, 18 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Luncheon", "moons": luncheon_moon_list})
    #

    # Bowsers
    moonCount = 6
    bowsers_moon_list = [{"name": MOONS[711]["name"], "trait": " [Story] "}, {"name": MOONS[712]["name"], "trait": " [Story] "}, {"name": MOONS[713]["name"], "trait": " [Story] "}, {"name": MOONS[714]["name"], "trait": " [Story] "}]
    sprinkleID = 715

    if bowserSprinkle:
        sprinkleID = 714

    bowsers_moon_list += generate(711, 772, sprinkleID, 8 - moonCount, collectedmoons, settings)
    output.append({"kingdom": "Bowser's", "moons": bowsers_moon_list})
    #

    return output
