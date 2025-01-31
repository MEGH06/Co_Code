import { Download } from "lucide-react"

function PanicNotes({ onBack }) {
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
    </div>
  )
}

export default PanicNotes

