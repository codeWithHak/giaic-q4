import chainlit as cl
from chainlit import Message

@cl.on_message
async def handle_message(message):
    message = Message(f"Recieved {message.content}")
    await message.send()