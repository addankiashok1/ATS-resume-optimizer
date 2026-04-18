# ATS Resume Optimizer Backend

A production-grade SaaS backend for AI-powered resume optimization against job descriptions.

## 🚀 Features

### Implemented Steps
- ✅ **Step 1:** Authentication (Email, Google, LinkedIn, JWT)
- ✅ **Step 2:** Resume Upload & Parsing (PDF/DOCX extraction)
- ✅ **Step 3:** Job Description Analysis (Keyword intelligence)
- ✅ **Step 4:** AI-Based Resume Optimization (Controlled rewriting)

### Core Capabilities
- Secure user authentication with multiple providers
- Intelligent resume parsing and text extraction
- Job description keyword extraction and weighting
- AI-powered resume optimization with hallucination prevention
- ATS-friendly content generation
- RESTful API with FastAPI

## 🛠 Tech Stack

- **Backend:** Python 3.11+, FastAPI
- **Database:** PostgreSQL with SQLAlchemy (async)
- **AI:** OpenAI API (GPT-4o-mini)
- **Authentication:** JWT, OAuth2 (Google/LinkedIn)
- **Parsing:** PyMuPDF (PDF), python-docx (DOCX)
- **NLP:** spaCy for keyword analysis
- **Deployment:** Ready for Docker/Uvicorn

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL database
- OpenAI API key
- Google/LinkedIn OAuth credentials

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/addankiashok1/ATS-resume-optimizer.git
   cd ATS-resume-optimizer/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Fill in your API keys and database URL

5. **Run database migrations:**
   ```bash
   # Using Alembic or manual SQLAlchemy create_all
   python -c "from app.config.database import engine, Base; import asyncio; asyncio.run(engine.run_sync(Base.metadata.create_all))"
   ```

6. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📖 API Documentation

Once running, visit `http://localhost:8000/docs` for interactive Swagger UI.

### Key Endpoints

#### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /auth/google` - Google OAuth
- `GET /auth/linkedin` - LinkedIn OAuth

#### Resume Management
- `POST /resume/upload` - Upload resume (PDF/DOCX)
- `GET /resume/{id}` - Get parsed resume

#### Job Description Analysis
- `POST /jd/analyze` - Analyze job description
- `GET /jd/{id}/keywords` - Get extracted keywords

#### AI Optimization
- `POST /optimize` - Optimize resume against JD

## 🔐 Environment Variables

```env
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ats_resume_optimizer
JWT_SECRET_KEY=your-super-secret-key
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
GOOGLE_CLIENT_ID=your-google-client-id
LINKEDIN_CLIENT_ID=your-linkedin-client-id
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.3
OPENAI_MAX_TOKENS=800
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🚀 Deployment

### Docker
```bash
docker build -t ats-resume-optimizer .
docker run -p 8000:8000 ats-resume-optimizer
```

### Production
- Use Uvicorn with workers: `uvicorn app.main:app --workers 4`
- Set up reverse proxy (nginx)
- Configure SSL certificates
- Use environment-specific configs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues, please open a GitHub issue or contact the maintainers.

---

**Built with ❤️ for job seekers and recruiters**