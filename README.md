# Urban SDK Homework
Built with ❤️ for Urban SDK by Pat Blair.

A FastAPI-based traffic data analysis service that provides REST APIs for 
querying and visualizing aggregated traffic speed data on road networks. Built
with PostgreSQL + PostGIS for spatial data operations.

> [!WARNING]
> This project was created to demonstrate the my understanding of application
> development in general, and geospatial applications in particular, using 
> tools like FastAPI and PostGIS.  The repository will be removed in the 
> near future.

> [!NOTE]
> This is a first draft for demonstration.  There are many #TODOs.  Thank you
> in advance for your patience and understanding.


## 🚧 TODOS

- Add pytest and Gherkin. 
- Add a PostGIS container to the development `docker-compose.yaml`.
- Lots of other stuff.


## 🚀 Features

- **Traffic Speed Analytics**: Query aggregated speed data by day of week and time period
- **Spatial Filtering**: Filter results using bounding box coordinates with PostGIS
- **Road Network Data**: Access link geometry and metadata (road names, lengths)
- **Interactive Visualization**: Jupyter notebook support with Folium and Plotly
- **RESTful API**: FastAPI with automatic OpenAPI documentation
- **Enum Support**: Human-readable day/period names in API responses

## 📁 Project Structure

```
urban-sdk-homework/
├── urban_sdk_homework/          # Main application package
│   ├── core/                    # Core utilities and base classes
│   │   ├── fastapi.py          # FastAPI router configuration
│   │   ├── geometry.py         # GeoJSON models
│   │   ├── models.py           # Base Pydantic models
│   │   └── services.py         # Base service class
│   └── modules/
│       └── traffic/            # Traffic analysis module
│           ├── api/            # FastAPI endpoints
│           │   ├── endpoints.py
│           │   └── dependencies.py
│           ├── models.py       # Data models and enums
│           └── services.py     # Business logic
│           └── settings.py     # Traffic service settings
├── scripts/
│   └── load.sh                 # Data loading utilities
├── notebooks/                  # Jupyter analysis notebooks
├── data/                       # Raw data files
├── justfile                    # Task runner commands
└── pyproject.toml              # Project dependencies
```

## 🛠️ Quick Start

### Prerequisites

- **Dev Container**: VS Code with Remote-Containers extension (recommended)
- **Local Setup**: Python 3.11+, PostgreSQL with PostGIS

### Option 1: Dev Container (Recommended)

1. **Open in VS Code**:
   ```bash
   git clone <repository-url>
   cd urban-sdk-homework
   code .
   # When prompted, reopen in container
   ```

2. **Setup environment**:
   ```bash
   just setup
   ```

3. **Start development container**:
   ```bash
   just dev
   ```

### Option 2: Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd urban-sdk-homework
   DEV_CONTAINER=0 just setup
   source .venv/bin/activate
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your PostgreSQL connection details
   ```

   ```bash
   urban_sdk_homework__traffic__sqa_conn="postgresql://postgres:postgres@localhost:5432/urbansdk"
   ```

3. **Load sample data** (if available):

   Copy [duval_jan1_2024.parquet.gz](https://cdn.urbansdk.com/data-engineering-interview/link_info.parquet.gz)
   [link_info.parquet.gz](https://cdn.urbansdk.com/data-engineering-interview/duval_jan1_2024.parquet.gz) 
   into the `data` directory and run the `load.sh` script to load and ETL the
   data.

   ```bash
   ./scripts/load.sh
   ```

4. **Start the API**:
   ```bash
   homework api start
   ```

5. **Launch Jupyter for analysis**:
   ```bash
   just notebooks
   ```

## 📡 API Documentation

### Interactive Docs
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Core Endpoints

#### Traffic Links
```bash
# Get all links
GET /links/

# Get specific link
GET /link/{link_id}
```

#### Traffic Aggregates
```bash
# Get aggregates by day and period
GET /aggregates/?day=Monday&period=Evening

# Get aggregates for specific link
GET /aggregates/{link_id}?day=Monday&period=Evening

# Spatial filtering with bounding box
POST /aggregates/spatial_filter/
Content-Type: application/json
{
  "day": 2,
  "period": 3,
  "bbox": [-81.8, 30.1, -81.6, 30.3]
}
```

### Data Formats

#### Day of Week (1-7)
- **1**: Sunday
- **2**: Monday
- **3**: Tuesday
- **4**: Wednesday
- **5**: Thursday
- **6**: Friday
- **7**: Saturday

#### Time Periods (1-7)
- **1**: Overnight
- **2**: Early Morning
- **3**: AM Peak
- **4**: Midday
- **5**: Early Afternoon
- **6**: PM Peak
- **7**: Evening

#### Bounding Box Format
`[min_longitude, min_latitude, max_longitude, max_latitude]`

Example for Jacksonville, FL area:
```json
[-81.8, 30.1, -81.6, 30.3]
```

## 📊 Data Visualization

### Jupyter Notebooks

Start Jupyter Lab:
```bash
just notebooks
```

Example visualization code:
```python
import folium
import json
from urban_sdk_homework.modules.traffic.services import TrafficService

# Connect to service
service = TrafficService()

# Get traffic data
aggregates = service.get_aggregates(day=2, period=3)

# Create interactive map
m = folium.Map(location=[30.3322, -81.6557], zoom_start=11)

# Add traffic data as colored lines
for agg in aggregates:
    if agg.geom:
        color = 'red' if agg.speed < 30 else 'yellow' if agg.speed < 50 else 'green'
        folium.GeoJson(
            agg.geom.dict(),
            style_function=lambda x, color=color: {
                'color': color, 'weight': 3, 'opacity': 0.8
            }
        ).add_to(m)

m
```

### Supported Libraries
- **Folium**: Interactive Leaflet maps
- **Plotly**: Interactive charts and Mapbox integration
- **GeoPandas**: Spatial data analysis
- **Mapbox GL**: Advanced mapping (with token)

## 🗄️ Database Schema

### Core Tables

#### `traffic.links`
- `link_id`: Unique road segment identifier
- `road_name`: Street/highway name
- `length`: Segment length in meters
- `geom`: PostGIS LineString geometry

#### `traffic.speed_records`
- `link_id`: Foreign key to links
- `day_of_week`: Day (1-7)
- `period`: Time period (1-7)
- `speed`: Average speed in mph

#### `traffic.link_aggs` (if using pre-aggregated data)
- Pre-computed speed statistics by link/day/period

## ⚙️ Available Commands

```bash
# Service
homework api start

# Development
just dev              # Start FastAPI development server
just setup            # Initial project setup
just pre-commit       # Run code quality checks

# Data Analysis
just notebooks        # Launch Jupyter Lab
./scripts/load.sh     # Load traffic data (if available)

# Utilities  
just killport 8000    # Kill process on port 8000
```

## 🔧 Configuration

### Environment Variables

Create `.env` file:
```bash
# Database Configuration
PGHOST=localhost
PGPORT=5432
PGDATABASE=urbansdk
PGUSER=postgres
PGPASSWORD=postgres

# Development
DEV_CONTAINER=1      # Set to 1 in dev container, 0 for local
BROWSER=google-chrome # Or your preferred browser command
```

## 🏗️ Technology Stack

- **Backend**: FastAPI, SQLModel, SQLAlchemy
- **Database**: PostgreSQL with PostGIS extension
- **Spatial**: PostGIS for geometric operations
- **Visualization**: Folium, Plotly, Mapbox GL
- **Data Processing**: Pandas, GeoPandas
- **Development**: uv (package manager), pre-commit hooks
- **Deployment**: Docker dev containers

## 🧪 Example API Responses

### Aggregate Data
```json
{
  "link_id": 1240632857,
  "day_of_week": "Monday",
  "period": "AM Peak", 
  "speed": 45.2,
  "road_name": "Philips Hwy",
  "length": 156.8,
  "geom": {
    "type": "LineString",
    "coordinates": [[-81.59791, 30.24124], [-81.59801, 30.24135]]
  }
}
```

### GeoJSON Output
Compatible with standard GIS tools and web mapping libraries.

## 🤝 Contributing

1. **Setup pre-commit hooks**: `just setup`
2. **Run tests**: `just pre-commit`
3. **Follow existing patterns**: SQLModel for data, FastAPI for endpoints
4. **Add tests**: For new functionality
5. **Update docs**: Keep README current

## 📄 License

[TBD]

## 🏗️ System Architecture

![System Architecture](docs/images/architecture.png)

The system follows a layered architecture with:
- **Presentation Layer**: Jupyter Labs for visualization and analysis
- **API Layer**: FastAPI service providing REST endpoints
- **Business Logic**: Traffic service components
- **Data Layer**: PostgreSQL with PostGIS for spatial operations

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/gardenio-dev/urban-sdk-homework/issues)
- **Documentation**: See `/openapi` endpoint when running
- **Dev Container**: Pre-configured with all dependencies
