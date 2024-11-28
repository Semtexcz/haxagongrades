# Haxagon Grades



Haxagon Grades CLI is a command-line tool designed to manage and generate reports for Haxagon classes. The tool allows you to fetch and export class reports in different formats.

## Features

- Generate class reports in CSV or JSON format.
- Specify output directory for the generated reports.
- Supports headless mode for automated environments.

## Installation

Install the CLI using `pipx` to keep it isolated from your system Python packages:

```bash
pipx install haxagongrades
```

Make sure you have `pipx` installed. If not, you can install it via pip:

```bash
pip install pipx
pipx ensurepath
```

## Usage

After installing, you can use the `haxagongrades` command to interact with the CLI.

### Commands

#### `report`

Generate a report for a specific class.

```bash
haxagongrades report <class_name> [OPTIONS]
```

##### Options

- `-f, --format [csv|json]` (Required): Choose the output format.
- `-o, --output PATH`: The path to the output folder (default is `/tmp`).
- `-l, --login TEXT`: The username to login with.
- `-p, --password TEXT`: The password to login with.
- `--headless`: Run in headless mode (default is `False`).

### Examples

Generate a report in CSV format for class `3.A` and save it to the `/reports` directory:

```bash
haxagongrades report "3.A" --format csv --output /reports
```

Generate a JSON report for class `3.A` using headless mode:

```bash
haxagongrades report "3.A" --format json --headless
```

## Development

To contribute to this project, clone the repository and install the dependencies:

```bash
git clone https://github.com/Semtexcz/haxagongrades.git
cd haxagongrades
pip install -e .
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


