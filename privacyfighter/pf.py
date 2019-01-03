#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import shutil
import fileinput

from pathlib import Path, PurePath

import requests
from gooey import Gooey, GooeyParser


__version__ = "0.0.3"


@Gooey(
    progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100",
    program_name='Privacy Fighter',
    requires_shell=False)
def main():
    parser = argparse.ArgumentParser(
        description="Privacy-Fighter: A Browser Setup For Increased Privacy And Security"
    )
    # parser.add_argument("-v", "--version", action="version", version="Privacy-Fighter " + __version__)
    parser.add_argument("-p", "--profile", dest="profile_name", default="TEST",
                        help="Firefox Profile Name: Leave value to 'default' if unsure or using only single firefox profile", type=str)

    args = parser.parse_args()
    init()
    run(args.profile_name)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def download_extension(url, extensions_folder, extension_id):
    r = requests.get(url, allow_redirects=True)
    open(os.path.join(extensions_folder, extension_id), 'wb').write(r.content)


def download_file(url, dest):
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)


def init():
    total_steps = 12

    pref_add = [
        # {'pref': '"browser.newtabpage.activity-stream.improvesearch.topSiteSearchShortcuts.searchEngines"',
        #  'value': '"duckduckgo"'},
        {'pref': '"dom.event.clipboardevents.enabled"', 'value': 'false'},
        {'pref': '"app.update.auto"', 'value': 'true'},     # enable auto updates
    ]

    # preferences to be modified in the users.j. if 'value' is given in here, it will be overwritten
    # using these. If 'value' is '', that preference will be deleted from users.js , so Firefox's Default
    # or user's original preference stays in place.
    # '' is used to get rid of undesired preferences set in pyllyukko's user.js. such as "places.history.enabled", "false"
    pref_mods = [
        {'pref': '"browser.safebrowsing.enabled"', 'value': 'false'},
        {'pref': '"browser.safebrowsing.phishing.enabled"', 'value': 'false'},
        {'pref': '"browser.safebrowsing.malware.enabled"', 'value': 'false'},
        {'pref': '"browser.safebrowsing.downloads.remote.enabled"', 'value': 'false'},
        {'pref': '"privacy.clearOnShutdown.cookies"', 'value': 'true'},

        {'pref': '"browser.search.suggest.enabled"', 'value': ''},
        {'pref': '"keyword.enabled"', 'value': ''},         # don't block search from urlbar

        {'pref': '"browser.urlbar.suggest.history"', 'value': ''},
        # {'pref': '"browser.urlbar.suggest.searches"', 'value': ''},
        {'pref': '"browser.urlbar.autoFill"', 'value': ''},
        {'pref': '"browser.urlbar.autoFill.typed"', 'value': ''},

        {'pref': '"places.history.enabled"', 'value': ''},
        {'pref': '"browser.formfill.enable"', 'value': ''},
        {'pref': '"browser.newtabpage.enabled"', 'value': ''},
        {'pref': '"privacy.clearOnShutdown.history"', 'value': ''},
        {'pref': '"privacy.clearOnShutdown.formdata"', 'value': ''},
        {'pref': '"privacy.clearOnShutdown.openWindows"', 'value': ''},
        {'pref': '"privacy.clearOnShutdown.downloads"', 'value': ''},
        {'pref': '"browser.download.manager.retention"', 'value': ''},
        {'pref': '"browser.bookmarks.max_backups"', 'value': 5},
        {'pref': '"browser.newtabpage.activity-stream.enabled"', 'value': ''},
        {'pref': '"browser.newtab.url"', 'value': ''},
        {'pref': '"privacy.sanitize.sanitizeOnShutdown"', 'value': ''},     # don't enforce history clear on shutdown
        # // Sets time range to "Everything" as default in "Clear Recent History"
        {'pref': '"privacy.sanitize.timeSpan"', 'value': ''},
    ]

    extensions = [
        {'name': 'decentraleyes', 'id': 'jid1-BoFifL9Vbdl2zQ@jetpack.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1078499/decentraleyes-2.0.8-an+fx.xpi'},
        {'name': 'cookie_autodelete', 'id': 'CookieAutoDelete@kennydo.com.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/954445/cookie_autodelete-2.2.0-an+fx.xpi'},
        {'name': 'https_everywhere', 'id': 'https-everywhere@eff.org.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1132037/https_everywhere-2018.10.31-an+fx.xpi'},
        {'name': 'ublock_origin', 'id': 'uBlock0@raymondhill.net.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1114441/ublock_origin-1.17.2-an+fx.xpi'},
        {'name': 'canvas_blocker', 'id': 'CanvasBlocker@kkapsner.de.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1108171/canvasblocker-0.5.5-an+fx.xpi'},
        # {'name': 'chameleon', 'id': '{3579f63b-d8ee-424f-bbb6-6d0ce3285e6a}.xpi',
        #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1157451/chameleon-0.9.23-an+fx.xpi'},
        # {'name': 'privacy_badger', 'id': 'jid1-MnnxcxisBPnSXQ@jetpack.xpi',
        #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1099313/privacy_badger-2018.10.3.1-an+fx.xpi'},
        {'name': 'clear_urls', 'id': '{74145f27-f039-47ce-a470-a662b129930a}.xpi',
            'url': 'https://addons.mozilla.org/fidownload_filerefox/downloads/file/1101996/clearurls-1.3.4.0-an+fx.xpi'},
        {'name': 'privacy_possum', 'id': 'woop-NoopscooPsnSXQ@jetpack.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1062944/privacy_possum-2018.8.31-an+fx.xpi'},
        {'name': 'multi_account_containers', 'id': '@testpilot-containers.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1171317/firefox_multi_account_containers-6.0.1-fx.xpi'},
        {'name': 'facebook_container', 'id': '@contain-facebook.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1149344/facebook_container-1.4.2-fx.xpi'},
        {'name': 'google_container', 'id': '@contain-google.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/1144065/google_container-1.3.4-fx.xpi'},
        {'name': 'temporary_containers', 'id': '{c607c8df-14a7-4f28-894f-29e8722976af}.xpi',
            'url': 'https://addons.mozilla.org/firefox/downloads/file/957989/temporary_containers-0.90-an+fx-linux.xpi'},

    ]

    # Create folders
    profile_folder = resource_path("profile")
    extensions_folder = os.path.join(profile_folder, "extensions")

    os.makedirs(profile_folder, exist_ok=True)
    os.makedirs(extensions_folder, exist_ok=True)

    for index, ext in enumerate(extensions):
        # for i in range(2):
        print("Downloading {}".format(ext['name']))
        download_extension(ext['url'], extensions_folder, ext['id'])

        print("progress: {}/{}".format(index + 1, total_steps))
        sys.stdout.flush()

    # download_file("https://raw.githubusercontent.com/pyllyukko/user.js/relaxed/user.js", os.path.join(profile_folder, "user.js"))
    download_file("https://github.com/ghacksuserjs/ghacks-user.js/raw/master/user.js",
                  os.path.join(profile_folder, "user.js"))

    for line in fileinput.input(os.path.join(profile_folder, "user.js"), inplace=True):
        for i in pref_mods:
            if i['pref'] in line:
                if not i['value']:
                    line = ''
                else:
                    line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
            # remove comment lines
            # if line[:2] == '//':
                # line = ''
            # remove todo lines
            if line[:8] == '// TODO:':
                line = ''

        sys.stdout.write(line)

    with open(os.path.join(profile_folder, "user.js"), "a") as userjs:
        for i in pref_add:
            line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
            userjs.write(line)


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
                    # print(i)      # pref being added
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
    # here subprocess.run("firefox -p -no-remote"), ask user to create another profile TEMP, https://github.com/mhammond/pywin32
    print("You can now close this and run Firefox :)")
    # shutil.copy("profile/user.js", os.path.join(profile, "user.js"))
    # shutil.copy("profile/search.json.mozlz4", os.path.join(profile, "search.json.mozlz4"))


if __name__ == "__main__":
    main()
