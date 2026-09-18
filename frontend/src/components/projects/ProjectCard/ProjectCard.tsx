import { Link } from "react-router-dom";
import type { Project } from "../../../types/project";
import "./ProjectCard.css";

interface ProjectCardProps {
  project: Project;
}

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getFullImageUrl(url?: unknown): string {
  if (!url || typeof url !== "string") return "/placeholder.jpg";
  if (url.startsWith("http://") || url.startsWith("https://")) {
    return url;
  }
  return `${API_BASE_URL}${url.startsWith("/") ? "" : "/"}${url}`;
}

export default function ProjectCard({ project }: ProjectCardProps) {
  const rawImageUrl =
    (project as Record<string, unknown>).cover_image ||
    project.images?.[0]?.image_url ||
    (project as Record<string, unknown>).image_url;

  const mainImage = getFullImageUrl(rawImageUrl);

  return (
    <article className="project-card">
      <Link to={`/projects/${project.slug}`} className="project-card__link">
        <div className="project-card__image-wrapper">
          <img
            src={mainImage}
            alt={project.images?.[0]?.alt_text || project.title}
            loading="lazy"
            className="project-card__image"
            onError={(e) => {
              (e.target as HTMLImageElement).src = "/placeholder.jpg";
            }}
          />
          {/* Minimalist floating pill badge instead of a heavy full overlay */}
          <div className="project-card__action-badge">
            <span>Explore</span>
            <span className="project-card__arrow">→</span>
          </div>
        </div>

        <div className="project-card__meta">
          <div className="project-card__header">
            <h3 className="project-card__title">{project.title}</h3>
            <span className="project-card__year">{project.year}</span>
          </div>
          <div className="project-card__sub">
            <span className="project-card__category">{project.category}</span>
            {project.location && (
              <>
                <span className="project-card__dot">•</span>
                <span className="project-card__location">{project.location}</span>
              </>
            )}
          </div>
        </div>
      </Link>
    </article>
  );
}