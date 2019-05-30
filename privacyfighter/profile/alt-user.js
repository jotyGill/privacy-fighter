

/* PRIVACY FIGHTHER 'user.js' FOR 'alternative' PROFILE

This setup only clears all types of persistent storage (cookies and caches) on shutdown.
To be used with the 'alternative' profile. Much better option than needing Chrome for rare occations when
a website breaks in the main profile.

***/


user_pref("privacyfighter.config.version", 67.0.0); // corresponds to firefox version, run PF again to fetch latest configuration sets


// enforce caches and cookies to clear on shutdown
user_pref("privacy.sanitize.sanitizeOnShutdown", true);
user_pref("privacy.clearOnShutdown.history", false);
user_pref("privacy.clearOnShutdown.formdata", false);
user_pref("privacy.clearOnShutdown.downloads", false);
user_pref("privacy.clearOnShutdown.openWindows", false);
