# E-commerce AI Agent - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Quick Start](#quick-start)
3. [Architecture](#architecture)
4. [API Documentation](#api-documentation)
5. [Database Schema](#database-schema)
6. [Configuration](#configuration)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Project Overview

The E-commerce AI Agent is a sophisticated system that answers natural language questions about e-commerce data by converting them to SQL queries and providing visual responses.

### Key Features
- 🤖 **Natural Language Processing**: Convert questions to SQL using local LLM
- 📊 **Data Visualization**: Generate charts and graphs for query results
- 🔄 **Streaming Responses**: Real-time typing effect for better UX
- 🗄️ **SQLite Database**: Efficient data storage and querying
- 🚀 **REST API**: Easy integration with web applications
- 📈 **Business Metrics**: RoAS, CPC, conversion rates, and more

### Sample Questions Supported
- "What is my total sales?"
- "Calculate the RoAS (Return on Ad Spend)"
- "Which product had the highest CPC (Cost Per Click)?"
- "Show me the top performing products"
- "What is the average conversion rate?"

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- (Optional) Ollama with Llama 3.2 model for enhanced AI capabilities

### Installation

1. **Clone or download the project**:
   ```bash
   cd c:\21MIP\LLM\NapQueen
   ```

2. **Run the setup script**:
   ```bash
   python setup.py
   ```
   This will:
   - Install all dependencies
   - Create necessary directories
   - Initialize the database
   - Load sample data
   - Optionally set up Ollama

3. **Start the server**:
   ```bash
   python main.py
   ```
   Or use the convenient scripts:
   - Windows: `run_server.bat`
   - PowerShell: `run_server.ps1`

4. **Test the API**:
   ```bash
   python test_api.py
   ```

### Quick API Test
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is my total sales?", "include_chart": true}'
```

## Architecture

### System Components

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI       │    │   Query          │    │   SQLite        │
│   Web Server    │◄──►│   Processor      │◄──►│   Database      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                        │                       
         ▼                        ▼                       
┌─────────────────┐    ┌──────────────────┐              
│   Streaming     │    │   LLM Client     │              
│   Responses     │    │   (Ollama)       │              
└─────────────────┘    └──────────────────┘              
         │                                                
         ▼                                                
┌─────────────────┐                                      
│   Chart         │                                      
│   Generator     │                                      
└─────────────────┘                                      
```

### Directory Structure
```
NapQueen/
├── src/                        # Source code
│   ├── api/                   # API endpoints and routing
│   │   ├── routes.py          # Main API routes
│   │   └── streaming.py       # Streaming response handlers
│   ├── ai/                    # AI and LLM integration
│   │   ├── llm_client.py      # LLM client (Ollama)
│   │   └── query_processor.py # Natural language to SQL
│   ├── database/              # Database models and setup
│   │   ├── models.py          # SQLAlchemy models
│   │   └── setup.py           # Database initialization
│   ├── visualization/         # Chart generation
│   │   └── charts.py          # Plotly chart creation
│   └── utils/                 # Utility functions
│       └── data_loader.py     # Data loading and processing
├── data/                      # Data files
│   ├── raw/                   # Original CSV files
│   ├── processed/             # Cleaned data
│   └── database.db            # SQLite database
├── static/                    # Static files (charts)
│   └── charts/                # Generated chart files
├── tests/                     # Test files
├── main.py                    # Application entry point
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
└── setup.py                   # Setup script
```

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /health
```
**Response**:
```json
{
  "status": "healthy",
  "database": "connected",
  "products_in_db": 20,
  "llm_available": true
}
```

#### 2. Database Statistics
```http
GET /stats
```
**Response**:
```json
{
  "tables": {
    "product_eligibility": 20,
    "product_ad_sales": 16,
    "product_total_sales": 20
  },
  "metrics": {
    "total_sales": 125000.00,
    "total_ad_spend": 8500.00,
    "estimated_roas": 14.71
  }
}
```

#### 3. Ask Question
```http
POST /ask
```
**Request Body**:
```json
{
  "question": "What is my total sales?",
  "include_chart": true
}
```
**Response**:
```json
{
  "answer": "The total sales amount is $125,000.00",
  "data": [{"total_sales": 125000.00}],
  "query": "SELECT SUM(total_sales) as total_sales FROM product_total_sales",
  "success": true,
  "chart_url": "/static/charts/sales_chart_20250722_143052.html"
}
```

#### 4. Streaming Question
```http
POST /ask/stream
```
**Request Body**: Same as `/ask`
**Response**: Server-Sent Events (SSE) stream
```
data: {"content": "The", "done": false}
data: {"content": " total", "done": false}
data: {"content": " sales", "done": false}
...
data: {"done": true, "data": [...], "query": "..."}
```

#### 5. Sample Questions
```http
GET /sample-questions
```
**Response**:
```json
{
  "sample_questions": [
    "What is my total sales?",
    "Calculate the RoAS (Return on Ad Spend)",
    "Which product had the highest CPC (Cost Per Click)?",
    ...
  ]
}
```

### Interactive Documentation
Visit `http://localhost:8000/docs` for Swagger UI documentation with interactive testing.

## Database Schema

### Table: product_eligibility
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| product_id | TEXT | Unique product identifier |
| product_name | TEXT | Product name |
| category | TEXT | Product category |
| subcategory | TEXT | Product subcategory |
| brand | TEXT | Product brand |
| is_eligible_for_ads | INTEGER | 1 if eligible, 0 otherwise |
| eligibility_reason | TEXT | Reason for eligibility status |
| created_at | DATETIME | Record creation timestamp |

### Table: product_ad_sales
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| product_id | TEXT | Product identifier |
| campaign_name | TEXT | Advertising campaign name |
| ad_spend | REAL | Amount spent on advertising |
| impressions | INTEGER | Number of ad impressions |
| clicks | INTEGER | Number of ad clicks |
| ctr | REAL | Click-through rate (%) |
| cpc | REAL | Cost per click |
| ad_sales | REAL | Sales generated from ads |
| ad_orders | INTEGER | Orders from ads |
| conversion_rate | REAL | Conversion rate (%) |
| acos | REAL | Advertising Cost of Sales (%) |
| date_reported | DATETIME | Report date |
| created_at | DATETIME | Record creation timestamp |

### Table: product_total_sales
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| product_id | TEXT | Product identifier |
| total_sales | REAL | Total sales amount |
| total_orders | INTEGER | Total number of orders |
| organic_sales | REAL | Sales not from ads |
| organic_orders | INTEGER | Orders not from ads |
| sessions | INTEGER | Product page sessions |
| session_percentage | REAL | Session percentage |
| page_views | INTEGER | Number of page views |
| page_view_percentage | REAL | Page view percentage |
| buy_box_percentage | REAL | Buy box percentage |
| date_reported | DATETIME | Report date |
| created_at | DATETIME | Record creation timestamp |

### Key Relationships
- All tables are linked by `product_id`
- Products in `product_eligibility` may have corresponding records in sales tables
- Only eligible products (where `is_eligible_for_ads = 1`) should have ad sales data

## Configuration

### Environment Variables
You can create a `.env` file to override default configurations:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Configuration
LLM_MODEL=llama3.2
LLM_BASE_URL=http://localhost:11434

# Database Configuration
DATABASE_PATH=data/database.db
```

### Configuration Options (config.py)
```python
# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "database.db"

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000

# LLM Configuration
LLM_MODEL = "llama3.2"
LLM_BASE_URL = "http://localhost:11434"
```

## Testing

### Automated Testing
Run the comprehensive test suite:
```bash
python test_api.py
```

This will test:
- Health endpoint
- Statistics endpoint
- All required questions
- Streaming functionality
- Chart generation

### Manual Testing

#### 1. Basic Health Check
```bash
curl http://localhost:8000/health
```

#### 2. Test Required Questions
```bash
# Total Sales
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is my total sales?"}'

# RoAS Calculation
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Calculate the RoAS (Return on Ad Spend)"}'

# Highest CPC
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which product had the highest CPC?"}'
```

#### 3. Test with Charts
```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me top products by sales", "include_chart": true}'
```

### Load Your Own Data

1. **Place CSV files** in `data/raw/` directory with these names:
   - `product_eligibility.csv`
   - `product_ad_sales.csv`
   - `product_total_sales.csv`

2. **Load the data**:
   ```bash
   python load_data.py
   ```

3. **Verify data loading**:
   ```bash
   curl http://localhost:8000/stats
   ```

## Deployment

### Local Development
```bash
python main.py
```

### Production Deployment

#### Using Gunicorn (Linux/Mac)
```bash
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker src.api.routes:app --bind 0.0.0.0:8000
```

#### Using Docker
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python", "main.py"]
```

#### Environment Considerations
- **Database**: For production, consider PostgreSQL or MySQL instead of SQLite
- **LLM**: Ensure Ollama service is running and accessible
- **Scaling**: Use load balancers for multiple instances
- **Security**: Add authentication and rate limiting

## Troubleshooting

### Common Issues

#### 1. "Import sqlalchemy could not be resolved"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

#### 2. "LLM not available" or "Ollama connection failed"
**Solutions**:
- Install Ollama: https://ollama.ai/download
- Pull model: `ollama pull llama3.2`
- Start Ollama service
- Check if running: `ollama list`

#### 3. "Database file not found"
**Solution**: Initialize database
```bash
python -c "from src.database.setup import initialize_database; initialize_database()"
```

#### 4. "No module named 'src'"
**Solution**: Run from project root directory
```bash
cd c:\21MIP\LLM\NapQueen
python main.py
```

#### 5. Port 8000 already in use
**Solutions**:
- Change port in `config.py`
- Kill existing process: `netstat -ano | findstr :8000`
- Use different port: `python main.py --port 8001`

#### 6. Charts not generating
**Solutions**:
- Install kaleido: `pip install kaleido`
- Check static/charts directory permissions
- Verify plotly installation: `pip install plotly`

### Performance Issues

#### Slow Response Times
- Check database size and add indexes
- Monitor LLM response time
- Consider caching frequent queries

#### Memory Usage
- Monitor database connections
- Limit chart generation
- Use pagination for large results

### Debugging

#### Enable Debug Mode
Add to `config.py`:
```python
DEBUG = True
LOG_LEVEL = "debug"
```

#### View Logs
```bash
python main.py > app.log 2>&1
```

#### Database Debugging
```python
from src.database.models import engine
engine.echo = True  # Enable SQL logging
```

### Support

For issues not covered here:
1. Check the project's GitHub issues
2. Review the API documentation at `/docs`
3. Verify all dependencies are installed correctly
4. Ensure Ollama is properly configured

## License

This project is provided for educational and demonstration purposes.

---

*Happy coding! 🚀*
