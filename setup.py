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
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    include_package_data=True,
    install_requires = [
        'django~=3.2',
        'django-user-agents',
        'django-simple-history==3.1.1',
        'Django-UserService~=3.1',
        'Django-SupportTools',
        'djangorestframework~=3.12',
        'UW-RestClients-SWS~=2.3',
        'UW-RestClients-GWS~=2.3',
        'UW-RestClients-PWS~=2.1',
        'UW-Django-SAML2~=1.5',
        'urllib3~=1.25',
        'axdd-person-client==1.0.8'
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
