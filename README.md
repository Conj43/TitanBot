# TitanBot
TitanBot is a Python chatbot that leverages the OpenAI API to query ChatGPT and interact with your transportation database. It allows users to ask natural language questions, query SQL databases, and receive insightful responses with interactive visuals. TitanBot can also dynamically generate and execute Python code, enabling real-time data analysis and customized outputs based on user queries.

## Installation
Follow these steps to install and configure TitanBot locally:

Make sure you have:
- Python 3.7 or later (https://www.python.org/downloads/)
- OpenAI API key (https://platform.openai.com/api-keys)
- Docker Installed and Running (https://docs.docker.com/engine/install/)


## Clone Repository
```
git clone https://github.com/Conj43/TitanBot.git
cd TitanBot/'TitanBot Code'
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
##### Command Prompt
```
set OPENAI_API_KEY=your-openai-api-key
```
##### PowerShell
```
$env:OPENAI_API_KEY="your-openai-api-key"
```
#### macOS/Linux
```
export OPENAI_API_KEY=your-openai-api-key
```

## Deactivate and Reactivate your Virtual Environment
#### Windows
```
deactivate
venv\Scripts\activate
```
#### macOS/Linux
```
deactivate
source venv/bin/activate
```

## Running the Application
```
streamlit run main.py
```
### For Files Over 200MB (Example is for 400MB max but it can be increased)
```
streamlit run main.py --server.maxUploadSize 400
```

## Usage
You'll need to upload a database in order to chat with TitanBot. You may use a SQLite database, one or multiple CSV files, or an API link to a database.
Databases are opened in Read-Only mode, and CSV files and API links are queried by creating temporary SQLite databases, so no need to worry about data corruption.








## Demonstration

#### SQL Schema and Simple Query Execution
https://github.com/user-attachments/assets/c53f170b-acfb-441a-b7ac-178ab533c6c0



#### Speed Index for One Year Demo
https://github.com/user-attachments/assets/38e6dc77-753e-4957-b88b-1d7939f43a21



#### Accident Map Demo
https://github.com/user-attachments/assets/8389dab2-d162-4f54-84e8-e25c1355d7bd



#### Plot Displaying Average Speed by Hour of the Day
https://github.com/user-attachments/assets/fa1d80a5-33ef-46d5-a2dd-399d797ee0a4





#### Aggregated Travel Time Index Saved to CSV File
https://github.com/user-attachments/assets/381a47b0-f3c2-4d42-8db6-12ff30ec9b7a





## Contact
If you have any questions, suggestions, or feedback, please feel free to reach out to us via one of our emails. We would love to hear from you!

- Neema Jakisa Owor: nodyv@missouri.edu
- Connor Joyce: cpjtdx@missouri.edu

We welcome and encourage contributions from the community! If you have ideas on how to expand or improve this project, please fork the repository and submit a pull request. Let's make this project even better together.

