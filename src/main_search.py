from selenium import webdriver
import time
import os
import pickle
import sys
from colorama import Fore
from selenium.webdriver.chrome.options import Options
import itertools
from selenium.webdriver.common.by import By
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display


class Search():

    def __init__(self, options, song):
        self.chrome = options
        self.song = song
        self.done = False
        self.hasAd = False
        self.driver = webdriver.Chrome(options=self.chrome)
        self.actions = ActionChains(self.driver)

    def GetPlaylist(self):
        next5 = {}
        for i in range(2,7):
            link = self.driver.find_element_by_xpath(
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                +str(i)+r']/a').get_attribute('href')
            title = self.driver.find_element_by_xpath(
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div[2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                +str(i)+r']/a/div/div[2]/h4/span').text
            next5[link]=title
        return next5

    def search(self):

        try:
            time.sleep(5)
            done = self.done
            t = threading.Thread(target=self.animate)
            t.start()
            options = self.chrome
            # options.add_argument('--headless')
            display = Display(visible=0, size=(1080, 1920))
            display.start()
            time.sleep(10)
            self.driver.implicitly_wait(10)
            self.driver.get("https://www.youtube.com")

            if os.path.isfile("cookies.pkl"):

                cookies = pickle.load(open("cookies.pkl", "rb"))

                for cookie in cookies:

                    if 'expiry' in cookie:

                        del cookie['expiry']

                    self.driver.add_cookie(cookie)
            self.song = "+".join(self.song.split(' '))
            self.driver.get(
                "https://www.youtube.com/results?search_query="+self.song)
            self.driver.maximize_window()
            self.driver.find_element_by_id("search-icon-legacy").click()
            self.done = True
            print("\n")
            self.driver.find_element_by_class_name(
                "style-scope ytd-video-renderer").click()
            self.done = True
            time.sleep(4)
            try:
                self.driver.find_element_by_class_name(
                    "style-scope ytd-compact-radio-renderer").click()
            except:
                print("Might not be a song!! No associated playlist!!")

            # info = self.driver.find_element_by_class_name("style-scope ytd-video-primary-info-renderer").text
            info = self.driver.find_element_by_xpath(
                r'//*[@id="container"]/h1/yt-formatted-string').text
            print(Fore.LIGHTRED_EX +
                  f"Now Playing: {Fore.LIGHTCYAN_EX + str(info)}")

            playlist = self.GetPlaylist()

            print(Fore.LIGHTRED_EX + "\nPlaylist:\n")

            for i, name in enumerate(playlist.values()):
                print(Fore.LIGHTRED_EX + 
                   f"{i+1}: {Fore.LIGHTCYAN_EX + name}")

            try:

                while True:

                    info2 = self.driver.find_element_by_xpath(
                        r'//*[@id="container"]/h1/yt-formatted-string').text
                    if(info2 != info):
                        print(Fore.LIGHTRED_EX +
                              f"\nNow Playing: {Fore.LIGHTCYAN_EX + str(info2)}")
                        info = info2
                        continue
                    else:
                        val = input(Fore.LIGHTRED_EX +
                            "New song: s\nPause: o\nNext song: p\nPrev song: i\nQuit: q\n>")
                        self.action(val)

            except KeyboardInterrupt:
                # driver.find_element_by_id("movie_player").click()
                # driver.quit()
                display.stop()
                print("\n")
                val = input(Fore.LIGHTRED_EX +
                            "New song: s\nPause: o\nNext song: p\nPrev song: i\nQuit: q\n>")
                return self.action(val)

        except KeyboardInterrupt:

            self.done = True
            print("\n")

            print(
                Fore.BLUE + "Interrupted before call completion. Exiting..." + Fore.RESET)
            # sys.exit(1)
            os._exit(1)

    def animate(self):

        for c in itertools.cycle(['|', '/', '-', '\\']):
            if self.done:
                break
            sys.stdout.write(Fore.LIGHTMAGENTA_EX +
                             '\rSearching for your song ' + c + Fore.RESET)
            sys.stdout.flush()
            time.sleep(0.1)

        # sys.stdout.write('\rDone!\n')

    def action(self, val):
        self.actions = ActionChains(self.driver)
        if val.lower() == "s":
            # display.stop()
            print("\n")
            new_song = input("Which Song: ")
            new_song = '+'.join(new_song.split(' '))
            self.driver.get("https://www.youtube.com/results?search_query="+new_song)
            self.driver.find_element_by_class_name(
                "style-scope ytd-video-renderer").click()
            

        elif val.lower() == 'o':
            self.actions.send_keys('k')
            self.actions.perform()
            self.actions = None

        elif val.lower() == 'p':
            self.actions.send_keys(Keys.LEFT_SHIFT + 'N')
            self.actions.perform()
            self.actions = None

        elif val.lower() == 'i':
            self.actions.send_keys(Keys.LEFT_SHIFT + 'P')
            self.actions.perform()
            self.actions = None
        
        elif val.lower() == "q":
            self.driver.quit()
            print(Fore.WHITE + "\nQuitting...")
            # display.stop()
            os._exit(1)

        else:
            self.actions = None
            print('Invalid option selected.\n')
            return
