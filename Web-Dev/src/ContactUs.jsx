import { Phone, Mail, MapPin } from "lucide-react"

function ContactUs() {
  return (
    <div className="main-content">
      <div className="contact-card">
        <h2 className="contact-title">CONTACT US:</h2>
        <div className="contact-info">
          <div className="contact-item">
            <Phone className="contact-icon" />
            <span>+91 9326370332</span>
          </div>
          <div className="contact-item">
            <Mail className="contact-icon" />
            <span>kruttikahebbar@gmail.com</span>
          </div>
          <div className="contact-item">
            <MapPin className="contact-icon" />
            <span>Mumbai, Maharashtra, India</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ContactUs

