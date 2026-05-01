"""
Billions Network Agent Portal - Flask Backend
Professional real estate agent website with lead capture
"""

import os
import json
import re
from datetime import datetime
from functools import wraps
from pathlib import Path

from flask import Flask, render_template, jsonify, request, current_app, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import func
import logging

# Import configuration from config.py
from config import get_config, Config, DevelopmentConfig, ProductionConfig, TestingConfig


# ========================================
# APPLICATION FACTORY
# ========================================

def create_app(config_name='development'):
    """Create and configure Flask application"""
    
    # Create Flask app
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    # Load configuration from config module
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)
    
    # Initialize configuration
    config_obj.init_app(app)
    
    # Ensure upload folder exists (but don't fail on read-only filesystems)
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except (OSError, PermissionError):
        # Silently ignore on read-only filesystems
        pass
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})
    
    # Setup logging
    setup_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Error handlers
    register_error_handlers(app)
    
    # CLI commands
    register_cli_commands(app)
    
    # Create tables
    with app.app_context():
        db.create_all()

    # Optionally start background scheduler when explicitly enabled
    if os.environ.get('START_SCHEDULER', 'false').lower() == 'true':
        try:
            from tasks import start_scheduler
            start_scheduler(app)
        except Exception as e:
            app.logger.exception('Failed to start background scheduler')
    
    return app


# ========================================
# DATABASE INITIALIZATION
# ========================================

db = SQLAlchemy()


# ========================================
# DATABASE MODELS
# ========================================

class Lead(db.Model):
    """Lead/Contact model for form submissions"""
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new', index=True)  # new, contacted, converted
    source = db.Column(db.String(50), default='contact_form')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    notes = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Lead {self.name} - {self.email}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'status': self.status,
            'source': self.source,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'notes': self.notes
        }


class Property(db.Model):
    """Property listing model"""
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # residential, commercial, luxury
    bedrooms = db.Column(db.Integer, default=0)
    bathrooms = db.Column(db.Float, default=0)
    sqft = db.Column(db.Integer, default=0)
    address = db.Column(db.String(255))
    city = db.Column(db.String(100), index=True)
    state = db.Column(db.String(2))
    zip_code = db.Column(db.String(10))
    image_url = db.Column(db.String(500))
    featured = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Property {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'sqft': self.sqft,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'zip_code': self.zip_code,
            'image_url': self.image_url,
            'featured': self.featured,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


# ========================================
# BLUEPRINTS
# ========================================

def register_blueprints(app):
    """Register Flask blueprints"""
    from flask import Blueprint
    
    # Main routes blueprint
    main_bp = Blueprint('main', __name__)
    
    @main_bp.route('/')
    def index():
        """Render homepage"""
        return render_template('index.html')
    
    @main_bp.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})
    
    @main_bp.route('/verify')
    def verify_page():
        """Render a local agent verification page"""
        agent_info = app.config['AGENT_INFO']
        return render_template('verify.html', agent=agent_info)
    
    # API routes blueprint
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    
    @api_bp.route('/contact', methods=['POST'])
    def submit_contact():
        """Handle contact form submission"""
        try:
            data = request.get_json(silent=True)
            if not data:
                data = request.form.to_dict()
            
            # Validate input
            errors = validate_contact_form(data)
            if errors:
                return jsonify({'success': False, 'message': errors[0]}), 400
            
            # Create lead
            lead = Lead(
                name=data['name'].strip(),
                email=data['email'].strip().lower(),
                phone=data['phone'].strip(),
                message=data['message'].strip(),
                source='contact_form'
            )
            
            db.session.add(lead)
            db.session.commit()
            
            current_app.logger.info(f"New lead created: {lead.email}")
            
            return jsonify({
                'success': True,
                'message': 'Thank you! We\'ll contact you soon.',
                'lead_id': lead.id
            }), 201
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error processing contact form: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'An error occurred. Please try again later.'
            }), 500
    
    @api_bp.route('/properties', methods=['GET'])
    def get_properties():
        """Get all properties with optional filters"""
        try:
            category = request.args.get('category')
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 12, type=int)
            
            query = Property.query.filter_by(active=True)
            
            if category and category != 'all':
                query = query.filter_by(category=category)
            
            paginated = query.paginate(page=page, per_page=per_page)
            
            return jsonify({
                'success': True,
                'properties': [prop.to_dict() for prop in paginated.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': paginated.total,
                    'pages': paginated.pages
                }
            }), 200
            
        except Exception as e:
            current_app.logger.error(f"Error fetching properties: {str(e)}")
            return jsonify({'success': False, 'message': 'Error fetching properties'}), 500
    
    @api_bp.route('/properties/<int:property_id>', methods=['GET'])
    def get_property(property_id):
        """Get specific property"""
        try:
            prop = Property.query.get_or_404(property_id)
            return jsonify({'success': True, 'property': prop.to_dict()}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Property not found'}), 404
    
    @api_bp.route('/stats', methods=['GET'])
    def get_stats():
        """Get portal statistics"""
        try:
            stats = {
                'total_leads': Lead.query.count(),
                'new_leads': Lead.query.filter_by(status='new').count(),
                'total_properties': Property.query.filter_by(active=True).count(),
                'featured_properties': Property.query.filter_by(featured=True, active=True).count(),
                'leads_this_month': Lead.query.filter(
                    func.strftime('%Y-%m', Lead.created_at) == datetime.now().strftime('%Y-%m')
                ).count()
            }
            return jsonify({'success': True, 'stats': stats}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error fetching stats'}), 500
    
    @api_bp.route('/verify', methods=['GET'])
    def verify_agent():
        """Get agent verification information"""
        try:
            agent_info = {
                'did': app.config['AGENT_INFO']['agent_did'],
                'city': app.config['AGENT_INFO']['city'],
                'network': app.config['AGENT_INFO']['network'],
                'verified': True,
                'verification_url': url_for('main.verify_page', _external=True)
            }
            return jsonify({'success': True, 'agent': agent_info}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': 'Error fetching agent verification'}), 500

    @api_bp.route('/checkin', methods=['GET', 'POST'])
    def api_checkin():
        from tasks import daily_checkin
        daily_checkin()
        return {"status": "ok", "task": "checkin", "time": str(datetime.now())}

    @api_bp.route('/post-listings', methods=['GET', 'POST'])
    def api_post_listings():
        from tasks import auto_post_listings
        auto_post_listings()
        return {"status": "ok", "task": "post_listings"}

    @api_bp.route('/send-messages', methods=['GET', 'POST'])
    def api_send_messages():
        from tasks import auto_send_messages
        auto_send_messages()
        return {"status": "ok", "task": "send_messages"}

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)


# ========================================
# VALIDATION FUNCTIONS
# ========================================

def validate_contact_form(data):
    """Validate contact form data"""
    errors = []
    
    if not data:
        return ['No data provided']
    
    # Validate name
    if not data.get('name', '').strip():
        errors.append('Name is required')
    elif len(data['name']) > 120:
        errors.append('Name is too long')
    
    # Validate email
    email = data.get('email', '').strip()
    if not email:
        errors.append('Email is required')
    elif not is_valid_email(email):
        errors.append('Please enter a valid email address')
    
    # Validate phone
    phone = data.get('phone', '').strip()
    if not phone:
        errors.append('Phone number is required')
    elif not is_valid_phone(phone):
        errors.append('Please enter a valid phone number')
    
    # Validate message
    message = data.get('message', '').strip()
    if not message:
        errors.append('Message is required')
    elif len(message) < 10:
        errors.append('Message must be at least 10 characters')
    elif len(message) > 5000:
        errors.append('Message is too long')
    
    return errors


def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def is_valid_phone(phone):
    """Validate phone number format"""
    # Remove non-digit characters and check length
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10


# ========================================
# ERROR HANDLERS
# ========================================

def register_error_handlers(app):
    """Register error handlers"""
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400


# ========================================
# LOGGING SETUP
# ========================================

def setup_logging(app):
    """Setup application logging"""
    if not app.debug:
        try:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = logging.FileHandler('logs/agent_portal.log')
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('Agent Portal startup')
        except (OSError, PermissionError):
            # Silently skip file logging on read-only filesystems
            pass


# ========================================
# CLI COMMANDS
# ========================================

def register_cli_commands(app):
    """Register CLI commands"""
    
    @app.cli.command()
    def init_db():
        """Initialize the database"""
        db.create_all()
        print('Database initialized successfully!')
    
    @app.cli.command()
    def seed_db():
        """Seed database with sample data"""
        from datetime import datetime
        
        # Check if already seeded
        if Property.query.first() is not None:
            print('Database already contains data!')
            return
        
        # Sample properties
        sample_properties = [
            Property(
                title="Luxury Penthouse Manhattan",
                category="luxury",
                price=12500000,
                bedrooms=4,
                bathrooms=3,
                sqft=3500,
                address="123 Park Avenue",
                city="New York",
                state="NY",
                zip_code="10016",
                image_url="https://images.unsplash.com/photo-1512917774080-9991f1c52dbe",
                featured=True,
                description="Stunning luxury penthouse with breathtaking city views"
            ),
            Property(
                title="Modern Downtown Apartment",
                category="residential",
                price=2800000,
                bedrooms=3,
                bathrooms=2,
                sqft=1800,
                address="456 Broadway",
                city="New York",
                state="NY",
                zip_code="10013",
                image_url="https://images.unsplash.com/photo-1545321503-63ab60ceac42",
                featured=True,
                description="Contemporary apartment in vibrant downtown location"
            ),
            Property(
                title="Premium Office Space",
                category="commercial",
                price=5500000,
                bedrooms=0,
                bathrooms=4,
                sqft=8500,
                address="789 5th Avenue",
                city="New York",
                state="NY",
                zip_code="10022",
                image_url="https://images.unsplash.com/photo-1497366216548-37526070297c",
                featured=False,
                description="State-of-the-art office complex perfect for businesses"
            ),
        ]
        
        db.session.add_all(sample_properties)
        db.session.commit()
        print('Database seeded successfully!')
    
    @app.cli.command()
    def clear_db():
        """Clear the database"""
        if input('Are you sure? (yes/no): ').lower() == 'yes':
            db.drop_all()
            print('Database cleared!')
        else:
            print('Cancelled.')

    @app.cli.command()
    def run_scheduler():
        """Start the background task scheduler."""
        from tasks import start_scheduler
        start_scheduler(app)
        print('Background scheduler started.')


# ========================================
# WSGI APPLICATION
# ========================================

# Create top-level app for WSGI servers and Vercel
app = create_app(os.environ.get('FLASK_ENV', 'development'))
application = app
handler = app

# ========================================
# MAIN
# ========================================

if __name__ == '__main__':
    scheduler = start_scheduler()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )
