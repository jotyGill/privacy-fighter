#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import shutil
import fileinput
import tempfile
import datetime

from pathlib import Path, PurePath

import requests
import psutil
from gooey import Gooey, GooeyParser

__version__ = "0.0.11"
__basefilepath__ = os.path.dirname(os.path.abspath(__file__))

# temporary folder to download files in
temp_folder = tempfile.mkdtemp()

# progress bar steps
total_steps = 12

# Create folders
extensions_folder = os.path.join(temp_folder, "extensions")
os.makedirs(extensions_folder, exist_ok=True)


# Now excluded extensions

#     # {'name': 'chameleon', 'id': '{3579f63b-d8ee-424f-bbb6-6d0ce3285e6a}.xpi',
#     #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1157451/chameleon-0.9.23-an+fx.xpi'},
#     # {'name': 'privacy_badger', 'id': 'jid1-MnnxcxisBPnSXQ@jetpack.xpi',
#     #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1099313/privacy_badger-2018.10.3.1-an+fx.xpi'},
#     # {'name': 'privacy_possum', 'id': 'woop-NoopscooPsnSXQ@jetpack.xpi',
#     #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1062944/privacy_possum-2018.8.31-an+fx.xpi'},

# Download the extensions list with their download links from the repo
r = requests.get(
    'https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/config/extensions.json')
extensions = r.json()["extensions"]

# Download the "user-overrides.js" with the latest ruleset from the repo
r = requests.get(
    "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/config/user-overrides.js", allow_redirects=True)
open(os.path.join(temp_folder, "user-overrides.js"), 'wb').write(r.content)


@Gooey(
    progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
    progress_expr="current / total * 100",
    program_name='Privacy Fighter',
    requires_shell=False)
def main():
    parser = argparse.ArgumentParser(
        description="Privacy-Fighter: A Browser Setup For Increased Privacy And Security"
    )
    # parser.add_argument("-v", "--version", action="version",
    #                     version="Privacy-Fighter " + __version__ + __basefilepath__)
    parser.add_argument("-p", "--profile", dest="profile_name", default="TEST",
                        help="Firefox Profile Name: Leave value to 'default' if unsure or using only single firefox profile", type=str)

    args = parser.parse_args()
    run(args.profile_name)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = __basefilepath__

    return os.path.join(base_path, relative_path)


def download_extensions():
    for index, ext in enumerate(extensions):
        print("Downloading {}".format(ext['name']))

        r = requests.get(ext['url'], allow_redirects=True)
        open(os.path.join(extensions_folder, ext['id']), 'wb').write(r.content)

        print("progress: {}/{}".format(index + 1, total_steps))
        sys.stdout.flush()


def download_file(url, dest):
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)


def setup_userjs():
    download_file("https://github.com/ghacksuserjs/ghacks-user.js/raw/master/user.js",
                  os.path.join(temp_folder, "user.js"))

    remove_prefs = extract_user_overrides()

    # Modifying user.js: if a pref set to be removed in "user-overrides.js", remove it from user.js
    # the pattern to remove a pref is "//// --- comment-out --- 'preference'"
    # this is taken from ghacksuserjs Updater Script. making it cross complatable with it.
    # https://github.com/ghacksuserjs/ghacks-user.js/wiki/3.3-Updater-Scripts
    with fileinput.input(os.path.join(temp_folder, "user.js"), inplace=True) as userjs_file:
        for line in userjs_file:
            for i in remove_prefs:
                if line[:9] == "user_pref":  # active pref
                    pref = '"{}"'.format(i[0])
                    comment = i[1]
                    if pref in line:        # TODO make sure pref.subpref doens't mess up parent
                        line = "// {}   // [PRIVACYFIGHTER EXCLUDED] {}\n".format(
                            line.strip("\n"), comment)

            sys.stdout.write(line)

    # Append "user-overrides.js", to "user.js". this will add additional prefs
    with open(os.path.join(temp_folder, "user.js"), "a") as userjs:
        with open(os.path.join(temp_folder, "user-overrides.js"), "r") as user_overrides:
            for line in user_overrides:
                userjs.write(line)


def extract_user_overrides():
    remove_prefs = []
    with open(os.path.join(temp_folder, "user-overrides.js"), "r") as user_overrides:
        # user_overrides = ["//// --- comment-out --- 'app.update.auto'",
        # "//// --- comment-out --- 'keyword.enabled'         // don't block search from urlbar"]
        for line in user_overrides:
            if line[:24] == "//// --- comment-out ---":
                pref_comment_pair = []
                pref_begins = line[line.find("'") + 1:]
                pref = pref_begins[:pref_begins.find("'")]
                print(pref)

                comment = pref_begins[pref_begins.find("'") + 1:]
                pref_comment_pair.append(pref)
                pref_comment_pair.append(comment.strip("\n"))
                remove_prefs.append(pref_comment_pair)
            elif line[:9] == "user_pref":
                pref_comment_pair = []
                pref_comment_pair.append(line.strip("\n"))
    # print(remove_prefs)
    return(remove_prefs)


# apply some prefs directly to "pref.js", users can change these later.
def apply_one_time_prefs(profile):
    # To show all addons in the toolbar
    ui_customization_raw = r'{\"placements\":{\"widget-overflow-fixed-list\":[],\"PersonalToolbar\":[\"personal-bookmarks\"],\"nav-bar\":[\"back-button\",\"forward-button\",\"stop-reload-button\",\"home-button\",\"customizableui-special-spring1\",\"urlbar-container\",\"downloads-button\",\"history-panelmenu\",\"bookmarks-menu-button\",\"library-button\",\"sidebar-button\",\"_3579f63b-d8ee-424f-bbb6-6d0ce3285e6a_-browser-action\",\"canvasblocker_kkapsner_de-browser-action\",\"cookieautodelete_kennydo_com-browser-action\",\"jid1-bofifl9vbdl2zq_jetpack-browser-action\",\"https-everywhere_eff_org-browser-action\",\"ublock0_raymondhill_net-browser-action\",\"jid1-mnnxcxisbpnsxq_jetpack-browser-action\",\"woop-noopscoopsnsxq_jetpack-browser-action\",\"_74145f27-f039-47ce-a470-a662b129930a_-browser-action\"],\"toolbar-menubar\":[\"menubar-items\"],\"TabsToolbar\":[\"tabbrowser-tabs\",\"new-tab-button\",\"alltabs-button\"]},\"seen\":[\"developer-button\",\"_3579f63b-d8ee-424f-bbb6-6d0ce3285e6a_-browser-action\",\"canvasblocker_kkapsner_de-browser-action\",\"cookieautodelete_kennydo_com-browser-action\",\"jid1-bofifl9vbdl2zq_jetpack-browser-action\",\"https-everywhere_eff_org-browser-action\",\"ublock0_raymondhill_net-browser-action\",\"jid1-mnnxcxisbpnsxq_jetpack-browser-action\",\"woop-noopscoopsnsxq_jetpack-browser-action\",\"_74145f27-f039-47ce-a470-a662b129930a_-browser-action\"],\"dirtyAreaCache\":[\"PersonalToolbar\",\"nav-bar\",\"toolbar-menubar\",\"TabsToolbar\"],\"currentVersion\":14,\"newElementCount\":4}'

    ui_customization_str = '"' + ui_customization_raw + '"'

    print("\nApplying onetime preferences to 'prefs.js'\n")

    # prefs to be applied directly to 'prefs.js' instead of 'users.js' so end users can change these
    # contains 'exists' to change if found and turn 'exists' True. the ones not found will be later added
    # keep this in profile loop, so 'exists' True resets for next profile
    pref_one_time = [
        {'pref': '"browser.uiCustomization.state"', 'value': ui_customization_str, 'exists': False},
        {'pref': '"browser.startup.homepage"', 'value': '"https://duckduckgo.com"', 'exists': False},
        {'pref': '"browser.startup.page"', 'value': '"https://duckduckgo.com"', 'exists': False},
    ]
    prefsjs_file = os.path.join(profile, "prefs.js")

    # touch prefs.js because the old one was moved to prefs-backups
    if not os.path.exists(prefsjs_file):
        Path(prefsjs_file).touch()

    # If pref exists, overwrite it
    with fileinput.input(prefsjs_file, inplace=True) as prefs_file:
        for line in prefs_file:
            for i in pref_one_time:
                if i['pref'] in line:
                    line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
                    # it is found, turn 'exists' to True
                    i['exists'] = True
                    # print(line)
            sys.stdout.write(line)

    # now append the rest of preferences
    with open(prefsjs_file, "a") as prefsjs:
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
    elif detected_os == "darwin":
        firefox_path == os.path.join(Path.home(), "Library/Application Support/Firefox/Profiles")

    if not os.path.exists(firefox_path):
        print("Please download and install firefox first https://www.mozilla.org/en-US/firefox/new/")
        sys.exit(1)

    # print("List of All Firefox Profiles : ", os.listdir(firefox_path))

    # onlydirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]
    # print(onlydirs)
    return firefox_path


def run(profile_name):
    if firefox_is_running():
        print("Firefox is currently running, please close firefox first then run Privacy Fighter again")
        sys.exit(1)

    # bundled "profile" folder that includes extension's config files
    bundled_profile_folder = resource_path("profile")
    # print(bundled_profile_folder)

    firefox_path = get_firefox_path()

    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    # sys.exit()
    if not profiles:
        print("ERROR: No Firefox Profile Found With The Name of '{}'. If Unsure Keep it 'default'".format(
            profile_name))
        sys.exit(1)
    elif len(profiles) == 1:
        profile = profiles[0]
        print("Firefox Profile to be secured/modified : ", profile, "\n")
    elif len(profiles) > 1:
        print("ERROR: 'Profile Name' string matches more than one profile folders, please provide a full name instead: ", profiles, "\n")
        sys.exit(1)

    setup_userjs()
    download_extensions()

    print("\nModified Preferences (Users.js) and Extensions will now be copied to {}\n".format(profile))
    # firefox profile path on the os
    firefox_p_path = os.path.join(firefox_path, profile)
    backup_prefsjs(firefox_p_path)
    recusive_copy(bundled_profile_folder, firefox_p_path)  # copies extension's config files
    recusive_copy(temp_folder, firefox_p_path)         # copies modified user.js, extensions
    apply_one_time_prefs(profile)                                    # modifies "prefs.js"

    # cleanup
    shutil.rmtree(temp_folder)

    print("------------------DONE-------------------\n")
    # here subprocess.run("firefox -p -no-remote"), ask user to create another profile TEMP, https://github.com/mhammond/pywin32
    print("You can now close this and run Firefox :)")
    # shutil.copy("profile/user.js", os.path.join(profile, "user.js"))
    # shutil.copy("profile/search.json.mozlz4", os.path.join(profile, "search.json.mozlz4"))


def backup_prefsjs(firefox_p_path):
    prefsjs_path = os.path.join(firefox_p_path, "prefs.js")
    prefsjs_backups_folder = os.path.join(firefox_p_path, "prefs-backups")
    prefsjs_backup_name = os.path.join(prefsjs_backups_folder, ("prefs-"
                                                                + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".js")))
    # create directory to store "prefs.js" backups
    # Changed in version 3.6: Accepts a path-like object.
    os.makedirs(prefsjs_backups_folder, exist_ok=True)
    print("Backing up the current 'prefs.js' to '{}'\n".format(prefsjs_backup_name))
    shutil.move(prefsjs_path, prefsjs_backup_name)


def recusive_copy(source_path, destination_path):
    for dirpath, dirnames, filenames in os.walk(source_path):
        for dirname in dirnames:
            pass
            # src_folder_path = os.path.join(dirpath, dirname)
            # dst_path = os.path.join(prof, dirname)
        for filename in filenames:
            src_file_path = os.path.join(dirpath, filename)
            src_list = list(Path(src_file_path).parts)
            # remove first element '/' from the list
            src_list.pop(0)
            # find index of base folder in order to extract subfolder paths
            # these subfolder paths will be created in dest location then appended to
            # the full path of files ~/.mozilla/firefox/TEST/"extensions/uBlock0@raymondhill.net.xpi"
            base_folder_ends = len(list(Path(source_path).parts)) - 1

            # extract section after 'profile' out of '/home/user/privacy-fighter/profile/extensions/ext.xpi'
            src_list = src_list[base_folder_ends:]

            # now src_file would be e.g extensions/ext.xpi
            src_file = Path(*src_list)

            dst_file_path = os.path.join(destination_path, src_file)
            # print("file : ", src_file_path, dst_file_path)
            print("Copying: ", src_file)
            # create parent directory
            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
            shutil.copy(src_file_path, dst_file_path)


def firefox_is_running():
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            # Check if process name contains the given name string.
            if "firefox" in pinfo['name'].lower():
                # print(pinfo)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if __name__ == "__main__":
    main()
