import { useState } from "react"

function Quizard({ onBack }) {
  const [currentQuestion, setCurrentQuestion] = useState(1)
  const [selectedOption, setSelectedOption] = useState("")
  const totalQuestions = 12

  const handleSubmit = (e) => {
    e.preventDefault()
    // Handle answer submission
    console.log("Submitted answer:", selectedOption)
  }

  const handleNext = () => {
    if (currentQuestion < totalQuestions) {
      setCurrentQuestion((prev) => prev + 1)
      setSelectedOption("")
    }
  }

  const handleQuestionSelect = (questionNumber) => {
    setCurrentQuestion(questionNumber)
    setSelectedOption("")
  }

  return (
    <div className="main-content">
      <div className="quizard-card">
        <div className="question-navigation">
          {Array.from({ length: totalQuestions }, (_, i) => i + 1).map((num) => (
            <button
              key={num}
              onClick={() => handleQuestionSelect(num)}
              className={`question-nav-button ${currentQuestion === num ? "active" : ""}`}
            >
              {num}
            </button>
          ))}
        </div>

        <form onSubmit={handleSubmit} className="quiz-form">
          <div className="question-content">
            <h3 className="question-text">{currentQuestion}.Question Statement</h3>

            <div className="options-list">
              {["Option 1", "Option 2", "Option 3", "Option 4"].map((option, index) => (
                <label key={index} className="option-label">
                  <input
                    type="radio"
                    name="quiz-option"
                    value={option}
                    checked={selectedOption === option}
                    onChange={(e) => setSelectedOption(e.target.value)}
                    className="option-input"
                  />
                  <span className="option-text">{option}</span>
                </label>
              ))}
            </div>

            <button type="submit" className="submit-button">
              Submit
            </button>
          </div>
        </form>

        <div className="quiz-navigation">
          <button onClick={handleNext} className="nav-button" disabled={currentQuestion === totalQuestions}>
            Next
          </button>
          <button onClick={onBack} className="nav-button">
            End
          </button>
        </div>
      </div>
    </div>
  )
}

export default Quizard

