

/* PRIVACY FIGHTHER 'user.js' FOR 'alternative' PROFILE

This setup only clears all types of persistent storage (cookies, caches, offline data) on shutdown.
To be used with the 'alternative' profile. Much better option than needing Chrome for rare occations when
a website breaks in the main profile.

***/


user_pref("privacyfighter.config.version", 68.0.0); // corresponds to firefox version, run PF again to fetch latest configuration sets


// enforce caches, cookies, ofline data to clear on shutdown
user_pref("privacy.sanitize.sanitizeOnShutdown", true);

user_pref("privacy.clearOnShutdown.cache", true);
user_pref("privacy.clearOnShutdown.cookies", true);
user_pref("privacy.clearOnShutdown.offlineApps", true); // Offline Website Data
user_pref("privacy.clearOnShutdown.sessions", true); // Active Logins

user_pref("privacy.clearOnShutdown.siteSettings", false); // Site Preferences
user_pref("privacy.clearOnShutdown.history", false); // Browsing & Download History
user_pref("privacy.clearOnShutdown.formdata", false); // Form & Search History
user_pref("privacy.clearOnShutdown.downloads", false);
user_pref("privacy.clearOnShutdown.openWindows", false);
