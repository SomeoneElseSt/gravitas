# Gravitas API Documentation

## Overview

The Gravitas API provides endpoints for analyzing urban heat patterns using satellite imagery from Google Earth Engine. The API processes Landsat 8 data to generate four key indices:

1. **UHI** - Urban Heat Index
2. **NDVI** - Normalized Difference Vegetation Index
3. **LST** - Land Surface Temperature
4. **UTFVI** - Urban Thermal Field Variance Index

## Base URL

- **Local Development**: `http://localhost:8000`
- **Production**: TBD (deploy on Cloud Run, Railway, or Fly.io)

## API Endpoints

### 1. Get Available Cities

Retrieves the list of cities available for analysis with their coordinates.

**Endpoint:** `GET /api/cities`

**Response:**
```json
{
  "cities": {
    "San Francisco": {
      "name": "San Francisco",
      "center": [-122.4194, 37.7749],
      "bbox": [
        [-122.5194, 37.8749],
        [-122.5194, 37.6749],
        [-122.3194, 37.6749],
        [-122.3194, 37.8749]
      ]
    },
    "Belgrade": {
      "name": "Belgrade",
      "center": [20.4489, 44.7866],
      "bbox": [...]
    }
    // ... more cities
  }
}
```

**Available Cities:**
- San Francisco
- Belgrade
- Zagreb
- Sarajevo
- Podgorica
- Skopje
- Tirana
- Pristina
- Novi Sad
- Banja Luka

---

### 2. Process Imagery

Processes satellite imagery for a specified city and date range. Returns tile URLs for all four indices plus statistical data.

**Endpoint:** `POST /api/process-imagery`

**Request Body:**
```json
{
  "city": "Belgrade",
  "start_date": "2022-05-01",
  "end_date": "2022-12-31"
}
```

**Request Parameters:**
- `city` (string, required): Name of the city to analyze (must be from available cities)
- `start_date` (string, required): Start date in ISO format (YYYY-MM-DD)
- `end_date` (string, required): End date in ISO format (YYYY-MM-DD)

**Response:**
```json
{
  "city": "Belgrade",
  "start_date": "2022-05-01",
  "end_date": "2022-12-31",
  "layers": {
    "uhi": {
      "tile_url": "https://earthengine.googleapis.com/v1/...",
      "visualization": {
        "min": -4,
        "max": 4,
        "palette": ["313695", "74add1", "fed976", "feb24c", "fd8d3c", "fc4e2a", "e31a1c", "b10026"]
      },
      "name": "Urban Heat Index",
      "description": "Shows relative heat concentration compared to city average"
    },
    "ndvi": {
      "tile_url": "https://earthengine.googleapis.com/v1/...",
      "visualization": {
        "min": -1,
        "max": 1,
        "palette": ["blue", "white", "green"]
      },
      "name": "NDVI",
      "description": "Vegetation health and density index"
    },
    "lst": {
      "tile_url": "https://earthengine.googleapis.com/v1/...",
      "visualization": {
        "min": 7,
        "max": 50,
        "palette": [...]
      },
      "name": "Land Surface Temperature",
      "description": "Surface temperature in degrees Celsius"
    },
    "utfvi": {
      "tile_url": "https://earthengine.googleapis.com/v1/...",
      "visualization": {
        "min": -1,
        "max": 0.3,
        "palette": [...]
      },
      "name": "Urban Thermal Field Variance Index",
      "description": "Temperature comfort level classification"
    }
  },
  "statistics": {
    "lst_mean": 28.45,
    "lst_std": 3.21,
    "ndvi_min": -0.15,
    "ndvi_max": 0.82
  },
  "aoi_bounds": [[20.3489, 44.8866], [20.3489, 44.6866], [20.5489, 44.6866], [20.5489, 44.8866]]
}
```

**Error Responses:**

- **400 Bad Request** - Invalid city or date range
  ```json
  {
    "error": "Invalid request",
    "detail": "City 'InvalidCity' not found. Available cities: [...]"
  }
  ```

- **500 Internal Server Error** - Earth Engine processing error
  ```json
  {
    "error": "Processing failed",
    "detail": "Earth Engine error details"
  }
  ```

---

### 3. Health Check

Simple health check endpoint.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy"
}
```

---

## Index Calculations

### NDVI (Normalized Difference Vegetation Index)
```
NDVI = (NIR - Red) / (NIR + Red)
```
- **Range**: -1 to 1
- **Higher values** = healthier vegetation
- **Lower values** = bare surfaces, built-up areas

### LST (Land Surface Temperature)
```
LST = BT / (1 + (λ × BT / c2) × ln(E)) - 273.15
```
- **Units**: Degrees Celsius
- **Range**: Typically 7°C to 50°C
- Calculated from thermal band with emissivity correction

### UHI (Urban Heat Index)
```
UHI = (LST - LST_mean) / LST_std
```
- **Range**: Typically -4 to 4
- **Positive values** = hotter than average (heat island)
- **Negative values** = cooler than average

### UTFVI (Urban Thermal Field Variance Index)
```
UTFVI = (LST - LST_mean) / LST
```
- **Range**: -1 to 0.3
- **Higher values** = higher heat stress
- Quantifies temperature variation for comfort assessment

---

## Data Processing Pipeline

1. **Image Collection**: Filter Landsat 8 Collection 2 images by date and location
2. **Cloud Masking**: Remove cloudy pixels using QA_PIXEL band
3. **Scale Factors**: Apply correction factors to optical and thermal bands
4. **Median Composite**: Create median image from filtered collection
5. **Calculate Indices**: Compute NDVI, LST, UHI, UTFVI from composite
6. **Generate Tiles**: Create map tile URLs from Earth Engine
7. **Compute Statistics**: Calculate mean, std dev, min, max values

---

## Frontend Integration

### TypeScript Types

All API types are defined in `frontend/lib/types/api.ts` and match the backend Pydantic schemas.

### API Client

Use the client functions in `frontend/lib/api/client.ts`:

```typescript
import { getCities, processImagery } from "@/lib/api/client";

// Fetch cities
const { data, error } = await getCities();
if (error) {
  console.error("Failed to fetch cities:", error);
  return;
}

// Process imagery
const result = await processImagery({
  city: "Belgrade",
  start_date: "2022-05-01",
  end_date: "2022-12-31",
});

if (result.error) {
  console.error("Failed to process imagery:", result.error);
  return;
}

// Use tile URLs in map
const uhiTileUrl = result.data.layers.uhi.tile_url;
```

### Error Handling

All API functions return `{ data, error }` tuples. Always check for errors before using data:

```typescript
const { data, error } = await processImagery(request);

if (error) {
  // Handle error explicitly
  return;
}

// data is guaranteed to be non-null here
console.log(data.statistics.lst_mean);
```

---

## Development

### Backend Setup

```bash
cd backend

# Install dependencies with uv
uv pip install -e ".[dev]"

# Configure environment
cp .env.example .env
# Edit .env with your GCP project name

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies with pnpm
pnpm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your API URL

# Run development server
pnpm dev
```

### Testing API

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

---

## Deployment

### Backend (Python API)

Recommended platforms:
- **Google Cloud Run** (native GCP integration)
- **Railway**
- **Fly.io**

Environment variables needed:
- `GCP_SERVICE_ACCOUNT_EMAIL`
- `GCP_SERVICE_ACCOUNT_KEY` (or key file path)
- `CORS_ORIGINS`

### Frontend (Next.js)

Deploy on **Vercel**:

```bash
cd frontend
vercel
```

Environment variables:
- `NEXT_PUBLIC_API_URL` (production backend URL)

---

## Rate Limiting & Caching

**Note**: Earth Engine processing can be slow (5-30 seconds per request). Consider:

1. **Caching**: Cache processed results in Redis or database
2. **Rate Limiting**: Limit requests per user/IP
3. **Background Jobs**: Process imagery asynchronously with Celery/RQ
4. **Pre-computation**: Pre-process common city/date combinations

These will be implemented in future iterations.
