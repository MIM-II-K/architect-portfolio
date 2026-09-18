import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import type { ProjectResponse } from "../../../../types/project";
import "./FeaturedProjects.css";

interface FeaturedProjectsProps {
  projects: ProjectResponse[];
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getFullImageUrl(url?: unknown): string {
  if (!url || typeof url !== "string") return "";

  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  return `${API_BASE_URL}${url.startsWith("/") ? "" : "/"}${url}`;
}

export default function FeaturedProjects({
  projects,
}: FeaturedProjectsProps) {
  const featuredProjects = (projects || [])
    .filter((project) => project.featured && project.published)
    .slice(0, 3);

  if (featuredProjects.length === 0) return null;

  return (
    <section className="featured-projects">
      <div className="featured-projects__header">
        <div>
          <span className="featured-projects__eyebrow">
            Selected work
          </span>
          <h2>Featured projects</h2>
        </div>

        <Link to="/projects" className="featured-projects__all">
          <span>View all work</span>
          <ArrowUpRight size={16} className="featured-projects__arrow" />
        </Link>
      </div>

      <div className="featured-projects__grid">
        {featuredProjects.map((project, index) => {
          const rawImageUrl =
            project.images?.[0]?.image_url ||
            project.cover_image ||
            "";

          const imageUrl = getFullImageUrl(rawImageUrl);
          const isLargeCard = index === 2; // The 3rd item spans full width

          return (
            <Link
              key={project.id}
              to={`/projects/${project.slug}`}
              className={`featured-project ${isLargeCard ? "featured-project--large" : ""}`}
            >
              <div className="featured-project__image-wrap">
                {imageUrl ? (
                  <img
                    src={imageUrl}
                    alt={project.images?.[0]?.alt_text || project.title}
                    loading="lazy"
                    className="featured-project__img"
                  />
                ) : (
                  <div className="featured-project__placeholder" />
                )}
                
                {/* Floating minimal category tag */}
                <div className="featured-project__tag">
                  {project.category}
                </div>
              </div>

              <div className="featured-project__info">
                <div className="featured-project__titles">
                  <h3>{project.title}</h3>
                  {project.location && (
                    <span className="featured-project__location">
                      {project.location}
                    </span>
                  )}
                </div>

                <span className="featured-project__year">{project.year}</span>
              </div>
            </Link>
          );
        })}
      </div>
    </section>
  );
}