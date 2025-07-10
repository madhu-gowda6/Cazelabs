# Deployment Guide - Google Drive Access Management Portal

## 🚀 Production Deployment

### Prerequisites
- Python 3.8+
- Google Cloud Project with Drive API enabled
- Gmail account for notifications (optional)
- Web server (Apache/Nginx) for production

### Step 1: Environment Setup

1. **Clone and Setup**:
```bash
git clone <your-repo>
cd google-drive-access-portal
pip install -r requirements.txt
```

2. **Google Cloud Configuration**:
   - Create project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google Drive API and Admin SDK API
   - Create OAuth 2.0 credentials (Web application)
   - Download credentials as `credential.json`
   - Add your domain to authorized origins

3. **Environment Variables**:
```bash
export FLASK_SECRET_KEY="your-super-secure-secret-key"
export FLASK_ENV="production"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/credential.json"
```

### Step 2: Security Configuration

1. **Update Secret Key**:
```python
# In gdapa-v8.py, line 18
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secure-key-here')
```

2. **Configure Email Settings**:
```python
# Update email configuration in gdapa-v8.py
SMTP_SERVER = "smtp.your-domain.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply@your-domain.com"
SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD')
ADMIN_EMAIL = "admin@your-domain.com"
```

3. **Update OAuth Settings**:
   - Add production URL to Google OAuth settings
   - Update redirect URIs in Google Cloud Console

### Step 3: Production Server Setup

#### Option A: Using Gunicorn (Recommended)

1. **Install Gunicorn**:
```bash
pip install gunicorn
```

2. **Create WSGI file** (`wsgi.py`):
```python
from gdapa-v8 import app

if __name__ == "__main__":
    app.run()
```

3. **Run with Gunicorn**:
```bash
gunicorn --bind 0.0.0.0:5004 --workers 4 wsgi:app
```

#### Option B: Using Docker

1. **Create Dockerfile**:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5004

CMD ["gunicorn", "--bind", "0.0.0.0:5004", "--workers", "4", "wsgi:app"]
```

2. **Build and Run**:
```bash
docker build -t drive-portal .
docker run -p 5004:5004 -e FLASK_SECRET_KEY="your-key" drive-portal
```

### Step 4: Nginx Configuration

Create `/etc/nginx/sites-available/drive-portal`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5004;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files (if needed)
    location /static {
        alias /path/to/your/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/drive-portal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: SSL Certificate (Recommended)

Using Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Step 6: Systemd Service

Create `/etc/systemd/system/drive-portal.service`:
```ini
[Unit]
Description=Google Drive Access Portal
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment="PATH=/path/to/your/venv/bin"
Environment="FLASK_SECRET_KEY=your-secret-key"
ExecStart=/path/to/your/venv/bin/gunicorn --bind 127.0.0.1:5004 --workers 4 wsgi:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable drive-portal
sudo systemctl start drive-portal
```

### Step 7: Monitoring and Logs

1. **Log Configuration**:
```python
# Add to gdapa-v8.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/drive-portal.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

2. **Health Check Endpoint**:
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'version': '1.0.0'}, 200
```

### Step 8: Backup Strategy

1. **Database Backup** (if using external DB):
```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
cp /path/to/audit_trail.json /backups/audit_trail_$DATE.json
```

2. **Configuration Backup**:
```bash
# Backup credentials and config
tar -czf config_backup_$DATE.tar.gz credential.json token.json audit_trail.json
```

### Step 9: Security Hardening

1. **Firewall Configuration**:
```bash
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

2. **File Permissions**:
```bash
chmod 600 credential.json
chmod 600 token.json
chmod 644 gdapa-v8.py
```

3. **Regular Updates**:
```bash
# Update dependencies regularly
pip list --outdated
pip install --upgrade package-name
```

### Step 10: Performance Optimization

1. **Database Optimization** (for larger deployments):
   - Consider migrating from JSON files to PostgreSQL/MySQL
   - Implement connection pooling
   - Add database indexing

2. **Caching**:
```python
# Add Redis caching for API responses
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'redis'})

@cache.memoize(timeout=300)
def get_file_permissions(file_id):
    # Cached permission lookup
    pass
```

3. **Load Balancing** (for high traffic):
```nginx
upstream drive_portal {
    server 127.0.0.1:5004;
    server 127.0.0.1:5005;
    server 127.0.0.1:5006;
}

server {
    location / {
        proxy_pass http://drive_portal;
    }
}
```

## 📊 Monitoring Dashboard

Consider implementing:
- **Application Performance Monitoring** (APM)
- **Error Tracking** (Sentry, Rollbar)
- **Uptime Monitoring** (Pingdom, UptimeRobot)
- **Log Analytics** (ELK Stack, Fluentd)

## 🔒 Security Checklist

- [ ] HTTPS enabled with valid SSL certificate
- [ ] Strong secret keys configured
- [ ] OAuth credentials secured
- [ ] File permissions properly set
- [ ] Firewall configured
- [ ] Regular security updates
- [ ] Audit logging enabled
- [ ] Backup strategy implemented
- [ ] Error handling configured
- [ ] Rate limiting implemented (if needed)

## 🚨 Troubleshooting

### Common Issues

1. **OAuth Authentication Errors**:
   - Verify redirect URIs in Google Cloud Console
   - Check credential.json file permissions
   - Ensure APIs are enabled

2. **Permission Denied Errors**:
   - Verify Google Drive API scopes
   - Check service account permissions
   - Validate OAuth consent screen setup

3. **Email Notification Failures**:
   - Verify SMTP settings
   - Check app password for Gmail
   - Test email connectivity

### Log Analysis
```bash
# View application logs
sudo journalctl -u drive-portal -f

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

## 📞 Support

For production deployment support:
- Review application logs in `audit.log`
- Check system logs with `journalctl`
- Monitor resource usage with `htop`
- Test API endpoints with health checks

---

**Production deployment completed! 🎉**
