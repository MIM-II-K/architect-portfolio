import React, { useState } from "react";
import { submitContactForm, type ContactFormData } from "../../services/contactService";
import ErrorMessage from "../../components/common/ErrorMessage";
import "../../styles/Contact.css";

export default function Contact() {
  const [formData, setFormData] = useState<ContactFormData>({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setSuccessMessage(null);

    try {
      const response = await submitContactForm(formData);
      setSuccessMessage(response.message || "Thank you. Your message has been received.");
      setFormData({ name: "", email: "", subject: "", message: "" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="contact-page animate-fade-up">
      <div className="container">
        <header className="contact-header">
          <p className="mono-eyebrow">Contact // Studio Arch</p>
          <h1 className="contact-title">Start a Conversation</h1>
        </header>

        <div className="contact-grid">
          {/* Sidebar / Info Column */}
          <div className="contact-info">
            <p className="contact-description">
              We are open to new architectural commissions, urban research collaborations, and spatial design inquiries globally.
            </p>

            <div className="info-group">
              <span className="info-label">Direct Email</span>
              <a href="mailto:studio@arch-studio.com" className="info-link">
                studio@arch-studio.com
              </a>
            </div>

            <div className="info-group">
              <span className="info-label">Office Address</span>
              <address className="info-address">
                Central Plaza, 4th Floor<br />
                8001 Zurich, Switzerland
              </address>
            </div>

            <div className="info-group">
              <span className="info-label">Socials</span>
              <div className="social-links">
                <a href="https://instagram.com" target="_blank" rel="noreferrer">Instagram</a>
                <span>/</span>
                <a href="https://linkedin.com" target="_blank" rel="noreferrer">LinkedIn</a>
                <span>/</span>
                <a href="https://archdaily.com" target="_blank" rel="noreferrer">ArchDaily</a>
              </div>
            </div>
          </div>

          {/* Form Column */}
          <div className="contact-form-wrapper">
            {successMessage ? (
              <div className="success-banner">
                <p className="success-title">Message Sent</p>
                <p>{successMessage}</p>
                <button
                  onClick={() => setSuccessMessage(null)}
                  className="reset-btn"
                >
                  Send another message
                </button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="contact-form">
                {error && <ErrorMessage message={error} />}

                <div className="form-group">
                  <label htmlFor="name" className="form-label">Name *</label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    placeholder="Jane Doe"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="email" className="form-label">Email Address *</label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="jane@example.com"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="subject" className="form-label">Project Type / Subject</label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    placeholder="New Residence / Pavilion / Commission"
                    className="form-input"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="message" className="form-label">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    required
                    rows={5}
                    value={formData.message}
                    onChange={handleChange}
                    placeholder="Tell us about the scope, location, and timeline of your project..."
                    className="form-input form-textarea"
                  />
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="submit-btn"
                >
                  {loading ? "Sending..." : "Submit Inquiry →"}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}