# Understand the Why Behind Every Line Of Code!

## History Based Chatbot with Chainlit and OpenAI Agents SDK

This project demonstrates how to use Chainlit with OpenAI Agents SDK to build a chatbot that maintains conversation history. It ensures each user message and AI response is stored, so the assistant can respond with context.

## What this project does

Each time the user sends a message:
1. The message is added to a session-based history.
2. The entire history is sent to the agent.
3. The agent’s reply is added to the same history.
4. Both user and assistant messages are saved in the session.

## Questions and Doubts Answered

### 1. What is `cl.user_session.get()` and `cl.user_session.set()`?

These are Chainlit methods used to handle session data:

- `get("history")` retrieves the current session's message history.
- `set("history", history)` saves or updates the message history.

Chainlit internally treats this like a key-value store, similar to a Python dictionary.

### 2. Why is `set()` used after `append()`?

Even though `append()` modifies the list in Python, Chainlit does not automatically detect changes in session data. You must explicitly call `set()` to tell Chainlit to save the updated list in the session.

### 3. Is `set()` a built-in Python method?

No. `cl.user_session.set()` is provided by Chainlit. It is not the same as Python’s `set()` type. This method is specific to Chainlit's session handling.

### 4. Is session data stored in the browser?

No. Chainlit stores session data on the server side. It is temporary and tied to the current user session. When the session ends (e.g., browser tab closes), the data is lost unless custom persistence is implemented.

## Code Summary

The key logic behind the project:

```python
@cl.on_chat_start
cl.user_session.set("history", [])

@cl.on_message
history = cl.user_session.get("history")
history.append({"role": "user", "content": message.content})

result = await Runner.run(starting_agent=agent, input=history)

history.append({"role": "assistant", "content": result.final_output})
cl.user_session.set("history", history)

await cl.Message(content=result.final_output).send()
