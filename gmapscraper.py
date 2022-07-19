import time
import copy
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


# bfdHYd
def scrapping_details(driver,output_data):
    try:
        search_result = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"Nv2PK")))
    except TimeoutException :
        print("connection problem")
        driver.quit()
    time_data = ["closed","open","AM","PM","HOURS","hours"]
    count = 1
    for i in range(10):
        try:
            driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div/span")
        except:
            count = count + 1
        else:
            break
    for i in range(0,len(search_result)):
        driver.execute_script("arguments[0].scrollIntoView();",search_result[i])
        search_result[i].click()
        if size["width"] < 952:
            back_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"fKm1Mb")))
            back_button.click()
        time.sleep(2)
        try:
            name = driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[1]/div/span")
            name_val = name.text
        except:
            name_val = ""
        try:
            rating = driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[3]/div/span[2]/span[2]")
            rating_val = rating.text
        except:
            rating_val = ""
        try:
            type = driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/span[1]/jsl/span[2]")
            type_val = type.text
        except:
            type_val = ""
        try:
            address = driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[1]/span[2]/jsl/span[2]")
            address_val = address.text
        except:
            address_val = ""
        try:
            infos  = driver.find_element(By.XPATH,f"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[{count}]/div/div[2]/div[2]/div[1]/div/div/div/div[4]/div[2]")
            infos = infos.find_elements(By.XPATH,"*")
        except:
            infos = []
        working_hours = ""
        contact_details = ""
        for info in infos:
            value = copy.copy(info.text)
            if any(ele in value for ele in time_data):
                working_hours = info.text
                continue
            number=value.replace("-","").replace("+","").replace(" ","").replace("·","")
            if number.isnumeric():
                contact_details = info.text.replace("·","")
        data = {"name":name_val,"type":type_val,"rating":rating_val,"address":address_val,"working_hours":working_hours,"contact_details":contact_details}
        output_data.append(data)
        count = count+2


search_keyword = input("enter the key to search : ")
csv_file_name = search_keyword
search_keyword.replace(" ","+")
driver = webdriver.Chrome(executable_path="/home/sharuk/Downloads/chromedriver_linux64/chromedriver")
driver.get('https://www.google.com/maps/search/'+search_keyword)
print(search_keyword)
actions = ActionChains(driver)
driver.implicitly_wait(10)
# driver.minimize_window()
wait = WebDriverWait(driver,10)
driver.maximize_window()
time.sleep(3)
try:
    element = driver.find_element(By.XPATH,"//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]")
except:
    print("invalid input")
    driver.quit()
time.sleep(10)
size = driver.get_window_size()
verical_ordinate = size["height"]
while True:
    driver.execute_script("arguments[0].scrollTop = arguments[1]", element, verical_ordinate)
    verical_ordinate += size["height"]
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME,"Nv2PK")))
    except TimeoutException:
        print("connection error")
        driver.quit()
    cont = driver.find_elements(By.CLASS_NAME,"HlvSq")
    if len(cont) >0:
        break

# search = driver.find_element(By.ID,"searchboxinput")
# search.send_keys(search_keyword)
# search_button = driver.find_element(By.ID,"searchbox-searchbutton")
# search_button.click()
time.sleep(5)
output_data = []
scrapping_details(driver,output_data)
df = pd.DataFrame.from_dict(output_data)
df.to_csv(rf'{csv_file_name}.csv',index=False,header=True)
driver.quit()

# while True:
#     scrapping_details(driver,count,output_data)
#     cont = driver.find_elements(By.CLASS_NAME,"HlvSq")
#     print(len(cont))
#     if len(cont) >0:
#         html = driver.page_source
#         soup = BeautifulSoup(html,'html.parser')
#         search_result = soup.find_all('div',attrs={'class':'Nv2PK'})
#         print(len(search_result),"result")
#         if len(search_result) > count[0]:
#             scrapping_details(driver,count,output_data)
#         break
