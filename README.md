# TitanBot
TitanBot is a Python chatbot that leverages the OpenAI API to query ChatGPT and interact with your transportation database. It allows users to ask natural language questions and receive insightful responses and interactive visuals, making database interactions more intuitive and efficient. 

## Installation
Follow these steps to install and configure TitanBot locally:

Make sure you have:
- Python 3.7 or later
- OpenAI API key

## Clone Repository
```
git clone https://github.com/Conj43/TitanBot.git
cd TitanBot
```
## Create and Activate a Virtual Environment

#### Windows
```
python -m venv venv
venv\Scripts\activate
```
#### macOS/Linux
```
python -m venv venv
source venv/bin/activate
```

## Install Dependencies
```
pip install -r requirements.txt
```

## Configure OpenAI API Key
#### Windows
```
set OPENAI_API_KEY='your-openai-api-key'
```
#### macOS/Linux
```
export OPENAI_API_KEY='your-openai-api-key'
```

## Running the Application
```
streamlit run main.py
```

## Usage
You'll need to upload a database in order to chat with TitanBot. You may use a SQLite database, or an API link to a database.
Databases are opened in Read-Only mode, so no need to worry about data corruption.








## Demonstration

#### Query Distribution of Accidents in Different Light Conditions
https://github.com/user-attachments/assets/85f463de-c845-4940-bb90-acabd096f3a2

#### Query Accident Distribution of Days of the Week
https://github.com/user-attachments/assets/e9a02aba-3f80-42a2-b2d1-17ce1aa99b41



## Contact


