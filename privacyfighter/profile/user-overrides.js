

/* PRIVACY FIGHTHER USER-OVERRIDES.JS START ***/
user_pref("_user.js.parrot", "overrides section syntax error");
user_pref("privacyfighter.config.version", 68.0.0); // corresponds to firefox version, run PF again to fetch latest configuration sets
user_pref("browser.newtabpage.blocked", "{\"4gPpjkxgZzXPVtuEoAL9Ig==\":1,\"K00ILysCaEq8+bEqV/3nuw==\":1,\"26UbzFJ7qT9/4DhodHKA1Q==\":1,\"mZmevP23jfB3rScn/QCWnw==\":1,\"BRX66S9KVyZQ1z3AIk0A7w==\":1}");


// SECTION 0100: STARTUP
//// --- comment-out --- 'browser.shell.checkDefaultBrowser'
//// --- comment-out --- 'browser.startup.homepage'
//// --- comment-out --- 'browser.startup.page'
//// --- comment-out --- 'browser.newtabpage.enabled'


// [SECTION 0200]: GEOLOCATION
// [SECTION 0300]: QUIET FOX

//// --- comment-out --- 'app.update.auto'
//// --- comment-out --- 'extensions.update.autoUpdateDefault'    # Keep extensions updated

//// --- comment-out --- 'browser.search.update'

// Don't force disable `Pocket`, as it has large userbase (10M+ installs on Androids alone)
// pocket is owned by Mozilla, if any organisation can be trusted with our bookmarks, it's got to be it.
//// --- comment-out --- 'extensions.pocket.enabled'

//// --- comment-out --- 'captivedetect.canonicalURL'
//// --- comment-out --- 'network.captive-portal-service.enabled'


// [SECTION 0500]: SYSTEM ADD-ONS / EXPERIMENTS
//// --- comment-out --- 'extensions.systemAddon.update.enabled'
//// --- comment-out --- 'extensions.systemAddon.update.url'

//// --- comment-out --- 'extensions.formautofill.addresses.enabled'
//// --- comment-out --- 'extensions.formautofill.available'
//// --- comment-out --- 'extensions.formautofill.heuristics.enabled'


// [SECTION 0700]: HTTP* / TCP/IP / DNS / PROXY / SOCKS etc
//// --- comment-out --- 'network.dns.disableIPv6'

//// --- comment-out --- 'network.http.altsvc.enabled'
//// --- comment-out --- 'network.http.altsvc.oe'

// //// --- comment-out --- 'network.proxy.socks_remote_dns'  // TODO See if problematic

//// --- comment-out --- 'network.file.disable_unc_paths'
//// --- comment-out --- 'network.gio.supported-protocols'


// [SECTION 0800]: LOCATION BAR / SEARCH BAR / SUGGESTIONS / HISTORY / FORMS
//// --- comment-out --- 'keyword.enabled'         // don't block search from urlbar

//// --- comment-out --- 'browser.search.suggest.enabled'    // live searches in urlbar
//// --- comment-out --- 'browser.urlbar.suggest.searches'
//// --- comment-out --- 'network.file.disable_unc_paths'
//// --- comment-out --- 'browser.formfill.enable'
// //// --- comment-out --- 'dom.forms.datetime'    // TODO See if problematic


// [SECTION 0900]: PASSWORDS
//// --- comment-out --- 'security.ask_for_password'
//// --- comment-out --- 'security.password_lifetime'

//// --- comment-out --- 'signon.autofillForms'
//// --- comment-out --- 'signon.formlessCapture.enabled'

//// --- comment-out --- 'network.auth.subresource-http-auth-allow' // some breakage https://bugzilla.mozilla.org/show_bug.cgi?id=1197944
//// --- comment-out --- 'signon.formlessCapture.enabled'


// [SECTION 1000]: CACHE / SESSION (RE)STORE / FAVICONS
//// --- comment-out --- 'browser.sessionstore.interval'


// [SECTION 1200]: HTTPS (SSL/TLS / OCSP / CERTS / HPKP / CIPHERS)
//// --- comment-out --- 'security.ssl.require_safe_negotiation'
//// --- comment-out --- 'security.tls.enable_0rtt_data'

//// --- comment-out --- 'security.OCSP.require'
//// --- comment-out --- 'security.pki.sha1_enforcement_level' // dont disable SHA-1 certificates
//// --- comment-out --- 'security.family_safety.mode'      // dont disable windows family safety cert
//// --- comment-out --- 'security.cert_pinning.enforcement_level'  // dont inforce cert pinning
//// --- comment-out --- 'security.mixed_content.block_display_content'


// [SECTION 1400]: FONTS
//// --- comment-out --- 'gfx.font_rendering.opentype_svg.enabled'
//// --- comment-out --- 'gfx.font_rendering.graphite.enabled'


// [SECTION 1600]: HEADERS / REFERERS
//// --- comment-out --- 'network.http.referer.XOriginPolicy'


// [SECTION 1700]: CONTAINERS
// [SECTION 1800]: PLUGINS
//// --- comment-out --- 'plugin.sessionPermissionNow.intervalInMinutes'

//// --- comment-out --- 'plugin.state.flash'  // dont force disable flash

// dont disable widevine CDM (Content Decryption Module)
//// --- comment-out --- 'media.gmp-widevinecdm.visible'
//// --- comment-out --- 'media.gmp-widevinecdm.enabled'

// dont disable all DRM content (EME: Encryption Media Extension)
//// --- comment-out --- 'media.eme.enabled'


// [SECTION 2000]: MEDIA / CAMERA / MIC
// keep WebRTC but expose only default ip (don't leak)
//// --- comment-out --- 'media.peerconnection.enabled'
//// --- comment-out --- 'media.peerconnection.ice.default_address_only'
//// --- comment-out --- 'media.peerconnection.ice.no_host'

// dont disable webGL
//// --- comment-out --- 'webgl.disabled'
//// --- comment-out --- 'webgl.dxgl.enabled'
//// --- comment-out --- 'webgl.enable-webgl2'
//// --- comment-out --- 'webgl.min_capability_mode'
//// --- comment-out --- 'webgl.disable-extensions'
//// --- comment-out --- 'webgl.disable-fail-if-major-performance-caveat'

// dont disable screensharing
//// --- comment-out --- 'media.getusermedia.screensharing.enabled'
//// --- comment-out --- 'media.getusermedia.browser.enabled'
//// --- comment-out --- 'media.getusermedia.audiocapture.enabled'


// [SECTION 2200]: WINDOW MEDDLING & LEAKS / POPUPS
// [SECTION 2300]: WEB WORKERS
// dont disable web workers, webnotifications
//// --- comment-out --- 'dom.serviceWorkers.enabled'


// [SECTION 2400]: DOM (DOCUMENT OBJECT MODEL) & JAVASCRIPT
//// --- comment-out --- 'dom.event.clipboardevents.enabled'

//// --- comment-out --- 'dom.allow_cut_copy'

// don't disable "Confirm you want to leave" dialog on page close
//// --- comment-out --- 'dom.disable_beforeunload'

//// --- comment-out --- 'javascript.options.asmjs'    // dont disable asm.js
//// --- comment-out --- 'javascript.options.wasm'    // dont disable WebAssembly
//// --- comment-out --- 'dom.vibrator.enabled'


// [SECTION 2500]: HARDWARE FINGERPRINTING
// [SECTION 2600]: MISCELLANEOUS
//// --- comment-out --- 'browser.tabs.remote.allowLinkedWebInFileUriProcess'
//// --- comment-out --- 'browser.pagethumbnails.capturing_disabled'
//// --- comment-out --- 'browser.uitour.enabled'
//// --- comment-out --- 'browser.uitour.url'
//// --- comment-out --- 'devtools.chrome.enabled'
//// --- comment-out --- 'network.IDN_show_punycode'
//// --- comment-out --- 'pdfjs.disabled'   # don't force enable it, as it doesn't always rendender properly

//// --- comment-out --- 'network.protocol-handler.external.ms-windows-store'

//// --- comment-out --- 'browser.download.manager.addToRecentDocs'
//// --- comment-out --- 'security.csp.experimentalEnabled'

//// --- comment-out --- 'extensions.enabledScopes'
//// --- comment-out --- 'extensions.autoDisableScopes'


// [SECTION 2700]: PERSISTENT STORAGE
// allow third party cookies, but session only and "4" exclude known trackers
//// --- comment-out --- 'network.cookie.cookieBehavior'  // ovewrritten to 4 in "user-overrides.js"
user_pref("network.cookie.cookieBehavior", 4);

// don't enforce history and downloads to clear on shutdown but cache, cookies, offline web data will be cleared
user_pref("privacy.sanitize.sanitizeOnShutdown", true);
user_pref("privacy.clearOnShutdown.history", false);
user_pref("privacy.clearOnShutdown.formdata", false);
user_pref("privacy.clearOnShutdown.downloads", false);
user_pref("privacy.clearOnShutdown.openWindows", false);

// // dont set time range to "Everything" as default in "Clear Recent History"
//// --- comment-out --- 'privacy.sanitize.timeSpan'


// [SECTION 4000]: FPI (FIRST PARTY ISOLATION)
// disable first party isolation, we use temporary_containers
//// --- comment-out --- 'privacy.firstparty.isolate'
//// --- comment-out --- 'privacy.firstparty.isolate.restrict_opener_access'


// [SECTION 4500]: RFP (RESIST FINGERPRINTING)
// heard this prevents from reviewing addons on AMO
//// --- comment-out --- 'privacy.resistFingerprinting.block_mozAddonManager'


user_pref("_user.js.parrot", "SUCCESS");
