#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import shutil
import fileinput
from gooey import Gooey, GooeyParser

from pathlib import Path, PurePath

__version__ = "0.0.2"


@Gooey
def main():
    parser = argparse.ArgumentParser(
        description="Privacy-Fighter: Easy privacy solution"
        " Licensed Under: GPLv3"
    )
    # parser.add_argument("-v", "--version", action="version", version="Privacy-Fighter " + __version__)
    parser.add_argument("-p", "--profile", dest="profile_name", default="TEST", help="Profile name", type=str)

    args = parser.parse_args()

    run(args.profile_name)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def apply_one_time(profiles):
    ui_customization_raw = r'{\"placements\":{\"widget-overflow-fixed-list\":[],\"PersonalToolbar\":[\"personal-bookmarks\"],\"nav-bar\":[\"back-button\",\"forward-button\",\"stop-reload-button\",\"home-button\",\"customizableui-special-spring1\",\"urlbar-container\",\"downloads-button\",\"history-panelmenu\",\"bookmarks-menu-button\",\"library-button\",\"sidebar-button\",\"_3579f63b-d8ee-424f-bbb6-6d0ce3285e6a_-browser-action\",\"canvasblocker_kkapsner_de-browser-action\",\"cookieautodelete_kennydo_com-browser-action\",\"jid1-bofifl9vbdl2zq_jetpack-browser-action\",\"https-everywhere_eff_org-browser-action\",\"ublock0_raymondhill_net-browser-action\",\"jid1-mnnxcxisbpnsxq_jetpack-browser-action\",\"woop-noopscoopsnsxq_jetpack-browser-action\",\"_74145f27-f039-47ce-a470-a662b129930a_-browser-action\"],\"toolbar-menubar\":[\"menubar-items\"],\"TabsToolbar\":[\"tabbrowser-tabs\",\"new-tab-button\",\"alltabs-button\"]},\"seen\":[\"developer-button\",\"_3579f63b-d8ee-424f-bbb6-6d0ce3285e6a_-browser-action\",\"canvasblocker_kkapsner_de-browser-action\",\"cookieautodelete_kennydo_com-browser-action\",\"jid1-bofifl9vbdl2zq_jetpack-browser-action\",\"https-everywhere_eff_org-browser-action\",\"ublock0_raymondhill_net-browser-action\",\"jid1-mnnxcxisbpnsxq_jetpack-browser-action\",\"woop-noopscoopsnsxq_jetpack-browser-action\",\"_74145f27-f039-47ce-a470-a662b129930a_-browser-action\"],\"dirtyAreaCache\":[\"PersonalToolbar\",\"nav-bar\",\"toolbar-menubar\",\"TabsToolbar\"],\"currentVersion\":14,\"newElementCount\":4}'

    ui_customization_str = '"' + ui_customization_raw + '"'

    pref_one_time = [
        {'pref': '"browser.uiCustomization.state"', 'value': ui_customization_str},
        {'pref': '"browser.startup.homepage"', 'value': '"https://duckduckgo.com"'},
    ]

    for pref in profiles:
        for line in fileinput.input(pref + "/prefs.js", inplace=True):
            for i in pref_one_time:
                if i['pref'] in line:
                    line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
                    # print(line)
            sys.stdout.write(line)


def get_firefox_path():
    detected_os = sys.platform

    if detected_os == "linux":
        firefox_path = os.path.join(Path.home(), ".mozilla/firefox/")
    elif detected_os == "win32":
        firefox_path = os.path.join(os.getenv('APPDATA'), "Mozilla\Firefox\Profiles""\\")

    if not os.path.exists(firefox_path):
        print("Please download and install firefox first https://www.mozilla.org/en-US/firefox/new/")
        sys.exit(0)
    print(os.listdir(firefox_path))
    print(os.listdir("."))
    # onlydirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]

    # print(onlydirs)
    return firefox_path


def run(profile_name):

    privacy_fighter_profile = resource_path("profile")
    print(privacy_fighter_profile)

    firefox_path = get_firefox_path()

    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    # firefox_path = Path.joinpath(Path(os.getenv('APPDATA')), Path("Mozilla/Firefox/Profiles/"))
    # profiles = firefox_path.glob("TEST")

    print(profiles)

    for prof in profiles:
        for dirpath, dirnames, filenames in os.walk(privacy_fighter_profile):
            for dirname in dirnames:
                src_path = os.path.join(dirpath, dirname)
                dst_path = os.path.join(prof, dirname)
                # print("dirs :", src_path, dst_path)
            for filename in filenames:

                src_path = os.path.join(dirpath, filename)
                src_list = list(Path(src_path).parts)
                src_list.pop(0)
                src_file = Path(*src_list)
                firefox_p_path = os.path.join(firefox_path, prof)
                dst_path = os.path.join(firefox_p_path, src_file)
                # print("file :", src_path, dst_path)
                print("Copied: ", dst_path)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(src_path, dst_path)
    apply_one_time(profiles)

    # shutil.copy("profile/user.js", os.path.join(profile, "user.js"))
    # shutil.copy("profile/search.json.mozlz4", os.path.join(profile, "search.json.mozlz4"))


if __name__ == "__main__":
    main()
