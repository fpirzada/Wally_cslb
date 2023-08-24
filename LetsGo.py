from Scraper.engine import Engine
from EStore import main

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup

import time
import json


def newTab(driver,url):

    # Open a new tab (Ctrl/Command + T)
    driver.execute_script("window.open('', '_blank');")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[1])

    # Navigate to a new URL in the new tab
    driver.get(url)

def closeTab(driver):
    # Close the new tab (Ctrl/Command + W)
    driver.close()

    # Switch back to the original tab
    driver.switch_to.window(driver.window_handles[0])


def get_city():
    # Open and read the JSON file
    with open('Data/US_States_and_Cities.json', 'r') as json_file:
        data = json.load(json_file)
    return data

def set_driver():
    try:
        manager = Engine()
        driver = manager.create_browser(timeout=5, headless=False, proxy=None, window_size='--start-maximized', clear_cache=False)
        return driver
    except Exception as e:
        print("===")
        print(e)

def click_FindMyLicensedContractor(driver,wait):
    driver.get("https://www.cslb.ca.gov/Consumer.aspx")
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.list-understated li')))
        FindMyLicensedContractor = driver.find_elements(By.CSS_SELECTOR, 'ul.list-understated li')
        FindMyLicensedContractor[1].find_element(By.TAG_NAME,"a").click()
    except Exception as e:
        print(e)

def click_next_page(driver,a_):
    # Get the current window handle (main page)
    main_window = driver.current_window_handle

    # Create an instance of ActionChains
    action_chains = ActionChains(driver)

    # Perform the control+click action on the link
    action_chains.key_down(Keys.COMMAND).click(a_).key_up(Keys.COMMAND).perform()

    # Switch to the newly opened tab
    new_window = driver.window_handles[-1]
    driver.switch_to.window(new_window)

    # Now you are on the newly opened tab
    # You can perform scraping using BeautifulSoup or any other method
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    return main_window, soup

def LicenseDetail(driver,wait,LicNo,result):
    try:
        wait.until(EC.presence_of_element_located((By.ID, 'SearchByLicenseNumber')))
        driver.find_element(By.ID,"MainContent_LicNo").send_keys("592080")
        driver.find_element(By.ID,"MainContent_Contractor_License_Number_Search").click()
    except Exception as e:
        print(e)
        print("-------- NO Contractor License #	PAGE --------")

    InsuranceCompanyCode = None
    P_Name = None
    P_Title = None
    P_AssociationDate = None
    P_Classification = None

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'MainContent_LicTable')))
        get_InsuranceCompanyCode = driver.find_element(By.ID,"MainContent_WCStatus").find_elements(By.TAG_NAME,'a')
        for index, a_ in enumerate(get_InsuranceCompanyCode):
            if index == 0:
                try:
                    main_window, soup = click_next_page(driver,a_)
                    driver.implicitly_wait(2)
                    soup_ = soup.find(id="MainContent_lblCode")
                    print(soup_.text)
                    InsuranceCompanyCode = soup_.text
                except Exception as e:
                    print("--")
                    print(e)
                    # driver.implicitly_wait(2)
                    # soup = soup.find(id="MainContent_dlHisList")
                    # print("-")
                    # table_ = soup.find("table")
                    # tr_ = table_.find_all("tr")
                    # for tr in tr_:
                    #     print(tr.text)
            # Close the newly opened tab
            driver.close()

            # Switch back to the main window
            driver.switch_to.window(main_window)

    except Exception as e:
        print(e)

    
    try:
        get_MainContent_PersonnelLink = driver.find_element(By.ID,"MainContent_PersonnelLink")
        main_window, soup = click_next_page(driver,get_MainContent_PersonnelLink)
        driver.implicitly_wait(2)
        soup_ = soup.find(id="MainContent_dlAssociated").find_all("table")
        for index, _ in enumerate(soup_):
            if index == 0:
                tr = _.find_all("tr")
                for tr_ in tr:
                    if tr_.find(id="MainContent_dlAssociated_hlName_0"):
                        P_Name = tr_.text
                    if tr_.find(id="MainContent_dlAssociated_lblTitle_0"):
                        P_Title = tr_.text
                    if tr_.find(id="MainContent_dlAssociated_lblAssociationDate_0"):
                        P_AssociationDate = tr_.text
                    if tr_.find(id="MainContent_dlAssociated_lblClassification_0"):
                        P_Classification = tr_.text
            
        # Close the newly opened tab
        driver.close()

        # Switch back to the main window
        driver.switch_to.window(main_window)

    except Exception as e:
        print(e)

    try:
        wait.until(EC.presence_of_element_located((By.ID, 'MainContent_LicTable')))
        driver.implicitly_wait(3)
        # Get the page source HTML
        page_source = driver.page_source

        # Create a Beautiful Soup instance to parse the page source
        soup = BeautifulSoup(page_source, 'html.parser')
        # print(soup[0])
        soup = soup.find(id="MainContent_LicTable")
        soup = soup.find_all('tr')

        MainContent_Entity = False
        MainContent_IssDt = False
        MainContent_ReIssueDt = False
        MainContent_ExpDt = False

        MainContent_Status = False
        MainContent_ClassCellTable = False
        MainContent_CertCellTable = False

        Contractor_Bond = False
        LLC_BOND = False
        BQI_Bond = False
        BQI_Bond_link = False

        MainContent_LLIStatus_ = False
        for tr in soup:
            
            print("--")
            if tr.select('h2.subheading'):
                print("-------- "+tr.text+" --------")
            if tr.select('td#MainContent_BusInfo'):
                print(list(tr.stripped_strings))
                for x in list(tr.stripped_strings):
                    print(x)
            if tr.select("td#MainContent_Entity"):
                print("Entity : "+tr.text)
                Entity = tr.text
                result.append(Entity.replace("Entity", ""))
                MainContent_Entity = True
            if tr.select("td#MainContent_IssDt"):
                IssDt = tr.text
                if MainContent_Entity:
                    print("Issue Date : "+tr.text)
                    result.append(IssDt.replace("Issue Date", ""))
                    MainContent_IssDt = True
                else:
                    result.append('')
                    result.append(IssDt.replace("Issue Date", ""))
                    MainContent_IssDt = True
                    
            if tr.select("td#MainContent_ReIssueDt"):
                ReIssueDt = tr.text
                if MainContent_IssDt:
                    print("Reissue Date : "+tr.text)
                    result.append(ReIssueDt.replace("Reissue Date", ""))
                    MainContent_ReIssueDt = True
                else:
                    result.append('')
                    result.append(ReIssueDt.replace("Reissue Date", ""))
                    MainContent_ReIssueDt = True

            if tr.select("td#MainContent_ExpDt"):
                ExpDt = tr.text
                if MainContent_ReIssueDt:
                    print("Expire Date : "+tr.text)
                    result.append(ExpDt.replace("Expire Date", ""))
                    MainContent_ExpDt = True
                else:
                    result.append('')
                    result.append(ExpDt.replace("Expire Date", ""))
                    MainContent_ExpDt = True
            
            if tr.select("td#MainContent_Status"):
                if MainContent_ExpDt:
                    print("MainContent_Status : "+tr.text)
                    result.append(tr.text)
                    MainContent_Status = True
                else:
                    result.append('')
                    result.append(tr.text)
                    MainContent_Status = True

            if tr.select("td#MainContent_ClassCellTable"):
                a_ = tr.find_all('a')
                class_ = ""
                for a in a_:
                    if MainContent_Status:
                        print("MainContent_ClassCellTable : "+a.text)
                        print(a['href'])
                        class_ += a.text + "\n"

                        MainContent_ClassCellTable = True
                    else:
                        result.append('')
                        class_ += a.text + "\n"
                        print(a['href'])
                        MainContent_ClassCellTable = True
                result.append(class_)

            if tr.select("td#MainContent_CertCellTable"):
                a_ = tr.find_all('a')
                Cert_ = ""
                for a in a_:
                    if MainContent_ClassCellTable:
                        print("MainContent_CertCellTable : "+a.text)
                        print(a['href'])
                        Cert_ += a.text + "\n"
                        MainContent_CertCellTable = True
                    else:
                        result.append('')
                        Cert_ += a.text + "\n"
                        print(a['href'])
                        MainContent_CertCellTable = True
                result.append(Cert_)
            if tr.select("td#MainContent_BondingCellTable"):
                MainContent_BondingCellTable_all = tr.find_all(['p', 'a', 'table'])
                count_ = 0
                for element in MainContent_BondingCellTable_all:
                    if element.name == 'table' and "Contractor's" in element.text:
                        if MainContent_CertCellTable:
                            Contractor_Bond = True
                        else:
                            result.append('')
                            Contractor_Bond = True
                    
                    if element.name == 'table' and "LLC" in element.text:
                        if Contractor_Bond:
                            LLC_BOND = True
                            if count_ == 5:
                                pass
                            else:
                                re_count = 5 - count_
                                for x in range(re_count):
                                    result.append('')
                        else:
                            result.append('')
                            result.append('')
                            result.append('')
                            result.append('')
                            result.append('')
                            LLC_BOND = True

                    if element.name == 'table' and "Qualifying" in element.text:
                        if LLC_BOND:
                            BQI_Bond = True
                            if count_ == 10:
                                pass
                            else:
                                re_count = 10 - count_
                                for x in range(re_count):
                                    result.append('')
                        else:
                            result.append('')
                            result.append('')
                            result.append('')
                            result.append('')
                            result.append('')
                            BQI_Bond = True

                    if element.name == 'table':
                        print("-------- "+element.text+" --------")
                    elif element.name == 'p':
                        result.append(element.text)
                        print(element.text)
                    elif element.name == 'a':
                        if "BQI" in element.text:
                            BQI_Bond_link = True
                        if "History" in element.text:
                            result.append(element['href'])
                            print('Link:', element['href'])
                        
            
            if tr.select("td#MainContent_WCStatus"):
                PolicyNumber = False
                EffectiveDate = False
                ExpireDate = False
                History = False
                count_ = 0
                if BQI_Bond_link == False:
                    result.append("")
                print(tr.select("td#MainContent_WCStatus"))
                print(list(tr.stripped_strings))
                for x in list(tr.stripped_strings):
                    if "Policy Number" in x:
                        PolicyNumber = True
                    if "Effective Date" in x:
                        if PolicyNumber:
                            EffectiveDate = True
                        else:
                            result.append("")
                            EffectiveDate = True

                    if "Expire Date" in x:
                        if EffectiveDate:
                            ExpireDate = True
                        else:
                            result.append("")
                            ExpireDate = True

                    if "History" in x:
                        if ExpireDate:
                            History = True
                        else:
                            result.append("")
                            History = True
                    else:
                        count_ += 1
                        result.append(x)
                if tr.find("a"):
                    if History == False:
                        result.append(x)
                    if "History" in tr.find("a").text:
                        count_ += 1
                        print(tr.find("a")['href'])
                        result.append(tr.find("a")['href'])
                
                result.append(InsuranceCompanyCode)
                count_ += 1
                if count_ != 6:
                    re_count = 6 - count_
                    for x in range(re_count):
                        result.append('')
            
            
            if tr.select("td#MainContent_LLIStatus"):
                count_ = 0
                MainContent_LLIStatus_all = tr.find_all(['p'])
                for element in MainContent_LLIStatus_all:
                    if element.name == 'p':
                        print(element.text)
                        count_ += 1
                        result.append(element.text)
                    if element.name == 'a':
                        if "History" in element.text:
                            count_ += 1
                            result.append(element['href'])
                            MainContent_LLIStatus_ =True
                
                if count_ != 7:
                    re_count =7 - count_
                    for x in range(re_count):
                        result.append('')

            if tr.select("td#MainContent_ActionCodesCellTable"):
                if MainContent_LLIStatus_:
                    MainContent_ActionCodesCellTable_all = tr.find_all(['li'])
                    Miscellaneous_ = ""
                    for element in MainContent_ActionCodesCellTable_all:
                        if element.name == 'li':
                            Miscellaneous_ += element.text + "\n"
                    result.append(Miscellaneous_)
                else:
                    result.append('')
                    MainContent_ActionCodesCellTable_all = tr.find_all(['li'])
                    Miscellaneous_ = ""
                    for element in MainContent_ActionCodesCellTable_all:
                        if element.name == 'li':
                            Miscellaneous_ += element.text + "\n"
                    result.append(Miscellaneous_)

            print(result)
            print("++++++++++++")

            if tr.select("td#MainContent_MultiLicDisplay"):
                result.append(tr.text)
                print(tr.text)
    
    except Exception as e:
        print(e)

    

   
def ZipCodeSearch(driver,wait):
    States = get_city()
    for State, list_citys in States.items():
        for city in list_citys:
            click_FindMyLicensedContractor(driver,wait)
            
            # Find the dropdown element by its ID
            dropdown_element = driver.find_element(By.ID,'ddlLicenseType')
            # Initialize the Select class with the dropdown element
            dropdown = Select(dropdown_element)
            # Get all the options from the dropdown
            options = dropdown.options
            # Loop through each option and select it
            for index, option in enumerate(options):
                try:
                    print(city)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input.form-control.ui-autocomplete-input')))
                    # Find an input field by its ID and type text into it
                    input_field = driver.find_element(By.CSS_SELECTOR,'input.form-control.ui-autocomplete-input')
                    input_field.send_keys("san diego")
                    dropdown_element = driver.find_element(By.ID,'ddlLicenseType')
                    dropdown = Select(dropdown_element)
                    options = dropdown.options
                    dropdown.select_by_index(index)
                    # Do something with the selected option (e.g., print it)
                    print(f"Selected option: {options[index].text} | index is: {index}")
                    driver.find_element(By.CSS_SELECTOR,".SearchButton").click()
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.section')))
                    try:
                        GridItem = driver.find_elements(By.CSS_SELECTOR,'table.Grid tr')
                        for index, list in enumerate(GridItem):
                            data = []
                            if index == 0:
                                pass
                            else:
                                row = list.find_elements(By.TAG_NAME,'td')
                                for x in row:
                                    if list.find_element(By.TAG_NAME,'a'):
                                        license_a = list.find_element(By.TAG_NAME,'a')
                                    if x != '':
                                        data.append(x.text)
                                license = license_a.text
                                clean_data = [item for item in data if item.strip()]
                                print(clean_data)
                                print(license_a.get_attribute('href'))
                                print(license)
                                newTab(driver,license_a.get_attribute('href'))
                                LicenseDetail(driver,wait,license,clean_data)
                                breakpoint()
                                closeTab(driver)
                                
                    except Exception as e:
                        print(e)
                    driver.back()
                except Exception as e:
                    print(e)   
def run():
    driver = set_driver()
    wait = WebDriverWait(driver, 10)
    ZipCodeSearch(driver,wait)


if __name__=="__main__":
    run()

