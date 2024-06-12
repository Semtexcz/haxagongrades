import json
import tempfile
from pathlib import Path

import click

from haxagongrades.main import HaxagonManager
from haxagongrades.utility import convert_json2csv, get_password, get_username


@click.group()
def cli():
    pass


@cli.command()
@click.argument("class_id")
@click.option('-f', '--format', type=click.Choice(['csv', 'json'], case_sensitive=False), prompt=True,
              help='Choose a output format')
@click.option('-o', '--output',
              type=click.Path(exists=True, file_okay=False, dir_okay=True, writable=True, readable=True,
                              resolve_path=True), help='The path to the output folder', default="/tmp")
@click.option('-l', '--login', 'login', default=lambda: get_username())
@click.option('-p', '--password', default=lambda: get_password(), help='The password to login with')
@click.option('--headless', is_flag=True, default=False, help='Run in headless mode')
def report(class_id: str, format: str, login: str, password: str, output: str, headless: bool):
    try:
        manager = HaxagonManager(headless=headless)
        manager.login(login, password)
        points = manager.classrooms[class_id].points

        if format == 'csv':
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(points, temp_file, indent=4, ensure_ascii=False)
                temp_file_path = temp_file.name
            convert_json2csv(temp_file_path, str(Path(output).resolve() / f'{class_id}.csv'))
        elif format == 'json':
            json.dump(points, str(Path(output).resolve() / f'{class_id}.json'), indent=4, ensure_ascii=False)
        else:
            raise NotImplementedError(format)
    except Exception as e:
        raise click.ClickException(f"Error: {e}")


@cli.command()
@click.option('-l', '--login', 'login', prompt=True)
@click.option('-p', '--password', prompt=True, hide_input=True, help='The password to login with')
def list(login: str, password: str):
    try:
        manager = HaxagonManager()
        manager.login(login, password)
        for classroom in manager.classrooms.keys():
            click.echo(classroom)
    except Exception as e:
        raise click.ClickException(f"Error: {e}")


if __name__ == '__main__':
    cli()
