import base64


class Settings:
    overrides : list
    bowser_sprinkle : bool
    peace_skips : bool
    fms : bool
    version : str

    def __init__(self) -> None:
        self.overrides = []
        self.bowser_sprinkle = False
        self.peace_skips = False
        self.fms = False
        self.version = "0.2.1"

    def __str__(self) -> str:
        return encode_settings(self)


def check_bool(string : str) -> bool:
    return string == "True"


def overrides_to_string(overrides : list) -> str:
    output = ""
    for x in overrides:
        output += str(x['moon']) + "=" + str(x['override']) + "|"
    return output


def string_to_overrides(overrides : str) -> list:
    output = []
    temp = overrides.split("|")
    temp = temp[:-1]
    for x in temp:
        override_str = x.split("=")
        print(override_str)
        if len(override_str) != 2:
            return ValueError
        if override_str[1] == "True":
            override_bool = True
        else:
            override_bool = False
        output.append({
            "moon": int(override_str[0]),
            "override": override_bool
        })
    return output


def parse_form(settings : dict) -> Settings:
    try:
        sprinkle = settings['sprinkle'] == "on"
    except:
        sprinkle = False
    try:
        peace = settings['peaceskips'] == "on"
    except:
        peace = False
    try:
        fms = settings['fms'] == "on"
    except:
        fms = False

    allowlist = settings['allowlist'].split("\n")
    blocklist = settings['blocklist'].split("\n")
    if allowlist[0] == '':
        allowlist = []
    if blocklist[0] == '':
        blocklist = []
    overrides = []
    for x in allowlist:
        x = x.replace("\r", "")
        overrides.append({
            "moon": int(x),
            "override": True
        })
    for x in blocklist:
        x = x.replace("\r", "")
        overrides.append({
            "moon": int(x),
            "override": False
        })

    settings_class = Settings()
    settings_class.bowser_sprinkle = sprinkle
    settings_class.peace_skips = peace
    settings_class.overrides = overrides
    settings_class.fms = fms

    return settings_class


def decode_settings(settings : str) -> Settings:
    decodedBytes = base64.urlsafe_b64decode(settings)
    decoded_settings_str = str(decodedBytes, "UTF-8")
    decoded_settings_list = decoded_settings_str.split("P")
    
    settings_ver = str(decoded_settings_list[0])
    overrides = string_to_overrides(decoded_settings_list[1])
    sprinkle = check_bool(decoded_settings_list[2])
    peaceskips = check_bool(decoded_settings_list[3])
    settings = Settings()
    settings.peace_skips = peaceskips
    settings.bowser_sprinkle = sprinkle
    settings.overrides = overrides

    if settings_ver != "0.1.0":
        settings.fms = check_bool(decoded_settings_list[4])
    
    return settings


def encode_settings(settings : Settings) -> str:
    output = str(settings.version) + "P"
    output += overrides_to_string(settings.overrides) + "P"
    output += str(settings.bowser_sprinkle) + "P"
    output += str(settings.peace_skips) + "P"
    output += str(settings.fms)
    return str(base64.urlsafe_b64encode(bytes(output, "UTF-8")), "UTF-8")

if __name__ == '__main__':
    settings = Settings()
    settings.bowser_sprinkle = True
    settings.peace_skips = True
    print(str(settings))
