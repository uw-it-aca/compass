import os
from setuptools import setup

README = """
See the README on `GitHub
<https://github.com/uw-it-aca/compass>`_.
"""

# The VERSION file is created by travis-ci, based on the tag name
version_path = "compass/VERSION"
VERSION = open(os.path.join(os.path.dirname(__file__), version_path)).read()
VERSION = VERSION.replace("\n", "")

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

url = "https://github.com/uw-it-aca/compass"
setup(
    name="compass",
    version=VERSION,
    packages=["compass"],
    author="UW-IT Student & Educational Technology Services",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires=[
        'azure-storage-blob~=12.27',
        'django~=5.2',
        'django-user-agents',
        'django-simple-history==3.1.1',
        'django-userservice~=3.2',
        'django-supporttools~=3.6',
        'django-persistent-message~=1.3',
        'django-storages[google]>=1.10',
        'djangorestframework~=3.12',
        'django-person-client~=1.1',
        'uw-restclients-sws~=2.4',
        'uw-restclients-gws~=2.3',
        'uw-restclients-pws~=2.1',
        'uw-restclients-django-utils~=2.3',
        'uw-django-saml2~=1.8',
        'uw-memcached-clients~=1.0',
        'urllib3~=1.25',
        'python-dateutil~=2.8',
        'chardet~=5.0',
    ],
    license="Apache License, Version 2.0",
    description="A application for managing student advising information.",
    long_description=README,
    url=url,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
)
