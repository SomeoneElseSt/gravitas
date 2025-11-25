# Gravitas - Urban Heat Analysis Platform

A full-stack application for analyzing urban heat patterns using satellite imagery from Google Earth Engine.

## Overview

Gravitas analyzes Land Surface Temperature (LST) and Urban Heat Island (UHI) effects in cities using Landsat 8 satellite data. The platform provides interactive maps showing:

- **UHI (Urban Heat Index)** - Relative heat concentration
- **NDVI (Normalized Difference Vegetation Index)** - Vegetation health
- **LST (Land Surface Temperature)** - Surface temperature in °C
- **UTFVI (Urban Thermal Field Variance Index)** - Temperature comfort levels

## Project Structure

```
.
├── frontend/              # Next.js frontend application
│   ├── app/              # Next.js app router pages
│   ├── lib/              # Shared utilities and types
│   │   ├── api/         # API client
│   │   ├── types/       # TypeScript types
│   │   └── constants/   # Constants and configs
│   └── components/       # React components
│
├── backend/              # Python FastAPI backend
│   ├── app/
│   │   ├── api/         # API routes
│   │   ├── lib/         # Core logic
│   │   │   └── earth_engine/  # Earth Engine modules
│   │   ├── models/      # Pydantic schemas
│   │   └── config/      # Configuration and constants
│   └── pyproject.toml   # Python dependencies (uv)
│
├── prototype_v1.1.py     # Original Streamlit prototype
├── .CLAUDE.md           # Code guidelines and architecture
└── API.md               # API documentation
```

## Technology Stack

### Frontend
- **Next.js 16** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Leaflet.js** or **Mapbox GL JS** for maps (to be implemented)
- **React Query** for data fetching (to be implemented)

### Backend
- **Python 3.10+**
- **FastAPI** for REST API
- **Google Earth Engine** for satellite imagery processing
- **Pydantic** for data validation
- **uvicorn** as ASGI server

## Getting Started

### Prerequisites

- **Node.js** 18+ and **pnpm**
- **Python** 3.10+ and **uv**
- **Google Cloud Platform** account with Earth Engine enabled
- **Earth Engine API** credentials

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   uv pip install -e ".[dev]"
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env with your GCP project name
   ```

4. Initialize Earth Engine (first time only):
   ```bash
   earthengine authenticate
   ```

5. Run development server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   API will be available at `http://localhost:8000`

   API docs: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Configure environment:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your API URL (default: http://localhost:8000)
   ```

4. Run development server:
   ```bash
   pnpm dev
   ```

   Frontend will be available at `http://localhost:3000`

## Development Workflow

1. **Start backend**: `cd backend && uvicorn app.main:app --reload`
2. **Start frontend**: `cd frontend && pnpm dev`
3. **Make changes**: Edit files in respective directories
4. **Test API**: Use `http://localhost:8000/docs` for interactive API testing

## API Endpoints

See [API.md](./API.md) for detailed API documentation.

**Quick overview:**

- `GET /api/cities` - Get available cities
- `POST /api/process-imagery` - Process imagery for a city
- `GET /health` - Health check

## Code Guidelines

See [.CLAUDE.md](./.CLAUDE.md) for detailed code guidelines. Key points:

1. ✅ Handle errors explicitly with early returns
2. ✅ Write flat code, avoid nested ifs
3. ✅ Separate concerns into dedicated functions
4. ✅ Use **uv** for Python, **pnpm** for TypeScript
5. ✅ Name variables in English, declare constants at top
6. ✅ Keep frontend types in sync with backend schemas

## Available Cities

- San Francisco, USA
- Belgrade, Serbia
- Zagreb, Croatia
- Sarajevo, Bosnia and Herzegovina
- Podgorica, Montenegro
- Skopje, North Macedonia
- Tirana, Albania
- Pristina, Kosovo
- Novi Sad, Serbia
- Banja Luka, Bosnia and Herzegovina

## Current Status

### ✅ Completed
- [x] Next.js frontend scaffolding
- [x] FastAPI backend structure
- [x] API endpoint contracts
- [x] TypeScript types matching backend schemas
- [x] Constants and configuration
- [x] API client for frontend
- [x] Documentation

### 🚧 In Progress
- [ ] Earth Engine integration (imagery processing)
- [ ] Map component with Leaflet/Mapbox
- [ ] UI components (city selector, date picker)
- [ ] Layer visualization and legends

### 📋 Planned (Later)
- [ ] Statistics display
- [ ] Caching and optimization
- [ ] Gemini AI chat integration
- [ ] Deployment configuration

## Next Steps

### Backend Implementation
1. Implement Earth Engine client initialization (`app/lib/earth_engine/client.py`)
2. Port imagery collection and filtering logic
3. Implement NDVI, LST, UHI, UTFVI calculations
4. Generate tile URLs for map layers
5. Add error handling and logging

### Frontend Implementation
1. Create map component with Leaflet/Mapbox
2. Build city selector component
3. Build date range picker
4. Implement layer toggle controls
5. Add legends for each index
6. Display statistics

## Testing

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
pnpm test

# API health check
curl http://localhost:8000/health
```

## Deployment

### Backend
Deploy on **Google Cloud Run**, **Railway**, or **Fly.io**

### Frontend
Deploy on **Vercel**:
```bash
cd frontend
vercel
```

## Contributing

Follow the code guidelines in `.CLAUDE.md` when contributing.

## License

TBD

## Notes

- Earth Engine processing can take 5-30 seconds per request
- Some cities may have gaps due to Landsat 8 dataset limitations
- Gemini AI chat integration is planned for later phases
