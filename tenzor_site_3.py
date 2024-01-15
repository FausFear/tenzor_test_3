import os
import wget
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time


class SbisDownloader:
    def __init__(self, url):
        self.url = url
        self.browser = Chrome()

    # Открываем сайт
    def open_website(self):
        self.browser.get(self.url)
        time.sleep(2)

    # Нажимаем кнопку Скачать
    def download_sbis_key(self):
        button_download_sbis = self.browser.find_element(By.PARTIAL_LINK_TEXT, "Скачать СБИС")
        button_download_sbis.send_keys(Keys.ENTER)
        time.sleep(2)

    # Нажимаем кнопку на боковой панели Плагин
    def download_plugin(self):
        button_plugin = self.browser.find_elements(By.CSS_SELECTOR, ".controls-TabButton__caption")[1]
        self.browser.execute_script("arguments[0].scrollIntoView(true);", button_plugin)
        actions = ActionChains(self.browser)
        actions.move_to_element(button_plugin).click().perform()
        time.sleep(2)

    # Скачиваем файл
    def download_file_name(self):
        file_button_download = (
            self.browser.find_elements(By.CSS_SELECTOR, ".sbis_ru-DownloadNew-loadLink__link.js-link"))[16]
        file_url = file_button_download.get_attribute("href")
        file_name = file_url.split('/')[-1]
        wget.download(file_url)
        time.sleep(5)
        return file_name

    # Получаем размер файла в мегабайтах
    def get_file_size(self, file_name):
        size_in_bytes = os.path.getsize(file_name)
        size_in_mb = round(size_in_bytes / (1024 * 1024), 2)
        return size_in_mb

    # Сравниваем размеры файла и размеры указанные на сайте
    def compare_file_size(self, file_size, expected_size):
        return file_size == expected_size

    def close_browser(self):
        self.browser.quit()


def main():
    sbis_downloader = SbisDownloader("https://sbis.ru/")
    sbis_downloader.open_website()
    sbis_downloader.download_sbis()
    sbis_downloader.download_plugin()
    downloaded_file = sbis_downloader.download_file_name()

    expected_size = float(
        sbis_downloader.browser.find_elements(By.CSS_SELECTOR, ".sbis_ru-DownloadNew-loadLink__link.js-link")[
            16].text.split(' ')[-2])
    file_size = sbis_downloader.get_file_size(downloaded_file)

    if sbis_downloader.compare_file_size(file_size, expected_size):
        print("Размер файла совпадает")
    else:
        print("Размер файла не верный")

    sbis_downloader.close_browser()


if __name__ == "__main__":
    main()
