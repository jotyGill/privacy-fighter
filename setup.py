import sys

import setuptools

# import os

# from pillowcover_gui import __version__

# pf_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), "privacyfighter")
# exec(open(os.path.join(pf_location, "version.py")).read())
__version__ = "0.1.0"

if sys.version_info < (3, 5):
    sys.stderr.write("ERROR: requires Python 3.5 or above." + "Install using 'pip3' instead of just 'pip' \n")
    sys.exit(1)

with open("README.md", encoding="utf-8") as readme_file:
    full_description = readme_file.read()
    readme_file.close()

setuptools.setup(
    name="privacyfighter",
    version=__version__,
    description="Privacy-Fighter: A Browser Setup For Increased Privacy And Security",
    license="GNU General Public License v3 or later (GPLv3+)",
    author="JGill",
    zip_safe=False,
    author_email="joty@mygnu.org",
    url="https://gitlab.com/JGill/privacy-fighter",
    keywords=["privacy", "firefox", "browser"],
    python_requires=">=3.5",
    install_requires=["requests", "psutil"],
    platforms=["GNU/Linux", "Ubuntu", "Debian", "Kali", "CentOS", "Arch", "Fedora"],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": ["pf = privacyfighter.pf:main", "privacyfighter = privacyfighter.pf:main"]
    },
    include_package_data=True,
    long_description=full_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Security",
    ],
)
