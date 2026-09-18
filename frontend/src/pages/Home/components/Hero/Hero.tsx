import { Link } from "react-router-dom";
import "./Hero.css";

export default function Hero() {
  return (
    <section className="hero-section">
      <div className="hero-glow" aria-hidden="true" />
      
      <div className="container hero-container">
        <div className="hero-header">
          <span className="mono-eyebrow">Architectural Practice — Est. 2024</span>
        </div>

        <h1 className="hero-title">
          Sculpting space through structural clarity & material honesty.
        </h1>

        <div className="hero-footer">
          <p className="hero-subtext">
            Specializing in high-end residential, cultural pavilions, and adaptive reuse architecture worldwide.
          </p>
          
          <Link to="/projects" className="hero-cta">
            <span>Explore Portfolio</span>
            <span className="hero-cta-arrow">→</span>
          </Link>
        </div>
      </div>
    </section>
  );
}