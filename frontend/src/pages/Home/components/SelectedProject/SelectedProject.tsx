import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";

import type { Project } from "../../../../types/project";
import "./SelectedProject.css";

interface SelectedProjectProps {
  project?: Project;
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

export default function SelectedProject({
  project,
}: SelectedProjectProps) {
  if (!project) {
    return null;
  }

  const rawImageUrl =
    (project as Record<string, unknown>).cover_image ||
    project.images?.[0]?.image_url ||
    (project as Record<string, unknown>).image_url;

  const imageUrl = getFullImageUrl(rawImageUrl);

  return (
    <section className="selected-project">
      <div className="selected-project__header">
        <div>
          <span className="selected-project__eyebrow">
            02 · Project spotlight
          </span>
          <h2>{project.title}</h2>
        </div>

        <span className="selected-project__year">
          {project.year}
        </span>
      </div>

      <Link
        to={`/projects/${project.slug}`}
        className="selected-project__visual"
      >
        {imageUrl ? (
          <img
            src={imageUrl}
            alt={project.images?.[0]?.alt_text || project.title}
            loading="lazy"
            className="selected-project__img"
          />
        ) : (
          <div className="selected-project__placeholder" />
        )}

        {/* Minimalist floating glass pill button */}
        <div className="selected-project__badge">
          <span>Explore project</span>
          <ArrowUpRight size={16} className="selected-project__arrow" />
        </div>
      </Link>

      <div className="selected-project__meta">
        <span className="selected-project__category">{project.category}</span>
        {project.location && (
          <span className="selected-project__location">{project.location}</span>
        )}
      </div>
    </section>
  );
}