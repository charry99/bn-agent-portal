# 🚀 Quick Reference Guide

## Installation & Running

### **Linux/Mac Setup**
```bash
# 1. Create environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup configuration
cp .env.example .env

# 4. Initialize database
flask init-db

# 5. Run server
python run.py
# OR
flask run
# OR
bash start.sh
```

### **Windows Setup**
```bash
# 1. Create environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup configuration
copy .env.example .env

# 4. Initialize database
flask init-db

# 5. Run server
python run.py
# OR
flask run
# OR
start.bat
```

### **Docker Setup**
```bash
# Start services
docker-compose up -d

# Initialize database
docker-compose exec web flask init-db

# View logs
docker-compose logs -f web

# Stop services
docker-compose down
```

---

## Environment Variables

Edit `.env` file:

```env
FLASK_ENV=development           # development, production, testing
DEBUG=True                      # Debug mode
SECRET_KEY=your-secret-key      # Change in production!
DATABASE_URL=sqlite:///app.db   # SQLite for dev, PostgreSQL for prod
PORT=5000                       # Server port
```

---

## API Endpoints

### **Contact Form (Lead Capture)**
```bash
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "5551234567",
  "message": "Interested in luxury properties"
}

Response:
{
  "success": true,
  "message": "Thank you! We'll contact you soon.",
  "lead_id": 1
}
```

### **Get Properties**
```bash
GET /api/properties?category=residential&page=1&per_page=12

Response:
{
  "success": true,
  "properties": [...],
  "pagination": {
    "page": 1,
    "per_page": 12,
    "total": 25,
    "pages": 3
  }
}
```

### **Get Single Property**
```bash
GET /api/properties/1

Response:
{
  "success": true,
  "property": {...}
}
```

### **Get Statistics**
```bash
GET /api/stats

Response:
{
  "success": true,
  "stats": {
    "total_leads": 42,
    "new_leads": 12,
    "total_properties": 15,
    "featured_properties": 5,
    "leads_this_month": 8
  }
}
```

### **Health Check**
```bash
GET /health

Response:
{
  "status": "healthy",
  "timestamp": "2024-05-01T10:30:00"
}
```

---

## Database Management

```bash
# Initialize database
flask init-db

# Seed with sample data
flask seed-db

# Clear database
flask clear-db

# Database migrations
flask db init        # First time only
flask db migrate -m "Description"
flask db upgrade
flask db downgrade

# Access database shell
flask shell
# >>> from app import db, Lead, Property
# >>> leads = Lead.query.all()
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest test_app.py

# Run specific test
pytest test_app.py::TestContactForm::test_valid_contact_submission

# Run with verbose output
pytest -v

# Run with print statements
pytest -s
```

---

## Code Quality

```bash
# Format code with Black
black app.py config.py

# Check style with Flake8
flake8 app.py config.py

# Sort imports with isort
isort app.py config.py

# All at once
black . && flake8 . && isort .
```

---

## Common Tasks

### **Add a Property**
```python
from app import create_app, db, Property

app = create_app()

with app.app_context():
    prop = Property(
        title="Luxury Home",
        category="luxury",
        price=5000000,
        bedrooms=4,
        bathrooms=3,
        sqft=3500,
        city="New York",
        state="NY",
        featured=True
    )
    db.session.add(prop)
    db.session.commit()
    print(f"Property {prop.id} created!")
```

### **Query Leads**
```python
from app import create_app, db, Lead

app = create_app()

with app.app_context():
    # All leads
    all_leads = Lead.query.all()
    
    # New leads
    new_leads = Lead.query.filter_by(status='new').all()
    
    # By email
    lead = Lead.query.filter_by(email='john@example.com').first()
    
    # Recent leads
    recent = Lead.query.order_by(Lead.created_at.desc()).limit(10).all()
```

### **Update Database**
```python
from app import create_app, db, Property

app = create_app()

with app.app_context():
    prop = Property.query.get(1)
    prop.price = 4500000
    prop.featured = False
    db.session.commit()
```

### **Delete Data**
```python
from app import create_app, db, Lead

app = create_app()

with app.app_context():
    # Delete specific lead
    lead = Lead.query.get(1)
    db.session.delete(lead)
    db.session.commit()
    
    # Delete all leads
    Lead.query.delete()
    db.session.commit()
```

---

## File Locations

| Task | File |
|------|------|
| Add HTML sections | `templates/index.html` |
| Add CSS styles | `static/css/style.css` |
| Add JavaScript | `static/js/main.js` |
| Backend logic | `app.py` |
| Configuration | `config.py` |
| Tests | `test_app.py` |
| Environment | `.env` |
| Dependencies | `requirements.txt` |

---

## Troubleshooting

### **Port Already in Use**
```bash
# Linux/Mac
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### **Database Errors**
```bash
# Reset database
rm instance/agent_portal.db
flask init-db

# Or with Docker
docker-compose exec web rm instance/agent_portal.db
docker-compose exec web flask init-db
```

### **Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Or with fresh environment
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### **Template Not Found**
Make sure your working directory is the project root:
```bash
pwd
# Should show: /path/to/bn-agent-portal

# If not:
cd /path/to/bn-agent-portal
python run.py
```

---

## Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/awesome-feature
   ```

2. **Make Changes**
   - Edit files
   - Test locally
   - Format code

3. **Test Everything**
   ```bash
   pytest
   black .
   flake8 .
   ```

4. **Commit & Push**
   ```bash
   git add .
   git commit -m "Add awesome feature"
   git push origin feature/awesome-feature
   ```

5. **Create Pull Request**
   - Go to GitHub
   - Create PR with description
   - Request review

---

## Production Checklist

- [ ] Update `SECRET_KEY` in `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Set `DEBUG=False`
- [ ] Switch to PostgreSQL
- [ ] Configure `MAIL_SERVER`
- [ ] Enable HTTPS/SSL
- [ ] Setup database backups
- [ ] Configure logging
- [ ] Test all API endpoints
- [ ] Run full test suite
- [ ] Check performance
- [ ] Setup monitoring

---

## Performance Tips

1. **Database Queries**
   - Use `.first()` instead of `.all()` when you need one result
   - Use `.count()` instead of `len(query.all())`
   - Add indexes to frequently queried columns

2. **Frontend**
   - Compress images before uploading
   - Use CDN for static assets
   - Enable browser caching

3. **Caching**
   - Cache property listings
   - Cache statistics
   - Set appropriate TTL

---

## Resources

- 📖 [Flask Documentation](https://flask.palletsprojects.com/)
- 🗄️ [SQLAlchemy Docs](https://docs.sqlalchemy.org/)
- 🎨 [Tailwind CSS](https://tailwindcss.com/)
- 🧪 [Pytest Docs](https://docs.pytest.org/)
- 🐳 [Docker Docs](https://docs.docker.com/)

---

## Need Help?

1. Check [README.md](README.md) for detailed documentation
2. See [CONTRIBUTING.md](CONTRIBUTING.md) for development guide
3. Run tests to validate: `pytest`
4. Check logs: `logs/agent_portal.log`
5. Use Flask shell: `flask shell`

---

**Last Updated: May 2024**
