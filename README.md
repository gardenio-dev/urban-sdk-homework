# Urban SDK Homework
Built with ❤️ for Urban SDK by Pat Blair.

A FastAPI-based traffic data analysis service that provides REST APIs for 
querying and visualizing aggregated traffic speed data on road networks. Built
with PostgreSQL + PostGIS for spatial data operations.

The project was built to address the requirements of the homework assignment,
but I'm also attempting to address issues like maintainable project structure.

> [!WARNING]
> This project was created to demonstrate my understanding of application
> development in general, and geospatial applications in particular, using 
> tools like FastAPI and PostGIS.  The repository will be removed in the 
> near future.

> [!NOTE]
> This is a first draft for demonstration.  There are many #TODOs.  I will 
> continue to work on it.  Thank you in advance for your patience and 
> understanding.


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
├── .devcontainer/               # VS Code dev container configuration
├── .vscode/                     # VS Code workspace settings
├── urban_sdk_homework/          # Main application package
│   ├── core/                    # Core utilities and base classes
│   │   ├── auth/               # Authentication framework
│   │   │   ├── __init__.py
│   │   │   ├── errors.py       # Auth-specific exceptions
│   │   │   ├── models.py       # User/Friend models with Frontegg
│   │   │   ├── providers.py    # Authentication provider abstractions
│   │   │   ├── settings.py     # Auth configuration settings
│   │   │   └── web.py          # Auth API endpoints (/whoami)
│   │   ├── geometry/           # Spatial data handling
│   │   │   ├── __init__.py
│   │   │   ├── errors.py       # Geometry-specific exceptions
│   │   │   ├── geojson.py      # GeoJSON models and utilities
│   │   │   └── proj.py         # Projection and coordinate transformation
│   │   ├── project/            # Project metadata management
│   │   │   ├── __init__.py
│   │   │   ├── metadata.py     # Version and package information
│   │   │   └── web.py          # Project metadata API endpoints
│   │   ├── settings/           # Configuration management
│   │   │   ├── __init__.py
│   │   │   ├── api.py          # Settings API router factory
│   │   │   ├── base.py         # Base settings class with env support
│   │   │   └── errors.py       # Settings-specific exceptions
│   │   ├── __init__.py
│   │   ├── click.py            # Click CLI utilities and decorators
│   │   ├── console.py          # Rich console pretty printing
│   │   ├── errors.py           # Base application exceptions
│   │   ├── fastapi.py          # Enhanced FastAPI router with auto-discovery
│   │   ├── jinja.py            # Jinja2 template environment
│   │   ├── logging.py          # Structured logging with structlog
│   │   ├── models.py           # Base Pydantic models
│   │   ├── modules.py          # Dynamic module loading utilities
│   │   ├── services.py         # Base service class
│   │   └── strings.py          # String manipulation utilities (camel/snake/kebab)
│   └── modules/
│       ├── api/                # Main API module
│       │   ├── cli/            # Command-line interface
│       │   │   ├── __init__.py
│       │   │   └── commands.py # API CLI commands
│       │   ├── __init__.py
│       │   ├── app.py          # FastAPI application instance
│       │   ├── services.py     # API service (Uvicorn runner)
│       │   └── settings.py     # API configuration settings
│       └── traffic/            # Traffic analysis module
│           ├── api/            # Traffic-specific endpoints
│           │   ├── __init__.py
│           │   ├── endpoints.py # REST API routes
│           │   └── dependencies.py # Dependency injection
│           ├── cli/            # Traffic CLI commands
│           │   ├── __init__.py
│           │   └── commands.py # Traffic CLI operations
│           ├── __init__.py
│           ├── errors.py       # Traffic-specific exceptions
│           ├── models.py       # Data models and enums
│           ├── services.py     # Business logic and database operations
│           └── settings.py     # Traffic service configuration
├── scripts/
│   └── load.sh                 # Data loading and ETL utilities
├── notebooks/                  # Jupyter analysis notebooks
│   └── links.ipynb            # Traffic data visualization example
├── data/                       # Raw data files (.parquet.gz)
├── temp/                       # Temporary output files
├── docs/
│   └── images/                 # Documentation assets
│       └── architecture.png    # System architecture diagram
├── .env                        # Environment variables (not in git)
├── .env.example               # Environment template
├── .gitignore                 # Git ignore rules
├── justfile                   # Task runner commands
├── pyproject.toml             # Project dependencies and metadata
└── README.md                  # This file
```

## 🛠️ Quick Start

### Prerequisites

#### For Dev Container (Recommended)
- **Docker Desktop**: Required for dev container support
- **VS Code**: With Remote-Containers extension
- **Git**: For cloning the repository

#### For Local Development
- **Python 3.11+**: Managed via pyenv (recommended)
- **pyenv**: For Python version management
- **just**: Command runner for project tasks
- **PostgreSQL**: With PostGIS extension
- **Docker Desktop**: Optional, for containerized database

#### Installation Commands (Ubuntu 22.04.5 LTS)

```bash
# Install just (command runner)
curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install pyenv for Python version management
curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
source ~/.bashrc

# Install Python 3.11 via pyenv
pyenv install 3.11.10
pyenv global 3.11.10

# Install Docker Desktop (follow official instructions)
# https://docs.docker.com/desktop/install/ubuntu/
```

> [!NOTE]
> **Why these tools?**
> - **just**: Task runner that simplifies common development commands (like make, but better)
> - **pyenv**: Ensures consistent Python version across environments
> - **Docker Desktop**: Provides containerized PostgreSQL/PostGIS for development

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
  "day": "Monday",
  "period": "Evening",
  "bbox": [-81.8, 30.1, -81.6, 30.3]
}
```

#### Traffic Patterns
```bash
# Get consistently slow links
GET /patterns/slow_links/?period=AM%20Peak&threshold=25.0&min_days=3

# Example with curl
curl "http://localhost:8000/patterns/slow_links/?period=AM%20Peak&threshold=25.0&min_days=3" \
  -H "Accept: application/json"
```

### Example Requests

```bash
# Get Monday evening traffic data
curl "http://localhost:8000/aggregates/?day=Monday&period=Evening"

# Get specific link details
curl "http://localhost:8000/link/1240632857"

# Find links consistently slow during AM Peak (< 25 mph for 3+ days)
curl "http://localhost:8000/patterns/slow_links/?period=AM%20Peak&threshold=25.0&min_days=3"

# Spatial filtering with bounding box
curl -X POST "http://localhost:8000/aggregates/spatial_filter/" \
  -H "Content-Type: application/json" \
  -d '{
    "day": "Monday",
    "period": "Evening",
    "bbox": [-81.8, 30.1, -81.6, 30.3]
  }'
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
