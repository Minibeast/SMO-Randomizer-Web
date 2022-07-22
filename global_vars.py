import json

with open('moons.json') as moon_file:
    MOONS = json.load(moon_file)['results']
    moon_file.close()

COIN_MOONS = [217, 283, 329, 412, 453, 528, 598, 658, 740] # Shop moons for every kingdom.
PURPLE_MOONS = [228, 285, 342, 465, 466, 536, 537, 604, 660, 661, 742, 743] # All moons that require a purple coin outfit.
DEEP_WOODS = list(range(334, 343)) # Every moon in the Deep Woods in Wooded Kingdom