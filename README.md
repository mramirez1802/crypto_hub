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

## Installation

Clone the repository and navigate to the project folder:

```
git clone https://github.com/your-repo/crypto-hub.git  
cd crypto-hub
```

## Create a virtual environment (recommended):

```
python -m venv venv  
source venv/bin/activate  # Linux/Mac  
venv\Scripts\activate  # Windows  
```

## Install dependencies

```
pip install -r requirements.txt  
```

## Environment Configuration

Ensure you have a `.env` file in the `config/` directory containing the following environment variables:

```
DEBUG=True  
MYSQL_DATABASE=my_database  
MYSQL_USER=my_user  
MYSQL_PASSWORD=my_password  
MYSQL_HOST=localhost  
MYSQL_PORT=3306  
API_URL=https://api.coingecko.com/api/v3  
API_TOKEN=your_token_here  
MARKET_DATA=True  
CURRENCY=usd  
START_DATE_UNIX=1672531200  
END_DATE_UNIX=1672617600  
LOG_LEVEL=INFO
```

## Running the Project

```
Execute the `main.py` script to start the process:
python main.py  
```
