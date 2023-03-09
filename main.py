from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIGURATION
EMPLOYEES_CODE = 'YOUR_CODE'
PIN = 'YOUR_PIN'
WINDOW_WIDTH = 830
WINDOW_HEIGHT = 290
URL = 'https://app.tangerino.com.br/Tangerino/pages/LoginPage/wicket:pageMapName/wicket-0'

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)

def getTargetDay():
    today = date.today()
    delta = 1 if today.weekday() != 0 else 3
    targetDay = today - timedelta(delta)
    return targetDay

def formatTargetDay(char):
    return getTargetDay().strftime('%d' + char + '%m' + char + '%Y')

def formatToday(char):
    return date.today().strftime('%d' + char + '%m' + char + '%Y')

def browseTo(url):
    driver.get(url)

def tangerinoLogin(employeesCode, pin):
    middleButton = driver.find_element(By.PARTIAL_LINK_TEXT, value='Colaborador')
    actions.click(middleButton).perform()

    employeesCodeForm = driver.find_element(By.NAME, value='codigoEmpregador')
    passwordForm = driver.find_element(By.NAME, value='pin')
    actions.send_keys_to_element(employeesCodeForm, employeesCode).send_keys_to_element(passwordForm, pin, Keys.RETURN).perform()

def waitForLoginToComplete():
    try:
        waitCondition = EC.presence_of_element_located((By.NAME, 'hiddenEmployeeData'))
        wait.until(waitCondition)
    except:
        print("LOGIN FAILED")
        browserClose()

def clickOnApropriacaoHoras():
    driver.find_element(By.XPATH, '//div[1]/nav/a[3]').click()

def filterDaysByTargetDay():
    initialDateInput = driver.find_element(By.NAME, 'containerPorPeriodo:dataInicio')
    finalDateInput = driver.find_element(By.NAME, 'containerPorPeriodo:dataFim')
    queryButton = driver.find_element(By.NAME, 'consultar')
    
    actions.send_keys_to_element(initialDateInput, Keys.BACKSPACE * 10, formatTargetDay('/'))
    actions.send_keys_to_element(finalDateInput, Keys.BACKSPACE * 10, formatTargetDay('/'))
    actions.click(queryButton).pause(2).perform()

def prepareWindowFrame(width, height):    
    driver.execute_script('document.getElementsByClassName("nav-rapida menu_lateral")[0].style.display = "none"')
    driver.execute_script('document.getElementsByClassName("corpo")[0].style.padding = 0')
    driver.execute_script('document.getElementsByClassName("corpo")[0].style.margin = 0')
    driver.set_window_size(width, height)

def prepareTablePosition():
    tableRows = driver.find_elements(By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/span/form/div[2]/div[2]/table/tbody/tr')
    location = tableRows[0].location
    x, y = location['x'], location['y']
    driver.execute_script('window.scrollTo({}, {})'.format(x,y))
        
def takeTableScreenshot():
    driver.save_screenshot('Tangerino [{}].png'.format(formatTargetDay("-")))

def browserClose():
    driver.quit()

# PROGRAM START
print('TODAY IS', formatToday("/"))
print('TARGET DAY IS', formatTargetDay("/"))

try:
    browseTo(URL)
    tangerinoLogin(EMPLOYEES_CODE, PIN)
    waitForLoginToComplete()
    clickOnApropriacaoHoras()
    filterDaysByTargetDay()
    prepareWindowFrame(WINDOW_WIDTH, WINDOW_HEIGHT)
    prepareTablePosition()
    takeTableScreenshot()
except:
    print('ERROR: TABLE NOT FOUND')
finally:
    browserClose()