import { useState } from "react"
import { FolderUp, Folder, Check } from "lucide-react"
import PanicNotes from "./PanicNotes"
import CramBot from "./CramBot"
import Quizard from "./Quizard"

function GetStarted() {
  const [dragActive, setDragActive] = useState(false)
  const [files, setFiles] = useState([])
  const [isUploading, setIsUploading] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadComplete, setUploadComplete] = useState(false)
  const [currentView, setCurrentView] = useState("upload") // 'upload', 'panic-notes', 'crambot', 'quizard'

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }

  const simulateUpload = () => {
    setIsUploading(true)
    setUploadProgress(0)
    setUploadComplete(false)

    const interval = setInterval(() => {
      setUploadProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setTimeout(() => {
            setIsUploading(false)
            setUploadComplete(true)
          }, 500)
          return 100
        }
        return prev + 2
      })
    }, 50)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFiles([...e.dataTransfer.files])
      simulateUpload()
    }
  }

  const handleChange = (e) => {
    e.preventDefault()
    if (e.target.files && e.target.files[0]) {
      setFiles([...e.target.files])
      simulateUpload()
    }
  }

  const renderUploadStatus = () => {
    if (isUploading) {
      return (
        <div className="progress-container">
          <div className="progress-header">
            <Folder className="folder-icon" />
            <span className="filename">Folder Name</span>
            <span className="percentage">{uploadProgress}%</span>
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: `${uploadProgress}%` }} />
          </div>
        </div>
      )
    }

    if (uploadComplete) {
      return (
        <div className="progress-container completed">
          <div className="progress-header">
            <Folder className="folder-icon" />
            <span className="filename">Folder Name</span>
            <Check className="check-icon" />
          </div>
          <div className="progress-bar">
            <div className="progress-fill" style={{ width: "100%" }} />
          </div>
        </div>
      )
    }

    return null
  }

  if (currentView === "panic-notes") {
    return <PanicNotes onBack={() => setCurrentView("upload")} />
  }

  if (currentView === "crambot") {
    return <CramBot onBack={() => setCurrentView("upload")} />
  }

  if (currentView === "quizard") {
    return <Quizard onBack={() => setCurrentView("upload")} />
  }

  return (
    <div className="main-content get-started-page">
      {isUploading || uploadComplete ? (
        <div className="upload-progress">
          <h2>Uploaded Folder</h2>
          {renderUploadStatus()}
        </div>
      ) : (
        <div
          className={`upload-area ${dragActive ? "drag-active" : ""}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <FolderUp className="upload-icon" />
          <p>drag and drop file here</p>
          <p className="or-text">-OR-</p>
          <label className="browse-button">
            Browse Files
            <input type="file" className="hidden-input" multiple onChange={handleChange} />
          </label>
        </div>
      )}

      <div className="features">
        <div
          className={`feature-card pink ${uploadComplete ? "clickable" : "disabled"}`}
          onClick={uploadComplete ? () => setCurrentView("panic-notes") : undefined}
        >
          <h3>Generate Your Panic Notes</h3>
        </div>
        <div
          className={`feature-card purple ${uploadComplete ? "clickable" : "disabled"}`}
          onClick={uploadComplete ? () => setCurrentView("crambot") : undefined}
        >
          <h3>Ask CramBot Anything</h3>
        </div>
        <div
          className={`feature-card purple-light ${uploadComplete ? "clickable" : "disabled"}`}
          onClick={uploadComplete ? () => setCurrentView("quizard") : undefined}
        >
          <h3>Quizard</h3>
        </div>
      </div>
    </div>
  )
}

export default GetStarted

