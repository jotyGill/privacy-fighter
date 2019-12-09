The project can be directly installed using pip without needing to build any binaries.

`sudo pip3 install -U privacyfighter`

OR

`python3 -m pip install --user -U privacyfighter`


## GNU/Linux
Building binary in GNU/Linux.

```bash
sudo apt install python3-pip
sudo pip3 install pyinstaller psutil requests
git clone https://github.com/jotyGill/privacy-fighter
cd privacy-fighter/privacyfighter
pyinstaller build-cli.spec --clean
```

## Windows with GUI
Uncomment lines in pf.py to 1. import 'gooey', 2. set gui_mode='True', 3. uncomment the gooey decorator

Building binary in windows.

```bash
pip3 install Gooey pyinstaller psutil requests
git clone https://github.com/jotyGill/privacy-fighter
cd privacy-fighter\privacyfighter
pyinstaller build.spec --clean
```
