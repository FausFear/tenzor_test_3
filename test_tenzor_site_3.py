import os
import pytest
from tenzor_site_3 import SbisDownloader
from selenium.webdriver.common.by import By

@pytest.fixture(scope="module")
def sbis_downloader():
    url = "https://sbis.ru/"
    sbis_downloader = SbisDownloader(url)
    sbis_downloader.open_website()
    sbis_downloader.download_sbis()
    sbis_downloader.download_plugin()
    yield sbis_downloader
    sbis_downloader.close_browser()

# Тест на проверку скачался ли файл
def test_download_file(sbis_downloader):
    downloaded_file = sbis_downloader.download_file_name()
    assert os.path.exists(downloaded_file)

# Тест на сравнение размеров файла и размеров указанных на сайте
def test_file_size(sbis_downloader):
    downloaded_file = sbis_downloader.download_file_name()
    expected_size = float(
        sbis_downloader.browser.find_elements(By.CSS_SELECTOR, 
            ".sbis_ru-DownloadNew-loadLink__link.js-link")[16].text.split(' ')[-2])
    file_size = sbis_downloader.get_file_size(downloaded_file)
    assert file_size == expected_size

if __name__ == "__main__":
    pytest.main()
