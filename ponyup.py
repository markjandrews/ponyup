import argparse
import json
import os
import re
import sys
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from auth import auth
from config import configs
from ponyup.common import wait_until_browser_close

SCRIPT_DIR = os.path.dirname(__file__)
CHROME_PATH = os.path.join(SCRIPT_DIR, 'chromedriver.exe')


def find_input_files(input_file):
    if os.path.exists(input_file):
        return [input_file]

    input_dir, input_filename = os.path.split(os.path.abspath(input_file))
    base, ext = os.path.splitext(input_filename)

    input_files = []

    for file_in_dir in os.listdir(input_dir):
        full_filepath = os.path.join(input_dir, file_in_dir)
        if not os.path.isfile(full_filepath):
            continue

        m = re.match(r'%s\d+%s' % (base, ext), file_in_dir)
        if m:
            input_files.append(full_filepath)

    return input_files


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Fills out lottery entry form ready for payment')
    parser.add_argument('-f', '--input-file', required=True, help='Path to picked numbers json')
    parser.add_argument('-u', '--user-name', help='user name of lottery account')
    parser.add_argument('-p', '--password', help='password to decrypt account password')
    parser.add_argument('game', choices=configs.keys())

    args = parser.parse_args(argv)

    password = auth.get_creds('nswlotteries', args.user_name, args.password)

    input_files = find_input_files(args.input_file)

    for input_file in input_files:
        print('Processing: %s' % input_file)
        with open(input_file, 'r') as inf:
            picked_list = json.load(inf)

        processor = configs[args.game].klass(webdriver.Chrome(CHROME_PATH), args.user_name, password)
        processor.set_games(picked_list)

        wait_until_browser_close(processor.driver)

        print('Processing Complete')

if __name__ == '__main__':
    main()
