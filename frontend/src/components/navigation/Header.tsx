import { Menu, X } from "lucide-react";
import { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";

import "./Header.css";

export default function Header() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const closeMenu = () => {
    setMenuOpen(false);
    document.body.style.overflow = "auto";
  };

  const toggleMenu = () => {
    const nextState = !menuOpen;
    setMenuOpen(nextState);
    document.body.style.overflow = nextState ? "hidden" : "auto";
  };

  return (
    <header
      className={`site-header ${isScrolled ? "is-scrolled" : ""} ${
        menuOpen ? "is-open" : ""
      }`}
    >
      <div className="site-header__inner">
        <NavLink to="/" className="site-header__brand" onClick={closeMenu}>
          <span className="site-header__brand-name">STUDIO ARCH</span>
          <span className="site-header__brand-loc">Zurich &bull; Oslo</span>
        </NavLink>

        {/* Desktop Navigation */}
        <nav className="site-header__nav" aria-label="Main navigation">
          <NavLink to="/" className="site-header__link" onClick={closeMenu}>
            Home
          </NavLink>
          <NavLink to="/projects" className="site-header__link" onClick={closeMenu}>
            Projects
          </NavLink>
          <NavLink to="/about" className="site-header__link" onClick={closeMenu}>
            About
          </NavLink>
          <NavLink to="/contact" className="site-header__link" onClick={closeMenu}>
            Contact
          </NavLink>
        </nav>

        {/* Artistic Mobile Toggle Button */}
        <button
          type="button"
          className="site-header__toggle"
          onClick={toggleMenu}
          aria-label={menuOpen ? "Close navigation" : "Open navigation"}
          aria-expanded={menuOpen}
        >
          <div className="site-header__toggle-icon">
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </div>
        </button>
      </div>

      {/* Cinematic Artistic Mobile Nav Overlay */}
      <div className="mobile-nav" aria-label="Mobile navigation">
        <div className="mobile-nav__container">
          <div className="mobile-nav__header-tracker">
            <span>Navigation Index</span>
            <span>[ 04 ]</span>
          </div>

          <div className="mobile-nav__list">
            <NavLink to="/" className="mobile-nav__item" onClick={closeMenu}>
              <span className="mobile-nav__num">01</span>
              <span className="mobile-nav__text">Home</span>
            </NavLink>
            <NavLink to="/projects" className="mobile-nav__item" onClick={closeMenu}>
              <span className="mobile-nav__num">02</span>
              <span className="mobile-nav__text">Projects</span>
            </NavLink>
            <NavLink to="/about" className="mobile-nav__item" onClick={closeMenu}>
              <span className="mobile-nav__num">03</span>
              <span className="mobile-nav__text">About Studio</span>
            </NavLink>
            <NavLink to="/contact" className="mobile-nav__item" onClick={closeMenu}>
              <span className="mobile-nav__num">04</span>
              <span className="mobile-nav__text">Contact</span>
            </NavLink>
          </div>

          <div className="mobile-nav__footer">
            <div className="mobile-nav__meta">
              <span className="mobile-nav__meta-title">Inquiries</span>
              <a href="mailto:hello@studioarch.com">hello@studioarch.com</a>
            </div>
            <div className="mobile-nav__meta">
              <span className="mobile-nav__meta-title">Office</span>
              <p>Bahnhofstrasse 10, Zurich</p>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}