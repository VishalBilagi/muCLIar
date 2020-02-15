from selenium import webdriver
import time
import os
import pickle
import sys
from colorama import Fore
import itertools
import threading
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from pyvirtualdisplay import Display
from getkey import getkey, keys

quitTitle = False

class Search():

    def __init__(self, options, song):
        self.chrome = options
        self.song = song
        self.done = False
        self.hasAd = False
        self.display = Display(visible=0, size=(1080, 1920))
        self.display.start()
        self.driver = webdriver.Chrome(options=self.chrome)
        self.actions = ActionChains(self.driver)
        self.title = None
        self.playlist = None


    def display_title(self):
        while True:
            try:
                info = self.driver.find_element_by_xpath(
                        r'//*[@id="container"]/h1/yt-formatted-string').text
                if (info != self.title and info != ''):
                    print(Fore.LIGHTRED_EX +
                            f"\nNow Playing: {Fore.LIGHTCYAN_EX + str(info)}")
                    self.title = info
            except Exception:
                pass
            global quitTitle
            if quitTitle:
                break

    def look_up_playlist(self):           
        try:
            self.driver.find_element_by_class_name(
                "style-scope ytd-compact-radio-renderer").click()
            self.playlist = self.GetPlaylist()
            print(Fore.LIGHTRED_EX + "\nUp Next:\n")
            for i, name in enumerate(self.playlist.values()):
                print(Fore.LIGHTRED_EX + 
                   f"{i+1}: {Fore.LIGHTCYAN_EX + name}")
            print("\n")
        except:
            print("Might not be a song!! No associated playlist!!\n")
            self.playlist = None

    def GetPlaylist(self):
        next5 = {}
        for i in range(2,7):
            link = self.driver.find_element_by_xpath(
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div['
                r'2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                + str(i) + r']/a').get_attribute('href')
            title = self.driver.find_element_by_xpath(
                r'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[4]/div['
                r'2]/div/ytd-playlist-panel-renderer/div/div[2]/ytd-playlist-panel-video-renderer['
                + str(i) + r']/a/div/div[2]/h4/span').text
            next5[link]=title
        return next5

    def search(self):

        try:
            time.sleep(5)
            done = self.done
            t = threading.Thread(target=self.animate)
            t.start()
            options = self.chrome
            #display = Display(visible=0, size=(1080, 1920))
            #display.start()
            # options.add_argument('--headless')
            
            
            time.sleep(10)
            self.driver.implicitly_wait(10)
            #self.driver.get("https://www.youtube.com")

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
            

            # info = self.driver.find_element_by_class_name("style-scope ytd-video-primary-info-renderer").text
            self.displayCheck = threading.Thread(target=self.display_title)
            self.displayCheck.start()
            self.look_up_playlist()

            while True:
                print(Fore.LIGHTGREEN_EX +
                    "\nNew song: s\nPause: o\nNext song: p\nPrev song: i\nQuit: q\nSeek 5 seconds backward: ←\n"
                      +"Seek 5 seconds forward: →\nVolume up: ↑\nVolume down: ↓\nMute: m\n" + Fore.RESET)
                val = getkey()
                self.command(val)

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

    def action(self, key_signal):
        self.actions = ActionChains(self.driver)
        self.actions.send_keys(key_signal)
        self.actions.perform()
        self.actions = None

    def command(self, val):
        self.actions = ActionChains(self.driver)
        if val.lower() == "s":
            # display.stop()
            print("\n")
            new_song = input("Which Song: ")
            new_song = '+'.join(new_song.split(' '))
            self.driver.get("https://www.youtube.com/results?search_query="+new_song)
            self.driver.find_element_by_class_name(
                "style-scope ytd-video-renderer").click()
            self.look_up_playlist()
            

        elif val.lower() == 'o':
            self.action('k')

        elif val.lower() == 'p':
            self.action(Keys.LEFT_SHIFT + 'N')

        elif val.lower() == 'i':
            self.action(Keys.LEFT_SHIFT + 'P')

        elif val.lower() == 'm':
            self.action('m')


        elif val == keys.LEFT:
            self.action(Keys.ARROW_LEFT)

        elif val == keys.RIGHT:
            self.action(Keys.ARROW_RIGHT)

        elif val == keys.UP:
            self.action(Keys.ARROW_UP)

        elif val == keys.DOWN:
            self.action(Keys.ARROW_DOWN)

        elif val.lower() == "q":
            self.driver.quit()
            global quitTitle
            quitTitle = True
            print(Fore.WHITE + "\nQuitting...")
            self.display.stop()
            os._exit(1)

        else:
            self.actions = None
            print('Invalid option selected.\n')
            return
