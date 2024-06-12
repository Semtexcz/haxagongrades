# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haxagongrades']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'pandas>=2.2.2,<3.0.0',
 'selenium>=4.21.0,<5.0.0',
 'tqdm>=4.66.4,<5.0.0',
 'webdriver-manager>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['haxagongrades = haxagongrades.cli:cli']}

setup_kwargs = {
    'name': 'haxagongrades',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Hexagon Grades',
    'author': 'Daniel Kopecký',
    'author_email': 'kopecky.d@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

