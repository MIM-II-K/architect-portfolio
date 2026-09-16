import { NavLink } from "react-router-dom";

const navigation = [
  { label: "Home", to: "/" },
  { label: "About", to: "/about" },
  { label: "Projects", to: "/projects" },
  { label: "Contact", to: "/contact" },
];

function Header() {
  return (
    <header className="site-header">
      <div className="container site-header__inner">
        <NavLink to="/" className="site-header__logo">
          MAEYRUNG
        </NavLink>

        <nav
          className="site-header__nav"
          aria-label="Main navigation"
        >
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `site-header__link ${
                  isActive ? "site-header__link--active" : ""
                }`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Header;