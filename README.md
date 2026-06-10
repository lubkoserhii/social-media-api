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

## Local Setup

Python and Git must be installed.

1. Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

3. Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

4. Apply the migrations:

```bash
python manage.py migrate
```

5. Start the development server:

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.
The project uses SQLite by default.

## Tests

```bash
python manage.py test
```
