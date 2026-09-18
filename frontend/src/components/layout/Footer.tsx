import { Link } from "react-router-dom";
import "../../styles/Footer.css";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="container site-footer__inner">
        <div className="footer-col branding">
          <Link to="/" className="footer-logo">
            STUDIO ARCH<span className="dot">.</span>
          </Link>
          <p className="footer-tagline">
            Architecture, spatial research & material design.
          </p>
        </div>

        <div className="footer-col nav">
          <span className="footer-heading">Navigation</span>
          <Link to="/projects">Projects</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
        </div>

        <div className="footer-col location">
          <span className="footer-heading">Studio</span>
          <p>Zurich — Switzerland</p>
          <p>Oslo — Norway</p>
        </div>

        <div className="footer-col copyright">
          <span className="footer-heading">Legal</span>
          <p>© {currentYear} Studio Arch.</p>
          <p>All Rights Reserved.</p>
        </div>
      </div>
    </footer>
  );
}