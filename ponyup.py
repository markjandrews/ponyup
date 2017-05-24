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

MAX_GAMES_PER_ENTRY = 50


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(description='Fills out lottery entry form ready for payment')
    parser.add_argument('-f', '--input-file', required=True, help='Path to picked numbers json')
    parser.add_argument('-u', '--user-name', help='user name of lottery account')
    parser.add_argument('-p', '--password', help='password to decrypt account password')
    parser.add_argument('game', choices=configs.keys())

    args = parser.parse_args(argv)

    password = auth.get_creds('nswlotteries', args.user_name, args.password)

    print('Processing: %s' % args.input_file)
    with open(args.input_file, 'r') as inf:
        picked_list = json.load(inf)

    current_game = 0
    while current_game < len(picked_list):
        processor = configs[args.game].klass(webdriver.Chrome(CHROME_PATH), args.user_name, password)
        entry_picked_list = picked_list[current_game:current_game + MAX_GAMES_PER_ENTRY]
        processor.set_games(entry_picked_list)
        wait_until_browser_close(processor.driver)
        current_game += MAX_GAMES_PER_ENTRY

    print('Processing Complete')

if __name__ == '__main__':
    main()
