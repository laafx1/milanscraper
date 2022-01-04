from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time 
import csv
import xlsxwriter
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException        



def welcome():
    url_base= ''
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-features=NetworkService,NetworkServiceInProcess')
    options.add_argument('--dns-prefetch-disable')
    # options.add_argument("--start-maximized")
    options.add_argument('window-size=1920x1080')
    options.add_argument('--headless')
    driver = webdriver.Chrome(chrome_options = options)
    last_page = int(input('По какую страницу парсить : '))
    url_base = input('Введите вашу ссылку без фильтров: ')
    time.sleep(5)
    save_href = []
    descriptions_all = []
    titles_all = []
    prices_all = []
    prosmotri_all = []
    tovaru_all = []
    registration_years = []
    urls = []
    new_final = []
    final_years = []
    final_prices = []
    final_views = []
    final_urls = []
    final_tovaru = []
    phone_numbers_last_result = []
    save_page = []
    finallyy = []

    for h in range(1, last_page):
        url_base1 = url_base + '?desde=25&?demanda=n&fromSearch=1&orden=date&vendedor=part&pagina=' + str(h)
        driver.get(url_base1)
        print('Мы на странице: ' + str(h) + ' Обьявлений собрано: ' + str(len(new_final)))
        time.sleep(1)
        scroll = 300
        links = []
        save_page_new = []
        save_page_new.clear()
        links.clear()
        save_page.clear()
        
        try:
            captcha1 = driver.find_element_by_xpath("//div[@class='sui-TcfFirstLayer-buttons']//button[@data-testid='TcfAccept']")
        except:
            pass
        else:
            captcha1.click()
        
        for i in range(1,11):
            scroll = scroll+1000
            driver.execute_script("window.scrollTo(0, "+str(scroll)+");")
            time.sleep(0.4) 
        links = driver.find_elements_by_xpath('//a[@data-e2e="ma-AdCard-titleLink"]') 

        for link in links:
            save_href = link.get_attribute('href')
            save_page.append(save_href)
        save_page_new = save_page[::2]

        for jopa in save_page_new:
            if jopa == None :
                continue
            else:
                driver.get(jopa)
                time.sleep(2.3)
                try: 
                    descriptions = driver.find_element_by_xpath("//p[@class='ma-AdDetail-description']").text
                except:
                    continue
                else: 
                    descriptions_all.append(descriptions)
                    title = driver.find_element_by_xpath("//h1[@class='ma-AdDetail-title ma-AdDetail-title-size-heading-m']").text
                    prices = driver.find_element_by_xpath("//span[@class='ma-AdPrice-value ma-AdPrice-value--default ma-AdPrice-value--heading--l']").text
                    prosmotri = driver.find_element_by_xpath("//p[@class='ma-AdDetail-stats-counter']").text
                    useraccount = driver.find_element_by_xpath("//a[@data-testid='USER_OVERVIEW_PROFILE_LINK']")
                    url = str(jopa)
                    real_phone_numbers = []
                    real_phone_numbers.clear()  
                     
                    try:
                        call_button = driver.find_element_by_xpath("//button[@class='sui-AtomButton sui-AtomButton--primary sui-AtomButton--solid sui-AtomButton--center sui-AtomButton--fullWidth ma-AdContactCallButton']")
                    except:
                        pass
                    else: 
                        time.sleep(0.2)
                        call_button.click()
                        wait = WebDriverWait(driver, 20)
                        phone_number_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@class='ma-ModalContactCallPhoneLink-phone']"))).text
                        phone_number_button = driver.find_element_by_xpath("//a[@class='ma-ModalContactCallPhoneLink-phone']").text
                        time.sleep(2)
                        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
                        finallyy.append(str(phone_number_button))
                        for finals in finallyy:
                            if finals in new_final:
                                continue
                            else:
                                useraccount.click()
                                time.sleep(1.5)
                                try:
                                    tovaru = driver.find_element_by_xpath("//li[@class='sui-MoleculeTabs-item is-active']").text
                                except:
                                    pass
                                else:
                                    registration_year = driver.find_element_by_xpath("//p[@class='ma-ProfileLayoutCard-member-since-text']").text    
                                    tovaru_without_shit = tovaru[18:]
                                    tovaru_without_shit1 = tovaru_without_shit[:1]
                                    registration_year_without_shit = registration_year[11:]
                                    new_final.append(finals)
                                    urls.append(url)
                                    titles_all.append(title)
                                    prices_all.append(prices)
                                    prosmotri_all.append(prosmotri)
                                    tovaru_all.append(tovaru_without_shit1)
                                    registration_years.append(registration_year_without_shit)
                                    continue

    for objects in finallyy:
        new_final.append(objects)             
    for i in registration_years:
        final_years.append(i)
    for i in tovaru_all:
        final_tovaru.append(i)
    for i in prosmotri_all:
        prosmotri_bez_tochki = "".join(d for d in i if d.isdecimal())
        final_views.append(prosmotri_bez_tochki)
    for i in prices_all:
        final_prices.append(i)
    for i in urls:
        final_urls.append(i)
    for i in new_final:
        phone_numbers_with_34 = '34' + i
        phone_numbers_last_result.append(phone_numbers_with_34)

    outWorkbook = xlsxwriter.Workbook("out.xlsx")
    outSheet = outWorkbook.add_worksheet()

    outSheet.write("A1","Ссылка на обьявление")
    outSheet.write("B1","Номер телефона")
    outSheet.write("C1","Цена")
    outSheet.write("D1","Количество просмотров")
    outSheet.write("E1","Дата регистрации")
    outSheet.write("F1","Количество товаров")
    for item in range(len(final_urls)):
        outSheet.write(item+1, 0, final_urls[item])
        outSheet.write(item+1, 1, phone_numbers_last_result[item])
        outSheet.write(item+1, 2, final_prices[item])
        outSheet.write(item+1, 3, final_views[item])
        outSheet.write(item+1, 4, final_years[item])
        outSheet.write(item+1, 5, final_tovaru[item])
    outWorkbook.close()

    time.sleep(0.5)
    print('Парс закончен, всего собрано контактов: ' + str(len(phone_numbers_last_result)))

def main():
    welcome()

if __name__ == "__main__":
    main() 
