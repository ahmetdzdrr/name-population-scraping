import os
import time
import json
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

class NameDataFetcher:
    def __init__(self, folder_path, output_file):
        self.folder_path = folder_path
        self.output_file = output_file
        self.driver = None

    def setup_chrome_driver(self):
        chrome_options = Options()
        service = Service('chromedriver') 
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def read_names_from_txt_folder(self):
        names = []
        for file_name in os.listdir(self.folder_path):
            if file_name.endswith('.txt'):
                with open(os.path.join(self.folder_path, file_name), 'r') as file:
                    names.extend([line.strip() for line in file.readlines()])
        return names

    def fetch_and_process_data(self, name, sex):
        url = f'https://nvb.meertens.knaw.nl/populariteit/absoluut/{sex}/eerstenaam/{name}#data'
        print(f"Fetching data for {name} ({sex})..")
        
        self.driver.get(url)
        time.sleep(3)

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        scripts = soup.find_all('script', type='text/javascript')

        year_list = None
        steptotal_approximation_list = None

        for script in scripts:
            script_content = script.text
            if script_content:
                year_list_match = re.search(r'var year_list\s*=\s*new Array\((.*?)\);', script_content, re.DOTALL)
                steptotal_approximation_list_match = re.search(r'var steptotal_approximation_list\s*=\s*new Array\((.*?)\);', script_content, re.DOTALL)
                
                if year_list_match:
                    year_list = year_list_match.group(1)
                if steptotal_approximation_list_match:
                    steptotal_approximation_list = steptotal_approximation_list_match.group(1)
                
                if all([year_list, steptotal_approximation_list]):
                    print(f"JavaScript variables found for {name} ({sex})")
                    break

        if all([year_list, steptotal_approximation_list]):
            try:
                years = json.loads(f"[{year_list}]")
                steptotal_approximations = json.loads(f"[{steptotal_approximation_list}]")

                df = pd.DataFrame({
                    'Year': years,
                    'Steptotal_Approximation': steptotal_approximations,
                    'Sex': sex,
                    'Name': name
                })

                print(f"Data successfully fetched and processed for {name} ({sex})")
                return df
            except json.JSONDecodeError as e:
                print(f"JSON decoding error for {name} ({sex}):", e)
                return None
        else:
            print(f"One or more JavaScript variables not found for {name} ({sex}).")
            return None

    def fetch_all_data(self):
        self.setup_chrome_driver()
        names = self.read_names_from_txt_folder()
        all_dfs = []

        for name in names:
            for sex in ['maan', 'vrouw']:
                print(f"\nProcessing {name} ({sex})")
                df = self.fetch_and_process_data(name, sex)
                if df is not None:
                    all_dfs.append(df)
                time.sleep(2) 
        
        if all_dfs:
            final_df = pd.concat(all_dfs, ignore_index=True)
            final_df.to_csv(self.output_file, index=False)
            print(f"Data saved to {self.output_file}")
            print(final_df)
        else:
            print("No data to save.")

        self.driver.quit()

if __name__ == "__main__":
    folder_path = 'names_txt'
    output_file = 'output.csv'
    data_fetcher = NameDataFetcher(folder_path, output_file)
    data_fetcher.fetch_all_data()
