import { useState } from "react"
import "./App.css"
import AboutUs from "./AboutUs"
import ContactUs from "./ContactUs"
import GetStarted from "./GetStarted"

function App() {
  const [currentPage, setCurrentPage] = useState("home")

  const renderPage = () => {
    switch (currentPage) {
      case "about":
        return <AboutUs />
      case "contact":
        return <ContactUs />
      case "get-started":
        return <GetStarted />
      default:
        return (
          <main className="main-content">
            <h1>
              OOPS! <span className="highlight">I DIDNT STUDY</span>
            </h1>
            <h2>BUT YOU CAN NOW!</h2>

            <button className="get-started" onClick={() => setCurrentPage("get-started")}>
              Get Started
            </button>

            <div className="features">
              <div className="feature-card pink">
                <h3>Generate Your Panic Notes</h3>
              </div>
              <div className="feature-card purple">
                <h3>Ask CramBot Anything</h3>
              </div>
              <div className="feature-card purple-light">
                <h3>Quizard</h3>
              </div>
            </div>
          </main>
        )
    }
  }

  return (
    <div className="app">
      <header className="header">
        <div className="logo">OOPS! I DIDNT STUDY</div>
        <div className="header-icons">
          <a href="https://github.com" className="icon-link">
            <img src="/github.svg" alt="GitHub" className="icon" />
          </a>
          <button className="account-icon">
            <img src="/user.svg" alt="Account" className="icon" />
          </button>
        </div>
      </header>

      <div className="container">
        <nav className="sidebar">
          <ul>
            <li className={currentPage === "home" ? "active" : ""} onClick={() => setCurrentPage("home")}>
              HOME
            </li>
            <li className={currentPage === "about" ? "active" : ""} onClick={() => setCurrentPage("about")}>
              ABOUT US
            </li>
            <li className={currentPage === "contact" ? "active" : ""} onClick={() => setCurrentPage("contact")}>
              CONTACT US
            </li>
          </ul>
        </nav>

        {renderPage()}
      </div>
    </div>
  )
}

export default App

