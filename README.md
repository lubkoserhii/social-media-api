# Social Media API

REST API for a social media platform built with Django REST Framework.

## Core Features

- User registration and JWT authentication.
- Authenticated users create their own profile after registration.
- View and edit your own profile.
- Search profiles by username or bio.
- Follow and unfollow other users.
- Create, view, edit, and delete posts.
- The personalized feed contains the user's own posts and posts from followed
  users.
- Search posts by text or hashtags.
- Add comments and likes.
- Only the owner can edit or delete an object.

Protected endpoints require an access token:

```text
Authorization: Bearer <access_token>
```

Profile endpoints:

- `POST /api/user/profiles/` creates the authenticated user's profile.
- `PATCH /api/user/profiles/{id}/` updates the profile bio or picture.
- `GET /api/user/profiles/` lists profiles.

API documentation is available after starting the project:

- Swagger UI: `http://127.0.0.1:8000/api/schema/swagger/`
- ReDoc: `http://127.0.0.1:8000/api/schema/redoc/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Docker Setup

Docker and Git must be installed.

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
```

2. Create the environment file and replace the example secrets:

```bash
cp .env.example .env
```

3. Build and start the application with PostgreSQL:

```bash
docker compose up --build
```

The database migrations run automatically. The API will be available at
`http://127.0.0.1:8000/`.

To stop the services:

```bash
docker compose down
```



## Tests

```bash
docker compose run --rm web python manage.py test
```
