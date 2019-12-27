#!/usr/bin/env python3

import argparse
import configparser
import datetime
import fileinput
import io
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

import psutil
import requests

# GUI-SETUP, is a tag used to find lines to change, to produce the gui-version
# from gooey import Gooey  # GUI-SETUP, comment out when producing cli version

gui_mode = False  # GUI-SETUP, change to 'True' in gui-version

__version__ = "2.0.0"
__basefilepath__ = os.path.dirname(os.path.abspath(__file__))

repo_location = "https://raw.githubusercontent.com/jotyGill/privacy-fighter/master/privacyfighter"

# temporary folder to download files in
temp_folder = tempfile.mkdtemp()

# progress bar steps
total_steps = 9

# Create folders
extensions_folder = os.path.join(temp_folder, "extensions")
os.makedirs(extensions_folder, exist_ok=True)


# GUI-SETUP, comment out the decorator @Gooey when in cli-mode
# @Gooey(
#     progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
#     progress_expr="current / total * 100",
#     hide_progress_msg=True,
#     program_name="Privacy Fighter",
#     requires_shell=False,
#     tabbed_groups=True,
#     default_size=(900, 530),
#     menu=[
#         {
#             "name": "About",
#             "items": [
#                 {
#                     "type": "AboutDialog",
#                     "menuTitle": "About",
#                     "name": "Privacy Fighter",
#                     "description": "A Browser Setup To Protect Your Privacy",
#                     "version": __version__,
#                     "website": "https://github.com/jotyGill/privacy-fighter",
#                     "developer": "https://github.com/jotyGill",
#                     "license": "GNU General Public License v3 or later (GPLv3+)",
#                 },
#                 {"type": "Link", "menuTitle": "Project Link", "url": "https://github.com/jotyGill/privacy-fighter"},
#             ],
#         }
#     ],
# )
def main():
    parser = argparse.ArgumentParser(description="Privacy-Fighter: A Browser Setup To Protect Your Privacy")
    if not gui_mode:
        parser.add_argument("-v", "--version", action="version", version="Privacy-Fighter " + __version__)
    install_tab = parser.add_argument_group(
        "Installation Info",
        "Please make sure:\n"
        "1. Firefox is installed but not running at the moment\n"
        "2. After this setup finishes, Remember to follow post installation instructions",
    )
    if gui_mode:
        install_tab.add_argument(
            "--show-post-installation-instructions",
            dest="post_installation_instructions",
            default="https://github.com/jotyGill/privacy-fighter/#70-post-installation",
            help="You can copy this link and open it after installation",
            type=str,
        )

    advance_options = parser.add_argument_group("Advance Options", "Advance Options for the geekz")
    advance_options.add_argument(
        "-p",
        "--profile",
        dest="profile_name",
        default="privacy-fighter",
        help="Firefox Profile to be configured with PF, default 'privacy-fighter'",
        type=str,
    )
    advance_options.add_argument(
        "-A",
        "-a",
        "--advance-setup",
        dest="advance_setup",
        default=False,
        help="Configure better protection with ghacks-user.js instead",
        action="store_true",
    )
    advance_options.add_argument(
        "-u",
        "--user-overrides-url",
        dest="user_overrides_url",
        default=repo_location + "/profile/advance/user-overrides.js",
        help="user-overrides.js to be applied over ghacks-user.js",
        type=str,
    )
    advance_options.add_argument(
        "--skip-extensions",
        dest="skip_extensions",
        default=False,
        help="Skip the installation/setup of extensions (NOT Recommended)",
        action="store_true",
    )
    advance_options.add_argument(
        "-i",
        "--import",
        dest="import_profile",
        default="default",
        help="Import history, bookmarks, saved passwords from old firefox profile",
        type=str,
    )

    if gui_mode:
        install_tab.add_argument(
            "--set-homepage",
            dest="set_homepage",
            default=True,
            help="Set homepage to privacy respecting search engine (DuckDuckGo)",
            action="store_false",
        )
        advance_options.add_argument(
            "--set-ui",
            dest="set_ui",
            default=True,
            help="Customise Firefox UI elements to better fit Addons (Recommended)",
            action="store_false",
        )
    else:
        install_tab.add_argument(
            "--no-homepage",
            dest="set_homepage",
            default=False,
            help="Don't change the homepage to duckduckgo",
            action="store_true",
        )
        advance_options.add_argument(
            "--no-ui", dest="set_ui", default=False, help="Don't customise firefox UI elements", action="store_true",
        )

    set_homepage = not parser.parse_args().set_homepage
    set_ui = not parser.parse_args().set_ui

    args = parser.parse_args()
    run(
        args.profile_name,
        args.user_overrides_url,
        args.skip_extensions,
        args.import_profile,
        args.advance_setup,
        set_homepage,
        set_ui,
    )


def run(profile_name, user_overrides_url, skip_extensions, import_profile, advance_setup, set_homepage, set_ui):
    if firefox_is_running():
        print("Firefox is currently running, please close firefox first then run Privacy Fighter again")
        sys.exit(1)
    if not latest_version():
        sys.exit(1)

    # if advance_setup is used and no profile name is given, name it "privacy-fighter-advance"
    if advance_setup and profile_name == "privacy-fighter":
        profile_name = "privacy-fighter-advance"

    detected_os = sys.platform

    # path to firefox profiles
    firefox_path = get_firefox_profiles_path(detected_os)

    firefox_ini_path = get_firefox_ini_path(detected_os)
    firefox_ini_config = parse_firefox_ini_config(firefox_ini_path)

    if not pf_profile_exists(profile_name, firefox_ini_config):
        create_pf_profile(profile_name, firefox_path, firefox_ini_path, firefox_ini_config, detected_os)
        import_profile_data(import_profile, profile_name, firefox_path, firefox_ini_config)
    setup_pf_profile(
        profile_name, firefox_path, user_overrides_url, skip_extensions, advance_setup, set_homepage, set_ui
    )

    # set firefox config to ask which profile to choose everytime you run firefox
    dont_autoselect_profiles(firefox_ini_path, firefox_ini_config)

    # cleanup
    shutil.rmtree(temp_folder)

    print("\n------------------DONE-------------------\n")
    # here subprocess.run("firefox -p -no-remote"), ask user to create another profile TEMP, https://github.com/mhammond/pywin32
    print(
        "You can now close this and run Firefox :)\n\n"
        "Remember to follow the post installation instructions (visit this link)\n"
        "https://github.com/jotyGill/privacy-fighter/#70-post-installation"
    )


# The actual setup: unless specified, a firefox profile with the name 'privacy-fighter' will be created and configured.
def setup_pf_profile(
    profile_name, firefox_path, user_overrides_url, skip_extensions, advance_setup, set_homepage, set_ui
):
    print("Setting up Firefox Profile '", profile_name, "'\n")

    # only setup ghacks-user.js, in advance mode, otherwise setup the "basic-user.js"
    if advance_setup:
        setup_ghacks_userjs(user_overrides_url)
    else:
        setup_basic_userjs()

    if not skip_extensions:
        setup_extensions(advance_setup)

    # privacy-fighter profile path on the os
    pf_profile_path = os.path.join(firefox_path, profile_name)
    backup_prefsjs(pf_profile_path)
    print("\nModified Preferences (user.js) and Extensions will now be copied to {}".format(pf_profile_path))
    recusive_copy(temp_folder, pf_profile_path)  # copies modified user.js, extensions
    if set_homepage:
        # set homepage to duckduckgo.com
        apply_one_time_prefs(pf_profile_path, repo_location + "/profile/set-homepage.json")
    if set_ui:
        # Customize Firefox UI to better fit all addons
        apply_one_time_prefs(pf_profile_path, repo_location + "/profile/set-ui.json")


def parse_firefox_ini_config(firefox_ini_path):
    config = configparser.ConfigParser()
    config.optionxform = str  # preserve string case

    config.read(firefox_ini_path)
    return config


def pf_profile_exists(profile_name, firefox_ini_config):
    for section in firefox_ini_config.sections():
        try:
            if firefox_ini_config.get(section, "Name") == profile_name:
                return True
        except configparser.NoOptionError:
            pass
    return False


def create_pf_profile(profile_name, firefox_path, firefox_ini_path, firefox_ini_config, detected_os):
    all_sections = firefox_ini_config.sections()
    # print(config.sections())

    pf_profile_path = os.path.join(firefox_path, profile_name)
    os.makedirs(pf_profile_path, exist_ok=True)

    # find the number of profiles setup in profiles.ini
    existing_no_of_profiles = len([p for p in all_sections if "Profile" in p])

    # choose new_profile's index to be same as len(existing profiles)
    # as existing profiles start from index 0 to len, excluding len
    new_profile = "Profile{!s}".format(existing_no_of_profiles)

    if detected_os == "linux":
        firefox_ini_config[new_profile] = {"Name": profile_name, "IsRelative": "1", "Path": profile_name}
    elif detected_os == "win32":
        firefox_ini_config[new_profile] = {
            "Name": profile_name,
            "IsRelative": "1",
            "Path": "Profiles/{}".format(profile_name),
        }
    elif detected_os == "darwin":
        firefox_ini_config[new_profile] = {
            "Name": profile_name,
            "IsRelative": "1",
            "Path": "Profiles/{}".format(profile_name),
        }
    firefox_ini_config.write(open(firefox_ini_path, "w"), space_around_delimiters=False)


def import_profile_data(import_profile, profile_name, firefox_path, firefox_ini_config):
    all_sections = firefox_ini_config.sections()
    # print(all_sections)

    import_profile_release = import_profile + "-release"
    import_profile_path = ""

    # Files to copy that store bookmarks, passwords db, site prefs etc.
    data_files = [
        "places.sqlite",
        "favicons.sqlite",
        "key4.db",
        "logins.json",
        "permissions.sqlite",
        "formhistory.sqlite",
    ]

    for section in all_sections:
        try:
            if import_profile_release in firefox_ini_config.get(section, "Name"):
                import_profile_path = os.path.join(firefox_path, firefox_ini_config.get(section, "Path"))
        except configparser.NoOptionError:
            pass
    # If "default-release" doesn't exist, find "default"
    if not import_profile_path:
        for section in all_sections:
            try:
                if firefox_ini_config.get(section, "Name") == import_profile:
                    # print(section)
                    import_profile_path = os.path.join(firefox_path, firefox_ini_config.get(section, "Path"))
                    # print(import_profile_path)
            except configparser.NoOptionError:
                pass

    for file in data_files:
        shutil.copy2(os.path.join(import_profile_path, file), os.path.join(firefox_path, profile_name))


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = __basefilepath__

    return os.path.join(base_path, relative_path)


def setup_extensions(advance_setup):
    # Download the extensions list with their download links from the repo
    ext_list = get_file(repo_location + "/profile/extensions.json")
    extensions = ext_list.json()["extensions"]

    for index, ext in enumerate(extensions):
        # only install some extensions in 'advance_setup' mode
        if not advance_setup and ext["advance_setup"] == "True":
            continue
        print("Downloading {}".format(ext["name"]))
        # Download and save extension.xpi files
        extension_xpi = get_file(ext["url"])
        open(os.path.join(extensions_folder, ext["id"]), "wb").write(extension_xpi.content)
        if gui_mode:
            print("progress: {}/{}".format(index + 1, total_steps))
        sys.stdout.flush()

    # Download the "browser-extensions-data". these are extension's configuration files
    extensions_configs = get_file(repo_location + "/profile/browser-extension-data.zip")
    with zipfile.ZipFile(io.BytesIO(extensions_configs.content)) as thezip:
        thezip.extractall(temp_folder)


# Download files using request.get(), throw error on exceptions
def get_file(url):
    try:
        r = requests.get(url, allow_redirects=True)
    except requests.RequestException:
        print(
            "Error while trying to download {} . Make sure internet connection is working then try again.".format(url)
        )
        sys.exit(1)
    return r


# Download files using request.get() and save them locally, throw error on exceptions
def download_file(url, dest):
    try:
        r = requests.get(url, allow_redirects=True)
        open(dest, "wb").write(r.content)
    except requests.RequestException:
        print(
            "Error while trying to download {} . Make sure internet connection is working then try again.".format(url)
        )
        sys.exit(1)


# Installs the default basic userjs
def setup_basic_userjs():
    # Download the simpler basic-user.js
    download_file(repo_location + "/profile/basic/basic-user.js", os.path.join(temp_folder, "user.js"))


# Installs the ghacks-user.js and applies the user_overrides
def setup_ghacks_userjs(user_overrides_url):
    # Download the ghacks user.js
    download_file(
        "https://raw.githubusercontent.com/ghacksuserjs/ghacks-user.js/master/user.js",
        os.path.join(temp_folder, "user.js"),
    )
    # Download the "user-overrides.js" with the latest ruleset from the repo
    download_file(user_overrides_url, os.path.join(temp_folder, "user-overrides.js"))

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
                    if pref in line:
                        line = "// {}   // [PRIVACYFIGHTER EXCLUDED] {}\n".format(line.strip("\n"), comment)

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
                pref_begins = line[line.find("'") + 1 :]
                pref = pref_begins[: pref_begins.find("'")]
                # print(pref)
                comment = pref_begins[pref_begins.find("'") + 1 :]
                pref_comment_pair.append(pref)
                pref_comment_pair.append(comment.strip("\n"))
                remove_prefs.append(pref_comment_pair)
            elif line[:9] == "user_pref":
                pref_comment_pair = []
                pref_comment_pair.append(line.strip("\n"))
    # print(remove_prefs)
    return remove_prefs


# apply some prefs directly to "pref.js", users can change these later.
def apply_one_time_prefs(profile, prefjs):
    # prefs to be applied directly to 'prefs.js' instead of 'user.js' so end users can change these
    # contains 'exists' to change if found and turn 'exists' True. the ones not found will be later added
    # keep this in profile loop, so 'exists' True resets for next profile

    # Download the config file containing preferences from the location
    r = get_file(prefjs)
    one_time_prefs = r.json()["prefs"]

    prefsjs_file = os.path.join(profile, "prefs.js")

    # touch prefs.js because the old one was moved to prefs-backups
    if not os.path.exists(prefsjs_file):
        Path(prefsjs_file).touch()

    # If pref exists, overwrite it
    with fileinput.input(prefsjs_file, inplace=True) as prefs_file:
        for line in prefs_file:
            for i in one_time_prefs:
                if i["pref"] in line:
                    line = "user_pref({}, {});\n".format(i["pref"], i["value"])
                    # it is found, turn 'exists' to True
                    i["exists"] = True
                    # print(line)
            sys.stdout.write(line)

    # now append the rest of preferences
    with open(prefsjs_file, "a") as prefsjs:
        for i in one_time_prefs:
            if not i["exists"]:
                line = "user_pref({}, {});\n".format(i["pref"], i["value"])
                # print(i)      # pref being added
                prefsjs.write(line)


def get_firefox_profiles_path(detected_os):
    if detected_os == "linux":
        firefox_path = os.path.join(str(Path.home()), ".mozilla/firefox/")
    elif detected_os == "win32":
        firefox_path = os.path.join(os.getenv("APPDATA"), "Mozilla\Firefox\Profiles" "\\")
        # firefox_path = Path.joinpath(Path(os.getenv('APPDATA')), Path("Mozilla/Firefox/Profiles/"))
    elif detected_os == "darwin":
        firefox_path = os.path.join(str(Path.home()), "Library/Application Support/Firefox/Profiles")

    if not os.path.exists(firefox_path):
        print("Please download and install firefox first https://www.mozilla.org/en-US/firefox/new/")
        sys.exit(1)

    return firefox_path


def get_firefox_ini_path(detected_os):
    if detected_os == "linux":
        firefox_ini_path = os.path.join(str(Path.home()), ".mozilla/firefox/profiles.ini")
    elif detected_os == "win32":
        firefox_ini_path = os.path.join(os.getenv("APPDATA"), "Mozilla\Firefox\profiles.ini")
    elif detected_os == "darwin":
        firefox_ini_path = os.path.join(str(Path.home()), "Library/Application Support/Firefox/profiles.ini")

    return firefox_ini_path


def latest_version():
    latest_version = get_file(
        "https://github.com/jotyGill/privacy-fighter/releases/latest/download/version.txt"
    ).text.strip()
    if __version__ >= latest_version:
        return True
    print("Newer Privacy Fighter version = {} is available.".format(latest_version))
    if gui_mode:
        print("Please download the latest version from https://github.com/jotyGill/privacy-fighter/releases/latest/")
    else:
        print(
            "Please download the latest version from "
            "https://github.com/jotyGill/privacy-fighter/releases/latest/ or upgrade via pip"
        )
    return False


def backup_prefsjs(pf_profile_path):
    prefsjs_path = os.path.join(pf_profile_path, "prefs.js")
    prefsjs_backups_folder = os.path.join(pf_profile_path, "prefs-backups")
    prefsjs_backup_name = os.path.join(
        prefsjs_backups_folder, ("prefs-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".js"))
    )
    # create directory to store "prefs.js" backups
    # Changed in version 3.6: Accepts a path-like object.
    os.makedirs(prefsjs_backups_folder, exist_ok=True)
    if os.path.exists(prefsjs_path):
        print("\nBacking up the current 'prefs.js' to '{}'".format(prefsjs_backup_name))
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

            dst_file_path = os.path.join(destination_path, str(src_file))
            # print("file : ", src_file_path, dst_file_path)
            # print("Copying: ", src_file)
            # create parent directory
            os.makedirs(os.path.dirname(dst_file_path), exist_ok=True)
            shutil.copy2(src_file_path, dst_file_path)


def firefox_is_running():
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if "firefox" in pinfo["name"].lower():
                # print(pinfo)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# set firefox config to ask which profile to choose everytime you run firefox
def dont_autoselect_profiles(firefox_ini_path, firefox_ini_config):

    try:
        firefox_ini_config.get("General", "StartWithLastProfile")
        firefox_ini_config["General"]["StartWithLastProfile"] = "0"
    except configparser.NoSectionError:
        firefox_ini_config["General"] = {"StartWithLastProfile": "0"}
    except configparser.NoOptionError:
        firefox_ini_config["General"]["StartWithLastProfile"] = "0"

    firefox_ini_config.write(open(firefox_ini_path, "w"), space_around_delimiters=False)


if __name__ == "__main__":
    main()
