# pip install requests selenium
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_zip_files(url):
    options = Options()
    
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tbody-content"]/tr/td[1]/a'))
        )
        
        if elements:
            # Create the 'data' folder if it doesn't exist
            if not os.path.exists('data'):
                os.makedirs('data')
            
            # Create the 'zips' subfolder inside 'data' if it doesn't exist
            zips_folder = os.path.join('data', 'zips')
            if not os.path.exists(zips_folder):
                os.makedirs(zips_folder)
            
            for element in elements:
                zip_url = element.get_attribute("href")
                zip_name = os.path.join(zips_folder, zip_url.split('/')[-1])
                
                print(f"Downloading {zip_name}...")
                
                response = requests.get(zip_url)
                
                if response.ok:
                    with open(zip_name, 'wb') as zip_file:
                        zip_file.write(response.content)
                    
                    print(f"{zip_name} downloaded successfully.")
                else:
                    print(f"Failed to download {zip_name}.")
        else:
            print("No zip files found on the page.")
    finally:
        driver.quit()

if __name__ == '__main__':
    url = 'https://divvy-tripdata.s3.amazonaws.com/index.html'
    download_zip_files(url)
