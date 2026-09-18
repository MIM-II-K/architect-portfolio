export interface ProjectImageCreate {
  image_url: string;
  alt_text: string;
  caption?: string | null;
  sort_order?: number;
}

export interface ProjectImageUpdate {
  image_url?: string;
  alt_text?: string;
  caption?: string | null;
  sort_order?: number;
}

export interface ProjectImageResponse {
  id: string;
  image_url: string;
  alt_text: string;
  caption?: string | null;
  sort_order: number;
}

export interface ProjectImageListResponse {
  images: ProjectImageResponse[];
  total: number;
}

export interface ProjectResponse {
  id: string;
  title: string;
  slug: string;
  description: string;
  location?: string | null;
  year?: number | null;
  category?: string | null;
  area?: string | null;
  client?: string | null;
  architect?: string | null;
  status?: string | null;
  cover_image?: string | null;
  featured: boolean;
  published: boolean;
  sort_order: number;
  images: ProjectImageResponse[];
  created_at?: string | null;
  updated_at?: string | null;
}

export interface PaginationMeta {
  page: number;
  page_size: number;
  total_pages: number;
}

export interface ProjectListResponse {
  projects: ProjectResponse[];
  pagination: PaginationMeta;
  total: number;
}