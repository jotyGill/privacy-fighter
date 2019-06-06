#!/usr/bin/env python3

import argparse
import datetime
import fileinput
import glob
import io
import os
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path, PurePath

import psutil
import requests

# from gooey import Gooey, GooeyParser

__version__ = "0.1.0"
__basefilepath__ = os.path.dirname(os.path.abspath(__file__))

# temporary folder to download files in
temp_folder = tempfile.mkdtemp()

# progress bar steps
total_steps = 8

# Create folders
extensions_folder = os.path.join(temp_folder, "extensions")
os.makedirs(extensions_folder, exist_ok=True)


# @Gooey(
#     progress_regex=r"^progress: (?P<current>\d+)/(?P<total>\d+)$",
#     progress_expr="current / total * 100",
#     program_name="Privacy Fighter",
#     requires_shell=False,
#     tabbed_groups=True,
#     default_size=(900, 530),
# )
def main():
    parser = argparse.ArgumentParser(description="Privacy-Fighter: A Browser Setup To Protect Your Privacy")
    parser.add_argument("-v", "--version", action="version",
                        version="Privacy-Fighter " + __version__)
    install_tab = parser.add_argument_group(
        "Install", "Please make sure:\n"
        "1. Firefox is installed but not running at the moment\n"
        "2. You have created a Firefox profile named 'alternative'\n"
        "3. After everything is finishes, remember to enable the installed addons/extensions."
    )
    install_tab.add_argument(
        "-m",
        "--setup-main",
        dest="setup_main",
        default=False,
        help="Part 1: Setup the main Firefox profile for day-to-day browsing",
        action="store_true",
    )
    install_tab.add_argument(
        "-a",
        "--setup-alt",
        dest="setup_alt",
        default=False,
        help="Part 2: Setup an 'alternative' Firefox profile. (to get around any issues)",
        action="store_true",
    )

    advance_options = parser.add_argument_group("Advance Options", "Customize the options")
    advance_options.add_argument(
        "-p",
        "--profile",
        dest="profile_name",
        default="default",
        help="Firefox Profile to be configured with PF",
        type=str,
    )
    advance_options.add_argument(
        "-u",
        "--user-overrides-url",
        dest="user_overrides_url",
        default="https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/profile/user-overrides.js",
        help="You can use your fork of user-overrides.js",
        type=str,
    )
    advance_options.add_argument(
        "-e",
        "--install-extensions",
        dest="install_extensions",
        default=True,
        help="Install and configure extensions (Highly Recommended)",
        action="store_true",
    )

    args = parser.parse_args()
    run(args.profile_name, args.user_overrides_url, args.install_extensions, args.setup_main, args.setup_alt)


def run(profile_name, user_overrides_url, install_extensions, setup_main, setup_alt):
    if not setup_main and not setup_alt:
        print("ERROR: At Least One 'setup_main' or 'setup_alt' Option Is Needed")
        sys.exit(1)

    if not latest_version():
        sys.exit(1)
    if firefox_is_running():
        print("Firefox is currently running, please close firefox first then run Privacy Fighter again")
        sys.exit(1)

    firefox_path = get_firefox_path()

    if setup_main:
        setup_main_profile(firefox_path, profile_name, user_overrides_url, install_extensions)
    if setup_alt:
        setup_alt_profile(firefox_path)

    # cleanup
    shutil.rmtree(temp_folder)

    print("------------------DONE-------------------\n")
    # here subprocess.run("firefox -p -no-remote"), ask user to create another profile TEMP, https://github.com/mhammond/pywin32
    print("You can now close this and run Firefox :)")


# The actual setup: if unless specified, the 'default' firefox profile will be setup with privacyfighter configs.
def setup_main_profile(firefox_path, profile_name, user_overrides_url, install_extensions):
    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    if not profiles:
        print(
            "ERROR: No Firefox Profile Found With The Name of '{}'. If Unsure Keep it 'default'".format(
                profile_name
            )
        )
        sys.exit(1)
    elif len(profiles) > 1:
        print(
            "ERROR: 'Profile Name' string matches more than one profile folders, please provide a full name instead: ",
            profiles,
            "\n",
        )
        sys.exit(1)
    else:
        profile = profiles[0]
        print("Firefox Profile to be secured/modified : ", profile, "\n")

    setup_userjs(user_overrides_url)
    if install_extensions:
        setup_extensions()

    # firefox profile path on the os
    firefox_p_path = os.path.join(firefox_path, profile)
    backup_prefsjs(firefox_p_path)
    print("\nModified Preferences (user.js) and Extensions will now be copied to {}\n".format(profile))
    recusive_copy(temp_folder, firefox_p_path)  # copies modified user.js, extensions
    apply_one_time_prefs(profile)  # modifies "prefs.js"


# The 'alternative' firefox profile.
def setup_alt_profile(firefox_path, profile_name="alternative"):

    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    if not profiles:
        print(
            "ERROR: No Firefox Profile Found With The Name of '{}'. First Create It (visit 'about:profiles' in Firefox) Then Run This Again\n".format(
                profile_name
            )
        )
    elif len(profiles) > 1:
        print(
            "ERROR: 'Profile Name' string matches more than one profile folders, please provide a full name instead: ",
            profiles,
            "\n",
        )
        sys.exit(1)
    else:
        profile = profiles[0]
        print("Firefox Profile to be configured as an alternative : ", profile, "\n")

        alt_userjs_path = os.path.join(firefox_path, profile, "user.js")
        download_file(
            "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/profile/alternative-user.js", alt_userjs_path)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = __basefilepath__

    return os.path.join(base_path, relative_path)


def setup_extensions():
    # Download the extensions list with their download links from the repo
    ext_list = get_file(
        "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/profile/extensions.json"
    )
    extensions = ext_list.json()["extensions"]

    for index, ext in enumerate(extensions):
        print("Downloading {}".format(ext["name"]))

        # Download and save extension.xpi files
        extension_xpi = get_file(ext["url"])
        open(os.path.join(extensions_folder, ext["id"]), "wb").write(extension_xpi.content)

        print("progress: {}/{}".format(index + 1, total_steps))
        sys.stdout.flush()

    # Download the "browser-extensions-data". these are extension's configuration files
    extensions_configs = get_file(
        "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/profile/browser-extension-data.zip"
    )
    with zipfile.ZipFile(io.BytesIO(extensions_configs.content)) as thezip:
        thezip.extractall(temp_folder)


# Download files using request.get(), throw error on exceptions
def get_file(url):
    try:
        r = requests.get(url, allow_redirects=True)
    except requests.RequestException:
        print(
            "Error while trying to download {} . Make sure internet connection is working then try again.".format(
                url
            )
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
            "Error while trying to download {} . Make sure internet connection is working then try again.".format(
                url
            )
        )
        sys.exit(1)


def setup_userjs(user_overrides_url):
    # Download the ghacks user.js
    download_file(
        "https://github.com/ghacksuserjs/ghacks-user.js/raw/master/user.js",
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
                pref_begins = line[line.find("'") + 1:]
                pref = pref_begins[: pref_begins.find("'")]
                # print(pref)
                comment = pref_begins[pref_begins.find("'") + 1:]
                pref_comment_pair.append(pref)
                pref_comment_pair.append(comment.strip("\n"))
                remove_prefs.append(pref_comment_pair)
            elif line[:9] == "user_pref":
                pref_comment_pair = []
                pref_comment_pair.append(line.strip("\n"))
    # print(remove_prefs)
    return remove_prefs


# apply some prefs directly to "pref.js", users can change these later.
def apply_one_time_prefs(profile):
    print("\nApplying onetime preferences to 'prefs.js'\n")

    # prefs to be applied directly to 'prefs.js' instead of 'user.js' so end users can change these
    # contains 'exists' to change if found and turn 'exists' True. the ones not found will be later added
    # keep this in profile loop, so 'exists' True resets for next profile

    # Download the "one time prefs" from the repo
    r = get_file(
        "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/profile/one-time-prefs.json"
    )
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


def get_firefox_path():
    detected_os = sys.platform

    if detected_os == "linux":
        firefox_path = os.path.join(Path.home(), ".mozilla/firefox/")
    elif detected_os == "win32":
        firefox_path = os.path.join(os.getenv("APPDATA"), "Mozilla\Firefox\Profiles" "\\")
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


def latest_version():
    # https://github.com/jotyGill/privacy-fighter/releases/latest/download/version.txt
    latest_version = get_file(
        "https://gitlab.com/JGill/privacy-fighter/raw/master/privacyfighter/version.txt"
    ).text.strip()
    if __version__ >= latest_version:
        return True
    print("Newer Privacy Fighter version = {} is available.".format(latest_version))
    print("please install the latest version from https://gitlab.com/JGill/privacy-fighter")
    return False


def backup_prefsjs(firefox_p_path):
    prefsjs_path = os.path.join(firefox_p_path, "prefs.js")
    prefsjs_backups_folder = os.path.join(firefox_p_path, "prefs-backups")
    prefsjs_backup_name = os.path.join(
        prefsjs_backups_folder,
        ("prefs-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".js")),
    )
    # create directory to store "prefs.js" backups
    # Changed in version 3.6: Accepts a path-like object.
    os.makedirs(prefsjs_backups_folder, exist_ok=True)
    print("\nBacking up the current 'prefs.js' to '{}'\n".format(prefsjs_backup_name))
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
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            # Check if process name contains the given name string.
            if "firefox" in pinfo["name"].lower():
                # print(pinfo)
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


if __name__ == "__main__":
    main()
