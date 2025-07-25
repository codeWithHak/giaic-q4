from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging, set_default_openai_api, OpenAIChatCompletionsModel, AsyncOpenAI
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel

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


@function_tool
def get_data_from_db(offset:int=0, limit:int=15) -> list[str]:
    """fetch 20,20 mails from db in and give it to summarize_mail tool"""

    connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
    cursor = connection.cursor()
    select_query = "SELECT * FROM huzair_mails ORDER BY rowid LIMIT ? OFFSET ?"
    rows = cursor.execute(select_query,(limit,offset)).fetchall()

    # select_query = "SELECT * FROM huzair_mails"
    # rows = cursor.execute(select_query).fetchall()
      
    mails = [f"Sender: {row[1]} | Subject: {row[2]} | Date: {row[3]} | Mail: {row[4]}" for row in rows]
    return mails

@function_tool
def summarize_mail(mails:list[str], prev_summary:str = '') -> str:
    """Create a one line summary for all mails recieved in {mails} and save in a file named mails_summary.json"""
    

    return f"Summarized {len(mails)} and appended into prev summary"



db_analyzer = Agent(name="Email Analyzer Agent",
                    instructions="""
Call get_data_from_db(offset=0, limit=15).

Pass those mails into summarize_mail.

If you received exactly 15 mails, increment your offset by 15 and repeat steps 1–3.

Otherwise, you’ve reached the end—call summarize_mail one last time (if needed) and then answer the user’s question, reporting the total mails you’ve read.
                 """,                
                    tools=[get_data_from_db, summarize_mail],
                    model = OpenAIChatCompletionsModel(
                        model="gpt-4-turbo",
                        openai_client=AsyncOpenAI()
                        )
                        
                    )

result = Runner.run_sync(starting_agent=db_analyzer, input="What's the name of the user?")

print(result.final_output)



# connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
# select_query = "SELECT * FROM huzair_mails ORDER BY rowid DESC LIMIT 20"
# cursor = connection.cursor()

# data = cursor.execute(select_query).fetchall()



    # summaries = []
    
    # mails = get_data_from_db()

    # for mail in mails:
    #     summary = "From: {sender} | Subject: {subject} | Date: {date} | Summary: {summarised_mail}"
    #     summaries.append(summary)