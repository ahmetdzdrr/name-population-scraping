# Name Population Scraping

This project is designed to scrape data related to names and their corresponding populations from a specified website. The extracted data can be utilized for various data analysis or statistical purposes. This repository provides a Python-based implementation of the web scraping process using popular libraries like `requests`, `BeautifulSoup`, and `pandas`.

## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Overview
This project aims to scrape a website containing name and population data, process the extracted data, and store it in a structured format like CSV for further analysis. The scraping process is handled by Python scripts that gather the data efficiently.

### Key Features
- Scrapes name and population data from a specified website.
- Handles web requests and data parsing using `requests` and `BeautifulSoup`.
- Stores scraped data in a structured CSV file for easy access and further analysis.
- Simple and easy-to-use code, designed for extensibility and customization.

## Prerequisites
Before running this project, you need to have the following software and libraries installed:

- **Python 3.x**
- **pip** (Python package installer)

The following Python libraries are required:
- `requests` – for sending HTTP requests to websites.
- `BeautifulSoup4` – for parsing HTML and extracting data.
- `pandas` – for structuring and saving the data in CSV format.

You can install the necessary libraries using the following command:

```bash
pip install -r requirements.txt
```

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/ahmetdzdrr/name-population-scraping.git
    cd name-population-scraping
    ```

2. **Install dependencies**:
    If you haven't already installed the required libraries, use the command:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To run the scraping script, simply execute the following command:

```bash
python name.py
```

```bash
python main.py
```

### Expected Output
1. After running the `name.py`, the data will be scraped from the specified website and stored in a text directory named `names.txt`. This directory will contain the following files:
- The all names that has been scraped and saved in text seperately.

2. After running `main.py`, the data will be scraped from the specified website and stored in a csv file with named `output.csv`. This CSV file will contains;
- `Name`: The name that has been scraped.
- `Population`: The population data corresponding to the name.

## Project Structure

```
name-population-scraping/
│
├── main.py                 # Main script that performs the web scraping
├── name.py                 # Name script that performs the collect all names
├── requirements.txt        # List of Python dependencies
├── output.csv              # Output file with scraped data 
└── README.md               # Project documentation
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`.
3. Make your changes and commit: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch`.
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.