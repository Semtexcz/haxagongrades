import json
import time
from collections import OrderedDict
from functools import cached_property
from typing import Dict, Optional

from loguru import logger
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager

from haxagongrades.utility import get_username, get_password, reorder_date


class Classroom:
    def __init__(self, name, element):
        self.name = name
        self.element: WebElement = element
        self._tasks: list = []
        self.manager = HaxagonManager()
        self._points = {}
        self._dates = {}

    @cached_property
    def tasks(self):
        if not self._tasks:
            self.manager.pick_classroom(self.name)
            # XPath pro nalezení všech odkazů, které mají href začínající na /challenge/ následované libovolným ID
            links = self.manager.driver.find_elements(By.XPATH, "//a[starts-with(@href, '/challenge/')]")

            # Pro výstup všech nalezených odkazů
            for link in links:
                self._tasks.append(Task(link.text, link.get_attribute('href')))
        return self._tasks

    @cached_property
    def points(self):
        if not self._points:
            logger.info("Collecting points for all tasks and all students in classroom")
            for task in tqdm(self.tasks):
                self._points[task.name] = task.points
        return self._points

    @cached_property
    def dates(self):
        if not self._dates:
            for task in tqdm(self.tasks):
                self._dates[task.name] = task.created

            self._dates = OrderedDict(sorted(self._dates.items(), key=lambda item: item[1]))
        return self._dates


class HaxagonManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HaxagonManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, headless: bool = False):
        if not hasattr(self, 'initialized'):
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            options.page_load_strategy = 'normal'
            self.driver: WebDriver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),
                                                      options=options)
            self.driver.implicitly_wait(10)
            self._classrooms: Dict[str, Classroom] = {}
            self.current_classroom: str | None = None
            self.initialized = True

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def login(self, username: Optional = None, password: Optional = None):
        if not username or not password:
            raise Exception('Missing required environment variables username and password.')
        self.driver.get("https://haxagon.xyz/")
        username_field = self.driver.find_element(By.TAG_NAME,
                                                  'input')
        password_field = self.driver.find_element(By.CSS_SELECTOR,
                                                  '#layout > main > div > div > form > div:nth-child(2) > div > input')

        username_field.send_keys(username)
        password_field.send_keys(password)

        password_field.send_keys(Keys.ENTER)
        time.sleep(10)
        logger.info("Logging in to haxagon")

    @property
    def is_class_menu_opened(self):
        value = self.driver.find_element(By.CSS_SELECTOR,
                                         "nav p")
        if value.text == 'Dashboard':
            return False
        else:
            return True

    @property
    def classrooms(self) -> Dict[str, Classroom]:
        classes = self.driver.find_elements(By.CSS_SELECTOR, 'nav h4')
        for class_ in classes[1:]:
            self._classrooms[class_.text] = Classroom(class_.text, class_)
        return self._classrooms

    def pick_classroom(self, class_name):
        if not self.is_class_menu_opened:
            self.open_classes_menu()
        self.classrooms[class_name].element.click()
        self.current_classroom = class_name
        time.sleep(5)
        logger.info(f"Picking classroom: {class_name}")

    def open_classes_menu(self):
        self.driver.find_element(By.CSS_SELECTOR, 'nav h4').click()


class Task:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.driver = HaxagonManager().driver
        self._points = {}
        self._created = None

    @cached_property
    def points(self):
        if not self._points:
            self.driver.get(self.url + "/solves")

            # Explicitní čekání na načtení tabulky
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main tr'))
            )

            rows = self.driver.find_elements(By.CSS_SELECTOR, 'main tr')[1:]
            for row in rows:
                cells = row.find_elements(By.CSS_SELECTOR, 'td')
                name = cells[0].text
                task_points = cells[1].text
                self._points[name] = task_points
        return self._points

    @cached_property
    def created(self):
        if not self._created:
            self.driver.get(self.url)

            # Explicitní čekání na načtení tabulky
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                                     '#layout > main > div > div > div.flex.flex-col.gap-8 > div.flex.flex-col.gap-4 > div.flex.flex-col.md\:flex-row.md\:gap-16 > div:nth-child(2) > div > span.font-medium'))
            )

            date = self.driver.find_element(By.CSS_SELECTOR,
                                            '#layout > main > div > div > div.flex.flex-col.gap-8 > div.flex.flex-col.gap-4 > div.flex.flex-col.md\:flex-row.md\:gap-16 > div:nth-child(2) > div > span.font-medium')
            self._created = reorder_date(date.text)
        return self._created


if __name__ == '__main__':
    manager = HaxagonManager()
    manager.login(get_username(), get_password())
    tasks = manager.classrooms["IFM - BASE - OMEGA"].dates
    # print(manager.classrooms["IFM - BASE - OMEGA"].tasks[1].created)
    # points = manager.classrooms["IFM - BASE - OMEGA"].points
    with open("/tmp/omega_tasks.json", "w") as f:
        json.dump(tasks, f, indent=4, ensure_ascii=False)
    # manager.pick_classroom('IFM - BASE - OMEGA')
