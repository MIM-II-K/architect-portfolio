# Firestore Schema

## projects

Collection:

projects/{project_id}

Fields:

- id
- title
- slug
- description
- location
- year
- category
- area
- client
- architect
- status
- cover_image
- featured
- published
- sort_order
- created_at
- updated_at

---

## project_images

Collection:

project_images/{image_id}

Fields:

- id
- project_id
- image_url
- alt_text
- caption
- sort_order
- created_at

---

## categories

Collection:

categories/{category_id}

Fields:

- id
- name
- slug
- created_at

---

## inquiries

Collection:

inquiries/{inquiry_id}

Fields:

- id
- name
- email
- phone
- project_type
- budget
- message
- status
- created_at
- updated_at

---

## admins

Collection:

admins/{admin_id}

Fields:

- id
- email
- role
- created_at