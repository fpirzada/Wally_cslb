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
        driver = manager.create_browser(timeout=5, headless=True, proxy=None, window_size='--start-maximized', clear_cache=False)
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

    time.sleep(2)

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
        driver.find_element(By.ID,"MainContent_LicNo").send_keys(LicNo)
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
            try:
                print(a_.get_attribute('outerHTML'))
                main_window, soup = click_next_page(driver,a_)
                soup_ = soup.find(id="MainContent_lblCode")
                print(soup_.text)
                InsuranceCompanyCode = soup_.text
            except Exception as e:
                print("--")
                print(e)
                driver.implicitly_wait(2)
                soup = soup.find(id="MainContent_dlHisList_hlInsuranceCompany_0")
                print("-")
                hlInsuranceCompany = soup.text
                print(soup.text)
                
            # Close the newly opened tab
            driver.close()

            # Switch back to the main window
            driver.switch_to.window(main_window)

    except Exception as e:
        print(e)

    
    try:
        time.sleep(1)
        wait.until(EC.presence_of_element_located((By.ID, 'MainContent_PersonnelLink')))
        get_MainContent_PersonnelLink = driver.find_element(By.ID,"MainContent_PersonnelLink")
        main_window, soup = click_next_page(driver,get_MainContent_PersonnelLink)
        driver.implicitly_wait(2)
        soup_ = soup.find(id="MainContent_dlAssociated").find_all("table")
        for index, _ in enumerate(soup_):
            if index == 0:
                tr = _.find_all("tr")
                for tr_ in tr:
                    if tr_.find(id="MainContent_dlAssociated_hlName_0"):
                        P_Name = tr_.find(id="MainContent_dlAssociated_hlName_0").text
                    if tr_.find(id="MainContent_dlAssociated_lblTitle_0"):
                        P_Title = tr_.find(id="MainContent_dlAssociated_lblTitle_0").text
                    if tr_.find(id="MainContent_dlAssociated_lblAssociationDate_0"):
                        P_AssociationDate = tr_.find(id="MainContent_dlAssociated_lblAssociationDate_0").text
                    if tr_.find(id="MainContent_dlAssociated_lblClassification_0"):
                        P_Classification = tr_.find(id="MainContent_dlAssociated_lblClassification_0").text
            
        # Close the newly opened tab
        driver.close()

        # Switch back to the main window
        driver.switch_to.window(main_window)
        result.append((28,hlInsuranceCompany))

        result.append((20,InsuranceCompanyCode))
        result.append((28,P_Name))
        result.append((29,P_Title))
        result.append((30,P_AssociationDate))
        result.append((31,P_Classification))
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
        for tr in soup:
            try:
                print("--")
                if tr.select('h2.subheading'):
                    print("-------- "+tr.text+" --------")
                if tr.select('td#MainContent_BusInfo'):
                    print(list(tr.stripped_strings))
                    for x in list(tr.stripped_strings):
                        print(x)
                if tr.find(id="MainContent_Entity"):
                    Entity = tr.find(id="MainContent_Entity").text
                    result.append((8,Entity))
                    print(Entity)
                if tr.find(id="MainContent_IssDt"):
                    IssDt = tr.find(id="MainContent_IssDt").text
                    result.append((9,IssDt))
                    print(IssDt)
                if tr.find(id="MainContent_ReIssueDt"):
                    ReIssueDt = tr.find(id="MainContent_ReIssueDt").text
                    result.append((10,ReIssueDt))
                    print(ReIssueDt)
                if tr.find(id="MainContent_ExpDt"):
                    ExpDt = tr.find(id="MainContent_ExpDt").text
                    result.append((11,ExpDt))
                    print(ExpDt)
                if tr.find(id="MainContent_Status"):
                    MainContent_Status = tr.find(id="MainContent_Status").find('span').text
                    result.append((12,MainContent_Status))
                    print(MainContent_Status)
                if tr.find(id="MainContent_ClassCellTable"):
                    a_ = tr.find_all('a')
                    class_ = ""
                    for a in a_:
                        class_ += a.text + "\n"
                        print("MainContent_ClassCellTable : "+a.text)
                        print(a['href'])
                    result.append((13,class_))
            except Exception as e:
                print("@@@@@@@@@@@@@")
                print(e)

            if tr.select("td#MainContent_CertCellTable"):
                a_ = tr.find_all('a')
                Cert_ = ""
                for a in a_:
                    print("MainContent_CertCellTable : "+a.text)
                    print(a['href'])
                    Cert_ += a.text + "\n"
                result.append((14,Cert_))
            
            
            if tr.find(id="MainContent_WCStatus"):
                print(tr.find(id="MainContent_WCStatus"))
                print(list(tr.stripped_strings))
                data = list(tr.stripped_strings)
                print("==================")
                # Iterate through the data list

                for i in range(len(data)):
                    try:
                        if "This license has workers" in data[i]:
                            print(data[i + 1])
                            result.append((15,data[i + 1]))
                        elif "exempt" in data[i]:
                            result.append((15,""))
                            print("exempt")
                        elif "Policy Number" in data[i]:
                            print(data[i + 1])
                            result.append((16,data[i + 1]))
                        elif "Effective Date" in data[i]:
                            print(data[i + 1])
                            result.append((17,data[i + 1]))
                        elif "Expire Date" in data[i]:
                            print(data[i + 1])
                            result.append((18,data[i + 1]))
                    except Exception as e:
                        print("--MainContent_WCStatus-- ERROR")
                        print(e)
                try:
                    Status = tr.find(id="MainContent_WCStatus").find_all('p')
                    print(Status)
                    print(Status[1])
                    if   "History" in Status[1].text:
                        print(Status[1].find("a")['href'])
                        result.append((19,Status[1].find("a")['href']))
                except Exception as e:
                    print("--MainContent_WCStatus-- A -- ERROR")
                    print(e)
                
            if tr.find(id="MainContent_LLIStatus"):
                MainContent_LLIStatus_all = tr.find_all(['p'])
                for x in MainContent_LLIStatus_all:
                    if x.find('a'):
                        result.append((21,x.find('a').text))
                    if "Policy Number" in x.text:
                        print(x.text)
                        PolicyNumber = x.text.replace("Policy Number:","")
                        result.append((22,PolicyNumber))
                    if "Amount" in x.text:
                        print(x.text)
                        Amount = x.text.replace("Amount:","")
                        result.append((23,Amount))
                    if "Effective Date" in x.text:
                        print(x.text)
                        Effective = x.text.replace("Effective Date:","")
                        result.append((24,Effective))
                    if "Expiration Date" in x.text:
                        print(x.text)
                        Expiration = x.text.replace("Expiration Date:","")
                        result.append((25,Expiration))

            if tr.find(id="MainContent_ActionCodesCellTable"):
            
                MainContent_ActionCodesCellTable_all = tr.find_all(['li'])
                Miscellaneous_ = ""
                for element in MainContent_ActionCodesCellTable_all:
                    if element.name == 'li':
                        Miscellaneous_ += element.text + "\n"
                result.append((26,Miscellaneous_))
            
            

            if tr.find(id="MainContent_MultiLicDisplay"):
                print(tr.text)
                result.append((27,tr.text))
        return result
    except Exception as e:
        print("--000--")
        print(e)

    
def pagination(driver):
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    if soup.select("tr.GridPager"):
        return driver.find_element(By.CSS_SELECTOR,"tr.GridPager").find_elements(By.TAG_NAME,"td")
    else:
        pass
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
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr.GridItem')))
                    try:
                        count_page = 0
                        first_time = True
                        while True:
                            GridItem = driver.find_elements(By.CSS_SELECTOR,'table.Grid tr')
                            print(len(GridItem))
                            for index, list in enumerate(range(len(GridItem)-2)):
                                if GridItem[list]:
                                    print(index)
                                    data = []
                                    if index == 0:
                                        pass
                                    else:
                                        try:
                                            row = GridItem[list].find_elements(By.TAG_NAME,'td')
                                            license_a = row[1].find_element(By.TAG_NAME,"a").get_attribute('href')
                                            license = row[1].text
                                            data.append((1,license))
                                            data.append((2,license_a))
                                            data.append((3,row[2].text))
                                            data.append((4,row[3].text))
                                            data.append((5,row[4].text))
                                            data.append((6,row[5].text))
                                            data.append((7,row[6].text))
                                        except Exception as e:
                                            print(e)
                                        
                                        print(license_a)
                                        print(license)
                                        newTab(driver,license_a)
                                        data = LicenseDetail(driver,wait,license,data)
                                        print("=======================")
                                        print(data)
                                        print("=======================")
                                        main(data)
                                        closeTab(driver)
                            print("====")
                            page_ = pagination(driver)
                            if page_:
                                
                                count_page += 1
                                try:
                                    if page_[count_page].text ==  str(count_page) or page_[count_page].text == "...":
                                        if "href" in page_[count_page].get_attribute('outerHTML'):
                                            page_[count_page].find_element(By.TAG_NAME,"a").click()
                                            time.sleep(10)
                                        else:
                                            print("--")
                                    else:
                                        print("==")
                                        break
                                except Exception as e:
                                    print(e)  
                                    break
                            else:
                                break
                                
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

