import { Link } from "react-router-dom";
import "./NotFound.css";

export default function NotFound() {
  return (
    <div className="not-found-page">
      <div className="container not-found-content">
        <p className="mono-eyebrow">404 — Error</p>
        <h1 className="not-found-title">Spatial Void</h1>
        <p className="not-found-desc">
          The page or project route you are looking for does not exist or has been relocated.
        </p>
        <Link to="/" className="not-found-btn">
          Return to Home →
        </Link>
      </div>
    </div>
  );
}