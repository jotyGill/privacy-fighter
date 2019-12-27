# Privacy-Fighter
<p align="center">
<a href="https://pypi.python.org/pypi/privacyfighter"><img alt="PyPi" src="https://img.shields.io/pypi/v/privacyfighter.svg"></a>
<a href="https://saythanks.io/to/jotyGill"><img alt="Say Thanks" src="https://img.shields.io/badge/say-thanks-ff69b4.svg"></a></p>

Easy to install, privacy protection browser setup.
A collection of best browser extensions and some configurations to help you fight for your privacy.

The deeper you dig, more you find that we're [loosing privacy from corporations](https://github.com/jotyGill/privacy). You might even start to believe that there's nothing you can do about it. You can!. With the right information, tools and dedication, you can do a lot to protect your privacy and stand up for your basic human right.
There are brilliant, hard working people who spend countless hours to make these privacy protecting tools. This project is a collection and setup of the best privacy protecting browser tools that exist today.
The basic setup installs the following addons and some [user.js configurations](https://github.com/jotyGill/privacy-fighter/blob/master/privacyfighter/profile/basic/basic-user.js)

1. [uBlock Origin](https://addons.mozilla.org/en-US/firefox/addon/ublock-origin/)
2. [Temporary Containers](https://addons.mozilla.org/en-US/firefox/addon/temporary-containers/)
3. [HTTPS Everywhere](https://addons.mozilla.org/en-US/firefox/addon/https-everywhere/)
4. [Canvas Blocker](https://addons.mozilla.org/en-US/firefox/addon/canvasblocker/)
5. [Decentraleyes](https://addons.mozilla.org/en-US/firefox/addon/decentraleyes/)
6. [ClearURLs](https://addons.mozilla.org/en-US/firefox/addon/clearurls/)
7. [Terms of Service; Didn't Read](https://addons.mozilla.org/en-US/firefox/addon/terms-of-service-didnt-read/)

**For further details about the project see [DOCS](https://github.com/jotyGill/privacy-fighter/tree/master/docs)**

**NOTE: From version 2.0 Privacy-Fighter is installed in a separate Firefox profile called "privacy-fighter". When upgrading from version 1.x to 2.x I recommend that you refresh your 'default' Firefox profile.
visit `about:support` and click "Refresh Firefox" (right corner)**

### 1.0 Installation<a name="installation"></a>
Advance users can check out the [Advance Options](https://github.com/jotyGill/privacy-fighter/tree/master/docs#advance). For the basic setup just follow the following instructions.

### 1.1 Installation Steps for Windows OS<a name="windows"></a>

1. If you don't have Firefox installed, First download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/).
2. Download [Privacy-Fighter.exe](https://github.com/jotyGill/privacy-fighter/releases/latest/download/Privacy-Fighter.exe).
3. Close Firefox and run the downloaded file Privacy-Fighter.exe
4. **After the installation finishes, follow the ["Post Installation"](#post-installation) section.**

### 1.2 Installation Steps for GNU/Linux and MacOS<a name="linux"></a>

1. If you don't have Firefox installed, First download and install [Firefox](https://www.mozilla.org/en-US/firefox/new/).
2. Close Firefox.
3. ON GNU/LINUX: Download and run the [privacyfighter-linux-amd64](https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-linux-amd64).
``` bash
wget https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-linux-amd64
chmod +x ./privacyfighter-linux-amd64
./privacyfighter-linux-amd64
```
3. ON MACOS: Download and run the [privacyfighter-macos-amd64](https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-macos).
``` bash
wget https://github.com/jotyGill/privacy-fighter/releases/latest/download/privacyfighter-macos
chmod +x ./privacyfighter-macos
./privacyfighter-macos
```
4. **After the installation finishes, follow the ["Post Installation"](#post-installation) section.**


### 2.0 Post Installation<a name="post-installation"></a>
1. After installation is done, open Firefox then "addons" (press Ctr+Shift+A) and enable all of them and allow them in private windows.
2. Open **Bookmarks Manager (press Ctr+Shift+O)** > **"Import and Backup"** (top menu item) > **Import Data from Another Browser**, follow wizard to import your bookmarks and history from your existing browser (Chrome/Edge/Safari).
3. You can change the default search engine from Google to DuckDuckGo.
 (Menu > Preferences > Search > Default Search Engine > DuckDuckGo)


### 3.0 Usage And Troubleshooting
After installing and following post installation setups. Every time you open Firefox, it will ask you to choose a profile.
Select "privacy-fighter" profile. If you ever encounter a webpage breakage simple copy the link, close Firefox then open the link in "default-release" profile.
