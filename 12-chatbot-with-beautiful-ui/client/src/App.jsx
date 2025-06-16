"use client"

import { useState, useRef, useEffect } from "react"
import { Send, Code, Heart, User, Zap, Smile } from "lucide-react"

// Enhanced markdown renderer
const SimpleMarkdown = ({ content }) => {
  if (!content) return null

  try {
    const parseInlineFormatting = (text) => {
      if (!text) return text

      // Handle inline code first (to avoid conflicts)
      text = text.replace(
        /`([^`]+)`/g,
        '<code class="bg-gray-800 text-green-400 px-2 py-1 rounded text-sm font-mono">$1</code>',
      )

      // Handle bold text
      text = text.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-bold text-green-300">$1</strong>')

      // Handle italic text (single asterisk, but not at start of line for bullet points)
      text = text.replace(/(?<!^|\s)\*([^*s][^*]*[^*s])\*(?!\*)/g, '<em class="italic text-green-200">$1</em>')

      // Handle links
      text = text.replace(
        /\[([^\]]+)\]$$([^)]+)$$/g,
        '<a href="$2" class="text-green-400 underline hover:text-green-300" target="_blank" rel="noopener noreferrer">$1</a>',
      )

      return text
    }

    const lines = content.split("\n")
    const elements = []
    let currentElement = []
    let inCodeBlock = false
    let inList = false
    let listItems = []

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i]
      const trimmedLine = line.trim()

      // Code blocks
      if (trimmedLine.startsWith("```")) {
        // End any current list
        if (inList && listItems.length > 0) {
          elements.push(
            <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
              {listItems.map((item, idx) => (
                <li
                  key={idx}
                  className="text-gray-100"
                  dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                />
              ))}
            </ul>,
          )
          listItems = []
          inList = false
        }

        if (inCodeBlock) {
          // End code block
          elements.push(
            <pre key={i} className="bg-gray-900 border border-green-500/20 rounded-lg p-4 overflow-x-auto mb-4">
              <code className="text-green-300 text-sm font-mono">{currentElement.join("\n")}</code>
            </pre>,
          )
          currentElement = []
          inCodeBlock = false
        } else {
          // Start code block
          if (currentElement.length > 0) {
            elements.push(
              <p
                key={`p-${i}`}
                className="mb-4 text-lg leading-relaxed text-gray-100"
                dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
              />,
            )
            currentElement = []
          }
          inCodeBlock = true
        }
        continue
      }

      if (inCodeBlock) {
        currentElement.push(line)
        continue
      }

      // Headers
      if (trimmedLine.startsWith("### ")) {
        // End any current content
        if (inList && listItems.length > 0) {
          elements.push(
            <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
              {listItems.map((item, idx) => (
                <li
                  key={idx}
                  className="text-gray-100"
                  dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                />
              ))}
            </ul>,
          )
          listItems = []
          inList = false
        }
        if (currentElement.length > 0) {
          elements.push(
            <p
              key={`p-${i}`}
              className="mb-4 text-lg leading-relaxed text-gray-100"
              dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
            />,
          )
          currentElement = []
        }
        elements.push(
          <h3 key={i} className="text-xl font-bold mb-3 text-green-400">
            {trimmedLine.slice(4)}
          </h3>,
        )
      } else if (trimmedLine.startsWith("## ")) {
        // End any current content
        if (inList && listItems.length > 0) {
          elements.push(
            <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
              {listItems.map((item, idx) => (
                <li
                  key={idx}
                  className="text-gray-100"
                  dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                />
              ))}
            </ul>,
          )
          listItems = []
          inList = false
        }
        if (currentElement.length > 0) {
          elements.push(
            <p
              key={`p-${i}`}
              className="mb-4 text-lg leading-relaxed text-gray-100"
              dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
            />,
          )
          currentElement = []
        }
        elements.push(
          <h2 key={i} className="text-2xl font-bold mb-4 text-green-400">
            {trimmedLine.slice(3)}
          </h2>,
        )
      } else if (trimmedLine.startsWith("# ")) {
        // End any current content
        if (inList && listItems.length > 0) {
          elements.push(
            <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
              {listItems.map((item, idx) => (
                <li
                  key={idx}
                  className="text-gray-100"
                  dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                />
              ))}
            </ul>,
          )
          listItems = []
          inList = false
        }
        if (currentElement.length > 0) {
          elements.push(
            <p
              key={`p-${i}`}
              className="mb-4 text-lg leading-relaxed text-gray-100"
              dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
            />,
          )
          currentElement = []
        }
        elements.push(
          <h1 key={i} className="text-3xl font-bold mb-4 text-green-400">
            {trimmedLine.slice(2)}
          </h1>,
        )
      } else if (trimmedLine.startsWith("* ") || trimmedLine.startsWith("- ")) {
        // List item
        if (currentElement.length > 0) {
          elements.push(
            <p
              key={`p-${i}`}
              className="mb-4 text-lg leading-relaxed text-gray-100"
              dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
            />,
          )
          currentElement = []
        }
        inList = true
        listItems.push(trimmedLine.slice(2))
      } else if (trimmedLine === "") {
        // Empty line - end current content
        if (inList && listItems.length > 0) {
          elements.push(
            <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
              {listItems.map((item, idx) => (
                <li
                  key={idx}
                  className="text-gray-100"
                  dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                />
              ))}
            </ul>,
          )
          listItems = []
          inList = false
        }
        if (currentElement.length > 0) {
          elements.push(
            <p
              key={`p-${i}`}
              className="mb-4 text-lg leading-relaxed text-gray-100"
              dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
            />,
          )
          currentElement = []
        }
      } else {
        // Regular text
        if (inList) {
          // If we're in a list but this line doesn't start with *, end the list
          if (!trimmedLine.startsWith("* ") && !trimmedLine.startsWith("- ")) {
            elements.push(
              <ul key={`list-${i}`} className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
                {listItems.map((item, idx) => (
                  <li
                    key={idx}
                    className="text-gray-100"
                    dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }}
                  />
                ))}
              </ul>,
            )
            listItems = []
            inList = false
            currentElement.push(line)
          }
        } else {
          currentElement.push(line)
        }
      }
    }

    // Add remaining content
    if (inList && listItems.length > 0) {
      elements.push(
        <ul key="final-list" className="list-disc list-inside mb-4 space-y-2 text-lg ml-4">
          {listItems.map((item, idx) => (
            <li key={idx} className="text-gray-100" dangerouslySetInnerHTML={{ __html: parseInlineFormatting(item) }} />
          ))}
        </ul>,
      )
    } else if (currentElement.length > 0) {
      if (inCodeBlock) {
        elements.push(
          <pre key="final-code" className="bg-gray-900 border border-green-500/20 rounded-lg p-4 overflow-x-auto mb-4">
            <code className="text-green-300 text-sm font-mono">{currentElement.join("\n")}</code>
          </pre>,
        )
      } else {
        elements.push(
          <p
            key="final-p"
            className="mb-4 text-lg leading-relaxed text-gray-100"
            dangerouslySetInnerHTML={{ __html: parseInlineFormatting(currentElement.join(" ")) }}
          />,
        )
      }
    }

    return <div className="prose prose-invert prose-lg max-w-none">{elements}</div>
  } catch (error) {
    console.error("Markdown rendering error:", error)
    return <p className="text-lg leading-relaxed text-gray-100">{content}</p>
  }
}

function App() {
  const [messages, setMessages] = useState([])
  const [userInput, setUserInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!userInput.trim()) return

    console.log("Submitting message:", userInput)
    setError(null)

    const userMessage = {
      id: Date.now().toString(),
      content: userInput,
      role: "user",
    }

    setMessages((prev) => [...prev, userMessage])
    setUserInput("")
    setIsLoading(true)

    try {
      console.log("Making API call...")
      const response = await fetch("http://127.0.0.1:8080/api/home", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userInput }),
      })

      console.log("Response status:", response.status)

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      console.log("API Response:", data)

      // Handle different response formats
      let messageContent = ""
      if (typeof data === "string") {
        messageContent = data
      } else if (data.message) {
        messageContent = data.message
      } else if (data.response) {
        messageContent = data.response
      } else if (data.content) {
        messageContent = data.content
      } else {
        messageContent = JSON.stringify(data)
      }

      const assistantMessage = {
        id: (Date.now() + 1).toString(),
        content: messageContent,
        role: "assistant",
      }

      console.log("Adding assistant message:", assistantMessage)
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("API Error:", error)
      setError(error.message)

      const errorMessage = {
        id: (Date.now() + 1).toString(),
        content: `Sorry, I encountered an error: ${error.message}. Please try again.`,
        role: "assistant",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
      console.log("Request completed")
    }
  }

  const handleQuickAction = (action) => {
    setUserInput(action)
  }

  const quickActions = [
    { label: "Generate Code", icon: Code, prompt: "Help me generate code " },
    { label: "Have Fun", icon: Smile, prompt: "Tell me a joke about " },
    { label: "Mental Health", icon: Heart, prompt: "I want to talk about " },
  ]

  return (
    <div className="min-h-screen w-full bg-gradient-to-br from-black via-gray-950 to-black text-white relative overflow-hidden">
      {/* Enhanced Neon glow effects */}
      <div className="absolute inset-0 bg-gradient-to-r from-green-500/3 via-transparent to-green-500/3"></div>
      <div className="absolute top-0 left-1/4 w-96 h-96 bg-green-500/15 rounded-full blur-3xl animate-pulse"></div>
      <div
        className="absolute bottom-0 right-1/4 w-96 h-96 bg-green-400/15 rounded-full blur-3xl animate-pulse"
        style={{ animationDelay: "1s" }}
      ></div>
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-green-500/5 rounded-full blur-3xl"></div>

      {/* Neon grid overlay */}
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: `
          linear-gradient(rgba(34, 197, 94, 0.1) 1px, transparent 1px),
          linear-gradient(90deg, rgba(34, 197, 94, 0.1) 1px, transparent 1px)
        `,
          backgroundSize: "50px 50px",
        }}
      ></div>

      {/* Header */}
      <div className="border-b border-green-500/20 bg-black/60 backdrop-blur-sm relative z-10 w-full">
        <div className="w-full px-6 py-5">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-green-500 flex items-center justify-center shadow-lg shadow-green-500/25">
              <Zap className="w-6 h-6 text-black" />
            </div>
            <div className="flex items-center gap-3">
              <h1 className="text-2xl font-bold bg-gradient-to-r from-green-400 via-green-300 to-green-500 bg-clip-text text-transparent drop-shadow-lg">
                ChadGPT
              </h1>
              <span className="px-2 py-1 text-xs font-semibold bg-green-500/20 border border-green-400/30 rounded-full text-green-300 backdrop-blur-sm shadow-sm">
                BETA
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="w-full px-6 py-2">
          <div className="max-w-4xl mx-auto">
            <div className="bg-red-900/20 border border-red-500/30 rounded-lg p-3 text-red-300">Error: {error}</div>
          </div>
        </div>
      )}

      {/* Main Chat Area */}
      <div className="w-full px-6 py-6 flex flex-col h-[calc(100vh-80px)] relative z-10">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto space-y-6 mb-6 w-full">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center">
              <div className="w-20 h-20 rounded-full bg-gradient-to-r from-green-400 to-green-500 flex items-center justify-center mb-6 shadow-2xl shadow-green-500/30 hover:shadow-green-500/40 transition-shadow duration-500">
                <Zap className="w-10 h-10 text-black" />
              </div>
               <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-green-400 via-green-300 to-green-500 bg-clip-text text-transparent">
                Wassup, Chad?
              </h2>
              <p className="text-gray-300 max-w-md text-xl">
                Not your mid 5/10 Chatbot, that only talks. <br /> This a 10/10 AI Agent, that get things done
              </p>
            </div>
          ) : (
            <div className="max-w-4xl mx-auto w-full">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex gap-4 mb-6 ${message.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  {message.role === "assistant" && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-green-500 flex items-center justify-center flex-shrink-0 shadow-lg shadow-green-500/25 mt-1">
                      <Zap className="w-5 h-5 text-black" />
                    </div>
                  )}

                  <div className={`max-w-[75%] ${message.role === "user" ? "order-1" : ""}`}>
                    {message.role === "user" ? (
                      <div className="relative bg-gradient-to-r from-green-600 to-green-500 p-4 rounded-2xl shadow-lg shadow-green-500/20 ">
                        <p className="text-white text-lg leading-relaxed font-medium">{message.content}</p>
                      </div>
                    ) : (
                      <div className="text-gray-100 text-lg leading-relaxed">
                        <SimpleMarkdown content={message.content} />
                      </div>
                    )}
                  </div>

                  {message.role === "user" && (
                    <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-300 to-green-400 flex items-center justify-center flex-shrink-0 shadow-lg shadow-green-500/25 mt-1 order-2">
                      <User className="w-5 h-5 text-black" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {isLoading && (
            <div className="max-w-4xl mx-auto w-full">
              <div className="flex gap-4 justify-start">
                <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-400 to-green-500 flex items-center justify-center flex-shrink-0 shadow-lg shadow-green-500/25">
                  <Zap className="w-5 h-5 text-black" />
                </div>
                <div className="flex space-x-1 mt-3">
                  <div className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-sm shadow-green-400/50"></div>
                  <div
                    className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-sm shadow-green-400/50"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-3 h-3 bg-green-400 rounded-full animate-bounce shadow-sm shadow-green-400/50"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Actions - Centered */}
        {messages.length === 0 && (
          <div className="hidden md:flex justify-center mb-6">
            <div className="flex flex-wrap gap-4">
              {quickActions.map((action) => (
                <button
                  key={action.label}
                  onClick={() => handleQuickAction(action.prompt)}
                  className="bg-gray-900/60 border border-green-500/30 hover:bg-green-500/10 hover:border-green-400/50 text-green-300 hover:text-green-200 transition-all duration-300 backdrop-blur-sm shadow-lg hover:shadow-green-500/20 px-8 py-4 rounded-lg flex items-center gap-3 font-medium text-lg"
                >
                  <action.icon className="w-6 h-6" />
                  {action.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Input Form */}
        <div className="max-w-4xl mx-auto w-full">
          <form onSubmit={handleSubmit} className="flex gap-4">
            <div className="flex-1 relative">
              <input
                type="text"
                value={userInput}
                onChange={(e) => setUserInput(e.target.value)}
                placeholder="Farmaiye..."
                className="w-full bg-gray-900/60 border border-green-500/30 text-white placeholder-gray-400 focus:border-green-400 focus:ring-green-400/20 backdrop-blur-sm shadow-lg h-14 text-lg px-6 py-4 rounded-xl outline-none font-medium"
                disabled={isLoading}
              />
            </div>
            <button
              type="submit"
              disabled={isLoading || !userInput.trim()}
              className="bg-gradient-to-r from-green-500 to-green-400 hover:from-green-600 hover:to-green-500 border-none px-4 md:px-8 h-14 shadow-lg shadow-green-500/25 hover:shadow-green-500/40 transition-all duration-300 rounded-xl flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5 md:w-6 md:h-6" />
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}

export default App
