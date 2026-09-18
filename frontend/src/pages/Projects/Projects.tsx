import { useEffect, useState } from "react";
import type { Project } from "../../types/project";
import { getProjects } from "../../services/projectService";
import ProjectCard from "../../components/projects/ProjectCard/ProjectCard";
import Loading from "../../components/common/Loading";
import ErrorMessage from "../../components/common/ErrorMessage";
import "./Projects.css";

const CATEGORIES = ["All", "Residential", "Commercial", "Cultural", "Interior"];

export default function Projects() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [activeCategory, setActiveCategory] = useState("All");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchProjects() {
      setLoading(true);
      setError(null);
      try {
        const response = await getProjects({
          page,
          page_size: 9,
          category: activeCategory === "All" ? undefined : activeCategory,
        });

        setProjects(response.projects);
        setTotalPages(response.pagination.total_pages);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load projects.");
      } finally {
        setLoading(false);
      }
    }

    fetchProjects();
  }, [activeCategory, page]);

  const handleCategoryChange = (category: string) => {
    setActiveCategory(category);
    setPage(1);
  };

  return (
    <div className="projects-page">
      <div className="container">
        <header className="projects-header">
          <p className="mono-eyebrow">Index // Portfolio</p>
          <h1 className="projects-title">Selected Works</h1>
        </header>

        {/* Category Filters */}
        <nav className="category-filters" aria-label="Project categories">
          {CATEGORIES.map((cat) => (
            <button
              key={cat}
              className={`filter-btn ${activeCategory === cat ? "active" : ""}`}
              onClick={() => handleCategoryChange(cat)}
            >
              {cat}
            </button>
          ))}
        </nav>

        {/* Content States */}
        {loading && <Loading message="Loading works..." />}
        {error && <ErrorMessage message={error} />}

        {!loading && !error && projects.length === 0 && (
          <div className="empty-state">
            <p>No projects found in this category.</p>
          </div>
        )}

        {!loading && !error && projects.length > 0 && (
          <>
            <div className="projects-grid">
              {projects.map((project) => (
                <ProjectCard key={project.id} project={project} />
              ))}
            </div>

            {/* Pagination Controls */}
            {totalPages > 1 && (
              <div className="pagination">
                <button
                  disabled={page <= 1}
                  onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
                  className="pagination-btn"
                >
                  ← Previous
                </button>
                <span className="pagination-info">
                  {page} / {totalPages}
                </span>
                <button
                  disabled={page >= totalPages}
                  onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
                  className="pagination-btn"
                >
                  Next →
                </button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}