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


@Gooey(
    program_name='Privacy Fighter',
    requires_shell=False)
def main():
    parser = argparse.ArgumentParser(
        description="Privacy-Fighter: A Browser Setup For Increased Privacy And Security"
    )
    # parser.add_argument("-v", "--version", action="version", version="Privacy-Fighter " + __version__)
    parser.add_argument("-p", "--profile", dest="profile_name", default="TEST",
                        help="Firefox Profile Name: Leave value to 'default' if unsure or using only single profile", type=str)

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

    print("\nApplying onetime preferences to 'prefs.js'\n")

    for profile in profiles:
        # prefs to be applied directly to 'prefs.js' instead of 'users.js' so end users can change these
        # contains 'exists' to change if found and turn 'exists' True. the ones not found will be later added
        # keep this in profile loop, so 'exists' True resets for next profile
        pref_one_time = [
            {'pref': '"browser.uiCustomization.state"', 'value': ui_customization_str, 'exists': False},
            {'pref': '"browser.startup.homepage"', 'value': '"https://duckduckgo.com"', 'exists': False},
            {'pref': '"browser.search.suggest.enabled"', 'value': 'true', 'exists': False},     # TEMP TEST
        ]

        for line in fileinput.input(os.path.join(profile, "prefs.js"), inplace=True):
            for i in pref_one_time:
                if i['pref'] in line:
                    line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
                    # it is found, turn 'exists' to True
                    i['exists'] = True
                    # print(line)
            sys.stdout.write(line)

        # now add the rest of preferences
        with open(os.path.join(profile, "prefs.js"), "a") as prefsjs:
            for i in pref_one_time:
                if not i['exists']:
                    line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
                    print(i)
                    prefsjs.write(line)


def get_firefox_path():
    detected_os = sys.platform

    if detected_os == "linux":
        firefox_path = os.path.join(Path.home(), ".mozilla/firefox/")
    elif detected_os == "win32":
        firefox_path = os.path.join(os.getenv('APPDATA'), "Mozilla\Firefox\Profiles""\\")
    # firefox_path = Path.joinpath(Path(os.getenv('APPDATA')), Path("Mozilla/Firefox/Profiles/"))

    if not os.path.exists(firefox_path):
        print("Please download and install firefox first https://www.mozilla.org/en-US/firefox/new/")
        sys.exit(0)

    # print("List of All Firefox Profiles : ", os.listdir(firefox_path))
    # print(os.listdir("."))

    # onlydirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]
    # print(onlydirs)
    return firefox_path


def run(profile_name):

    privacy_fighter_profile = resource_path("profile")
    # print(privacy_fighter_profile)

    firefox_path = get_firefox_path()

    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    if not profiles:
        print("ERROR: No Firefox Profile Found With The Name of '{}'. If Unsure Keep it 'default'".format(profile_name))
        sys.exit(1)

    print("Firefox Profiles to be secured/modified : ", profiles, "\n")

    for prof in profiles:
        print("Modified Preferences (Users.js) and Extensions will now be copied to {}\n".format(prof))
        for dirpath, dirnames, filenames in os.walk(privacy_fighter_profile):
            for dirname in dirnames:
                src_path = os.path.join(dirpath, dirname)
                dst_path = os.path.join(prof, dirname)
                # print("dirs :", src_path, dst_path)
            for filename in filenames:
                src_path = os.path.join(dirpath, filename)
                src_list = list(Path(src_path).parts)
                # remove first element '/' from the list
                src_list.pop(0)
                # find last index of "profile" in location, in case there is another "profile" folder in path
                pf_folder_index = len(src_list) - 1 - src_list[::-1].index("profile")

                # extract section after 'profile' out of '/home/user/privacy-fighter/profile/extensions/ext.js'
                src_list = src_list[pf_folder_index + 1:]
                # now src_file would be e.g extensions/ext.js
                src_file = Path(*src_list)
                firefox_p_path = os.path.join(firefox_path, prof)
                dst_path = os.path.join(firefox_p_path, src_file)
                # print("file : ", src_path, dst_path)
                print("Copying: ", src_file)
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy(src_path, dst_path)
    apply_one_time(profiles)
    print("------------------DONE-------------------\n")
    print("You can now close this and run Firefox :)")
    # shutil.copy("profile/user.js", os.path.join(profile, "user.js"))
    # shutil.copy("profile/search.json.mozlz4", os.path.join(profile, "search.json.mozlz4"))


if __name__ == "__main__":
    main()
