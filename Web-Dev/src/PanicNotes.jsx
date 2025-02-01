import { Download } from "lucide-react"

function PanicNotes({ onBack, onCramBot, onQuizard, currentView }) {
  const handleDownload = () => {
    // Implement actual download logic here
    console.log("Downloading panic notes...")
  }

  return (
    <div className="main-content">
      <div className="panic-notes-card">
        <h2>Your panic notes are ready!</h2>
        <button className="download-button" onClick={handleDownload}>
          <Download className="download-icon" />
          DOWNLOAD
        </button>
      </div>

      <div className="features">
        <div className="feature-card pink active">
        <svg fill="white" width="40" height="40" viewBox="0 0 30 30" xmlns="http://www.w3.org/2000/svg" data-name="Layer 1"><path d="M16,14H8a1,1,0,0,0,0,2h8a1,1,0,0,0,0-2Zm0-4H10a1,1,0,0,0,0,2h6a1,1,0,0,0,0-2Zm4-6H17V3a1,1,0,0,0-2,0V4H13V3a1,1,0,0,0-2,0V4H9V3A1,1,0,0,0,7,3V4H4A1,1,0,0,0,3,5V19a3,3,0,0,0,3,3H18a3,3,0,0,0,3-3V5A1,1,0,0,0,20,4ZM19,19a1,1,0,0,1-1,1H6a1,1,0,0,1-1-1V6H7V7A1,1,0,0,0,9,7V6h2V7a1,1,0,0,0,2,0V6h2V7a1,1,0,0,0,2,0V6h2Z"/></svg>
          <h3>Generate Your Panic Notes</h3>
        </div>
        <div className="feature-card purple clickable" onClick={onCramBot}>
        <svg fill="white" xmlns="http://www.w3.org/2000/svg" 
	 width="40" height="40" viewBox="0 0 100 100" enable-background="new 0 0 100 100" xml:space="preserve">
<path d="M49.6,25.8c7.2,0,13,5.8,13,13v3.3c-4.3-0.5-8.7-0.7-13-0.7c-4.3,0-8.7,0.2-13,0.7v-3.3
	C36.6,31.7,42.4,25.8,49.6,25.8z"/>
<path d="M73.2,63.8l1.3-11.4c2.9,0.5,5.1,2.9,5.1,5.6C79.6,61.2,76.7,63.8,73.2,63.8z"/>
<path d="M25.9,63.8c-3.5,0-6.4-2.6-6.4-5.8c0-2.8,2.2-5.1,5.1-5.6L25.9,63.8z"/>
<path d="M68.7,44.9c-6.6-0.7-12.9-1-19-1c-6.1,0-12.5,0.3-19,1h0c-2.2,0.2-3.8,2.2-3.5,4.3l2,19.4
	c0.2,1.8,1.6,3.3,3.5,3.5c5.6,0.7,11.3,1,17.1,1s11.5-0.3,17.1-1c1.8-0.2,3.3-1.7,3.5-3.5l2-19.4v0C72.4,47,70.9,45.1,68.7,44.9z
	 M38.6,62.5c-1.6,0-2.8-1.6-2.8-3.7s1.3-3.7,2.8-3.7s2.8,1.6,2.8,3.7S40.2,62.5,38.6,62.5z M55.3,66.6c0,0.2-0.1,0.4-0.2,0.5
	c-0.1,0.1-0.3,0.2-0.5,0.2h-9.9c-0.2,0-0.4-0.1-0.5-0.2c-0.1-0.1-0.2-0.3-0.2-0.5v-1.8c0-0.4,0.3-0.7,0.7-0.7h0.2
	c0.4,0,0.7,0.3,0.7,0.7v0.9h8.1v-0.9c0-0.4,0.3-0.7,0.7-0.7h0.2c0.4,0,0.7,0.3,0.7,0.7V66.6z M60.6,62.5c-1.6,0-2.8-1.6-2.8-3.7
	s1.3-3.7,2.8-3.7s2.8,1.6,2.8,3.7S62.2,62.5,60.6,62.5z"/>
</svg>
          <h3>Ask CramBot Anything</h3>
        </div>
        <div className="feature-card purple-light clickable" onClick={onQuizard}>
        <svg fill="white" width="30" height="30" viewBox="0 0 2500 2500" xmlns="http://www.w3.org/2000/svg">
    <path d="m1647.608 931.313-2.665 707.614-236.558 236.68h-.121l-352.475-352.476 591.819-591.818ZM792.79 1438.707l85.635 85.757-264.295 264.174-85.636-85.635 264.296-264.296Zm-176.165-176.044 85.636 85.636-352.354 352.233-85.636-85.636 352.354-352.233Zm-176.092-176.249 85.514 85.757-440.411 440.29L0 1526.947l440.533-440.533ZM1033.44 317.28 441.744 908.977 89.27 556.745l236.68-236.679 707.492-2.786Zm597.548-41.17 55.96 2.059 2.301 56.08c2.302 54.992-13.323 138.932-100.897 226.384l-42.757 42.878-184.11-184.231 42.756-42.879c86.605-86.483 172.24-102.108 226.747-100.291Zm259.45-202.037c-73.28-27.617-341.21-101.382-615.558 172.967L570.173 951.747l221.417 221.538 221.418 221.417 704.707-704.828c273.016-273.017 199.857-543.005 172.725-615.801" fill-rule="evenodd"/>
</svg>
          <h3>Quizard</h3>
        </div>
      </div>
    </div>
  )
}

export default PanicNotes

