from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from time import sleep
import os
import geckodriver_autoinstaller
import chromedriver_autoinstaller
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

def login(driver, wait, email, pwd):
    driver.get('https://www.facebook.com/')
    sleep(5)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//a[contains(@id,"accept")]'))).click()
    sleep(5)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//input[contains(@id,"mail")]'))).send_keys(email)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//input[contains(@type,"password")]'))).send_keys(pwd)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//button[@name="login"]'))).click()
    sleep(5)
    wait.until(ec.visibility_of_element_located((By.TAG_NAME, 'button'))).click()
    sleep(4)
    return None

def spam(driver, wait, url, msg):
    driver.get(url)
    sleep(5)
    wait.until(ec.visibility_of_element_located((By.XPATH, '//div[contains(@onclick,"getElement")]'))).click()
    sleep(2)
    driver.find_elements_by_xpath("//textarea")[1].send_keys(msg)
    for el in driver.find_elements_by_xpath('//button[contains(text(),"Post")]'):
        try:
            el.click()
        except:
            pass
    sleep(4)
    return None

def group_extract(driver, wait):
    group_url = []
    sleep(5)
    driver.get('https://m.facebook.com/groups_browse/your_groups/')
    sleep(5)
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    sleep(2)
    for url in driver.find_elements_by_xpath('//a[contains(@href, "group")]'):
        group_url.append(url.get_attribute('href'))
    return group_url
      
def start():
      root.withdraw()
      
      progress = Tk()
      progress.title('FaceB Spammer')
      progress.config(background='#1c1c1c')
      window_height = 400
      window_width = 700
      screen_width = progress.winfo_screenwidth()
      screen_height = progress.winfo_screenheight()
      x_cordinate = int((screen_width/2) - (window_width/2))
      y_cordinate = int((screen_height/2) - (window_height/2))
      progress.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
      progress.resizable(False,False)

      progress_text = Text(progress, width = 90, height = 22)
      progress_text.place(x = 30, y = 30)
      progress_text.config(state='normal')
      progress_text.insert(END, 'Application spamming...\n')
      progress_text.insert(END, 'LoggedIn\n')
      progress_text.config(state='disabled')

      email = email_form.get()
      pwd = pwd_form.get()
      msg = msg_content.get("1.0", END)
      
      #DRIVER SETTINGS
      if browser_selected.get()==0:
            chromedriver_autoinstaller.install()
            chrome_options = Options()
            #chrome_options.add_argument("--headless")
            chrome_options.add_argument(f'user-agent={"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36"}')
            driver=webdriver.Chrome(options=chrome_options)
            wait = WebDriverWait(driver, 10)

      if browser_selected.get()==1:
            geckodriver_autoinstaller.install()
            firefox_options = FirefoxOptions()
            firefox_profile = webdriver.FirefoxProfile()
            firefox_profile.set_preference("general.useragent.override", 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.2 Safari/537.36')
            firefox_options.add_argument("--headless")
            driver = webdriver.Firefox(firefox_profile, options=firefox_options)
            wait = WebDriverWait(driver, 10)
            
      login(driver, wait, email, pwd)  
      #GROUP OPTIONS
      if group_option.get() == 0:
            group_list = group_extract(driver, wait)
      if group_option.get()==1:
            group_list = groups.get("1.0", END).split(',')

      #MESSAGE TO SPAM
      msg = msg_content.get("1.0", END)

      progress_text.config(state='normal')
      progress_text.insert(END, str(len(group_list))+' groups found...\n')
      progress_text.insert(END, 'Start spamming...\n')
      progress_text.config(state='disabled')


      for url, i in zip(group_list, range(len(group_list))):
          try:
              spam(driver, wait, url, msg)
          except Exception as e:
              print(e)
              progress_text.config(state='normal')
              progress_text.insert(END, 'something went wrong, please be sure the urls are correct. if problem insists, please report this iussue to creator.\n')
              progress_text.insert(END, str(e))
              progress_text.config(state='disabled')
              
      driver.close()
      progress_text.config(state='normal')
      progress_text.insert(END, str(len(group_list))+'/'+str(len(group_list))+' groups done.')
      progress_text.config(state='disabled')        
          
      progress.mainloop()
      
      
      
def hideForm(event = None):
    groups.place(x = 800, y = 170)

def showForm(event = None):
    groups.place(x = 400, y = 170)


    
#MAIN
root = Tk()
root.title('FaceB Spammer')
root.config(background='#1c1c1c')
photo=ImageTk.PhotoImage(Image.open("icon.gif"))
root.iconphoto(False, photo)
window_height = 600
window_width = 800
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
root.resizable(False,False)

#LOGO
img = ImageTk.PhotoImage(Image.open("logo.png").resize((130, 80), Image.ANTIALIAS))
panel = Label(root, image = img, width=130, height = 80, pady=10)
panel.config(background='#1c1c1c')
panel.pack()

#BROWSER SELECTION
browser_selected=IntVar()
browser_txt=Label(root, text='Select the browser you use')
browser_txt.config(font=('Helvetica', 16), fg='white', background='#1c1c1c')
browser_txt.place(x = 30, y = 115)

browser_opt1 = Radiobutton(root, text = 'Chrome', variable=browser_selected, value=0)
browser_opt1.config(font=('Helvetica'),fg='white', background='#1c1c1c')
browser_opt1.place(x=60, y = 145)

browser_opt2 = Radiobutton(root, text = 'Firefox', variable=browser_selected, value=1)
browser_opt2.config(font=('Helvetica'),fg='white', background='#1c1c1c')
browser_opt2.place(x=180, y = 145)

#SELECT GROUP
group_option=IntVar()
group_txt=Label(root, text='Select option you prefer about group where spamming')
group_txt.config(font=('Helvetica', 16), fg='white', background='#1c1c1c')
group_txt.place(x = 370, y = 115)

group_opt1 = Radiobutton(root, text = 'All groups I am subscribed', variable=group_option, value=0, command=hideForm)
group_opt1.config(font=('Helvetica'),fg='white', background='#1c1c1c')
group_opt1.place(x=400, y = 145)

group_opt2 = Radiobutton(root, text = 'Select some URLs', variable=group_option, value=1, command=showForm)
group_opt2.config(font=('Helvetica'),fg='white', background='#1c1c1c')
group_opt2.place(x=620, y = 145)

groups = Text(root, width=50, height=10)
groups.configure(font=('Helvetica', 12))
groups.place(x = 1000, y = 170)
groups.insert(END, 'WRITE URLs SEPARATED BY COMMAS.\nBE SURE YOU WRITE IT ACCURATELY TO AVOID ERRORS.\nDELETE THIS MESSAGE BEFORE TEXTING')


#INSERT CREDENTIALS
email=StringVar()
pwd=StringVar()
credentials_txt=Label(root, text='Insert your credentials')
credentials_txt.config(font=('Helvetica', 16), fg='white', background='#1c1c1c')
credentials_txt.place(x = 30, y = 235)

email_form =Entry(root, textvariable=email, width=30)
email_form.configure(font=('Helvetica', 10))
email_form.delete(0, tk.END)
email_form.insert(0, 'Insert Email/Phone Number')
email_form.place(x=60, y = 265)

pwd_form =Entry(root, textvariable=pwd, text='Insert Password', width=30)
pwd_form.configure(font=('Helvetica', 10))
pwd_form.delete(0, tk.END)
pwd_form.insert(0, 'Insert Password')
pwd_form.place(x=60, y = 295)

#INSERT MESSAGE TO SPAM
msg_txt=Label(root, text='Text message you want to spam')
msg_txt.config(font=('Helvetica', 16), fg='white', background='#1c1c1c')
msg_txt.place(x = 30, y = 340)

msg_content = Text(root, width=100, height=10)
msg_content.configure(font=('Helvetica', 12))
msg_content.place(x = 30, y = 370)
msg_content.insert(END, 'Write here message you want to spam.')

#COMMAND OPTION
send_img = ImageTk.PhotoImage(Image.open("start_button.png").resize((140, 50), Image.ANTIALIAS))
send=Label(root, image=send_img, cursor='hand2')
send.configure(background='#1c1c1c')
send.bind('<Button-1>', lambda *_: start()) 
send.place(x=335, y=530)


root.mainloop()



