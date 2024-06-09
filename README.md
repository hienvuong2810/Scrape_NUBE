# Scrape_NUBE

This project utilizes Python libraries such as `typing`, `beautifulsoup4`, `httpx`, and `pandas`. Below are the instructions to install dependencies and run the project.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://github.com/hienvuong2810/Scrape_NUBE/tree/main
    cd Scrape_NUBE
    ```

2. **Create a Virtual Environment (optional but recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies from `requirements.txt`**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Script

Before running the `harveynorman.py` script, make sure to fetch the latest cookie and user-agent from the website and replace as variable. This ensures that the script interacts with the website correctly.

To run the `harveynorman.py` script, use the following command:

```bash
python harveynorman.py
