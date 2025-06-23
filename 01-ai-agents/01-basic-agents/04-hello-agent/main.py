import chainlit as cl
from datetime import datetime




# template code
@cl.on_message
async def res(message):
    await cl.Message(f"Recieved {message.content} \n created at: {message.created_at}").send()

# my experiment
# @cl.on_message
# async def res(message:cl.Message):
#     try:
#         curr_time = datetime.utcnow()
#         created_at = datetime.fromisoformat(message.created_at.rstrip("z"))
#         if not created_at:
#             raise ValueError("message.create_at is missing")

#         total_time = f"{(curr_time - created_at).total_seconds():.3f}"
#         await cl.Message(content=f"Recieved {message.content} \n Responded in: {total_time} seconds").send()
#     except Exception as e:
#         await cl.Message(content=f"Error: {e}").send()
        
        

# easy code

# @cl.on_message
# async def res(message:cl.Message):
#     message = cl.Message(content=f"Hellooo {message.content}")
#     await message.send()
    # created_at