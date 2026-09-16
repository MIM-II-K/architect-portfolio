export interface ProjectImage {
  id: string;
  url: string;
  alt_text?: string | null;
  sort_order: number;
}

export interface Project {
  id: string;
  slug: string;
  title: string;
  description: string;
  location?: string | null;
  category?: string | null;
  year?: number | null;
  featured: boolean;
  published: boolean;
  sort_order: number;
  images: ProjectImage[];
}

export interface Pagination {
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}

export interface ProjectListResponse {
  projects: Project[];
  pagination: Pagination;
}