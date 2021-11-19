import streamlit as st
import tempfile
from pathlib import Path
import os

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options

import json
import sys
from urllib import request
from urllib.parse import parse_qsl
from urllib.parse import urlparse
import oauth2 as oauth

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

def search_keyword_by_image(file):
    try:
        driver = get_driver("https://www.google.com/imghp", headless=True)        
        driver.find_element_by_xpath("//div[@aria-label='Search by image']").click()
        driver.find_element_by_name("encoded_image").send_keys(file.name)
        q = driver.find_element_by_name("q").get_attribute("value")
        return q
    except:
        return ""
    finally:
        driver.close()
    

class Discogs():
    def __init__(self):
        # consumer
        consumer_key = os.environ['CONSUMER_KEY']
        consumer_secret = os.environ['CONSUMER_SECRET']
        token_key = os.environ['TOKEN_KEY']
        token_secret = os.environ['TOKEN_SECRET']
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        token = oauth.Token(key=token_key, secret=token_secret)
        self.client = oauth.Client(consumer, token)
        self.base_url = 'https://api.discogs.com/'
        self.user_agent = 'discogs_api_example/1.0'
        
    def search(self, q, type_="master"):
        res, content = self.client.request(f'{self.base_url}database/search?type={type_}&q={q}', headers={'User-Agent': self.user_agent})
        releases = json.loads(content.decode('utf-8'))
        return releases['results'] if 'results' in releases else []
        
    def fetch_master(self, master_id):
        res, content = self.client.request(f'{self.base_url}masters/{master_id}', headers={'User-Agent': self.user_agent})
        return  json.loads(content.decode('utf-8'))


st.title("レコード・ジャケットで検索")    
    
uploaded_file = st.file_uploader("画像をアップロードしてください")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        fp = Path(tmp_file.name)
        fp.write_bytes(uploaded_file.getvalue())
        
        st.image(uploaded_file)
        
        with st.spinner("検索中..."):
            # TODO: useragent
            q = search_keyword_by_image(tmp_file)

            client = Discogs()
            releases = client.search(q)
            
        st.header("検索結果")
        if len(releases) == 0: st.write("見つかりませんでした。")
        for release in releases:
            url = f"https://www.discogs.com/ja/master/{release['id']}"
            year = release['year'] if 'year' in release else ''
            country = release['country'] if 'country' in release else ''
            
            col1, col2 = st.beta_columns(2)
            with col1:
                st.image(release['thumb'])
            with col2:
                st.markdown(f"[{release['title']}]({url})")
                st.write(f'（{year} / {country})')
                
        
        
        
        
        
        

