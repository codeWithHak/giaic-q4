from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging, set_default_openai_api, AsyncOpenAI,OpenAIChatCompletionsModel
from rich import print
import sqlite3
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# set_default_openai_api("chat_completions")


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
def get_data_from_db(offset:int=0, limit:int=20) -> list[str]:
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
    """Create a one line summary for all mails recieved in {mails}"""
    
    return f"Summarized {len(mails)} and appended into prev summary"



db_analyzer = Agent(name="Email Analyzer Agent",
                    instructions="""Your job is to:
1. Call `get_data_from_db` starting with offset=0 and limit=20.
2. Use `summarize_mail` to keep building a full summary using the returned emails.
3. Repeat until no more emails are left (less than 20 returned).
4. Then answer the user's question using the full summary.
""",
                    tools=[get_data_from_db, summarize_mail],
                    model=OpenAIChatCompletionsModel(
                        model="gpt-4.1",
                        openai_client=AsyncOpenAI()
                        )
                    )

result = Runner.run_sync(starting_agent=db_analyzer, input="Does this goes to webinars?")

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