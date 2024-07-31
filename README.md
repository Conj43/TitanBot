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




## Demonstration

Querying for accidents by each day of the week:<br>
[![Watch the video](https://img.youtube.com/vi/Fg-2ccIZbTQ/0.jpg)](https://www.youtube.com/watch?v=Fg-2ccIZbTQ)
<br><br>
Querying for number of occurences of each light condition:<br>
[![Watch the video](https://img.youtube.com/vi/Fg-2ccIZbTQ/0.jpg)](https://youtu.be/6Z1PFLRdDqQ)



## Contact



