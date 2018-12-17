#!/usr/bin/env python3

import argparse
import sys
import requests
import fileinput


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
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1101996/clearurls-1.3.4.0-an+fx.xpi'},
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


def download_extension(url, extension_id):
    r = requests.get(url, allow_redirects=True)
    open('profile/extensions/' + extension_id, 'wb').write(r.content)


def download_file(url, dest):
    r = requests.get(url, allow_redirects=True)
    open(dest, 'wb').write(r.content)


for i in extensions:
    print("Downloading {}".format(i['name']))
    download_extension(i['url'], i['id'])


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
        # remove todo lines
        if line[:8] == '// TODO:':
            line = ''

    sys.stdout.write(line)

with open("profile/user.js", "a") as userjs:
    for i in pref_add:
        line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
        userjs.write(line)
