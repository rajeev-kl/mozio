
# Mozio Service Area API

## Overview
This project provides a Django REST API for managing transportation providers and their service areas using custom polygons. It allows providers to define, update, and query their service areas, supporting fast spatial queries and scalable integration.

## Features
- CRUD operations for Providers and Service Areas
- GeoJSON polygon support for service areas
- Fast spatial search endpoint: find all service areas containing a given lat/lng
- Sample data ingestion script for testing
- Rate limiting and CORS support via Nginx
- Production-ready deployment scripts (Gunicorn, Nginx, Systemd)
- PEP8-compliant codebase with comments

## Project Structure
```
datasmith/
  conf/         # Django project config (settings, urls, wsgi, asgi)
  findr/        # Main app: models, serializers, viewsets, migrations, scripts
    scripts/    # Data ingestion and utilities
  .env          # Environment variables
scripts/        # Formatting, server, and log scripts
system/         # Gunicorn systemd service, Nginx config
Pipfile, Pipfile.lock, pyproject.toml
```

## Setup & Installation
1. **Clone the repo**
2. **Install dependencies:**
   ```bash
   pipenv install --dev
   ```
3. **Configure environment:**
   - Copy `.env.example` to `.env` and set DB credentials, secret key, etc.
4. **Run migrations:**
   ```bash
   pipenv run python datasmith/manage.py migrate
   ```
5. **Ingest sample data:**
   ```bash
   pipenv run python datasmith/findr/scripts/ingest_sample_data.py
   ```
6. **Start development server:**
   ```bash
   pipenv run python datasmith/manage.py runserver
   ```

## API Endpoints
Base URL: `/api/`

### Provider
- `GET /api/providers/` — List providers
- `POST /api/providers/` — Create provider
- `GET /api/providers/{id}/` — Retrieve provider
- `PUT/PATCH /api/providers/{id}/` — Update provider
- `DELETE /api/providers/{id}/` — Delete provider

### Service Area
- `GET /api/service-areas/` — List service areas
- `POST /api/service-areas/` — Create service area
- `GET /api/service-areas/{id}/` — Retrieve service area
- `PUT/PATCH /api/service-areas/{id}/` — Update service area
- `DELETE /api/service-areas/{id}/` — Delete service area

### Spatial Search
- `GET /api/service-areas/search?lat={latitude}&lng={longitude}`
  - Returns all polygons containing the point, with polygon name, provider name, and price.

## Data Model
**Provider**
- name, email, phone_number, language, currency

**ServiceArea**
- provider (FK), name, price, geojson (Polygon)

## Sample Data
Run the script `datasmith/findr/scripts/ingest_sample_data.py` to populate the database with 100 providers and random overlapping polygons.

## Deployment
### Gunicorn
Use `scripts/gunicorn.sh` to start the Gunicorn server with optimal worker settings.

### Nginx
Reverse proxy, CORS, and rate limiting are configured in `mozio/.ansible/roles/nginx/templates/nginx.conf.j2`.

### Systemd
Service file `system/datasmith-gunicorn.service` for process management.

## Testing
Run tests with:
```bash
pipenv run python datasmith/manage.py test findr
```

## Development & Formatting
- Use `scripts/formatter.sh` for code formatting (isort, black, flake8)
- PEP8 style, 120 chars/line

## Dependencies
See `Pipfile` and `Pipfile.lock` for all dependencies. Key packages:
- Django, Django REST Framework, djangorestframework-gis, psycopg2-binary
- Gunicorn, django-cors-headers, django-extensions

## Environment Variables
Configure DB, secret key, and other settings in `.env`.

## Hosting Domain & Server Configuration

### Hosting Domain
The API is hosted on `mozio.prodot.in`

### Server Configuration
- **Nginx**: Acts as a reverse proxy, handles HTTPS (SSL/TLS), CORS, and rate limiting. See `mozio/.ansible/roles/nginx/templates/nginx.conf.j2` for example configuration.
- **Gunicorn**: Runs the Django application. Use `scripts/gunicorn.sh` for optimal worker settings.
- **Systemd**: Manages Gunicorn as a service. See `system/datasmith-gunicorn.service` for setup instructions.
- **SSL/TLS**: For production, obtain and configure SSL certificates (e.g., via Let's Encrypt) in your Nginx config.
- **Environment Variables**: Store sensitive settings (DB credentials, secret key) in `.env` and never commit them to source control.

Refer to the deployment section for more details on configuring each component.

## API Documentation
Use Postman to import `mozio.postman_collection.json` for interactive API testing and documentation.