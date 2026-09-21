import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import PageContainer from "../../components/layout/PageContainer";
import { getProjectBySlug, getProjects, getProjectImages } from "../../services/api"; // Added getProjectImages if available
import type { Project, ProjectImage } from "../../types/project";
import "./ProjectDetail.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getFullImageUrl(url?: unknown): string {
  if (!url || typeof url !== "string") return "/placeholder.jpg";
  if (url.startsWith("http://") || url.startsWith("https://")) return url;
  return `${API_BASE_URL}${url.startsWith("/") ? "" : "/"}${url}`;
}

function ProjectDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [extraImages, setExtraImages] = useState<ProjectImage[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      if (!slug) return;
      try {
        setLoading(true);
        setError(null);
        
        const [projectData, projectsData] = await Promise.all([
          getProjectBySlug(slug),
          getProjects(),
        ]);
        
        setProject(projectData);
        setProjects(Array.isArray(projectsData) ? projectsData : []);

        // If images aren't embedded directly in projectData, fetch them explicitly
        if (!projectData.images || projectData.images.length === 0) {
          try {
            const imagesRes = await getProjectImages(projectData.id);
            const fetched = Array.isArray(imagesRes) ? imagesRes : imagesRes?.images || [];
            setExtraImages(fetched);
          } catch {
            // Fallback gracefully if separate endpoint is unavailable
            setExtraImages([]);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load project");
      } finally {
        setLoading(false);
      }
    }
    fetchData();
    window.scrollTo(0, 0);
  }, [slug]);

  if (loading) {
    return (
      <PageContainer>
        <div className="project-detail__loading mono-eyebrow">Loading architectural archive...</div>
      </PageContainer>
    );
  }

  if (error || !project) {
    return (
      <PageContainer>
        <main className="project-detail project-detail--not-found animate-fade-up">
          <p className="mono-eyebrow">Error // 404</p>
          <h1 className="project-detail__title">Project not found</h1>
          <p className="project-detail__not-found-text">
            The project you are looking for does not exist or has been relocated.
          </p>
          <Link to="/projects" className="project-detail__back-link">
            ← Back to Index
          </Link>
        </main>
      </PageContainer>
    );
  }

  const currentIndex = projects.findIndex((item) => item.slug === project.slug);
  const previousProject = currentIndex > 0 ? projects[currentIndex - 1] : null;
  const nextProject = currentIndex >= 0 && currentIndex < projects.length - 1 ? projects[currentIndex + 1] : null;

  // Build full gallery: Cover image first + all additional project images
  const allImages: Array<{ id: string; image_url: string; alt_text?: string; caption?: string }> = [];

  // Add cover image if present
  if (project.cover_image) {
    allImages.push({
      id: "cover",
      image_url: project.cover_image,
      alt_text: `${project.title} Cover`,
    });
  }

  // Combine images attached directly or fetched separately
  const additionalImages = (project.images && project.images.length > 0) ? project.images : extraImages;

  additionalImages.forEach((img: any, idx: number) => {
    const rawUrl = img.image_url || img.url;
    // Prevent duplicating the cover image if it's also present in project.images
    if (rawUrl && rawUrl !== project.cover_image) {
      allImages.push({
        id: img.id || `img-${idx}`,
        image_url: rawUrl,
        alt_text: img.alt_text || `${project.title} image ${idx + 1}`,
        caption: img.caption,
      });
    }
  });

  return (
    <PageContainer>
      <main className="project-detail animate-fade-up">
        <header className="project-detail__header">
          <p className="mono-eyebrow">Index // {project.category}</p>
          <h1 className="project-detail__title">{project.title}</h1>
          <div className="project-detail__meta">
            {project.location && <span>{project.location}</span>}
            <span>{project.year}</span>
          </div>
        </header>

        {/* Cinematic Gallery Section */}
        <section className="project-detail__gallery">
          {allImages.length > 0 ? (
            allImages.map((image, index) => {
              const imageUrl = getFullImageUrl(image.image_url);

              return (
                <figure
                  key={image.id || `${imageUrl}-${index}`}
                  className={`project-detail__image-wrapper project-detail__image-wrapper--${(index % 4) + 1}`}
                >
                  <img
                    className="project-detail__image"
                    src={imageUrl}
                    alt={image.alt_text || `${project.title} image ${index + 1}`}
                    loading="lazy"
                    onError={(e) => {
                      (e.target as HTMLImageElement).src = "/placeholder.jpg";
                    }}
                  />
                  {image.caption && (
                    <figcaption className="project-detail__image-caption">
                      {image.caption}
                    </figcaption>
                  )}
                </figure>
              );
            })
          ) : (
            <figure className="project-detail__image-wrapper project-detail__image-wrapper--1">
              <img className="project-detail__image" src="/placeholder.jpg" alt={project.title} />
            </figure>
          )}
        </section>

        {/* Project Description */}
        <section className="project-detail__information">
          <div className="mono-eyebrow">Overview</div>
          <div className="project-detail__information-content">
            <h2>{project.title}</h2>
            {project.description && <p>{project.description}</p>}
          </div>
        </section>

        {/* Metadata Details */}
        <section className="project-detail__metadata">
          <div className="mono-eyebrow">Specifications</div>
          <dl className="project-detail__metadata-list">
            <div>
              <dt>Category</dt>
              <dd>{project.category}</dd>
            </div>
            <div>
              <dt>Location</dt>
              <dd>{project.location || "—"}</dd>
            </div>
            <div>
              <dt>Year</dt>
              <dd>{project.year}</dd>
            </div>
          </dl>
        </section>

        {/* Project Navigation */}
        <nav className="project-detail__navigation" aria-label="Project navigation">
          <div>
            {previousProject && (
              <Link to={`/projects/${previousProject.slug}`} className="project-detail__navigation-link">
                <span className="mono-eyebrow">← Previous Work</span>
                <strong>{previousProject.title}</strong>
              </Link>
            )}
          </div>
          <div>
            {nextProject && (
              <Link to={`/projects/${nextProject.slug}`} className="project-detail__navigation-link">
                <span className="mono-eyebrow">Next Work →</span>
                <strong>{nextProject.title}</strong>
              </Link>
            )}
          </div>
        </nav>
      </main>
    </PageContainer>
  );
}

export default ProjectDetail;