import configparser, pathlib
from datetime import date, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config.read(pathlib.Path(__file__).parent / 'config.ini')

EMPLOYEES_CODE = config['LOGIN']['code']
PIN = config['LOGIN']['pin']
WINDOW_WIDTH = config['SIZE']['width']
WINDOW_HEIGHT = config['SIZE']['height']
URL = config['URL']['url']

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
actions = ActionChains(driver)


def get_target_day():
    today = date.today()
    delta = 1 if today.weekday() != 0 else 3
    target_day = today - timedelta(delta)
    return target_day

def format_target_day(char):
    return get_target_day().strftime('%d' + char + '%m' + char + '%Y')

def format_today(char):
    return date.today().strftime('%d' + char + '%m' + char + '%Y')

def browse_to(url):
    driver.get(url)

def tangerino_login(employeesCode, pin):
    middleButton = driver.find_element(By.PARTIAL_LINK_TEXT, value='Colaborador')
    actions.click(middleButton).perform()

    employeesCodeForm = driver.find_element(By.NAME, value='codigoEmpregador')
    passwordForm = driver.find_element(By.NAME, value='pin')
    actions.send_keys_to_element(employeesCodeForm, employeesCode).send_keys_to_element(passwordForm, pin, Keys.RETURN).perform()

def wait_for_login():
    try:
        waitCondition = EC.presence_of_element_located((By.NAME, 'hiddenEmployeeData'))
        wait.until(waitCondition)
    except:
        print("LOGIN FAILED")
        browser_close()

def click_on_horas():
    driver.find_element(By.XPATH, '//div[1]/nav/a[3]').click()

def filter_days_by_target_day():
    initialDateInput = driver.find_element(By.NAME, 'containerPorPeriodo:dataInicio')
    finalDateInput = driver.find_element(By.NAME, 'containerPorPeriodo:dataFim')
    queryButton = driver.find_element(By.NAME, 'consultar')

    actions.send_keys_to_element(initialDateInput, Keys.BACKSPACE * 10, format_target_day('/'))
    actions.send_keys_to_element(finalDateInput, Keys.BACKSPACE * 10, format_target_day('/'))
    actions.click(queryButton).pause(2).perform()

def prepare_window_frame(width, height):
    driver.execute_script('document.getElementsByClassName("nav-rapida menu_lateral")[0].style.display = "none"')
    driver.execute_script('document.getElementsByClassName("corpo")[0].style.padding = 0')
    driver.execute_script('document.getElementsByClassName("corpo")[0].style.margin = 0')
    driver.set_window_size(width, height)

def prepare_table_position():
    tableRows = driver.find_elements(By.XPATH,
                                     '/html/body/div[1]/div[2]/div/div[2]/span/form/div[2]/div[2]/table/tbody/tr')
    location = tableRows[0].location
    x, y = location['x'], location['y']
    driver.execute_script('window.scrollTo({}, {})'.format(x, y))

def take_table_screenshot():
    driver.save_screenshot('Tangerino [{}].png'.format(format_target_day("-")))

def browser_close():
    driver.quit()

def main():
    print('TODAY IS', format_today("/"))
    print('TARGET DAY IS', format_target_day("/"))

    try:
        browse_to(URL)
        tangerino_login(EMPLOYEES_CODE, PIN)
        wait_for_login()
        click_on_horas()
        filter_days_by_target_day()
        prepare_window_frame(WINDOW_WIDTH, WINDOW_HEIGHT)
        prepare_table_position()
        take_table_screenshot()
    except:
        print('ERROR: TABLE NOT FOUND')
    finally:
        browser_close()


if __name__ == "__main__": 
    main()