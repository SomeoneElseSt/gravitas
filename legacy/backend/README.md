# Gravitas Backend API

Python FastAPI backend for processing satellite imagery with Google Earth Engine.

## Setup

### 1. Install Dependencies

Using **uv** (recommended):
```bash
uv pip install -e ".[dev]"
```

Or using pip:
```bash
pip install -e ".[dev]"
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your Google Cloud project name:
```env
GCP_PROJECT_NAME=your-project-name
```

### 3. Authenticate with Earth Engine

First time only:
```bash
earthengine authenticate
```

This will open a browser for Google authentication.

## Running the Server

### Development
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive docs**: http://localhost:8000/docs
- **Health check**: http://localhost:8000/health

### Production

For production deployment, use a production ASGI server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with gunicorn:
```bash
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### `GET /api/cities`
Get list of available cities with coordinates.

### `POST /api/process-imagery`
Process satellite imagery for a city and date range.

**Request body:**
```json
{
  "city": "Belgrade",
  "start_date": "2022-05-01",
  "end_date": "2022-12-31"
}
```

**Response:** Tile URLs and statistics for all 4 indices (UHI, NDVI, LST, UTFVI)

See [../API.md](../API.md) for complete API documentation.

## Project Structure

```
app/
├── main.py              # FastAPI app & CORS config
├── api/
│   └── routes/
│       └── imagery.py   # Process imagery endpoint
├── lib/
│   └── earth_engine/
│       ├── client.py        # EE initialization
│       ├── imagery.py       # Image collection & filtering
│       ├── calculations.py  # Index calculations
│       └── visualization.py # Tile generation
├── models/
│   └── schemas.py       # Pydantic models
└── config/
    └── constants.py     # All constants
```

## Environment Variables

### Local Development
- `GCP_PROJECT_NAME`: Your Google Cloud project name

### Production (Service Account)
- `GCP_SERVICE_ACCOUNT_EMAIL`: Service account email
- `GCP_SERVICE_ACCOUNT_KEY_PATH`: Path to key file, OR
- `GCP_SERVICE_ACCOUNT_KEY_JSON`: Key as JSON string
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated)

## Testing

Test the API with curl:

```bash
# Health check
curl http://localhost:8000/health

# Get cities
curl http://localhost:8000/api/cities

# Process imagery
curl -X POST http://localhost:8000/api/process-imagery \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Belgrade",
    "start_date": "2022-05-01",
    "end_date": "2022-12-31"
  }'
```

Or use the interactive docs at http://localhost:8000/docs

## Notes

- Earth Engine processing takes 5-30 seconds per request
- First request may be slower due to EE initialization
- Make sure Earth Engine API is enabled in Google Cloud Console
