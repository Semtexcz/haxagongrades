# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['haxagongrades']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.7,<9.0.0',
 'loguru>=0.7.2,<0.8.0',
 'pandas>=2.2.2,<3.0.0',
 'selenium>=4.21.0,<5.0.0',
 'tqdm>=4.66.4,<5.0.0',
 'webdriver-manager>=4.0.1,<5.0.0']

entry_points = \
{'console_scripts': ['haxagongrades = haxagongrades.cli:cli']}

setup_kwargs = {
    'name': 'haxagongrades',
    'version': '1.0.0a1',
    'description': '',
    'long_description': '# Hexagon Grades\n\n\n\nHaxagon Grades CLI is a command-line tool designed to manage and generate reports for Haxagon classes. The tool allows you to fetch and export class reports in different formats.\n\n## Features\n\n- Generate class reports in CSV or JSON format.\n- Specify output directory for the generated reports.\n- Supports headless mode for automated environments.\n\n## Installation\n\nInstall the CLI using `pipx` to keep it isolated from your system Python packages:\n\n```bash\npipx install haxagongrades\n```\n\nMake sure you have `pipx` installed. If not, you can install it via pip:\n\n```bash\npip install pipx\npipx ensurepath\n```\n\n## Usage\n\nAfter installing, you can use the `haxagongrades` command to interact with the CLI.\n\n### Commands\n\n#### `report`\n\nGenerate a report for a specific class.\n\n```bash\nhaxagongrades report <class_name> [OPTIONS]\n```\n\n##### Options\n\n- `-f, --format [csv|json]` (Required): Choose the output format.\n- `-o, --output PATH`: The path to the output folder (default is `/tmp`).\n- `-l, --login TEXT`: The username to login with.\n- `-p, --password TEXT`: The password to login with.\n- `--headless`: Run in headless mode (default is `False`).\n\n### Examples\n\nGenerate a report in CSV format for class `3.A` and save it to the `/reports` directory:\n\n```bash\nhaxagongrades report "3.A" --format csv --output /reports\n```\n\nGenerate a JSON report for class `3.A` using headless mode:\n\n```bash\nhaxagongrades report "3.A" --format json --headless\n```\n\n## Development\n\nTo contribute to this project, clone the repository and install the dependencies:\n\n```bash\ngit clone https://github.com/yourusername/haxagon-grades-cli.git\ncd haxagon-grades-cli\npip install -e .\n```\n\n## License\n\nThis project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.\n\n\n',
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

