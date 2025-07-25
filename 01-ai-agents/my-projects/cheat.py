from agents import Agent, Runner, function_tool, enable_verbose_stdout_logging
from rich import print
import sqlite3
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database connection
def connect_db():
    return sqlite3.connect(r"D:\huzair\coding\email-automation-system\mails.db")

# Tool 1: Fetch emails in batches
@function_tool
def get_data_from_db(batch_size=20, offset=0):
    """Fetch a batch of emails from the database."""
    connection = connect_db()
    cursor = connection.cursor()
    select_query = f"SELECT * FROM huzair_mails ORDER BY rowid DESC LIMIT {batch_size} OFFSET {offset}"
    cursor.execute(select_query)
    emails = cursor.fetchall()
    connection.close()
    
    # Format emails for the agent
    formatted_emails = [
        {
            "id": email[0],  # Adjust indices based on your table schema
            "sender": email[1],
            "subject": email[2],
            "body": email[3],
            "timestamp": email[4]
        } for email in emails
    ]
    return formatted_emails

# Tool 2: Summarize emails
@function_tool
def summarize_emails(emails, summary_storage="email_summaries.json"):
    """Summarize a batch of emails and append to storage."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    summaries = []
    
    for email in emails:
        # Summarize email body using Open AI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize the email content in 2-3 sentences, focusing on key points."},
                {"role": "user", "content": f"Subject: {email['subject']}\nBody: {email['body']}"}
            ],
            max_tokens=100
        )
        summary = {
            "id": email["id"],
            "sender": email["sender"],
            "subject": email["subject"],
            "summary": response.choices[0].message.content,
            "timestamp": email["timestamp"]
        }
        summaries.append(summary)
    
    # Load existing summaries
    try:
        with open(summary_storage, 'r') as f:
            existing_summaries = json.load(f)
    except FileNotFoundError:
        existing_summaries = []
    
    # Append new summaries
    existing_summaries.extend(summaries)
    
    # Save updated summaries
    with open(summary_storage, 'w') as f:
        json.dump(existing_summaries, f, indent=2)
    
    return {"status": "Summaries saved", "count": len(summaries)}

# Process all emails in batches
def process_all_emails(total_emails=500, batch_size=20):
    offset = 0
    while offset < total_emails:
        emails = get_data_from_db(batch_size=batch_size, offset=offset)
        if not emails:
            break
        summarize_emails(emails)
        offset += batch_size
    return {"status": "All emails processed"}

# Agent definition
db_analyzer = Agent(
    name="Email Analyzer Agent",
    instructions="""
    You are an email analyzer agent that answers user questions based on email summaries.
    Use the `summarize_emails` tool to process emails in batches and store summaries.
    When answering a query, load the summaries from 'email_summaries.json' and use them to respond.
    Include references to the email IDs, senders, and timestamps where the information was found.
    If no relevant information is found, clearly state so.
    Report the total number of emails processed based on the summaries.
    If detailed email content is needed, use the `get_data_from_db` tool to fetch specific emails.
    """,
    tools=[get_data_from_db, summarize_emails]
)

# Handle user query
def handle_query(query):
    # First, ensure all emails are processed
    process_all_emails(total_emails=500, batch_size=20)
    
    # Load summaries
    try:
        with open("email_summaries.json", 'r') as f:
            summaries = json.load(f)
    except FileNotFoundError:
        return "No email summaries found. Please process emails first."
    
    # Use Open AI to answer query based on summaries
    client = OpenAI(api_key=OPENAI_API_KEY)
    summary_text = json.dumps(summaries)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """
                Answer the user's query based on the provided email summaries.
                Include references to email IDs, senders, and timestamps.
                If no relevant information is found, state so.
                Mention the total number of emails processed.
            """},
            {"role": "user", "content": f"Query: {query}\nSummaries: {summary_text}"}
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    # enable_verbose_stdout_logging()
    query = "Does this go to webinars?"
    result = handle_query(query)
    print(result)