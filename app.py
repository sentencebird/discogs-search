import streamlit as st
import tempfile
from pathlib import Path
from PIL import Image

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

def get_driver(url, headless=True):
    if headless:
        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome('./chromedriver', chrome_options=options)
    else:
        driver =  webdriver.Chrome('./chromedriver')
    driver.get(url)    
    return driver


uploaded_file = st.file_uploader("Upload an image")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        st.markdown("## Original PDF file")
        fp = Path(tmp_file.name)
        fp.write_bytes(uploaded_file.getvalue())
        
        st.write(tmp_file.name)
        st.image(uploaded_file)
        
        
        #driver = get_driver("https://www.google.com/imghp", headless=False)        
        
        
        

