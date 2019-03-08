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

__version__ = "0.0.10"
__basefilepath__ = os.path.dirname(os.path.abspath(__file__))

# temporary folder to download files in
temp_folder = tempfile.mkdtemp()

# progress bar steps
total_steps = 12

# Create folders
extensions_folder = os.path.join(temp_folder, "extensions")
os.makedirs(extensions_folder, exist_ok=True)


pref_add = [
    # {'pref': '"browser.newtabpage.activity-stream.improvesearch.topSiteSearchShortcuts.searchEngines"',
    #  'value': '"duckduckgo"'},
    {'pref': '"app.update.auto"', 'value': 'true'},     # enable auto updates
    {'pref': '"privacyfighter.version"', 'value': '{}'.format(
        __version__)},     # Privacy Fighter Version
    # remove auto included Google, Youtube and Facebook shortcuts on newtabpage
    {'pref': '"browser.newtabpage.blocked"',
        'value': r'"{\"4gPpjkxgZzXPVtuEoAL9Ig==\":1,\"K00ILysCaEq8+bEqV/3nuw==\":1,\"26UbzFJ7qT9/4DhodHKA1Q==\":1}"', 'exists': False},
]

# preferences to be modified in the users.j. if 'value' is given in here, it will be overwritten
# using these. If 'value' is '', that preference will be deleted from users.js , so Firefox's Default
# or user's original preference stays in place.
# '' is used to get rid of undesired preferences set in ghacks's user.js. such as "places.history.enabled", "false"
pref_mods = [
    # SECTION 0100: STARTUP
    # dont enforce not checking defalut browser
    {'pref': '"browser.shell.checkDefaultBrowser"', 'value': ''},
    {'pref': '"browser.startup.homepage"', 'value': ''},
    {'pref': '"browser.startup.page"', 'value': ''},
    {'pref': '"browser.newtabpage.enabled"', 'value': ''},


    # [SECTION 0200]: GEOLOCATION
    # [SECTION 0300]: QUIET FOX
    {'pref': '"app.update.auto"', 'value': ''},
    {'pref': '"extensions.update.autoUpdateDefault"', 'value': 'true'},
    {'pref': '"app.update.service.enabled"', 'value': ''},
    {'pref': '"app.update.silent"', 'value': ''},
    {'pref': '"app.update.staging.enabled"', 'value': ''},
    {'pref': '"browser.search.update"', 'value': ''},

    {'pref': '"extensions.systemAddon.update.enabled"', 'value': ''},
    {'pref': '"extensions.formautofill.addresses.enabled"', 'value': ''},
    # {'pref': '"extensions.formautofill.creditCards.enabled"', 'value': ''},
    {'pref': '"extensions.formautofill.heuristics.enabled"', 'value': ''},
    {'pref': '"extensions.systemAddon.update.url"', 'value': ''},
    {'pref': '"network.dns.disableIPv6"', 'value': ''},
    {'pref': '"network.http.spdy.enabled"', 'value': ''},
    {'pref': '"network.http.spdy.enabled.deps"', 'value': ''},
    {'pref': '"network.http.spdy.enabled.http2"', 'value': ''},
    {'pref': '"network.http.spdy.websockets"', 'value': ''},

    {'pref': '"network.http.altsvc.enabled"', 'value': ''},
    {'pref': '"network.http.altsvc.oe"', 'value': ''},
    {'pref': '"network.http.spdy.websockets"', 'value': ''},
    {'pref': '"network.file.disable_unc_paths"', 'value': ''},
    {'pref': '"captivedetect.canonicalURL"', 'value': ''},
    {'pref': '"network.captive-portal-service.enabled"', 'value': ''},
    {'pref': '"network.gio.supported-protocols"', 'value': ''},
    # [SECTION 0500]: SYSTEM ADD-ONS / EXPERIMENTS
    {'pref': '"extensions.formautofill.addresses.enabled"', 'value': ''},
    {'pref': '"extensions.formautofill.available"', 'value': ''},
    {'pref': '"extensions.formautofill.heuristics.enabled"', 'value': ''},

    # [SECTION 0800]: LOCATION BAR / SEARCH BAR / SUGGESTIONS / HISTORY / FORMS


    {'pref': '"keyword.enabled"', 'value': ''},         # don't block search from urlbar
    # {'pref': '"browser.search.suggest.enabled"', 'value': ''},    # live searches in urlbar
    # {'pref': '"browser.urlbar.suggest.searches"', 'value': ''},
    {'pref': '"network.file.disable_unc_paths"', 'value': ''},
    {'pref': '"browser.formfill.enable"', 'value': ''},

    # [SECTION 0900]: PASSWORDS

    {'pref': '"security.ask_for_password"', 'value': ''},
    {'pref': '"security.password_lifetime"', 'value': ''},
    {'pref': '"signon.autofillForms"', 'value': ''},     # allow over tls but not for http
    {'pref': '"signon.autofillForms.http"', 'value': 'false'},  # DEL
    {'pref': '"network.auth.subresource-http-auth-allow"', 'value': ''},
    {'pref': '"signon.formlessCapture.enabled"', 'value': ''},

    # [SECTION 1000]: CACHE / SESSION (RE)STORE / FAVICONS
    {'pref': '"browser.sessionstore.interval"', 'value': ''},

    # [SECTION 1200]: HTTPS (SSL/TLS / OCSP / CERTS / HPKP / CIPHERS)
    {'pref': '"security.ssl.require_safe_negotiation"', 'value': ''},
    {'pref': '"security.tls.enable_0rtt_data"', 'value': ''},

    {'pref': '"security.OCSP.require"', 'value': ''},
    {'pref': '"security.pki.sha1_enforcement_level"', 'value': ''},     # dont disable SHA-1 certificates
    {'pref': '"security.family_safety.mode"', 'value': ''},     # dont disable windows family safety cert
    {'pref': '"security.cert_pinning.enforcement_level"', 'value': ''},  # dont inforce cert pinning
    {'pref': '"security.mixed_content.block_display_content"', 'value': ''},

    # [SECTION 1400]: FONTS
    {'pref': '"browser.display.use_document_fonts"', 'value': ''},  #
    {'pref': '"gfx.font_rendering.opentype_svg.enabled"', 'value': ''},
    {'pref': '"gfx.downloadable_fonts.woff2.enabled"', 'value': ''},
    {'pref': '"layout.css.font-loading-api.enabled"', 'value': ''},
    {'pref': '"gfx.font_rendering.graphite.enabled"', 'value': ''},

    # [SECTION 1600]: HEADERS / REFERERS
    {'pref': '"network.http.referer.XOriginPolicy"', 'value': ''},
    # [SECTION 1700]: CONTAINERS
    # [SECTION 1800]: PLUGINS
    {'pref': '"plugin.default.state"', 'value': ''},
    {'pref': '"plugin.defaultXpi.state"', 'value': ''},
    {'pref': '"plugin.sessionPermissionNow.intervalInMinutes"', 'value': ''},

    {'pref': '"plugin.state.flash"', 'value': ''},  # dont force disable flash
    {'pref': '"plugin.scan.plid.all"', 'value': ''},  # dont disable flash
    # dont disable all GMP (Gecko Media Plugins)
    {'pref': '"media.gmp-provider.enabled"', 'value': ''},
    {'pref': '"media.gmp.trial-create.enabled"', 'value': ''},
    {'pref': '"media.gmp-manager.url"', 'value': ''},
    {'pref': '"media.gmp-manager.url.override"', 'value': ''},
    {'pref': '"media.gmp-manager.updateEnabled"', 'value': ''},

    # dont disable widevine CDM (Content Decryption Module)
    {'pref': '"media.gmp-widevinecdm.visible"', 'value': ''},
    {'pref': '"media.gmp-widevinecdm.enabled"', 'value': ''},
    {'pref': '"media.gmp-widevinecdm.autoupdate"', 'value': ''},

    # dont disable all DRM content (EME: Encryption Media Extension)
    {'pref': '"media.eme.enabled"', 'value': ''},
    # dont disable the OpenH264 Video Codec by Cisco to
    {'pref': '"media.gmp-gmpopenh264.enabled"', 'value': ''},
    {'pref': '"media.gmp-gmpopenh264.autoupdate"', 'value': ''},
    # [SECTION 2000]: MEDIA / CAMERA / MIC
    # keep WebRTC but expose only default ip (don't leak)
    {'pref': '"media.peerconnection.enabled"', 'value': ''},
    {'pref': '"media.peerconnection.ice.default_address_only"', 'value': 'true'},
    {'pref': '"media.peerconnection.ice.no_host"', 'value': 'true'},

    # dont disable screensharing
    {'pref': '"media.getusermedia.screensharing.enabled"', 'value': ''},
    {'pref': '"media.getusermedia.browser.enabled"', 'value': ''},
    {'pref': '"media.getusermedia.audiocapture.enabled"', 'value': ''},
    {'pref': '"media.peerconnection.enabled"', 'value': ''},

    {'pref': '"canvas.capturestream.enabled"', 'value': ''},
    {'pref': '"media.autoplay.default"', 'value': ''},
    # [SECTION 2200]: WINDOW MEDDLING & LEAKS / POPUPS
    # [SECTION 2300]: WEB WORKERS
    # dont disable web workers, webnotifications
    {'pref': '"dom.serviceWorkers.enabled"', 'value': ''},
    {'pref': '"dom.webnotifications.enabled"', 'value': ''},
    {'pref': '"dom.webnotifications.serviceworker.enabled"', 'value': ''},
    # dont disable push notifications
    {'pref': '"dom.push.enabled"', 'value': ''},
    {'pref': '"dom.push.connection.enabled"', 'value': ''},
    {'pref': '"dom.push.serverURL"', 'value': ''},
    {'pref': '"dom.push.userAgentID"', 'value': ''},
    # [SECTION 2400]: DOM (DOCUMENT OBJECT MODEL) & JAVASCRIPT
    {'pref': '"dom.event.clipboardevents.enabled"', 'value': ''},
    # reconsider, disable "Confirm you want to leave" dialog on page close
    {'pref': '"dom.disable_beforeunload"', 'value': ''},
    {'pref': '"dom.allow_cut_copy"', 'value': ''},

    {'pref': '"javascript.options.asmjs"', 'value': ''},    # dont disable asm.js
    {'pref': '"javascript.options.wasm"', 'value': ''},    # dont disable WebAssembly
    {'pref': '"dom.vibrator.enabled"', 'value': ''},
    {'pref': '"dom.IntersectionObserver.enabled"', 'value': ''},

    {'pref': '"javascript.options.shared_memory"', 'value': ''},

    # [SECTION 2500]: HARDWARE FINGERPRINTING
    # [SECTION 2600]: MISCELLANEOUS
    {'pref': '"browser.tabs.remote.allowLinkedWebInFileUriProcess"', 'value': ''},
    {'pref': '"browser.pagethumbnails.capturing_disabled"', 'value': ''},
    {'pref': '"browser.uitour.enabled"', 'value': ''},
    {'pref': '"browser.uitour.url"', 'value': ''},
    {'pref': '"mathml.disabled"', 'value': ''},
    {'pref': '"network.IDN_show_punycode"', 'value': ''},
    {'pref': '"pdfjs.disabled"', 'value': ''},  # allow inbuilt pdfviewer

    {'pref': '"network.protocol-handler.external.ms-windows-store"', 'value': ''},
    {'pref': '"devtools.chrome.enabled"', 'value': ''},
    {'pref': '"browser.download.manager.addToRecentDocs"', 'value': ''},
    {'pref': '"browser.download.forbid_open_with"', 'value': ''},
    {'pref': '"security.csp.experimentalEnabled"', 'value': ''},

    # [SECTION 2700]: PERSISTENT STORAGE
    # allow third party cookies, but session only and "4" exclude known trackers
    {'pref': '"network.cookie.cookieBehavior"', 'value': '4'},

    # don't enforce history and downloads to clear on shutdown
    {'pref': '"privacy.sanitize.sanitizeOnShutdown"', 'value': 'true'},
    {'pref': '"privacy.clearOnShutdown.history"', 'value': 'false'},
    {'pref': '"privacy.clearOnShutdown.formdata"', 'value': 'false'},
    {'pref': '"privacy.clearOnShutdown.openWindows"', 'value': 'false'},
    {'pref': '"privacy.clearOnShutdown.downloads"', 'value': 'false'},
    # // dont set time range to "Everything" as default in "Clear Recent History"
    {'pref': '"privacy.sanitize.timeSpan"', 'value': ''},
    {'pref': '"dom.caches.enabled"', 'value': ''},

    # [SECTION 4000]: FPI (FIRST PARTY ISOLATION)
    # disable first party isolation, we use temporary_containers
    {'pref': '"privacy.firstparty.isolate"', 'value': 'false'},
    # [SECTION 4500]: RFP (RESIST FINGERPRINTING)

]

extensions = [
    {'name': 'decentraleyes', 'id': 'jid1-BoFifL9Vbdl2zQ@jetpack.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1671300/decentraleyes-2.0.9-an+fx.xpi'},
    {'name': 'cookie_autodelete', 'id': 'CookieAutoDelete@kennydo.com.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1209831/cookie_autodelete-3.0.1-an+fx.xpi'},
    {'name': 'https_everywhere', 'id': 'https-everywhere@eff.org.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1132037/https_everywhere-2018.10.31-an+fx.xpi'},
    {'name': 'ublock_origin', 'id': 'uBlock0@raymondhill.net.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1672871/ublock_origin-1.18.4-an+fx.xpi'},
    {'name': 'canvas_blocker', 'id': 'CanvasBlocker@kkapsner.de.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1677846/canvasblocker-0.5.8-an+fx.xpi'},
    # {'name': 'chameleon', 'id': '{3579f63b-d8ee-424f-bbb6-6d0ce3285e6a}.xpi',
    #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1157451/chameleon-0.9.23-an+fx.xpi'},
    # {'name': 'privacy_badger', 'id': 'jid1-MnnxcxisBPnSXQ@jetpack.xpi',
    #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1099313/privacy_badger-2018.10.3.1-an+fx.xpi'},
    {'name': 'clear_urls', 'id': '{74145f27-f039-47ce-a470-a662b129930a}.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1670276/clearurls-1.3.4.2-an+fx.xpi'},
    # {'name': 'privacy_possum', 'id': 'woop-NoopscooPsnSXQ@jetpack.xpi',
    #     'url': 'https://addons.mozilla.org/firefox/downloads/file/1062944/privacy_possum-2018.8.31-an+fx.xpi'},
    {'name': 'multi_account_containers', 'id': '@testpilot-containers.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1400557/firefox_multi_account_containers-6.1.0-fx.xpi'},
    {'name': 'facebook_container', 'id': '@contain-facebook.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1149344/facebook_container-1.4.2-fx.xpi'},
    {'name': 'google_container', 'id': '@contain-google.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1144065/google_container-1.3.4-fx.xpi'},
    {'name': 'temporary_containers', 'id': '{c607c8df-14a7-4f28-894f-29e8722976af}.xpi',
        'url': 'https://addons.mozilla.org/firefox/downloads/file/1675556/temporary_containers-0.91-fx.xpi'},

]


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

    # Modifying user.js: if "pref_mods" value is empty, remove it from user.js, if given overwrite it
    with fileinput.input(os.path.join(temp_folder, "user.js"), inplace=True) as userjs_file:
        for line in userjs_file:
            for i in pref_mods:
                if i['pref'] in line:
                    if not i['value']:
                        line = '// [PRIVACYFIGHTER EXCLUDED] ' + line
                    else:
                        line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
                # remove comment lines
                # if line[:2] == '//':
                    # line = ''
            sys.stdout.write(line)

    # Append additional prefs to user.js from "pref_add"
    with open(os.path.join(temp_folder, "user.js"), "a") as userjs:
        for i in pref_add:
            line = 'user_pref({}, {});\n'.format(i['pref'], i['value'])
            userjs.write(line)


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

    download_extensions()
    setup_userjs()

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
    prefsjs_backup_name = os.path.join(prefsjs_backups_folder, ("prefs-" +
                                                                str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".js")))
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
