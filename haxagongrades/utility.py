import os

import click
import pandas as pd


def convert_json2csv(input, output):
    with open(input, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)

    df.to_csv(output, encoding='utf-8')


def get_password():
    password = os.environ.get('HAXAGON_PASSWORD')
    if password is None:
        password = click.prompt('Please enter your password', hide_input=True)
        os.environ['HAXAGON_PASSWORD'] = password
    return password


def get_username():
    password = os.environ.get('HAXAGON_USERNAME')
    if password is None:
        password = click.prompt('Please enter your username')
        os.environ['HAXAGON_USERNAME'] = password
    return password


def reorder_date(date: str):
    date_list = date.split('/')
    return "-".join([date_list[-1], date_list[0], date_list[1]])


if __name__ == '__main__':
    # convert_json2csv("/tmp/omega.json", "/tmp/omega.csv")
    print(reorder_date("2/4/2024"))
