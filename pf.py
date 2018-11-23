#!/usr/bin/env python3

import argparse
import glob
import os
import sys
import requests
import fileinput

from pathlib import Path

pref_add = [
    # {'pref': '"browser.newtabpage.activity-stream.improvesearch.topSiteSearchShortcuts.searchEngines"',
    #  'value': '"duckduckgo"'},
    {'pref': '"browser.startup.homepage"', 'value': '"https://duckduckgo.com"'},
    {'pref': '"dom.event.clipboardevents.enabled"', 'value': 'false'},

]

pref_mods = [
    {'pref': '"browser.safebrowsing.enabled"', 'value': 'false'},
    {'pref': '"browser.safebrowsing.phishing.enabled"', 'value': 'false'},
    {'pref': '"browser.safebrowsing.malware.enabled"', 'value': 'false'},
    {'pref': '"browser.safebrowsing.downloads.remote.enabled"', 'value': 'false'},

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
    {'pref': '"browser.clearOnShutdown.formdata"', 'value': ''},
    {'pref': '"browser.clearOnShutdown.openWindows"', 'value': ''},
    {'pref': '"browser.clearOnShutdown.downloads"', 'value': ''},
    {'pref': '"browser.download.manager.retention"', 'value': 1},
    {'pref': '"browser.bookmarks.max_backups"', 'value': 5},
    {'pref': '"browser.newtabpage.activity-stream.enabled"', 'value': ''},
    {'pref': '"browser.newtab.url"', 'value': ''},

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


firefox_path = os.path.join(Path.home(), ".mozilla/firefox/")
# print(firefox_path)
# print(os.listdir(firefox_path))

onlydirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d))]

# print(onlydirs)
print(glob.glob(firefox_path + "*.default"))


def download_extension(url, extension_id):
    r = requests.get(url, allow_redirects=True)
    open('profile/extensions/' + extension_id, 'wb').write(r.content)


def download_file(url, dest):
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)


# for i in extensions:
#     print("Downloading {}".format(i['name']))
#     download_extension(i['url'], i['id'])


download_file("https://raw.githubusercontent.com/pyllyukko/user.js/relaxed/user.js", "profile/user.js")
# download_file("https://github.com/ghacksuserjs/ghacks-user.js/raw/master/user.js", "profile/user.js")


for line in fileinput.input("profile/user.js", inplace=True):
    for i in pref_mods:
        if i['pref'] in line:
            if not i['value']:
                line = ''
            else:
                line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
        # remove comment lines
        # if line[:2] == '//':
            # line = ''

    sys.stdout.write(line)

with open("profile/user.js", "a") as userjs:
    for i in pref_add:
        line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
        userjs.write(line)
