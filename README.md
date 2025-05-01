# Crypto Hub

## Overview

Crypto Hub is a Python-based project that integrates with the CoinGecko API to fetch cryptocurrency data and stores it
in a MySQL database. It efficiently manages API requests, caches responses, and ensures structured storage of market
data.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- MySQL Server (or use a MySQL Docker Container)
- [pip](https://pip.pypa.io/en/stable/) (Python package manager)
- Required dependencies listed in `requirements.txt`

## Setting Up MySQL with Docker

If you prefer running MySQL in a Docker container, follow these steps:

### 1. Pull the MySQL Docker image:

```
docker pull mysql:latest
```

### 2. Run a MySQL container with environment variables:

```
docker run --name mysql-container -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=my_database -e MYSQL_USER=my_user -e MYSQL_PASSWORD=my_password -p 3306:3306 -d mysql:latest
```

### 3. Verify the container is running:

```
docker ps
```

### 4. To access the MySQL container:

```
docker exec -it mysql-container mysql -u root -p
```

## Database Setup

Before running the project, ensure that the necessary MySQL tables are created. You can do this using DBeaver or
directly from the MySQL container.

1. Using DBeaver
    - Install [Dbeaver Community](https://dbeaver.io/) and install it following the instructions for your operating
      system.
2. Open DBeaver
    - Once installed, launch **DBeaver**.

3. Create a connection
    - Click on "New Connection".
    - Select MySQL from the available database types.
    - Configure the connection with the following parameters:
        - Host: localhost (or the MySQL Docker container's IP)
        - Port: 3306
        - Database: my_database
        - User: my_user
        - Password: my_password
    - Click **"Test Connection"** to verify that everything is set up correctly.
    - If successful, click "Finish".

4. Navigate to the SQL Editor and execute the required CREATE TABLE statements.

Table Schema Definitions

```
CREATE TABLE cryptos (
    id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    name VARCHAR(100) NOT NULL
) COMMENT = 'List of all cryptocurrencies';

CREATE TABLE market_bitcoin (
    crypto_id VARCHAR(50),
    currency VARCHAR(10) NOT NULL,
    current_price VARCHAR(30) NOT NULL,
    market_cap VARCHAR(30) NOT NULL,
    total_volume VARCHAR(30) NOT NULL,
    PRIMARY KEY (crypto_id, currency)
) COMMENT = 'Bitcoin market details';

CREATE TABLE historical_bitcoin_prices (
    timestamp VARCHAR(50) PRIMARY KEY,
    prices VARCHAR(30) NOT NULL,
    market_caps VARCHAR(30) NOT NULL,
    total_volumes VARCHAR(30) NOT NULL
) COMMENT = 'Daily Bitcoin price history for 2025';
```

## Installation

Clone the repository and navigate to the project folder:

```
git clone https://github.com/crypto_hub/crypto-hub.git  
cd crypto-hub
```

Create a virtual environment (recommended):

``` 
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate  # Windows  
```

Install dependencies

```
pip install -r requirements.txt  
```

## Environment Configuration

🔹 Configuration File Locations

- `.env` → Must be located in the project root. I created the `.env` file to contain credentials and sensitive settings.

Sample `.env` File:

```
# Database Configuration  
MYSQL_DATABASE=my_database  
MYSQL_USER=my_user  
MYSQL_PASSWORD=my_password  
MYSQL_HOST=localhost  
MYSQL_PORT=3306  

# CoinGecko API Configuration  
API_URL=https://api.coingecko.com/api/v3  
API_TOKEN=your_token_here  

# API Query Parameter Configuration  
MARKET_DATA=True  
CURRENCY=usd  
START_DATE_UNIX=1672531200  
END_DATE_UNIX=1672617600  
```

## Running the Project

Execute the `app.py` script to start the process

```
python app.py
```

## Running Unit Tests

To execute unit tests, run:

```
python -m unittest discover tests
```

## Running Jupyter Notebooks

To execute the notebooks for analysis, visualization, or testing within Anaconda, follow these steps:

1️⃣ Install Anaconda

Download it from [Anaconda](https://www.anaconda.com/) and follow the installation instructions for your operating
system.

2️⃣ Launch Jupyter Lab and install required packages:

```
!pip install pyspark==3.4.3
!pip install pandas
!pip install matplotlib
!pip install seaborn
```

## Available Jupyter Notebooks

The following notebooks are available in the `root/` directory, providing insights into cryptocurrency data
processing and visualization:

📌 **`extract_data_db.ipynb`** → Extracts and structures data from the MySQL database before processing.

📌 **`processing_data.ipynb`** → Transforms and analyzes data, including key metric calculations.

📌 **`analyze_and_visualization.ipynb`** → Performs trend analysis and creates interactive charts to visualize market
behavior.

## Notebook Executions

The executions of the first two notebooks will be saved in the following formats and paths:

1. **extract_data_db.ipynb**:
    - **Format**: CSV
    - **Path**: `/data/raw/`

2. **processing_data.ipynb**:
    - **Format**: PARQUET
    - **Path**: `/data/output/`

## Contributing

Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (`git checkout -b feature-branch`).
- Make your changes.
- Commit your changes (`git commit -m 'Add some feature'`).
- Push to the branch (`git push origin feature-branch`).
- Open a Pull Request.