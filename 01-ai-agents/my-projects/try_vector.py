from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging, set_default_openai_api, OpenAIChatCompletionsModel, AsyncOpenAI
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel
import sqlite_vec
from google import genai

set_default_openai_api("chat_completions")


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# enable_verbose_stdout_logging()
# enable_verbose_stdout_logging()

class Row(BaseModel):
    sender:str
    subject:str
    date:str
    mail:str


def get_data_from_db():
    """fetch 20,20 mails from db in and give it to summarize_mail tool"""

    connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
    cursor = connection.cursor()
    select_query = "SELECT * FROM huzair_mails "
    # rows = cursor.execute(select_query).fetchall()
    data = cursor.execute(select_query).fetchall()

    # select_query = "SELECT * FROM huzair_mails"
    rows = cursor.execute(select_query).fetchall()
      
    mails = [f"ID: {0} | Sender: {row[1]} | Subject: {row[2]} | Date: {row[3]} | Mail: {row[4]}" for row in rows]
    # return mails
    return data

def create_embeddings(text:str):
    client = genai.Client()

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text)

    return result.embeddings


def store_vectors_in_db():

    data = get_data_from_db()
    connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails_vector.db")
    cursor = connection.cursor()
    create_query = """
    CREATE VIRTUAL TABLE email_vectors USING vss0(
        rowid INTEGER PRIMARY KEY,
        email_id TEXT,
        vector(786)
        );
    """
    cursor.execute(create_query)

    embedding = create_embeddings("does this user listens to songs")

    insert_query = """
    INSERTI INTO email_vectors (email_id, vector) VALUES(?,?) ,   
    """


# result = Runner.run_sync(starting_agent=db_analyzer, input="What's the name of the user?")

# print(result.final_output)



# connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
# select_query = "SELECT * FROM huzair_mails ORDER BY rowid DESC LIMIT 20"
# cursor = connection.cursor()

# data = cursor.execute(select_query).fetchall()



    # summaries = []
    
    # mails = get_data_from_db()

    # for mail in mails:
    #     summary = "From: {sender} | Subject: {subject} | Date: {date} | Summary: {summarised_mail}"
    #     summaries.append(summary)