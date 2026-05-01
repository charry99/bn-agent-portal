# Billions Network Agent Portal

A professional, production-ready real estate agent website built with modern web technologies. Designed specifically for Billions Network agents to showcase properties, capture leads, and manage client relationships.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![SQLite/PostgreSQL](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Features

### Frontend Features
- ✨ **Responsive Design** - Works perfectly on desktop, tablet, and mobile
- 🎨 **Professional Aesthetics** - Millions Network brand colors (Navy Blue & Gold)
- 🏠 **Property Showcase** - Beautifully displayed property cards with filtering
- 📸 **Image Integration** - High-quality placeholder images via Unsplash API
- ⚡ **Smooth Animations** - AOS (Animate On Scroll) for engaging user experience
- 🔍 **Advanced Filters** - Filter properties by category (Residential, Commercial, Luxury)
- 📱 **Mobile Menu** - Responsive navigation for all devices
- 🎯 **Lead Capture Form** - Professional contact form with validation

### Backend Features
- 🗄️ **Database Management** - SQLite (development) or PostgreSQL (production)
- 👤 **Lead Management** - Store and track all contact submissions
- 📊 **Property Management** - Full CRUD operations for property listings
- 🔐 **Data Validation** - Comprehensive input validation and sanitization
- 📈 **Statistics API** - Real-time portal statistics and metrics
- 🛡️ **Error Handling** - Robust error management and logging
- ⚙️ **Configuration Management** - Environment-based configurations
- 📝 **Logging** - Detailed application logging for debugging

### Developer Experience
- 📚 **Well-Documented** - Comprehensive inline code documentation
- 🧪 **Easy to Customize** - Clean, modular code structure
- 🚀 **CLI Commands** - Helpful management commands
- 🔧 **Development Tools** - Pre-configured for easy development
- 📦 **Database Migrations** - Flask-Migrate for version control

## 📋 Tech Stack

### Frontend
- **HTML5** - Semantic markup and SEO-friendly structure
- **CSS3** - Custom styling with Tailwind CSS utility classes
- **Vanilla JavaScript** - No framework, pure JavaScript for better performance
- **Tailwind CSS** - Rapid UI development with utility-first CSS
- **AOS Library** - Scroll animations and effects
- **Font Awesome** - Icon library for UI elements

### Backend
- **Flask** - Lightweight Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Flask-Migrate** - Database migration management
- **Gunicorn** - Production WSGI server

### Database
- **SQLite** - Development and testing (file-based)
- **PostgreSQL** - Production database (recommended)

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)
- Modern web browser

### Installation

#### 1. Clone the Repository
```bash
git clone <repository-url>
cd bn-agent-portal
```

#### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment
Create a `.env` file in the root directory:
```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# Database (optional, uses SQLite by default)
DATABASE_URL=sqlite:///agent_portal.db

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Email Configuration (optional, for future email notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-password
```

#### 5. Initialize Database
```bash
# Create tables
flask db init
flask db migrate
flask db upgrade

# Or manually create tables
flask init-db

# Optional: Seed with sample data
flask seed-db
```

#### 6. Run Development Server
```bash
flask run
```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
bn-agent-portal/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                           # Environment configuration (create this)
├── .gitignore                     # Git ignore rules
├── README.md                      # This file
│
├── templates/
│   └── index.html                 # Main website template
│
├── static/
│   ├── css/
│   │   └── style.css              # Custom styling
│   ├── js/
│   │   └── main.js                # JavaScript functionality
│   └── images/                    # Image assets
│
├── database/
│   └── models.py                  # SQLAlchemy models
│
├── logs/                          # Application logs (auto-created)
├── uploads/                       # User uploads (auto-created)
└── venv/                          # Virtual environment (auto-created)
```

## 🎨 Customization

### Update Agent Information
Edit `/templates/index.html` and search for:
- Agent name and tagline (hero section)
- Agent photo (replace Unsplash URLs)
- Contact information (phone, email, address)
- Social media links
- Custom statistics

### Brand Colors
The site uses these primary colors (edit in `static/css/style.css`):
- Primary Blue: `#1E3A8A` (navy blue)
- Accent Gold: `#EAB308` (gold)
- Secondary Blue: `#3B82F6` (light blue)

### Add Properties
Edit property data in `static/js/main.js` in the `properties` array, or use the API:

```python
# In Flask shell or app context
from app import db, Property

property = Property(
    title="Your Property Title",
    category="residential",  # or "commercial", "luxury"
    price=2500000,
    bedrooms=3,
    bathrooms=2,
    sqft=1800,
    address="123 Main St",
    city="New York",
    state="NY",
    zip_code="10001",
    image_url="https://images.unsplash.com/...",
    featured=True
)
db.session.add(property)
db.session.commit()
```

### Modify Contact Form
The contact form validates:
- Name: 1-120 characters
- Email: Valid email format
- Phone: At least 10 digits
- Message: 10-5000 characters

Customize validation in `app.py` in the `validate_contact_form()` function.

## 🔌 API Endpoints

### Contact & Leads
**POST** `/api/contact`
- Submit contact form
- Body: `{name, email, phone, message}`
- Response: `{success, message, lead_id}`

### Properties
**GET** `/api/properties`
- Get all properties with filters
- Query params: `category`, `page`, `per_page`
- Response: `{success, properties[], pagination}`

**GET** `/api/properties/<id>`
- Get specific property
- Response: `{success, property}`

### Statistics
**GET** `/api/stats`
- Get portal statistics
- Response: `{success, stats{...}}`

### Health Check
**GET** `/health`
- Check if server is running
- Response: `{status, timestamp}`

## 🗄️ Database Schema

### Leads Table
```sql
CREATE TABLE leads (
    id INTEGER PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    message TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'new',  -- new, contacted, converted
    source VARCHAR(50) DEFAULT 'contact_form',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
```

### Properties Table
```sql
CREATE TABLE properties (
    id INTEGER PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    price FLOAT NOT NULL,
    category VARCHAR(50) NOT NULL,
    bedrooms INTEGER DEFAULT 0,
    bathrooms FLOAT DEFAULT 0,
    sqft INTEGER DEFAULT 0,
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(2),
    zip_code VARCHAR(10),
    image_url VARCHAR(500),
    featured BOOLEAN DEFAULT FALSE,
    active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🚢 Deployment

### Heroku Deployment
```bash
# 1. Create Heroku app
heroku create your-app-name

# 2. Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key

# 3. Deploy
git push heroku main
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]
```

Build and run:
```bash
docker build -t bn-agent-portal .
docker run -p 5000:5000 bn-agent-portal
```

### Production Checklist
- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `FLASK_ENV=production`
- [ ] Use PostgreSQL database
- [ ] Enable HTTPS/SSL
- [ ] Configure proper logging
- [ ] Set up regular database backups
- [ ] Enable error monitoring (Sentry)
- [ ] Configure CDN for static files
- [ ] Set up email notifications for leads
- [ ] Enable rate limiting on API endpoints

## 🧪 Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=.
```

## 🛠️ CLI Commands

```bash
# Initialize database
flask init-db

# Seed database with sample data
flask seed-db

# Clear database
flask clear-db

# Run development server
flask run

# Open Python shell with app context
flask shell
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Linux/Mac: Find process on port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or use different port
flask run --port 5001
```

### Database Errors
```bash
# Reset database
rm agent_portal.db
flask init-db
```

### Import Errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Create fresh environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 Performance Optimization

### Frontend Optimizations
- Lazy loading images with Intersection Observer
- Minified CSS and JavaScript
- Tailwind CSS purging unused styles
- Image optimization via Unsplash API
- Browser caching via HTTP headers

### Backend Optimizations
- Database query indexing
- SQLAlchemy query optimization
- Gzip compression for responses
- Connection pooling for database
- Production WSGI server (Gunicorn)

## 🔐 Security Features

- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Secure headers
- HTTPS enforcement (production)
- Rate limiting ready
- CSRF protection ready
- SQL Alchemy parameterized queries

## 📝 Code Style

The codebase follows:
- **Python**: PEP 8 style guide
- **JavaScript**: ES6+ standards
- **HTML/CSS**: Semantic markup and utility-first CSS

Format code:
```bash
black app.py
flake8 app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support & Contact

For issues, questions, or feature requests:
- Email: support@billionsnetwork.com
- Website: https://billionsnetwork.com
- GitHub Issues: [Create an issue](../../issues)

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Tailwind CSS](https://tailwindcss.com/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript/)

## 🚀 Future Enhancements

- [ ] User authentication and agent profiles
- [ ] Advanced property search with map integration
- [ ] Virtual property tours (360° images/video)
- [ ] Automated email notifications for leads
- [ ] Client portal for managing properties
- [ ] CRM integration
- [ ] SMS notifications
- [ ] Property comparison tool
- [ ] Market analysis dashboard
- [ ] Mobile app (React Native)

## 📈 Version History

### v1.0.0 (Current)
- Initial release
- Hero section with agent information
- Property listings with filtering
- Contact form with lead capture
- Responsive design
- Professional styling
- SEO-friendly structure

---

**Made with ❤️ for Billions Network Agents**

*Last Updated: May 2024*
