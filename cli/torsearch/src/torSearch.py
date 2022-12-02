import inquirer
import clipboard
from .utils.extractor import Extractor
from .utils.downloader import get_qbit_downloader
from .utils.cleaner import screen_clear
import json
import os
import time
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


class Handler(object):
    def __init__(self) -> None:
        try:
            self.qbit_downloader = get_qbit_downloader()
        except:
            self.qbit_downloader = None
        self.video_list = []

    def save_last_data(self):
        last_det = {
            'videos_list': self.video_list
        }

        os.chdir(os.getcwd())
        with open(f'{SCRIPT_DIR}/.last_data', 'w+') as f:
            json.dump(last_det, f)

    def search(self, query: str, src: int, page: int):
        if src == 1:
            temp_list = Extractor.extract_piratebay(query, page=page)
        elif src == 2:
            temp_list = Extractor.extract_kickass(query, page=page)
        else:
            temp_list = Extractor.extract_yify(query, page=page)

        self.video_list.extend(temp_list)

        self.save_last_data()

        self.show_list()

    def show_downloads(self):
        self.qbit_downloader.show_downloads(all=True)

    def show_current(self):
         while True:
            try:
                screen_clear()
                self.qbit_downloader.show_downloads(current=True)
                print("ℹ️ Press [CTRL+C] to exit")
                time.sleep(1)
            except KeyboardInterrupt as e:
                break

    def list_last(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        try:
            with open(f'{SCRIPT_DIR}/.last_data', 'r') as f:
                data = json.load(f)
                self.video_list = data['videos_list']
                self.show_list()
        except:
            print("🔥 No Entry Found!")

    def menu(self):
        screen_clear()
        print(
            "📃📃📃📃📃📃📃📃📃📃📃📃📃\n")
        options = [
            f"{i+1}. {self.video_list[i]['name']}" for i in range(len(self.video_list))]
        questions = [inquirer.List(
            'choice', message="Select an option?", choices=options, carousel=False)]
        
        # for i in range(len(self.video_list)):
        #     print(i+1, " 👉 ", self.video_list[i]['name'])
        # print()
        # index = int(input('Enter Your Choice (-1 to leave) ➼  '))
        
        try:
            index = inquirer.prompt(questions, raise_keyboard_interrupt=True, theme=inquirer.themes.load_theme_from_dict({
                "Question": {
                    "mark_color": "cyan",
                    "brackets_color": "normal",
                },
                "List": {
                    "selection_color": "magenta",
                    "selection_cursor": "👉"
                },
                "Checkbox": {
                    "selection_color": "magenta",
                    "selection_icon": "👉"
                }
            }))
        except KeyboardInterrupt:
            index = -1
        # print("ℹ️ Press [CTRL+C] to exit")
        if index is not None and not index == -1:
            urls = self.video_list[int(
                index['choice'][0].split('.')[0])-1]['magnetURL']
            if isinstance(urls, list):
                opts = [f"{j+1}. {link['text']}" for j,
                        link in enumerate(urls)]
                ques = [inquirer.Checkbox(
                    'choice', message="Select an option?", choices=opts, carousel=False)]
                try:
                    idx = inquirer.prompt(ques, raise_keyboard_interrupt=True, theme=inquirer.themes.load_theme_from_dict({
                        "Question": {
                            "mark_color": "cyan",
                            "brackets_color": "normal",
                        },
                        "List": {
                            "selection_color": "magenta",
                            "selection_cursor": "➼ "
                        }
                    }))
                except KeyboardInterrupt:
                    idx = -1
                # print("ℹ️ Press [CTRL+C] to exit")
                if idx is not None and not idx == -1:
                    url = urls[int(idx['choice'][0].split('.')[0])-1]['url']
            else:
                url = urls
            clipboard.copy(url)
            if self.qbit_downloader is not None:
                print('Your URL', ' >>> ', url)
                time.sleep(3)
                self.qbit_downloader.download_magnet_link(url)
                time.sleep(2)
                while True:
                    try:
                        screen_clear()
                        self.qbit_downloader.show_downloads()
                        print("ℹ️ Press [CTRL+C] to exit")
                        time.sleep(1)
                    except KeyboardInterrupt as e:
                        break
            else:
                while True:
                    try:
                        screen_clear()
                        print('Your URL', ' >>> ', url)
                        print("ℹ️ Press [CTRL+C] to exit")
                        time.sleep(1)
                    except KeyboardInterrupt as e:
                        break
            self.menu()

    def show_list(self):
        if len(self.video_list) > 0:
            self.menu()
