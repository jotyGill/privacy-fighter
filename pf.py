#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import requests
import fileinput

from pathlib import Path

to_add = [
    'user_pref("browser.newtabpage.activity-stream.improvesearch.topSiteSearchShortcuts.searchEngines", "duckduckgo");',
    'user_pref("browser.startup.homepage"; "https://start.duckduckgo.com");',
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
    {'name': 'chameleon', 'id': '{3579f63b-d8ee-424f-bbb6-6d0ce3285e6a}.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1148795/chameleon-0.9.21-an+fx.xpi'},

]


# id_decentraleyes = "jid1-BoFifL9Vbdl2zQ@jetpack.xpi"
# url_decentraleyes = "https://addons.mozilla.org/firefox/downloads/file/1078499/decentraleyes-2.0.8-an+fx.xpi"
#
# id_cookie_autodelete = "CookieAutoDelete@kennydo.com.xpi"
# url_cookie_autodelete = "https://addons.mozilla.org/firefox/downloads/file/954445/cookie_autodelete-2.2.0-an+fx.xpi"
#
# id_https_everywhere = "https-everywhere@eff.org.xpi"
# url_https_everywhere = "https://addons.mozilla.org/firefox/downloads/file/1132037/https_everywhere-2018.10.31-an+fx.xpi"
#
# id_ublock_origin = "uBlock0@raymondhill.net.xpi"
# url_ublock_origin = "https://addons.mozilla.org/firefox/downloads/file/1114441/ublock_origin-1.17.2-an+fx.xpi"
#
# id_canvas_blocker = "CanvasBlocker@kkapsner.de.xpi"
# url_canvas_blocker = "https://addons.mozilla.org/firefox/downloads/file/1108171/canvasblocker-0.5.5-an+fx.xpi"


firefox_path = os.path.join(Path.home(), ".mozilla/firefox/")
# print(firefox_path)
# print(os.listdir(firefox_path))

onlydirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]

# print(onlydirs)

print(glob.glob(firefox_path + "*.default"))

# for dirpath, dirnames, filenames in os.walk(os.path.join(Path.home(), ".mozilla/firefox/")):
#     for filename in filenames:
#         path = os.path.join(dirpath, filename)
#         print("file :", path)
#     for dirname in dirnames:
#         path = os.path.join(dirpath, filename)
#         print("dirs :", path)


def download_extension(url, extension_id):
    r = requests.get(url, allow_redirects=True)
    open('profile/extensions/' + extension_id, 'wb').write(r.content)


def download_file(url, dest):
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)


# for i in extensions:
#     print("Downloading {}".format(i['name']))
#     download_extension(i['url'], i['id'])

# download_extension(url_decentraleyes, id_decentraleyes)
# download_extension(url_ublock_origin, id_ublock_origin)
# download_extension(url_canvas_blocker, id_canvas_blocker)
# download_extension(url_cookie_autodelete, id_cookie_autodelete)
# download_extension(url_https_everywhere, id_https_everywhere)


download_file("https://raw.githubusercontent.com/pyllyukko/user.js/relaxed/user.js", "profile/user.js")
# download_file("https://github.com/ghacksuserjs/ghacks-user.js/raw/master/user.js", "profile/user.js")


# with open("profile/user.js") as o_config:
#     for line in o_config:
#         if 'user_pref("dom.vr.enabled"' in line:
#             print(line)
#         # print(line)

# https://stackoverflow.com/questions/39086/search-and-replace-a-line-in-a-file-in-python

# should_be_true = [
# // PREF: When using the location bar, don't suggest URLs from browsing history
# user_pref("browser.urlbar.suggest.history",			false);
# ]

for line in fileinput.input("profile/user.js", inplace=True):
    # line = line.rstrip('\r\n')
    if 'user_pref("dom.vr.enabled"' in line:
        # print(line.rstrip('\r\n') + "TSETSETST", end='\n')
        line = 'user_pref("dom.vr.enabled", true);'
    if 'user_pref("browser.urlbar.suggest.history"' in line:
        line = 'user_pref("browser.urlbar.suggest.history", true);'
    if 'user_pref("browser.urlbar.suggest.searches"' in line:
        line = 'user_pref("browser.urlbar.suggest.searches", true);'
    if 'user_pref("privacy.clearOnShutdown.history"' in line:
        line = 'user_pref("privacy.clearOnShutdown.history", false);'
    if 'user_pref("browser.clearOnShutdown.formdata"' in line:
        line = 'user_pref("browser.clearOnShutdown.formdata", false);'
    if 'user_pref("browser.clearOnShutdown.downloads"' in line:
        line = 'user_pref("browser.clearOnShutdown.formdata", false);'
    if 'user_pref("browser.clearOnShutdown.openWindows"' in line:
        line = 'user_pref("browser.clearOnShutdown.openWindows", false);'
    if 'user_pref("places.history.enabled"' in line:
        line = 'user_pref("places.history.enabled", true);'
    if 'user_pref("browser.download.manager.retention"' in line:
        line = 'user_pref("browser.download.manager.retention", 1);'
    if 'user_pref("browser.formfill.enable"' in line:
        line = 'user_pref("browser.formfill.enable", true);'
    if 'user_pref("browser.bookmarks.max_backups"' in line:
        line = 'user_pref("browser.bookmarks.max_backups", 5);'
    if 'user_pref("browser.newtabpage.enabled"' in line:
        line = 'user_pref("browser.newtabpage.enabled", true);'
    if 'user_pref("browser.newtab.url""' in line:
        line = ''
    if 'user_pref("browser.newtabpage.activity-stream.enabled"' in line:
        line = ''

    if line[:2] == '//':
        line = ''

    sys.stdout.write(line)
sys.stdout.write(
    'user_pref("browser.newtabpage.activity-stream.improvesearch.topSiteSearchShortcuts.searchEngines", "duckduckgo");\n')
