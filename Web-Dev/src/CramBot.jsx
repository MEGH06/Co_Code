import { useState } from "react"
import { Send } from "lucide-react"

function CramBot({ onBack }) {
  const [message, setMessage] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle message submission here
    console.log("Message sent:", message)
  }

  return (
    <div className="main-content">
      <div className="crambot-card">
        <h2>
          This is your time to <span className="underline">Cram!</span>
        </h2>

        <form onSubmit={handleSubmit} className="crambot-form">
          <div className="input-container">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Message CramBot"
              className="crambot-input"
            />
            <button type="submit" className="send-button">
              <Send className="send-icon" />
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CramBot

