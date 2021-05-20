from selenium import webdriver
import pandas as pd
import time
from SendEmail import send_mail
from pretty_html_table import build_table

#Initialized an empty DataFrame to be used as buffer later
df_buffer = pd.DataFrame()

hospital_names = []
Availability = []
Vaccine = []
Age = []
Dates = []

#chromedriver to be used with selenium
options = webdriver.ChromeOptions()
driver = webdriver.Chrome('Enter the path where you have downloaded the chromedriver')
#CoWIN's website to reach
driver.get('https://selfregistration.cowin.gov.in/')
time.sleep(3)
input = driver.find_element_by_id('mat-input-0')
#Enter your registered phone number
input.send_keys('Enter you phone number here')
get_otp_button = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[1]/ion-grid/form/ion-row/ion-col[2]/div/ion-button")
get_otp_button.click()
#Enter the OTP that you have recieved on your mobile here and wait for the verify proceed button to be clicked automatically
time.sleep(20)
verify_proceed_button = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-login/ion-content/div/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col/ion-grid/form/ion-row/ion-col[3]/div/ion-button")
verify_proceed_button.click()
time.sleep(2)
schedule_button = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-beneficiary-dashboard/ion-content/div/div/ion-grid/ion-row/ion-col/ion-grid[1]/ion-row[2]/ion-col/ion-grid/ion-row[4]/ion-col[2]/ul/li/a")

schedule_button.click()
time.sleep(2)
enter_pin = driver.find_element_by_xpath('//*[@id="mat-input-2"]')
#Enter the puncode for which you want to search
enter_pin.send_keys('Enter your pincode here')
while True:
    search_button = driver.find_element_by_xpath ("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[4]/ion-button")
    search_button.click()
    time.sleep(3)
     for i in range(1,50):
        try:
            data = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[10]/div/div/mat-selection-list/div[{}]/mat-list-option/div/div[2]/ion-row/ion-col[1]/div/h5".format(i))
            name_of_hospital = data.get_attribute('textContent')
            hospital_names.append(name_of_hospital)
            for j in range(2,3):
                try:
                    availability = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[10]/div/div/mat-selection-list/div[{}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{}]/div/div/a".format(i,j))
                    if availability.get_attribute('textContent').strip() == 'NA':
                        Availability.append ('NA')
                        Vaccine.append ('NA')
                        Age.append ('NA')
                    else:
                        vaccine_name = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[10]/div/div/mat-selection-list/div[{}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{}]/div/div/div[1]/h5".format(i, j))
                        age = driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[10]/div/div/mat-selection-list/div[{}]/mat-list-option/div/div[2]/ion-row/ion-col[2]/ul/li[{}]/div/div/div[2]/span".format(i, j))
                        availability_text = availability.get_attribute('textContent')
                        vaccine_name_text = vaccine_name.get_attribute('textContent')
                        age_text = age.get_attribute('textContent')
                        Availability.append(availability_text)
                        Vaccine.append(vaccine_name_text)
                        Age.append(age_text)
                except:
                    pass
        except:
            break

    for i in range(len(hospital_names)):
        Dates.append(driver.find_element_by_xpath("/html/body/app-root/ion-app/ion-router-outlet/app-appointment-table/ion-content/div/div/ion-grid/ion-row/ion-grid/ion-row/ion-col/ion-grid/ion-row/ion-col[2]/form/ion-grid/ion-row/ion-col[9]/div/div/ul/carousel/div/div/slide[2]/div/li/a/p").get_attribute('textContent'))

    data_for_df = {'Hospital' : hospital_names,
                   'Date' : Dates,
                   'Availability' : Availability,
                   'Vaccine' : Vaccine,
                   'Age' : Age
                   }

    df = pd.DataFrame(data_for_df)
    if df_buffer.equals(df):
        pass
    else:
        df_buffer = df
        output = build_table (df, 'blue_light')
        send_mail (output)

    print(df)
    print('executed')
    hospital_names.clear()
    Availability.clear()
    Vaccine.clear()
    Age.clear()
    Dates.clear()
    time.sleep(10)