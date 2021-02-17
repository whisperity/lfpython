import subprocess

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("README.md", encoding="utf-8", errors="ignore") as md:
    long_description = md.read()

try:
    commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
    commit = commit.decode().strip()
except subprocess.CalledProcessError:
    commit = "0000000"
except OSError:
    commit = "0000000"

try:
    version = subprocess.check_output(["git", "describe", "--tags",
                                       "--dirty=\"-dirty\""])
    version = version.decode().strip()
    if version[0] == "v":
        version = version[1:]
    version = version.replace("-dirty", "dev")
    version_parts = version.split("-")
    if len(version_parts) == 1:
        version = version_parts[0]
    else:
        # Skip the commit count and inject the hash only.
        version = version_parts[0] + "+" + version_parts[2]
except subprocess.CalledProcessError:
    # No version tag found.
    version = "0.0.0+" + commit
except OSError:
    version = "0.0.0"


setup(
    name="lpython",
    description="Linearly written Python scripts in a pipeline",
    version=version,
    author="Whisperity",
    author_email="whisperity-packages@protonmail.com",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="http://github.com/whisperity/lpython",
    license="GPLv3+",
    keywords="python shell pipeline script scripting",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 or "
        "later (GPLv3+)",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development",
        "Topic :: System :: Shells"
        ],
    python_requires=">=3.6",

    packages=["lpython",
              "lpython.modes"
              ],
    package_dir={
        "lpython": "src/lpython"
        },

    entry_points={
        "console_scripts": [
            "lpython=lpython.lpython:main"
            ]
        }
)
