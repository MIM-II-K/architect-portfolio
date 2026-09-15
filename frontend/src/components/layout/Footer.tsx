function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="container site-footer__inner">
        <p>© {currentYear} Architect Studio</p>

        <p>Architecture · Interiors · Design</p>
      </div>
    </footer>
  );
}

export default Footer;