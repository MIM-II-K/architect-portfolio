import "./About.css";

const PHILOSOPHIES = [
  {
    number: "01",
    title: "Material Honesty",
    description:
      "We prioritize raw stone, exposed timber, and structural concrete, allowing inherent textures and ageing processes to define spatial character.",
  },
  {
    number: "02",
    title: "Light & Proportion",
    description:
      "Architectural form serves as a vessel for natural daylight. We design structural openings to track light across seasonal arcs.",
  },
  {
    number: "03",
    title: "Contextual Permanence",
    description:
      "Every building responds to local topography, climate, and cultural heritage, aiming for timeless integration with its surrounding landscape.",
  },
];

const TEAM = [
  { name: "Elena Vance", role: "Principal Architect", location: "Zurich" },
  { name: "Soren Lindqvist", role: "Design Director", location: "Oslo" },
  { name: "Kaito Takahashi", role: "Lead Spatial Designer", location: "Kyoto" },
];

export default function About() {
  return (
    <div className="about-page animate-fade-up">
      <div className="container">
        <header className="about-header">
          <p className="mono-eyebrow">About // Studio Arch</p>
          <h1 className="about-title">
            Architectural clarity rooted in spatial rigor and material integrity.
          </h1>
        </header>

        {/* Studio Narrative */}
        <section className="about-intro-grid">
          <div className="intro-label">
            <span className="mono-eyebrow">Our Approach</span>
          </div>
          <div className="intro-text">
            <p>
              Founded in 2024, Studio Arch operates at the intersection of minimalist residential architecture, cultural pavilions, and urban adaptive reuse. We strip away unnecessary ornament to highlight spatial flow, volume, and natural light.
            </p>
            <p>
              Collaborating with private clients, public institutions, and craftspeople worldwide, our process relies on meticulous physical prototyping and digital site analysis.
            </p>
          </div>
        </section>

        {/* Philosophy Grid */}
        <section className="philosophy-section">
          <p className="mono-eyebrow section-title">Core Principles</p>
          <div className="philosophy-grid">
            {PHILOSOPHIES.map((item, index) => (
              <div key={item.number} className={`philosophy-card animate-fade-up delay-${index + 1}`}>
                <span className="philosophy-num">{item.number}</span>
                <h3 className="philosophy-heading">{item.title}</h3>
                <p className="philosophy-desc">{item.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Team Leadership */}
        <section className="team-section">
          <p className="mono-eyebrow section-title">Studio Leadership</p>
          <div className="team-list">
            {TEAM.map((member) => (
              <div key={member.name} className="team-row">
                <span className="team-name">{member.name}</span>
                <span className="team-role">{member.role}</span>
                <span className="team-location">{member.location}</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}