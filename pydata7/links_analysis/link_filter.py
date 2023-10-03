import json
import re

path_to_platform = "../regex/platform.json"

def platform_compile(path_to_platform):
    with open(path_to_platform, "r+") as plat:
        platform_list = json.load(plat)
