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
cd 'TitanBot Code'
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

#### Query Travel Time Index 
https://github.com/user-attachments/assets/8e263773-01d6-45d9-9bff-3938ca6ed70f

#### Query Congestion Level and Road Works



https://github.com/user-attachments/assets/2167b51d-ed2e-4139-9ad3-e433975f2ca2



#### Query Congestion Map
https://github.com/user-attachments/assets/7deb0020-24a4-4cf7-9893-d1a4be57d15a



## Contact
If you have any questions, suggestions, or feedback, please feel free to reach out to us via one of our emails. We would love to hear from you!

- Neema Jakisa Owor: nodyv@missouri.edu
- Connor Joyce: cpjtdx@missouri.edu

We welcome and encourage contributions from the community! If you have ideas on how to expand or improve this project, please fork the repository and submit a pull request. Let's make this project even better together.

