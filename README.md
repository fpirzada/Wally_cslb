
# CSLB Data Scraper

This project is designed to scrape data from the California State License Board (CSLB) website and store it in an Excel file. The extracted data can be used for various purposes, such as analysis, reporting, and more.

## Features

1. Scrapes data from the CSLB website.
2. Stores the extracted data in an Excel file.
3. Utilizes Python 3.10 for development.
4. Dependencies include:
   * `beautifulsoup4==4.12.2`
   * `selenium==4.11.2`
   * `openpyxl==3.1.2`

## Setup

Follow these steps to set up and run the project:

1. Run the `setup.sh` script to create a virtual environment and install dependencies.
2. Activate the virtual environment:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">source venv/bin/activate
   </code></div></div></pre>
3. Run the main script:
   <pre><div class="bg-black rounded-md mb-4"><div class="flex items-center relative text-gray-200 bg-gray-800 px-4 py-2 text-xs font-sans justify-between rounded-t-md"><span>bash</span><button class="flex ml-auto gap-2"><svg stroke="currentColor" fill="none" stroke-width="2" viewBox="0 0 24 24" stroke-linecap="round" stroke-linejoin="round" class="h-4 w-4" height="1em" width="1em" xmlns="http://www.w3.org/2000/svg"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"></path><rect x="8" y="2" width="8" height="4" rx="1" ry="1"></rect></svg>Copy code</button></div><div class="p-4 overflow-y-auto"><code class="!whitespace-pre hljs language-bash">python LetsGo.py
   </code></div></div></pre>

## Project Structure

* `LetsGo.py`: Main script to execute the data scraping process.
* `EStore.py`: Script for Excel storage settings.
* `scraper/engine.py`: Configuration for Selenium to interact with the website.
* `data/US_States_and_Cities.json`: JSON file containing city data for scraping.

## Usage

1. Run the setup script to create the virtual environment and install dependencies.
2. Activate the virtual environment.
3. Run the main script `LetsGo.py` to start the data scraping process.
4. The scraped data will be stored in an Excel file.

## Contributing

Contributions are welcome! If you find any issues or want to add enhancements, feel free to create pull requests or raise issues.

## License

This project is licensed under the [MIT License](https://chat.openai.com/c/LICENSE).
