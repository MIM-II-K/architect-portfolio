import type { Project, ProjectImage } from "../types/project";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "https://architect-portfolio-1.onrender.com";

interface ApiRequestOptions extends RequestInit {
  token?: string;
}

async function apiRequest<T>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<T> {
  const { token, headers, body, ...requestOptions } = options;

  const isFormData = body instanceof FormData;

  const requestHeaders: Record<string, string> = {
    ...(!isFormData && { "Content-Type": "application/json" }),
    ...(headers as Record<string, string>),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...requestOptions,
    body,
    headers: requestHeaders,
  });

  if (!response.ok) {
    let message = `Request failed with status ${response.status}`;

    try {
      const errorData = await response.json();
      if (typeof errorData?.detail === "string") {
        message = errorData.detail;
      }
    } catch {
      // Ignore invalid error response.
    }

    throw new Error(message);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return response.json() as Promise<T>;
}

export default apiRequest;

/* ==========================================================================
   API Service Endpoints
   ========================================================================== */

export async function getProjects(params?: {
  category?: string;
  year?: number;
  location?: string;
  sort?: string;
}): Promise<Project[]> {
  const queryParams = new URLSearchParams();

  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        queryParams.append(key, String(value));
      }
    });
  }

  const query = queryParams.toString() ? `?${queryParams.toString()}` : "";
  return apiRequest<Project[]>(`/api/projects${query}`);
}

export async function getProjectBySlug(slug: string): Promise<Project> {
  return apiRequest<Project>(`/api/projects/${slug}`);
}

export async function uploadProjectImage(
  projectId: string,
  file: File,
  token?: string
): Promise<ProjectImage> {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest<ProjectImage>(`/api/admin/projects/${projectId}/images`, {
    method: "POST",
    body: formData,
    token,
  });
}

export async function deleteProjectImage(
  projectId: string,
  imageId: string,
  token?: string
): Promise<void> {
  return apiRequest<void>(
    `/api/admin/projects/${projectId}/images/${imageId}`,
    {
      method: "DELETE",
      token,
    }
  );
}