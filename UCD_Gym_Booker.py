from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time
booked = False
tried = False
#take user input and parse the data
ID = int(input("Enter your Student ID: "))
booking_time = input("Enter booking time in format of (07:00): ")
actual_time = booking_time
class_number = input("Choose 0 for the Poolside Gym or 1 for the Performance Gym : ")
if(class_number == 0):
    class_number = "Poolside Gym"
else:
    class_number = "Performance gym"    
booking_time.split(':')
time_1 = booking_time[0] + booking_time[1]
time_1 = int(time_1) - 3
if(time_1 > 10):
    booking_time = str(time_1) + ':' + booking_time[3] + booking_time[4]
else:
    booking_time = '0' + str(time_1) + ':' + booking_time[3] + booking_time[4]
#booking function
def book():
    try:
        print("Searching for slot " + str(class_number) + " at " + str(actual_time) + ".....")
        # Initiate the browser
        browser  = webdriver.Chrome(ChromeDriverManager().install())
        # Open the Website
        browser.get('https://hub.ucd.ie/usis/W_HU_MENU.P_PUBLISH?p_tag=GYMBOOK')
        found = False
        i=0
        #find right slot
        while found != True:
            temp_times = browser.find_elements_by_xpath('//*[@id="SW300-1|' + str(i) + '"]/td[1]')
            times_list = []
            for times in temp_times:
                times_list.append(times.text)
            temp_time = times_list[0] 
            if str(temp_time) == str(actual_time):
                found = True
            else:
                i += 1
        #click slot
        slot_types = browser.find_elements_by_xpath('//*[@id="SW300-1|' + str(i) + '"]/td[2]')
        slot_list = []
        for slots in slot_types:
            slot_list.append(slots.text)
            slot_type = slot_list[0]
        if(slot_type != class_number):
            i += 1
        browser.find_element_by_xpath('//*[@id="SW300-1|' + str(i) + '"]/td[6]/a').click()
        #wait for popup then accept cookies
        time.sleep(3)
        browser.find_element_by_id('onetrust-accept-btn-handler').click()
        #enter student number
        browser.find_element_by_name("MEMBER_NO").send_keys(ID)
        #click proceed with booking
        browser.find_element_by_xpath('//*[@id="single-column-content"]/div/div/div/div[2]/div/form/input[5]').click()
        #confirm booking
        browser.find_element_by_xpath('//*[@id="single-column-content"]/div/div/div/div[2]/div/a[1]').click()
        #close browser
        browser.close()
        booked = True
        print("Booked succesfully for slot " + str(class_number) + " at " + str(actual_time))
    except:
        tried = True
#schedule the booking
schedule.every().day.at(booking_time).do(book)
while booked == False:
    if tried == True:
        time.sleep(60)
        book()
    else:
        print("Will launch at " + booking_time)
        schedule.run_pending()
        time.sleep(1)