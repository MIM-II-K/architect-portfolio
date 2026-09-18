import { useEffect, useState } from "react";
import type { Project } from "../../types/project";
import { getProjects } from "../../services/projectService";

import Hero from "./components/Hero/Hero";
import FeaturedProjects from "./components/FeaturedProjects/FeaturedProjects";
import StudioIntro from "./components/StudioIntro/StudioIntro";
import SelectedProject from "./components/SelectedProject/SelectedProject";
import ContactCTA from "./components/ContactCTA/ContactCTA";

import "../../styles/Home.css";

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadProjects() {
      try {
        const response = await getProjects({ page_size: 6 });
        setProjects(response.projects);
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load projects."
        );
      } finally {
        setLoading(false);
      }
    }

    loadProjects();
  }, []);

  const spotlightProject = projects.find((project) => project.featured);

  return (
    <div className="home-page">
      {/* Hero section loads immediately for instant visual feedback */}
      <Hero />

      {/* Studio introduction sits independently of API data */}
      <StudioIntro />

      {/* Projects section with graceful inline loading/error handling */}
      <section className="home-projects-section">
        {loading && (
          <div className="home-loading-state">
            <div className="home-spinner" />
            <p>Curating projects...</p>
          </div>
        )}

        {error && (
          <div className="home-error-state">
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && (
          <div className="animate-fade-in">
            <FeaturedProjects projects={projects} />
            <SelectedProject project={spotlightProject} />
          </div>
        )}
      </section>

      {/* Persistent high-conversion footer CTA */}
      <ContactCTA />
    </div>
  );
}