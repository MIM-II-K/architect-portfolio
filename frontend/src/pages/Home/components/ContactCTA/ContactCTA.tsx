import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import "./ContactCTA.css";

export default function ContactCTA() {
  return (
    <section className="contact-cta">
      <div className="contact-cta__label">
        <span>03</span>
        <span>Start a conversation</span>
      </div>

      <div className="contact-cta__content">
        <h2>
          Have a project <br />
          <span className="contact-cta__highlight">in mind?</span>
        </h2>

        <Link to="/contact" className="contact-cta__link">
          <span>Get in touch</span>
          <ArrowUpRight size={18} className="contact-cta__arrow" />
        </Link>
      </div>
    </section>
  );
}