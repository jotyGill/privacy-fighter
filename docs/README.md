# Privacy-Fighter
<p align="center">
<a href="https://pypi.python.org/pypi/privacyfighter"><img alt="PyPi" src="https://img.shields.io/pypi/v/privacyfighter.svg"></a>
<a href="https://saythanks.io/to/jotyGill"><img alt="Say Thanks" src="https://img.shields.io/badge/say-thanks-ff69b4.svg"></a></p>

Easy to install, privacy protection browser setup.
A collection of best browser extensions and some configurations to help you fight for your privacy.
**To install it, see the [Installation](#installation) section.**

The deeper you dig, more you find that we're [loosing privacy from corporations](https://github.com/jotyGill/privacy). You might even start to believe that there's nothing you can do about it. You can!. With the right information, tools and dedication, you can do a lot to protect your privacy and stand up for your basic human right.
There are brilliant, hard working people who spend countless hours to make these privacy protecting tools. This project is a collection and setup of the best privacy protecting browser tools that exist today. (if you have any suggestions, please create a github 'issue')


### Table of Contents
1. [Project Goals](#goals)
2. [Why Firefox?](#why)
3. [Disclaimer](#disclaimer)
4. [Installed/Configured Tools and Their Benefits](#tools)
5. [Security Improvements](#security)
6. [Installation](#installation)
7. [Post Installation](#post-installation)
8. [Known Inconveniences](#inconveniences)
9. [Advance Options](#advance)
10. [Troubleshooting](#troubleshooting)


### 1.0 Project Goals <a name="goals"></a>
The goals of this project are following:
* To create the best privacy protecting browser setup for average internet users, that doesn't break much functionality. "The best" is highly subjective, it is a battle between, functionality vs privacy, for better privacy we have to disable/work around many functionalities. The project aims for a sweet spot to minimise breakage of sites while retaining good privacy level.
* The project aims to protect users from hidden background tracking mechanisms and the ["filter bubbles"](https://www.ted.com/talks/eli_pariser_beware_online_filter_bubbles) that most don't even know exist. While using this setup every new tab is a completely new session. If you don't log in on a website you should see the results without any personalization thus escaping the filter bubbles. (Note: It can't protect your identity or privacy when you use a service (e.g Youtube/Facebook) while you are logged in.)
* [**Everyone is uniquely identifiable on the web**](https://github.com/gautamkrishnar/nothing-private), even if you use privacy protecting extensions/configurations. (see section: []). The project aims to create a single configuration set that minimises entropy (uniquely identifiable information). When same setup is used by many, it would make our digital fingerprints less unique.
* To Create a simple Installation method that takes just a few minutes to setup and requires minimal intervention. So that average internet user can install and benefit from it. (something that took me dozens of hours research, tinkering with configs/tools)
* The goal is not to blindly gather extensions (addons) or disable as many browser functionalities (using Firefox preferences) as possible. Neither it is to spoof as many browser values as possible, as doing that in some cases (user agent, OS, screen size) increases entropy (uniquely identifiable information). In this project I aim to research about, evaluate, test configuration sets and compatibility among the extensions and configurations that can help protect our privacy while browsing the web. Suggestions, corrections from all are welcome.

### 2.0 Why Firefox? <a name="why"></a>
**Requirement: Latest stable version of [Firefox](https://www.mozilla.org/en-US/firefox/new/): Currently 69**

If you are using Chrome (even Chromium) or Edge with default settings, not only they don't provide any privacy protection from third parties on the web.
**These browsers themselves collect detailed stats about your online behaviour.**
**The predominant browser Chrome tracks every webpage visit and periodically sends user location coordinates to Google. It also collects personal information(e.g. when a user completes online forms) and sends it to Google as part of the data synchronisation process. [c page 5, Google Data Collection Paper](https://digitalcontentnext.org/wp-content/uploads/2018/08/DCN-Google-Data-Collection-Paper.pdf)**
When you are logged into Chrome, all your browsing activity is without question linked to you. Even if you haven't logged in Chrome, Google still knows who you are with an extremely high precision.

Firefox on the other hand is developed by the non profit organisation Mozilla. It is the only viable fully open source competitor of Chrome. Mozilla being a non profit organisation has a fundamentally different business model than Google, which is a company built on profiling users and monetising that information.

### 3.0 Disclaimer <a name="disclaimer"></a>
This project is a collection of configurations to setup Firefox preferences and to setup and install third party extensions/addons. These extensions have been carefully chosen. They are downloaded straight from the "Firefox Add-ons store". Each addon is fully open source and anyone can view the code. Each of the addon's developer has high reputation and multi thousand downloads in the addons store. Because these addons are not developed by me, use them at your own risk.

### 4.0 Installed/Configured Tools and Their Benefits<a name="tools"></a>
This script installs and configures the following tools. A huge thanks to all the brilliant people behind these tools that have spent so much time and energy into making the world a better place.

0. [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/): Nothing like this would be possible without Firefox. "Firefox Containers" (Heavily utilised in this setup) is Mozilla's revolutionary approach to isolate online identities by containing cookies and local storage in multiple separate containers, allowing us to use the web with multiple identities or accounts simultaneously.

1. [ghacks-user.js](https://github.com/ghacksuserjs/ghacks-user.js/) When installed using the "Advance Setup" ghacks-user.js is used to modify more than a hundred Firefox preferences in order to improve privacy protection and reduce fingerprintablity.

    Configuration: To minimise breakage, a custom user-overrides.js is used to relax the non critical preferences

2. [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/): An efficient "wide-spectrum blocker", it blocks, ads, trackers and malware sites. [https://github.com/gorhill/uBlock]

3. [Temporary Containers](https://addons.mozilla.org/en-US/firefox/addon/temporary-containers/): Temporary Containers takes "Firefox Containers" to whole new level by making every new tab a different container. you may have heard of the advise to use multiple browsers. This pretty much makes every new tab a different, isolated (cookies, localstorage) browser, which gets deleted after it is closed. Eliminates long term tracking done using, cookies, storage caches, Etags.[https://github.com/stoically/temporary-containers]

    Configuration: Automatic mode enabled (every new tab opens in a new isolated container). Containers colour is set to random.

Get in the habit of opening new tabs and closing old ones. Also to open links in new containers (right click on link > "Open link in new Temporary Container Tab" instead.

4. [HTTPS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/):
HTTPS Everywhere is a Firefox extension by [EFF](https://www.eff.org/) to protect your communications by enabling HTTPS encryption automatically on sites that are known to support it.

5. [Canvas Blocker](https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/): Aims to prevent websites from using the some Javascript APIs to fingerprint users. resistFingerprinting takes preference to this, CanvasBlocker works as fallback for canvas fingerprinting. It also protects form fingerprinting the following APIs (by faking the values):
canvas 2d, webGL, audio, history, DOMRect [https://github.com/kkapsner/CanvasBlocker]

6. [Decentraleyes](https://addons.mozilla.org/en-US/firefox/addon/decentraleyes/): Protects you against tracking through "free", centralized, Content Delivery Networks, by locally storing libraries instead of fetching them from the tracking CDNs.

7. [ClearURLs](https://addons.mozilla.org/en-US/firefox/addon/clearurls/): Protects your privacy by removing the tracking fields in URLs.[https://gitlab.com/KevinRoebert/ClearUrls/]

8. [Terms of Service; Didn't Read](https://addons.mozilla.org/en-US/firefox/addon/terms-of-service-didnt-read/): Provides rating and extracts key points of the lengthy Terms and Conditions no one reads.[https://tosdr.org/]

### 5.0 Security Improvements<a name="security"></a>
Online ad networks are known to spread malware (malicious software: viruses, etc) [https://en.wikipedia.org/w/index.php?title=Ad_blocking&section=5#Security]. Effective Adblocking alone is a huge
security improvement. There are other security benefits of this setup. HttpsEveryware: for example ensures secure connections to well known websites. Leaving no persistent cache/cookies and making every new tab an isolated container, protects against several attack vectors.


### 6.0 Installation<a name="installation"></a>
If you are an advance user check out the [Advance Options](#advance), otherwise continue.

### 6.1 Installation Steps for Windows OS<a name="windows"></a>

1. If you don't have Firefox installed, First download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/).
2. Download [Privacy-Fighter.exe](https://github.com/jotyGill/privacy-fighter/releases/latest/download/Privacy-Fighter.exe).
3. Close Firefox and run the downloaded file Privacy-Fighter.exe
4. **After the installation finishes, follow the ["Post Installation"](#post-installation) section.**

### 6.2 Installation Steps for GNU/Linux and MacOS<a name="linux"></a>

1. If you don't have Firefox installed, First download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/).
2. Close Firefox.
3. ON GNU/LINUX: Download and run the [privacyfighter-linux-amd64](https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-linux-amd64).
``` bash
wget https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-linux-amd64
chmod +x ./privacyfighter-linux-amd64
./privacyfighter-linux-amd64
```
3. ON MACOS: Download and run the [privacyfighter-macos-amd64](https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-macos-amd64).
``` bash
wget https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-macos-amd64
chmod +x ./privacyfighter-macos-amd64
./privacyfighter-macos-amd64
```
4. **After the installation finishes, follow the ["Post Installation"](#post-installation) section.**


### 7.0 Post Installation<a name="post-installation"></a>
1. After installation is done, open Firefox then "addons" (press Ctr+Shift+A) and enable all of them and allow them in private windows.
2. Open **Bookmarks Manager (press Ctr+Shift+O)** > **"Import and Backup"** > **Import Data from Another Browser**, follow wizard to import your bookmarks and history from your existing browser (Chrome/Edge/Safari).
3. You can change the default search engine from Google to DuckDuckGo.
 (Menu > Preferences > Search > Default Search Engine > DuckDuckGo)

### 8.0 Known Inconveniences <a name="inconveniences"></a>
"I never said it would be easy". Ok I said the installation is easy.
* Firefox's internal window is smaller than usual. This is due to "privacy.resistFingerprinting" (RPF) protecting screen size (with letterboxing) in very clever way. It provides protections against screen size fingerprinting.
* You would have to fill google reCAPTCHA multiple times to confirm you are not robot. Have you noticed that these days you only have to check the reCAPTCHA box (reCAPTCHA v2) and don't need to fill any reCAPTCHA. And now v3 doesn't need any user interaction at all and you don't even know it's there. This works because [Google already knows exactly who you are](https://www.fastcompany.com/90369697/googles-new-recaptcha-has-a-dark-side) (on an average browser setup). **Google reCAPTCHA has become harsh to privacy aware users, you will have to fill it multiple times (3-8 times) and image squares will load very slowly. Google is abusing it's powerful position to deter users from using privacy protections [source](https://news.ycombinator.com/item?id=19623001) [discussion](https://github.com/ghacksuserjs/ghacks-user.js/issues/685).** I guess their approach is working when people start believing the problem is with the protection (privacy.resistFingerprinting) and the solution is to not use it [source](https://www.reddit.com/r/firefox/comments/a0dvrh/stuck_in_google_captcha_hell_try_disabling/).
* The reported time zone is set to UTC by RPF. All webapps (e.g your email site) would report UTC time.

These are the prices we have to pay, if we choose to fight for our privacy.

### 9.0 Advance Options <a name="advance"></a>
"--advance-setup": This mode installs ghacks-user.js to harden the profile and applies my user_overrides.js on it.
This mode provides better privacy protections but rarely some pages could break. To overcome those issues it is recommended to setup the 'alternative' profile and open those particular sites in it.

"--setup-alt": Setup the 'alternative' profile, which is a basic profile that deletes locally stored data (cookies,caches) on exit.
To use this option first you have to create a new profile and name it 'alternative'.
Open Firefox, visit link [`about:profiles`](about:profiles). Click `Create New Profile`, name it `alternative`.

"--profile": If you wish to setup PF in a different profile (other than 'default'). You can create a new profile and provide it's name. eg `~/.local/bin/privacyfighter -m -a -p your-new-profile-name`

### 10.0 Troubleshooting <a name="troubleshooting"></a>
Breakage on some pages might (hopefully very rarely) happen. You can just open the sites that break in the 'alternative' Firefox profile. That profile is setup to get around any site issues without needing any other browser.
To open it, visit link `about:profiles` in Firefox. Under `Profile: alternative`, click `Launch Profile In New Browser`

Or you can try troubleshooting the issue.

The steps to troubleshooting are
1. Disable UblockOrigin on that particular site (by clicking on it's icon then the blue power button) then reload the website and try again.
2. Temporarily disable ClearUrls (in Addons, Ctr+Shif+A) then reload the website and try again.
3. Please report any breakage bugs by filing an issue.
