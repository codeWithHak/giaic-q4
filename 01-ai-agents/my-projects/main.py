from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# enable_verbose_stdout_logging()

@function_tool
def get_data_from_db():
    """ fetch last 10 mails from the database"""

    connection = sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")
    select_query = "SELECT * FROM huzair_mails ORDER BY rowid DESC LIMIT 20"
    cursor = connection.cursor()
    data = cursor.execute(select_query).fetchall()

    return data


db_analyzer = Agent(name="Email Analyzer Agent",
                    instructions="""
                    You are and email analyzer agent, that answer user questions base on their emails.
                    You will analyze the mails base on user question, and answer to user.
                    Also, always add a reference of how you got to know that info about the user means in which mail you found it.

                    If you don't find any info in mails related to user's question clearly say that, and tell what kind of emails you found in data
                    """,
                    tools=[get_data_from_db]
                    )

result = Runner.run_sync(starting_agent=db_analyzer, input="Does this user listens to songs?")

print(result.final_output)



