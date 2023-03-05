from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#Credentials
EMPLOYEES_CODE = 'YOUR_CODE_HERE'
PIN = 'YOUR_PIN_HERE'


today = date.today()

delta = 1 if today.weekday() != 0 else 3

targetDay = today - timedelta(delta)

print("Today is", today.strftime("%d/%m/%Y"))
print("Target day is", targetDay.strftime("%d/%m/%Y"))

driver = webdriver.Chrome()
driver.get('https://app.tangerino.com.br/Tangerino/?wicket:bookmarkablePage=wicket-2:com.frw.tangerino.web.pages.web.cadastro.LoginFuncionarioPage&wicket:interface=wicket-2:12::INewBrowserWindowListener::')

form1 = driver.find_element(By.NAME, value='codigoEmpregador').send_keys(EMPLOYEES_CODE)

form2 = driver.find_element(By.NAME, value='pin')
form2.send_keys(PIN)
form2.send_keys(Keys.RETURN)

try:
    waitCondition = EC.presence_of_element_located((By.NAME, 'hiddenEmployeeData'))
    WebDriverWait(driver, 5).until(waitCondition)
    
    driver.find_element(By.XPATH, '//div[1]/nav/a[3]').click()

    table_rows = driver.find_elements(By.XPATH, '//table/tbody/tr')
    num_rows = len (table_rows)
    print(repr(num_rows) + " rows in table")

    for row in table_rows:
        if targetDay.strftime("%d/%m/%Y") in row.text:
            driver.set_window_size(830, 290)
            driver.execute_script('document.getElementsByClassName("nav-rapida menu_lateral")[0].style.display = "none"')
            driver.execute_script('document.getElementsByClassName("corpo")[0].style.padding = 0')
            driver.execute_script('document.getElementsByClassName("corpo")[0].style.margin = 0')
            
            location = row.location
            x, y = location['x'], location['y']
            driver.execute_script('window.scrollTo({}, {})'.format(x,y))
            
            row.screenshot('row.png')
            driver.save_screenshot('Tangerino [{}].png'.format(targetDay.strftime("%d-%m-%Y")))
except:
    print("ERROR: Row not found")
finally:
    driver.quit()