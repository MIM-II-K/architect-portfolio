import { useEffect, useState, useCallback } from "react";
import { Link, useParams } from "react-router-dom";
import PageContainer from "../../components/layout/PageContainer";
import { getProjectBySlug, getProjects, getProjectImages } from "../../services/api";
import type { Project, ProjectImage } from "../../types/project";
import "./ProjectDetail.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

function getFullImageUrl(url?: unknown): string {
  if (!url || typeof url !== "string") return "/placeholder.jpg";
  if (url.startsWith("http://") || url.startsWith("https://")) return url;
  return `${API_BASE_URL}${url.startsWith("/") ? "" : "/"}${url}`;
}

type AspectOrientation = "landscape" | "portrait" | "square";

function ProjectDetail() {
  const { slug } = useParams<{ slug: string }>();
  const [project, setProject] = useState<Project | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [extraImages, setExtraImages] = useState<ProjectImage[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const [imageRatios, setImageRatios] = useState<Record<string, AspectOrientation>>({});
  const [activeImageIndex, setActiveImageIndex] = useState<number | null>(null);

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

        if (!projectData.images || projectData.images.length === 0) {
          try {
            const imagesRes = await getProjectImages(projectData.id);
            const fetchedList = Array.isArray(imagesRes)
              ? imagesRes
              : imagesRes?.images || [];
            setExtraImages(fetchedList);
          } catch {
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

  const handleImageLoad = (
    id: string,
    e: React.SyntheticEvent<HTMLImageElement, Event>
  ) => {
    const { naturalWidth, naturalHeight } = e.currentTarget;
    if (!naturalWidth || !naturalHeight) return;

    const ratio = naturalWidth / naturalHeight;
    let orientation: AspectOrientation = "landscape";

    if (ratio < 0.85) {
      orientation = "portrait";
    } else if (ratio >= 0.85 && ratio <= 1.15) {
      orientation = "square";
    } else {
      orientation = "landscape";
    }

    setImageRatios((prev) => ({
      ...prev,
      [id]: orientation,
    }));
  };

  const rawGalleryList =
    project?.images && project.images.length > 0 ? project.images : extraImages;

  const galleryImages: Array<{
    id: string;
    image_url?: string;
    url?: string;
    alt_text?: string;
    caption?: string;
  }> = [];

  if (project?.cover_image) {
    galleryImages.push({
      id: "cover-image",
      image_url: project.cover_image,
      alt_text: `${project.title} Cover`,
    });
  }

  rawGalleryList.forEach((img: any, idx: number) => {
    const rawUrl = img.image_url || img.url;
    if (rawUrl && rawUrl !== project?.cover_image) {
      galleryImages.push({
        id: img.id || `gallery-img-${idx}`,
        image_url: rawUrl,
        alt_text: img.alt_text || `${project?.title} plate ${idx + 1}`,
        caption: img.caption,
      });
    }
  });

  const handleNextImage = useCallback(() => {
    setActiveImageIndex((prev) =>
      prev !== null ? (prev + 1) % galleryImages.length : null
    );
  }, [galleryImages.length]);

  const handlePrevImage = useCallback(() => {
    setActiveImageIndex((prev) =>
      prev !== null ? (prev - 1 + galleryImages.length) % galleryImages.length : null
    );
  }, [galleryImages.length]);

  const handleCloseLightbox = useCallback(() => {
    setActiveImageIndex(null);
  }, []);

  useEffect(() => {
    if (activeImageIndex === null) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") handleCloseLightbox();
      if (e.key === "ArrowRight") handleNextImage();
      if (e.key === "ArrowLeft") handlePrevImage();
    };
    window.addEventListener("keydown", handleKeyDown);
    document.body.style.overflow = "hidden";
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      document.body.style.overflow = "";
    };
  }, [activeImageIndex, handleCloseLightbox, handleNextImage, handlePrevImage]);

  if (loading) {
    return (
      <PageContainer>
        <div className="project-detail__loading mono-eyebrow">
          Loading architectural archive...
        </div>
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
  const nextProject =
    currentIndex >= 0 && currentIndex < projects.length - 1
      ? projects[currentIndex + 1]
      : null;

  return (
    <PageContainer>
      <main className="project-detail animate-fade-up">
        {/* Header Block */}
        <header className="project-detail__header">
          <div className="project-detail__header-meta">
            <span className="mono-eyebrow">INDEX // {project.category}</span>
            <span className="mono-eyebrow">{project.year}</span>
          </div>
          <h1 className="project-detail__title">{project.title}</h1>
        </header>

        {/* Content Layout */}
        <div className="project-detail__layout">
          {/* Left Column: Sidebar Specs */}
          <aside className="project-detail__aside">
            <div className="project-detail__aside-content">
              <section className="project-detail__section">
                <span className="mono-eyebrow">Overview</span>
                <p className="project-detail__text">
                  {project.description || "No project overview available."}
                </p>
              </section>

              <section className="project-detail__section">
                <span className="mono-eyebrow">Specifications</span>
                <dl className="project-detail__specs">
                  <div>
                    <dt>Category</dt>
                    <dd>{project.category}</dd>
                  </div>
                  <div>
                    <dt>Location</dt>
                    <dd>{project.location || "Unspecified"}</dd>
                  </div>
                  <div>
                    <dt>Year</dt>
                    <dd>{project.year}</dd>
                  </div>
                  <div>
                    <dt>Plates</dt>
                    <dd>{galleryImages.length} Artifacts</dd>
                  </div>
                </dl>
              </section>
            </div>
          </aside>

          {/* Right Column: Gallery Grid */}
          <section className="project-detail__grid">
            {galleryImages.length > 0 ? (
              galleryImages.map((image: any, index: number) => {
                const rawUrl = image.image_url || image.url;
                const imageUrl = getFullImageUrl(rawUrl);
                const tileId = image.id || `img-${index}`;
                const detectedOrientation = imageRatios[tileId] || "landscape";

                return (
                  <figure
                    key={tileId}
                    className={`project-detail__tile project-detail__tile--${detectedOrientation} ${
                      index === 0 ? "project-detail__tile--first" : ""
                    }`}
                    onClick={() => setActiveImageIndex(index)}
                  >
                    <div className="project-detail__tile-frame">
                      <img
                        className="project-detail__tile-img"
                        src={imageUrl}
                        alt={image.alt_text || `${project.title} plate ${index + 1}`}
                        loading="lazy"
                        onLoad={(e) => handleImageLoad(tileId, e)}
                        onError={(e) => {
                          (e.target as HTMLImageElement).src = "/placeholder.jpg";
                        }}
                      />
                      <span className="project-detail__tile-number mono-eyebrow">
                        IMG. 0{index + 1}
                      </span>
                    </div>
                    {image.caption && (
                      <figcaption className="project-detail__tile-caption">
                        {image.caption}
                      </figcaption>
                    )}
                  </figure>
                );
              })
            ) : (
              <figure className="project-detail__tile project-detail__tile--landscape project-detail__tile--first">
                <div className="project-detail__tile-frame">
                  <img
                    className="project-detail__tile-img"
                    src="/placeholder.jpg"
                    alt={project.title}
                  />
                </div>
              </figure>
            )}
          </section>
        </div>

        {/* Project Footer Nav */}
        <nav className="project-detail__nav" aria-label="Project navigation">
          <div>
            {previousProject && (
              <Link
                to={`/projects/${previousProject.slug}`}
                className="project-detail__nav-link"
              >
                <span className="mono-eyebrow">← Previous Work</span>
                <strong>{previousProject.title}</strong>
              </Link>
            )}
          </div>
          <div>
            {nextProject && (
              <Link
                to={`/projects/${nextProject.slug}`}
                className="project-detail__nav-link project-detail__nav-link--right"
              >
                <span className="mono-eyebrow">Next Work →</span>
                <strong>{nextProject.title}</strong>
              </Link>
            )}
          </div>
        </nav>

        {/* Lightbox Modal */}
        {activeImageIndex !== null && galleryImages[activeImageIndex] && (
          <div className="lightbox" onClick={handleCloseLightbox}>
            <button
              className="lightbox__close"
              onClick={handleCloseLightbox}
              aria-label="Close lightbox"
            >
              ✕
            </button>

            {galleryImages.length > 1 && (
              <>
                <button
                  className="lightbox__nav lightbox__nav--prev"
                  onClick={(e) => {
                    e.stopPropagation();
                    handlePrevImage();
                  }}
                  aria-label="Previous plate"
                >
                  ←
                </button>
                <button
                  className="lightbox__nav lightbox__nav--next"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleNextImage();
                  }}
                  aria-label="Next plate"
                >
                  →
                </button>
              </>
            )}

            <div className="lightbox__stage" onClick={(e) => e.stopPropagation()}>
              <img
                className="lightbox__img"
                src={getFullImageUrl(
                  galleryImages[activeImageIndex].image_url ||
                    galleryImages[activeImageIndex].url
                )}
                alt={galleryImages[activeImageIndex].alt_text || "Full screen view"}
              />
              <div className="lightbox__footer">
                <span className="mono-eyebrow">
                  PLATE 0{activeImageIndex + 1} / 0{galleryImages.length}
                </span>
                {galleryImages[activeImageIndex].caption && (
                  <p className="lightbox__caption">
                    {galleryImages[activeImageIndex].caption}
                  </p>
                )}
              </div>
            </div>
          </div>
        )}
      </main>
    </PageContainer>
  );
}

export default ProjectDetail;