from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
import time
import os
from selenium import webdriver
from bs4 import BeautifulSoup


def check_welder_naks(stigma):
    try:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        driver.set_window_size(1920, 1200)

        driver.get('https://naks.ru/registry/personal/')
        WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '/html/body/div[4]/div/div[3]/form/table/'
                                                                         'tbody/tr/td/table/tbody/tr[2]/td[1]/table/'
                                                                         'tbody/tr[4]/td[2]/font/input')))
        wind_naks = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/form/table/tbody/tr/td/table/'
                                                  'tbody/tr[2]/td[1]/table/tbody/tr[4]/td[2]/font/input')

        wind_naks.send_keys(f'{stigma["stigma"]["text"]}')

        naks_button = '/html/body/div[4]/div/div[3]/form/table/tbody/tr/td/table/tbody/tr[5]/td/font/input[1]'
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, naks_button)))

        driver.find_element(By.XPATH, '/html/body/div[4]/div/div[3]/form/table/tbody/tr/td/table/tbody/'
                                      'tr[5]/td/font/input[1]').click()

        time.sleep(3)
        table = driver.find_element(By.XPATH,
                                    '//*[@id="app_registry_personal"]/div/table')  # Таблица с данными на сварщика
        WebDriverWait(driver, 10).until(expected_conditions.visibility_of_element_located((By.XPATH,
                                                                                           '//*[@id="app_registry_personal"]/div/table')))
        table.location_once_scrolled_into_view


        b = BeautifulSoup(table.get_attribute('innerHTML'), 'html.parser')
        c = b.find_all('td', attrs={'rowspan': '2', 'align': 'center'})  # Верхняя часть таблицы с подписями полей

        test = b.find_all('td')

        welder_inf = {test[1].text.strip(): test[16].text.strip(), test[2].text.strip(): test[17].text.strip(),
                      test[3].text.strip(): test[18].text.strip(), test[4].text.strip(): test[19].text.strip(),
                      test[5].text.strip(): test[20].text.strip(), test[8].text.strip(): test[24].text.strip(),
                      test[9].text.strip(): test[25].text.strip(), test[10].text.strip(): test[26].text.strip(),
                      test[11].text.strip(): test[27].text.strip(),
                      test[12].text.strip(): test[28].text.strip().replace('подробнее', '')}
        print('table is parsed')
        # Вторая строка таблицы аттестации, при наличии
        second_attestation = []
        if len(test) > 30:
            second_attestation = [test[29].text.strip(), test[30].text.strip(), test[31].text.strip(),
                                  test[32].text.strip(),
                                  test[33].text.strip(), test[37].text.strip(), test[38].text.strip(),
                                  test[39].text.strip(),
                                  test[40].text.strip(), test[41].text.strip().replace('подробнее', '')]
        else:
            pass

        if second_attestation:
            welder_inf_second = {test[1].text.strip(): second_attestation[0],
                                 test[2].text.strip(): second_attestation[1],
                                 test[3].text.strip(): second_attestation[2],
                                 test[4].text.strip(): second_attestation[3],
                                 test[5].text.strip(): second_attestation[4],
                                 test[8].text.strip(): second_attestation[5],
                                 test[9].text.strip(): second_attestation[6],
                                 test[10].text.strip(): second_attestation[7],
                                 test[11].text.strip(): second_attestation[8],
                                 test[12].text.strip(): second_attestation[9].replace('подробнее', '')}

        # Модальное окно "подробнее об аттестации" первая строка

        WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="app_registry_personal"]/div/table'
                                                                         '/tbody/tr[3]/td[13]/a')))
        driver.find_element(By.XPATH, '//*[@id="app_registry_personal"]/div/table/tbody/tr[3]/td[13]/a').click()

        WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(
                (By.XPATH, '//*[@id="oblast_att"]/div[2]/table[2]/tbody')))
        podr = driver.find_element(By.XPATH, '//*[@id="oblast_att"]/div[2]/table[2]/tbody')

        details_attestation = (BeautifulSoup(podr.get_attribute('innerHTML'), 'html.parser')).find_all('td')
        details_attestation_1 = {details_attestation[0].text.strip(): details_attestation[1].text.strip(),
                                 details_attestation[2].text.strip(): details_attestation[3].text.strip(),
                                 details_attestation[4].text.strip(): details_attestation[5].text.strip(),
                                 details_attestation[6].text.strip(): details_attestation[7].text.strip(),
                                 details_attestation[8].text.strip(): details_attestation[9].text.strip(),
                                 details_attestation[10].text.strip(): details_attestation[11].text.strip(),
                                 details_attestation[12].text.strip(): details_attestation[13].text.strip(),
                                 details_attestation[14].text.strip(): details_attestation[15].text.strip(),
                                 details_attestation[16].text.strip(): details_attestation[17].text.strip(),
                                 }
        print('push details')

        details_attestation_3 = {}
        if second_attestation:
            driver.refresh()

            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="app_registry_personal"]/'
                                                                             'div/table/tbody/tr[4]/td[13]/a')))
            driver.find_element(By.XPATH, '//*[@id="app_registry_personal"]/div/table/tbody/tr[4]/td[13]/a').click()
            WebDriverWait(driver, 10).until(
                expected_conditions.visibility_of_element_located((By.XPATH, '//*[@id="oblast_att"]'
                                                                             '/div[2]/table[2]')))
            podr2 = driver.find_element(By.XPATH, '//*[@id="oblast_att"]/div[2]/table[2]')
            details_attestation_2 = (BeautifulSoup(podr2.get_attribute('innerHTML'), 'html.parser')).find_all('td')
            details_attestation_3 = {details_attestation_2[0].text.strip(): details_attestation_2[1].text.strip(),
                                     details_attestation_2[2].text.strip(): details_attestation_2[3].text.strip(),
                                     details_attestation_2[4].text.strip(): details_attestation_2[5].text.strip(),
                                     details_attestation_2[6].text.strip(): details_attestation_2[7].text.strip(),
                                     details_attestation_2[8].text.strip(): details_attestation_2[9].text.strip(),
                                     details_attestation_2[10].text.strip(): details_attestation_2[11].text.strip(),
                                     details_attestation_2[12].text.strip(): details_attestation_2[13].text.strip(),
                                     details_attestation_2[14].text.strip(): details_attestation_2[15].text.strip(),
                                     details_attestation_2[16].text.strip(): details_attestation_2[17].text.strip(),
                                     }

        summary_inf = ''
        # Первая строка аттестации
        summary_inf = summary_inf + 'Первая строка аттестации:\n'
        for key in welder_inf.keys():
            summary_inf = summary_inf + f'{key}   ---   {welder_inf[key]} \n'
        for key in details_attestation_1.keys():
            summary_inf = summary_inf + f'{key}  ---  {details_attestation_1[key]} \n'
        summary_inf = summary_inf + '\n\n\n'

        # Вторая строка аттестации, при наличии
        if second_attestation:
            summary_inf = summary_inf + 'Вторая строка аттестации:\n'
            for key in welder_inf_second.keys():
                summary_inf = summary_inf + f'{key}   ---   {welder_inf_second[key]}\n'
            for key in details_attestation_3:
                summary_inf = summary_inf + f'{key}  ---  {details_attestation_3[key]}\n'


        return summary_inf


    except Exception as e:
        return print(e)


