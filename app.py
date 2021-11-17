import streamlit as st
import tempfile
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

def get_driver(url, headless=True):
    if headless:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--remote-debugging-port=9222")        
        driver = webdriver.Chrome('chromedriver', chrome_options=options)
    else:
        driver =  webdriver.Chrome('chromedriver')
    driver.set_window_size(1920, 1080)
    driver.get(url)    
    return driver


uploaded_file = st.file_uploader("Upload an image")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        fp = Path(tmp_file.name)
        fp.write_bytes(uploaded_file.getvalue())
        
        st.write(tmp_file.name)
        st.image(uploaded_file)
        
        # TODO: useragent
        driver = get_driver("https://www.google.com/imghp")        
        driver.find_element_by_xpath("//div[@aria-label='Search by image']").click()
        driver.find_element_by_name("encoded_image").send_keys(tmp_file.name)
        q = driver.find_element_by_name("q").get_attribute("value")
        
        st.write(q)
        
        
        

