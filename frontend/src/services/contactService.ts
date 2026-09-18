import apiRequest from "./api";

export interface ContactFormData {
  name: string;
  email: string;
  subject?: string;
  message: string;
}

export interface ContactResponse {
  success: boolean;
  message: string;
}

/**
 * Send contact inquiry to backend API
 */
export async function submitContactForm(data: ContactFormData): Promise<ContactResponse> {
  return apiRequest<ContactResponse>("/api/contact", {
    method: "POST",
    body: JSON.stringify(data),
  });
}