# Privacy-Fighter
[UNDER DEVELOPMENT]

Easy to setup, fully transparent, online privacy protection browser setup.
A collection of browser configurations and extensions to help you fight for your online privacy.

The deeper you dig, more you find how we're loosing privacy from corporations [] (must read). You might wonder if it is a fight already lost or if you even have any choice. Well there are choices you can make to stand up for your basic human right.
There are brilliant, hard working people who spend countless hours to make these privacy protecting tools. This project is just a collection and setup of the best browser tools that exist today. (if you have any suggestions, please an create 'issue')

### Project Goals: <a name="goals"></a>
The goals of this project are following:
* To create the best privacy protecting browser setup for average internet users, that doesn't break much functionality and doesn't require much user intervention. "The best" is highly subjective, it is a battle between, functionality vs privacy, for better privacy we have to disable/work around many functionalities. The project aims for a sweet spot to minimise breakage of sites while retaining good privacy level.
* The project aims to protect users from hidden background tracking mechanisms and the "filter bubbles" that most don't even know exist. While using this setup every new tab is a completely new session. If you don't log in on a website you should see the results without any personalization thus escaping the filter bubbles. (Note: It can't protect your identity or privacy when you use a service (e.g Youtube/Facebook) while you are logged in.)
* **Everyone is uniquely identifiable on the web**, even if you use privacy protecting extensions/configurations. (see section: []). The project aims to create a single configuration set that minimises entropy (uniquely identifiable information). When same setup is used by many, it would make our digital fingerprints less unique. **This is the only way to combat fingerprinting.**
* To Create a simple Installation method and require minimal intervention so non technical people (even your grandma) can install and benefit from it.
* The goal is not to blindly gather extensions (addons) or disable as many browser functionalities (using firefox preferences) as possible. Neither it is to spoof as many browser values as possible, as doing that in some cases (user agent, OS, screen size) increases entropy (uniquely identifiable information). In this project I aim to research about, evaluate, test configuration sets and compatibility among the extensions and configurations that can help protect our privacy while browsing the web. Suggestions, corrections from all are welcome.

### Why Firefox?
**Requirement: Latest stable version of Firefox: 66**

If you are using Chrome (even Chromium) or Edge with default settings, not only they don't provide any privacy protection from third parties on the web.
**These browsers themselves collect detailed stats about your online behaviour, including every single webpage you have ever visited, every single search query you have ever made.**
**The predominant browser Chrome tracks every webpage visit and periodically sends user location coordinates to Google. It also collects personal information(e.g. when a user completes online forms) and sends it to Google as part of the data synchronisation process. [c page 5, Google Data Collection Paper]**
When you are logged into Chrome, all your browsing activity is without question linked to you. Even if you haven't logged in Chrome, Google still knows who you are with an extremely high precision (see section [] for details).

### Disclaimer.<a name="disclaimer"></a>
This project is a collection of configurations to setup firefox' preferences and to setup and install third party extensions/addons. These extensions have been carefully chosen. They are downloaded straight from the "Firefox Add-ons store". Each addon is fully open source and anyone can view the code. Each of the addon's developer has high reputation and multi thousand downloads in the addons store. Because these addons are not developed by me, use them at your own risk.

### Installed/Configured Tools and Their Benefits.
This script installs and configures the following tools. A huge thanks to all the brilliant people behind these tools that have spent so much time and energy into making the world a better place.

0. [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/): Developed by the non profit organization Mozilla, driving browser technologies and the only viable competitor of Chrome (by Google). Nothing like this would be possible without Firefox. "Firefox Containers" (Heavily utilised in this setup) is Mozilla's revolutionary approach to isolate online identities by containing cookies and local storage in multiple separate containers, allowing us to use the web with multiple identities or accounts simultaneously.

1. [ghacks-user.js](https://github.com/ghacksuserjs/ghacks-user.js/) is used to modify more than a hundred firefox preferences. "Tracking Protection", these have been shown to significantly improve privacy and security []. Another notable one being "privacy.resistFingerprinting".

    Configuration: To minimise breakage, a custom user-overrides.js is used to relax the non critical preferences

2. [Canvas Blocker](https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/): Aims to prevent websites from using the some Javascript APIs to fingerprint users. resistFingerprinting takes preference to this, CanvasBlocker works as fallback for canvas fingerprinting. It also protects form fingerprinting the following APIs (by faking the values):
canvas 2d, webGL, audio, history, DOMRect [https://github.com/kkapsner/CanvasBlocker]

    Configuration: disabled `Misc > Block data URL pages`

3. [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/): An efficient "wide-spectrum blocker", it blocks, ads, trackers and malware sites. [https://github.com/gorhill/uBlock]

    Configuration: Enabled "Fanboy's Cookie List" and "AdGuard Spyware filter". Expanded "requests blocked" pane.

4. [Cookie AutoDelete](https://addons.mozilla.org/en-US/firefox/addon/cookie-autodelete/):
When a tab closes, it automatically deletes any cookies that not being used. This prevents tracking by cookies, which is the primary method of tracking users. [](https://en.wikipedia.org/wiki/HTTP_cookie#Tracking) [https://github.com/Cookie-AutoDelete/Cookie-AutoDelete/]

    Configuration: Cookies are set to be deleted automatically after tab close. Enabled Support for Container Tabs

5. [Temporary containers](https://addons.mozilla.org/en-US/firefox/addon/temporary-containers/): Temporary Containers takes "Firefox Containers" to whole new level by making every new tab a different container. you may have heard of the advise to use multiple browsers[]. This pretty much makes every new tab a different, isolated (cookies, localstorage) browser, which gets deleted after it is closed. Eliminates long term tracking done using, cookies, storage caches, Etags.[https://github.com/stoically/temporary-containers]

    Configuration: Automatic mode enabled (every new tab becomes a new isolated container). Containers colour is set to purple. **Middle mouse click opens links in new isolated containers**.

6. [decentraleyes](https://addons.mozilla.org/en-US/firefox/addon/decentraleyes/): Protects you against tracking through "free", centralized, Content Delivery Networks, by locally storing libraries instead of fetching them from the tracking CDNs.

7. [clear_urls](https://gitlab.com/KevinRoebert/ClearUrls/): Protects your privacy by removing the tracking fields in URLs.[https://gitlab.com/KevinRoebert/ClearUrls/]

8. [Terms of Service; Didn't Read](https://addons.mozilla.org/en-US/firefox/addon/terms-of-service-didnt-read/): Provides rating and extracts key points of the lengthy Terms and Conditions no one reads.[https://tosdr.org/]

### Security Improvements:
Online ad networks are known to spread malware (malicious software: viruses, etc) [https://en.wikipedia.org/w/index.php?title=Ad_blocking&section=5#Security]. Effective Adblocking alone is a huge
security improvement. Many other security benifits included. HttpsEveryware: , CookieAutoDelete.


### Installation
The installation procedure.

1. If you don't have Firefox installed, Fist download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/).

**Advance Options** (For advance users)
1.1 If you have Firefox installed and wish to create another profile, visit `about:profiles`, create a new profile. Provide this name during the installation process.

#### Installation on Windows

2. Close Firefox then download and run [privacyfighter.exe]().
3. Now visit section "Post Installation".


#### Installation on GNU/Linux or MacOS

2. If you have python3 with pip, The best option is to install it using pip.
``` bash
python3 -m pip install --user privacyfighter --upgrade
```
3. Close Firefox then run `privacyfighter` or `~/.local/bin/privacyfighter` in terminal if it is a new Firefox installation.
Alternatively
3. Run while providing the new profile name `~/.local/bin/privacyfighter -p your-new-profile-name`

#### Post Installation
1. After installation is done, open Firefox then "addons" (Ctr+Shift+A) and enable all of them.
2. I recommend changing the default search engine from Google to DuckDuckGo or Startpage.
 (Menu > Preferences > Search > Default Search Engine > DuckDuckGo)
3. Remember Middle Mouse Click opens link in a new isolated container, get in the habit of using it. If you need to open a page in new tab that requires to you stay logged in. Use (right click > "Open in new tmp(number) Tab" instead.

### Known Inconveniences:
"I never said it would be easy". ok I said the installation is easy.
* Firefox opens in minimised window everytime. This is due to "privacy.resistFingerprinting" (RPF) protecting screen size which is used in fingerprinting.
* At times you would need to fill google reCAPTCHA multiple times to confirm you are not robot. Have you noticed that these days you only have to check the reCAPTCHA box (reCAPTCHA v2) and don't need to fill any reCAPTCHA. Even that is rarely needed because v3 doesn't need any user interaction at all. That is because **Google already knew exactly who you were.** **Google reCAPTCHA has become more harsh to privacy aware users, at times you will have to fill it multiple times (5-6 times). I assume it is another tactic to make people give up and not use any privacy protection against Google.**
* The reported time zone is set to UTC by RPF. All webapps (e.g your email site) would report UTC time.

These are the prices we have to pay, if we choose to fight for our privacy.

### Troubleshooting
Breakage would (hopefully very rarely) happen.

The steps to troubleshooting are
1. Disable UblockOrigin on that particular site (by clicking on it's icon then the blue power button) then reload the website and try again.
2. Temporarily disable ClearUrls (in Addons, Ctr+Shif+A) then reload the website and try again.
3. Please report any breakage bugs by filing an issue.

### References
