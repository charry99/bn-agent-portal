# 🚀 Deployment Guide

Complete instructions for deploying the Billions Network Agent Portal to various platforms.

## Table of Contents
1. [Local Development](#local-development)
2. [Docker Deployment](#docker-deployment)
3. [Heroku Deployment](#heroku-deployment)
4. [Traditional Server](#traditional-server)
5. [AWS Deployment](#aws-deployment)
6. [Production Checklist](#production-checklist)

---

## Local Development

### Quick Start
```bash
# Clone repository
git clone <repo-url>
cd bn-agent-portal

# Create environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env

# Database
flask init-db

# Run
python run.py
```

Visit: `http://localhost:5000`

---

## Docker Deployment

### Using Docker Compose (Recommended)

```bash
# 1. Start services
docker-compose up -d

# 2. Initialize database
docker-compose exec web flask init-db

# 3. Seed sample data (optional)
docker-compose exec web flask seed-db

# 4. Access application
# Web: http://localhost:5000
# Database Manager (Adminer): http://localhost:8080

# 5. View logs
docker-compose logs -f web

# 6. Stop services
docker-compose down
```

### Customizing Docker Compose

Edit `docker-compose.yml`:

```yaml
services:
  web:
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-production-key
      - DATABASE_URL=postgresql://user:password@postgres:5432/agent_portal
```

### Build Custom Docker Image

```bash
# Build image
docker build -t bn-agent-portal:latest .

# Run container
docker run -p 5000:5000 \
  -e FLASK_ENV=development \
  -e SECRET_KEY=your-secret \
  bn-agent-portal:latest
```

---

## Heroku Deployment

### Prerequisites
- Heroku account
- Heroku CLI installed

### Step-by-Step

#### 1. Create Heroku App
```bash
heroku create your-app-name
```

#### 2. Set Config Variables
```bash
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set DEBUG=False
```

#### 3. Add Procfile
Create `Procfile`:
```
web: gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 "app:create_app()"
release: flask db upgrade
```

#### 4. Add PostgreSQL Addon
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### 5. Deploy
```bash
git push heroku main
```

#### 6. Run Database Migrations
```bash
heroku run flask init-db
```

#### 7. View Application
```bash
heroku open
```

#### Debugging
```bash
# View logs
heroku logs --tail

# SSH into dyno
heroku ps:exec

# Run shell
heroku run flask shell
```

---

## Traditional Server (Ubuntu/Debian)

### Prerequisites
- Ubuntu 20.04+ or Debian 11+
- Python 3.8+
- Nginx (optional, for reverse proxy)
- Supervisor (for process management)

### Installation

#### 1. SSH into Server
```bash
ssh user@your-server-ip
```

#### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip python3-venv postgresql postgresql-contrib nginx supervisor
```

#### 3. Clone Repository
```bash
cd /var/www
git clone <repo-url> bn-agent-portal
cd bn-agent-portal
```

#### 4. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 6. Configure Database
```bash
# Create PostgreSQL database
sudo -u postgres createdb agent_portal
sudo -u postgres createuser agent_user

# Set password
sudo -u postgres psql
postgres=# ALTER USER agent_user WITH PASSWORD 'secure_password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE agent_portal TO agent_user;
postgres=# \q
```

#### 7. Configure Environment
```bash
cp .env.example .env
# Edit .env
nano .env
```

Set:
```env
FLASK_ENV=production
DEBUG=False
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://agent_user:secure_password@localhost/agent_portal
```

#### 8. Initialize Database
```bash
flask db upgrade
flask init-db
```

#### 9. Configure Gunicorn

Create `wsgi.py`:
```python
import os
from app import create_app

app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()
```

#### 10. Configure Supervisor

Create `/etc/supervisor/conf.d/agent_portal.conf`:
```ini
[program:agent_portal]
directory=/var/www/bn-agent-portal
command=/var/www/bn-agent-portal/venv/bin/gunicorn \
    --workers 4 \
    --bind unix:/var/run/gunicorn.sock \
    --timeout 120 \
    wsgi:app
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/agent_portal.log
```

Reload Supervisor:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start agent_portal
```

#### 11. Configure Nginx

Create `/etc/nginx/sites-available/agent_portal`:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    client_max_body_size 16M;

    location / {
        proxy_pass http://unix:/var/run/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /var/www/bn-agent-portal/static;
        expires 30d;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/agent_portal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 12. Setup SSL with Let's Encrypt
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

#### 13. Verify Deployment
```bash
curl http://localhost
# Should see HTML response
```

#### Monitoring & Logs
```bash
# View service status
sudo supervisorctl status agent_portal

# View logs
tail -f /var/log/agent_portal.log
sudo tail -f /var/log/nginx/error.log

# Restart service
sudo supervisorctl restart agent_portal

# Restart Nginx
sudo systemctl restart nginx
```

---

## AWS Deployment

### Using Elastic Beanstalk

#### 1. Install EB CLI
```bash
pip install awsebcli
```

#### 2. Initialize EB Application
```bash
cd bn-agent-portal
eb init -p python-3.11 agent-portal --region us-east-1
```

#### 3. Create Environment
```bash
eb create production-env --instance-type t3.small --database
```

#### 4. Configure Environment Variables
```bash
eb setenv \
  FLASK_ENV=production \
  SECRET_KEY=your-secret-key \
  DEBUG=False
```

#### 5. Deploy Application
```bash
eb deploy
```

#### 6. Open Application
```bash
eb open
```

#### Monitoring
```bash
# View logs
eb logs

# SSH into instance
eb ssh

# Scale up
eb scale 2
```

### Using EC2 + RDS

Follow the [Traditional Server](#traditional-server) guide, but:

1. Launch EC2 instance (Ubuntu 20.04+)
2. Create RDS PostgreSQL instance
3. Use RDS endpoint in `.env`:
   ```env
   DATABASE_URL=postgresql://user:password@your-rds-endpoint:5432/agent_portal
   ```

---

## Production Checklist

### Security
- [ ] Change `SECRET_KEY` to strong random value
- [ ] Set `DEBUG=False`
- [ ] Set `FLASK_ENV=production`
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Setup rate limiting
- [ ] Enable database backups
- [ ] Rotate database credentials
- [ ] Setup monitoring & alerts

### Performance
- [ ] Use PostgreSQL (not SQLite)
- [ ] Configure connection pooling
- [ ] Enable caching headers
- [ ] Setup CDN for static files
- [ ] Configure Gunicorn workers
- [ ] Monitor database performance
- [ ] Enable slow query logging

### Monitoring
- [ ] Setup error monitoring (Sentry)
- [ ] Configure logging
- [ ] Monitor uptime
- [ ] Track performance metrics
- [ ] Setup email alerts

### Maintenance
- [ ] Automate database backups
- [ ] Plan security updates
- [ ] Document deployment process
- [ ] Create runbooks
- [ ] Setup CI/CD pipeline

### Testing
- [ ] Run full test suite
- [ ] Load test application
- [ ] Test database backup/restore
- [ ] Test SSL certificate renewal
- [ ] Verify error handling

---

## Scaling Strategies

### Horizontal Scaling
```bash
# Multiple Gunicorn workers
gunicorn --workers 8 --bind 0.0.0.0:5000 wsgi:app

# Load balancer configuration
# Configure Nginx upstream with multiple backends
```

### Vertical Scaling
- Increase server resources
- Upgrade database instance
- Increase Gunicorn workers

### Database Optimization
- Add indexes
- Query caching
- Connection pooling
- Read replicas

### Caching
- Redis for session storage
- Cache property listings
- Cache statistics
- Cache API responses

---

## Backup & Recovery

### Database Backup
```bash
# PostgreSQL
pg_dump agent_portal > backup.sql

# Restore
psql agent_portal < backup.sql

# Automated backups with cron
0 2 * * * /usr/local/bin/backup_db.sh
```

### File Backup
```bash
# Backup uploads
tar -czf uploads_backup.tar.gz uploads/

# Backup code
tar -czf code_backup.tar.gz .
```

---

## Troubleshooting

### Application Won't Start
```bash
# Check logs
journalctl -u agent_portal -n 50

# Test Python
python -c "import app; print('OK')"

# Check dependencies
pip list | grep -i flask
```

### Database Connection Failed
```bash
# Test connection
psql postgresql://user:password@localhost/agent_portal

# Check credentials in .env
cat .env | grep DATABASE

# Restart database
sudo systemctl restart postgresql
```

### Nginx Error
```bash
# Test configuration
sudo nginx -t

# Check logs
sudo tail -f /var/log/nginx/error.log

# Restart
sudo systemctl restart nginx
```

### High Memory Usage
```bash
# Check processes
ps aux | grep gunicorn

# Reduce workers
# Edit Supervisor config, reduce workers from 8 to 4
```

---

## Monitoring & Logging

### Application Logs
```bash
# Docker
docker-compose logs -f web

# Traditional Server
tail -f /var/log/agent_portal.log

# Heroku
heroku logs --tail
```

### Performance Monitoring
```bash
# Monitor process
top -p $(pgrep -f gunicorn)

# Monitor disk
df -h

# Monitor memory
free -h
```

---

## Continuous Deployment

### GitHub Actions Example
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to server
        run: |
          ssh -i ${{ secrets.DEPLOY_KEY }} user@server
          cd /var/www/bn-agent-portal
          git pull origin main
          source venv/bin/activate
          pip install -r requirements.txt
          flask db upgrade
          sudo supervisorctl restart agent_portal
```

---

## Support

For deployment issues:
1. Check [README.md](README.md)
2. Review application logs
3. Check database connectivity
4. Verify environment variables
5. Test with simpler configuration

---

**Last Updated: May 2024**
