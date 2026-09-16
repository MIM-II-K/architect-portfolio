import "../../styles/Footer.css";

export default function Footer() {
  return (
    <footer className="site-footer">
      <div className="site-footer__inner">
        <p>
          © {new Date().getFullYear()} Architect
        </p>

        <p>
          Architecture · Space · Form
        </p>
      </div>
    </footer>
  );
}