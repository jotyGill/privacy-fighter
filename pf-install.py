#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import shutil
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


def run(profile_name):
    # pf_profile = os.path.abspath("profile")
    pf_profile = resource_path("profile")
    print(pf_profile)
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

    profiles = glob.glob("{}*{}".format(firefox_path, profile_name))

    # firefox_path = Path.joinpath(Path(os.getenv('APPDATA')), Path("Mozilla/Firefox/Profiles/"))
    # profiles = firefox_path.glob("TEST")

    print(profiles)

    for prof in profiles:
        for dirpath, dirnames, filenames in os.walk(pf_profile):
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

                # shutil.copy("profile/user.js", os.path.join(profile, "user.js"))
        # shutil.copy("profile/search.json.mozlz4", os.path.join(profile, "search.json.mozlz4"))

    # for dirpath, dirnames, filenames in os.walk(os.path.join(Path.home(), ".mozilla/firefox/")):
    #     for filename in filenames:
    #         path = os.path.join(dirpath, filename)
    #         print("file :", path)
    #     for dirname in dirnames:
    #         path = os.path.join(dirpath, filename)
    #         print("dirs :", path)


if __name__ == "__main__":
    main()
