# E-commerce AI Agent

# 🤖 E-commerce AI Agent with Gemini 2.5 Integration

A powerful AI-driven analytics platform that transforms natural language questions into SQL queries and provides intelligent insights for e-commerce data using Google's Gemini 2.5 API.

## ✨ Features

### 🎯 **Complete Workflow Visualization**
- **Question Processing**: Natural language understanding
- **SQL Generation**: Powered by Google Gemini 2.5 Flash
- **Smart Analytics**: Intelligent data analysis
- **Interactive Charts**: Dynamic Plotly visualizations

### 🚀 **Advanced Capabilities**
- **Real-time Streaming**: Live response generation
- **Multi-table Analysis**: Complex JOIN operations
- **Business Intelligence**: KPIs, RoAS, conversion rates
- **Beautiful Web Interface**: Modern gradient UI
- **API Documentation**: FastAPI with automatic docs

### 📊 **Data Coverage**
- **Product Eligibility**: 4,381 records
- **Ad Sales Performance**: 3,696 campaigns  
- **Total Sales Data**: 702 product records
- **Multi-dimensional Analytics**: 337+ unique products

## 🛠️ Technology Stack

- **Backend**: FastAPI, SQLite, SQLAlchemy
- **AI/ML**: Google Gemini 2.5 API, LangChain
- **Visualization**: Plotly, Chart.js
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Database**: SQLite with optimized schemas

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
Google Gemini API Key
Git
```

### Installation
```bash
# Clone the repository
git clone https://github.com/ashis2004/NapQueen.git
cd NapQueen

# Install dependencies
pip install -r requirements.txt

# Set up your Gemini API key in config.py
# GEMINI_API_KEY = "your-api-key-here"

# Load sample data
python load_real_data.py

# Start the application
python main.py
```

### Usage
1. **Web Interface**: Visit `http://localhost:8000`
2. **API Docs**: Access `http://localhost:8000/docs`
3. **Health Check**: `http://localhost:8000/health`

## 📝 Example Queries

### Basic Analytics
```
"What is my total sales revenue?"
"How much did I spend on advertising?"
"What's my Return on Ad Spend (RoAS)?"
```

### Advanced Analysis
```
"Show me products with high clicks but low conversion rates"
"Which campaigns have the best cost per acquisition?"
"Find underperforming products in high-potential categories"
```

### Business Intelligence
```
"Compare organic sales vs ad-driven sales"
"Which products should increase advertising spend?"
"Show me profitable advertising opportunities"
```

## 🎨 Web Interface

The application features a beautiful, responsive web interface with:
- **Gradient Design**: Modern CSS with smooth animations
- **Real-time Streaming**: Character-by-character response generation
- **Workflow Display**: Question → SQL → Answer → Chart
- **Interactive Charts**: Plotly-powered visualizations
- **Demo Questions**: Pre-built examples for testing

## 🔧 API Endpoints

### Core Endpoints
- `POST /ask` - Ask a question (regular response)
- `POST /ask/stream` - Ask a question (streaming response)  
- `GET /stats` - Database statistics
- `GET /health` - Health check
- `GET /charts/{filename}` - Serve generated charts

### Sample Request
```bash
curl -X POST "http://localhost:8000/ask" 
  -H "Content-Type: application/json" 
  -d '{"question": "What is my total sales?", "include_chart": true}'
```

## 📊 Database Schema

### Tables
- **product_eligibility**: Product advertising eligibility
- **product_ad_sales**: Advertising performance metrics
- **product_total_sales**: Overall sales performance

### Key Metrics
- Sales Revenue: $1,004,904.56
- RoAS: 7.92 (792% return)
- Total Ad Spend: $126,741.18
- Conversion Rates: Up to 23.47%

## 🤖 AI Integration

### Gemini 2.5 Features
- **Natural Language Processing**: Advanced question understanding
- **SQL Generation**: Intelligent query creation
- **Context Awareness**: Business logic integration
- **Fallback System**: Multiple AI provider support

### Query Processing
1. **Question Analysis**: NLP parsing and intent detection
2. **Schema Mapping**: Database structure understanding  
3. **SQL Generation**: Optimized query creation
4. **Result Formatting**: Human-readable responses

## 🔒 Security & Privacy

- **API Key Management**: Secure configuration
- **Input Validation**: SQL injection prevention
- **Error Handling**: Graceful failure management
- **Data Privacy**: Local processing, no external data sharing

## 📈 Performance

- **Response Time**: < 2 seconds average
- **Concurrent Users**: Supports multiple simultaneous queries
- **Database Optimization**: Indexed for fast retrieval
- **Caching**: Intelligent result caching

## 🛠️ Development

### Project Structure
```
NapQueen/
├── src/
│   ├── ai/           # AI and LLM integration
│   ├── api/          # FastAPI routes and endpoints  
│   ├── database/     # Database models and setup
│   ├── utils/        # Utility functions
│   └── visualization/# Chart generation
├── static/           # Web interface files
├── data/            # Database and processed data
├── dataset/         # Raw CSV data files
└── requirements.txt # Python dependencies
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Ashish Kumar**
- GitHub: [@ashis2004](https://github.com/ashis2004)
- Email: ap550083@gmail.com

## 🙏 Acknowledgments

- Google Gemini AI for advanced language processing
- FastAPI for the excellent web framework
- Plotly for beautiful data visualizations
- The open-source community for inspiration

## 🔗 Links

- [Live Demo](http://localhost:8000) (when running locally)
- [API Documentation](http://localhost:8000/docs)
- [GitHub Repository](https://github.com/ashis2004/NapQueen)

---

Made with ❤️ for the e-commerce analytics community

![E-commerce AI Agent](https://img.shields.io/badge/AI-Agent-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi) ![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python) ![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)

## 🎯 Features

- **Natural Language to SQL** conversion using local LLM
- **Real-time Web Interface** with beautiful UI
- **Streaming Responses** with typing effects
- **Interactive Charts** using Plotly
- **Real Business Data** analysis
- **RESTful API** endpoints
- **Local LLM Integration** with Ollama fallback

## 💰 Business Insights

Analyze your e-commerce data:
- **Total Sales Calculations** 
- **RoAS (Return on Ad Spend)** analysis
- **Product Performance** metrics
- **Cost Per Click (CPC)** analysis
- **Advertising Campaign** optimization

## 🚀 Live Demo

Access the web interface at: `http://localhost:8000`

### Sample Questions:
1. **"What is my total sales?"** - Get total revenue analysis
2. **"Calculate the RoAS"** - Performance metrics  
3. **"Which product had the highest CPC?"** - Top performer analysis

## Project Structure

```
NapQueen/
├── data/
│   ├── raw/                    # Original datasets
│   ├── processed/              # Cleaned datasets
│   └── database.db            # SQLite database
├── src/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py          # Database models
│   │   └── setup.py           # Database initialization
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py      # LLM integration
│   │   └── query_processor.py # Query processing logic
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py          # API endpoints
│   │   └── streaming.py       # Streaming responses
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── charts.py          # Chart generation
│   └── utils/
│       ├── __init__.py
│       └── data_loader.py     # Data loading utilities
├── tests/
├── requirements.txt
├── config.py
├── main.py
└── README.md
```

## 🏗️ Setup & Installation

### Prerequisites
- Python 3.8+
- Git

### Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/ecommerce-ai-agent.git
cd ecommerce-ai-agent
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up the database:**
```bash
python update_with_real_data.py
```

4. **Run the application:**
```bash
python main.py
```

5. **Open your browser:** http://localhost:8000

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Web interface |
| `/ask` | POST | Ask questions (JSON response) |
| `/ask/stream` | POST | Ask questions (streaming response) |
| `/health` | GET | Health check |
| `/stats` | GET | Database statistics |
| `/charts/{filename}` | GET | Serve chart files |

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI |
| **Database** | SQLite + SQLAlchemy ORM |
| **AI/LLM** | Ollama + Local LLM + Fallback System |
| **Visualization** | Plotly |
| **Data Processing** | Pandas |
| **Frontend** | HTML5, CSS3, JavaScript |
| **Styling** | Modern CSS with Gradients |

## 📁 Project Structure

```
NapQueen/
├── 📁 src/
│   ├── 🤖 ai/           # LLM integration & query processing
│   ├── 🌐 api/          # FastAPI routes & endpoints  
│   ├── 💾 database/     # SQLAlchemy models & setup
│   ├── 📊 visualization/ # Plotly chart generation
│   └── 🔧 utils/        # Data loading utilities
├── 📁 static/           # Web interface & charts
├── 📁 dataset/          # Real e-commerce CSV data
├── 📁 data/             # SQLite database
├── 📄 requirements.txt  # Python dependencies
├── ⚙️ config.py         # Configuration settings
├── 🚀 main.py          # Application entry point
└── 📋 README.md        # This file
```

## 🔧 Configuration

The application uses a fallback LLM system:
- **Primary**: Ollama with Llama 3.2 (if available)
- **Fallback**: Pattern-based responses for offline use

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -m 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- Plotly for beautiful visualizations
- SQLAlchemy for robust database ORM
- Ollama for local LLM integration
