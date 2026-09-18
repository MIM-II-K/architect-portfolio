import apiRequest from "./api";
import type { Project, ProjectListResponse } from "../types/project";

export interface GetProjectsParams {
  page?: number;
  page_size?: number;
  category?: string;
  featured?: boolean;
}

/**
 * Fetch paginated projects list from backend
 */
export async function getProjects(params?: GetProjectsParams): Promise<ProjectListResponse> {
  const queryParams = new URLSearchParams();

  if (params?.page) queryParams.append("page", params.page.toString());
  if (params?.page_size) queryParams.append("page_size", params.page_size.toString());
  if (params?.category) queryParams.append("category", params.category);
  if (params?.featured !== undefined) queryParams.append("featured", String(params.featured));

  const queryString = queryParams.toString();
  const endpoint = `/api/projects${queryString ? `?${queryString}` : ""}`;

  return apiRequest<ProjectListResponse>(endpoint);
}

/**
 * Fetch detailed project data by slug
 */
export async function getProject(slug: string): Promise<Project> {
  return apiRequest<Project>(`/api/projects/${slug}`);
}