from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import math
import os

alphabet = 'abcdefghijklmnopqrstuvwxyz'

def get_chrome_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)
    return driver

def get_page_count(description_text):
    try:
        start_index = description_text.lower().find('van') + len('van')
        number = int(description_text[start_index:].strip().split()[0])
        return math.ceil(number / 15) 
    except (ValueError, AttributeError):
        return 1 

def scrape_names_for_char(driver, char):
    base_url = f'https://nvb.meertens.knaw.nl/naam/begintmet/{char}'
    driver.get(base_url)
    
    try:
        WebDriverWait(driver, 0.2).until(
            EC.presence_of_element_located((By.CLASS_NAME, "namelist"))
        )
    except Exception as e:
        print(f"Error loading base page for letter '{char}': {e}")
        return []

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    description_div = soup.find('div', class_='namelist')

    if description_div:
        description_text_element = description_div.find('div', class_='description')
        if description_text_element:
            description_text = description_text_element.get_text(strip=True)
            page_count = get_page_count(description_text)
            print(f"Total pages for '{char}': {page_count}")
        else:
            print(f"No description text found for letter '{char}'")
            page_count = 1
    else:
        print(f"No namelist found for letter '{char}'")
        return []

    all_names = []

    for page_num in range(1, page_count + 1):
        page_url = f'https://nvb.meertens.knaw.nl/naam/pagina{page_num}/begintmet/{char}'
        driver.get(page_url)
        
        try:
            WebDriverWait(driver, 0.2).until(
                EC.presence_of_element_located((By.CLASS_NAME, "namelist"))
            )
        except Exception as e:
            print(f"Error loading page {page_num} for letter '{char}': {e}")
            continue

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        table_div = soup.find('div', class_='namelist')
        if table_div:
            table = table_div.find('table', class_='namelist')
            if table:
                rows = table.find_all('tr', class_='data')
                for row in rows:
                    a_tag = row.find('a')
                    if a_tag:
                        all_names.append(a_tag.get_text(strip=True))
            else:
                print(f"No table found on page {page_num} for letter '{char}'")
        else:
            print(f"No namelist div found on page {page_num} for letter '{char}'")
        
    return all_names

def save_names_to_txt(names_dict, output_directory='names_txt'):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    for char, names in names_dict.items():
        file_name = f'{char}_names.txt'
        file_path = os.path.join(output_directory, file_name)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            for name in names:
                file.write(name + '\n')
        
        print(f"Saved {len(names)} names for letter '{char}' to '{file_path}'")

def main():
    driver = get_chrome_driver()
    all_names_dict = {}
    
    try:
        for char in alphabet:
            if char in all_names_dict and all_names_dict[char]:
                print(f"Data for letter '{char}' already exists. Skipping...")
                continue

            print(f"Scraping names for letter '{char}'...")
            names = scrape_names_for_char(driver, char)
            if names:
                all_names_dict[char] = names
                print(f"Scraped {len(names)} names for letter '{char}'")
            else:
                print(f"No names found for letter '{char}'")
        
        save_names_to_txt(all_names_dict)

    finally:
        driver.quit()
        print("Driver closed.")

    print("Scraping complete.")

if __name__ == '__main__':
    main()
