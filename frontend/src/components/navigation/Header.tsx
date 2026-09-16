import { Menu, X } from "lucide-react";
import { useState } from "react";
import { NavLink } from "react-router-dom";

import "../../styles/Header.css";

export default function Header() {
  const [menuOpen, setMenuOpen] =
    useState(false);

  const closeMenu = () => {
    setMenuOpen(false);
  };

  return (
    <header className="site-header">
      <div className="site-header__inner">
        <NavLink
          to="/"
          className="site-header__logo"
          onClick={closeMenu}
        >
          MAEYRUNG
        </NavLink>

        <nav
          className={`site-header__nav ${
            menuOpen
              ? "site-header__nav--open"
              : ""
          }`}
          aria-label="Main navigation"
        >
          <NavLink
            to="/"
            onClick={closeMenu}
          >
            Home
          </NavLink>

          <NavLink
            to="/projects"
            onClick={closeMenu}
          >
            Projects
          </NavLink>

          <NavLink
            to="/about"
            onClick={closeMenu}
          >
            About
          </NavLink>

          <NavLink
            to="/contact"
            onClick={closeMenu}
          >
            Contact
          </NavLink>
        </nav>

        <button
          type="button"
          className="site-header__menu"
          onClick={() =>
            setMenuOpen(
              (open) => !open,
            )
          }
          aria-label={
            menuOpen
              ? "Close navigation"
              : "Open navigation"
          }
          aria-expanded={menuOpen}
        >
          {menuOpen ? (
            <X size={24} />
          ) : (
            <Menu size={24} />
          )}
        </button>
      </div>
    </header>
  );
}