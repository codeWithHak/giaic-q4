# 🧠 Understand the *Why* Behind Every Line – History-Based Chat with Chainlit + OpenAI

This is a small but powerful project that shows how to use **Chainlit** and **OpenAI agents** to create a chatbot that **remembers previous messages** in a `history`.

### 👋 What does this project do?

Every time you send a message, the bot:
1. **Remembers** what you said.
2. **Generates a smart reply** using OpenAI's API.
3. **Saves** that reply too.
4. So the next time you chat, the AI has full **context**!

---

## ❓ Questions I had (that you might too!)

### 1. What is `cl.user_session.get()` and `cl.user_session.set()`?
These are **Chainlit’s methods** to **get and save data** during a user’s session.

- `get("history")` → Get saved list of messages.
- `set("history", history)` → Save the updated list.

> 🧠 Think of `cl.user_session` like a dictionary — you store data using a key (`"history"`) and a value (the list of messages).

---

### 2. Why do we need to use `.set()` after appending to the list?
Even though we changed the list with `append()`, **Chainlit won’t automatically know** it’s changed. So we must **explicitly save it again** with `set()`.

> ✅ Yes, `.set()` replaces the old value with the new one — just like updating a Python dictionary.

---

### 3. Is `.set()` a Python method or Chainlit's?
`cl.user_session.set()` is **Chainlit’s method** — not Python’s.  
It is made specifically to handle session data **on the server** (not in the browser like `localStorage`).

---

### 4. Where is this session stored? Browser or backend?
**Chainlit stores the session on the server side** — not in the browser.  
It's temporary and resets when the tab is closed (unless persisted manually).

---

## 📦 Code Flow Summary

You don’t need the full code — here’s what happens in simple steps:

```python
@cl.on_chat_start
# Step 1: Start a new session
cl.user_session.set("history", [])

@cl.on_message
# Step 2: Get previous chat history
history = cl.user_session.get("history")

# Step 3: Add user's new message
history.append({"role": "user", "content": message.content})

# Step 4: Pass entire history to the AI
result = await Runner.run(starting_agent=agent, input=history)

# Step 5: Save AI's response
history.append({"role": "assistant", "content": result.final_output})

# Step 6: Save updated history back into session
cl.user_session.set("history", history)

# Step 7: Send AI's reply back to user
await cl.Message(content=result.final_output).send()
