import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import "./StudioIntro.css";

export default function StudioIntro() {
  return (
    <section className="studio-intro">
      <div className="studio-intro__label">
        <span className="studio-intro__number">01</span>
        <span className="studio-intro__title">Studio</span>
      </div>

      <div className="studio-intro__content">
        <h2>
          Architecture begins with{" "}
          <span className="studio-intro__highlight">understanding place.</span>
        </h2>

        <div className="studio-intro__bottom">
          <p>
            We approach every project through context, material, light, and the
            people who inhabit the space. The result is architecture that aims to
            feel considered rather than imposed.
          </p>

          <Link to="/about" className="studio-intro__link">
            <span>About the studio</span>
            <ArrowUpRight size={16} className="studio-intro__arrow" />
          </Link>
        </div>
      </div>
    </section>
  );
}