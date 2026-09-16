import {
  apiFetch,
} from "./api";

import type {
  ProjectListResponse,
} from "../types/project";

interface ProjectFilters {
  category?: string;
  year?: number;
  location?: string;
  sort?: string;
  page?: number;
  page_size?: number;
}

export async function getProjects(
  filters: ProjectFilters = {},
): Promise<ProjectListResponse> {
  const params =
    new URLSearchParams();

  if (filters.category) {
    params.set(
      "category",
      filters.category,
    );
  }

  if (filters.year) {
    params.set(
      "year",
      String(filters.year),
    );
  }

  if (filters.location) {
    params.set(
      "location",
      filters.location,
    );
  }

  if (filters.sort) {
    params.set(
      "sort",
      filters.sort,
    );
  }

  if (filters.page) {
    params.set(
      "page",
      String(filters.page),
    );
  }

  if (filters.page_size) {
    params.set(
      "page_size",
      String(filters.page_size),
    );
  }

  const query =
    params.toString();

  return apiFetch<ProjectListResponse>(
    `/projects${query ? `?${query}` : ""}`,
  );
}