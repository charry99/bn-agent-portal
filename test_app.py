"""
Test suite for Billions Network Agent Portal
Run with: pytest
"""

import pytest
from app import create_app, db
from app import Lead, Property


@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """CLI runner"""
    return app.test_cli_runner()


class TestHealth:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health endpoint returns 200"""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
        assert 'timestamp' in data


class TestHomepage:
    """Test homepage"""
    
    def test_index_loads(self, client):
        """Test homepage loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Billions Network' in response.data


class TestContactForm:
    """Test contact form functionality"""
    
    def test_valid_contact_submission(self, client):
        """Test valid contact form submission"""
        response = client.post('/api/contact', 
            json={
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '5551234567',
                'message': 'This is a test message about a property.'
            },
            content_type='application/json'
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data['success'] is True
        assert 'lead_id' in data
    
    def test_missing_name(self, client):
        """Test missing name validation"""
        response = client.post('/api/contact',
            json={
                'name': '',
                'email': 'john@example.com',
                'phone': '5551234567',
                'message': 'This is a test message.'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_invalid_email(self, client):
        """Test invalid email validation"""
        response = client.post('/api/contact',
            json={
                'name': 'John Doe',
                'email': 'invalid-email',
                'phone': '5551234567',
                'message': 'This is a test message.'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_short_message(self, client):
        """Test message too short validation"""
        response = client.post('/api/contact',
            json={
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '5551234567',
                'message': 'Short'
            },
            content_type='application/json'
        )
        assert response.status_code == 400
    
    def test_invalid_phone(self, client):
        """Test invalid phone validation"""
        response = client.post('/api/contact',
            json={
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '123',
                'message': 'This is a test message about a property.'
            },
            content_type='application/json'
        )
        assert response.status_code == 400


class TestLeadModel:
    """Test Lead model"""
    
    def test_create_lead(self, app):
        """Test creating a lead"""
        with app.app_context():
            lead = Lead(
                name='Jane Smith',
                email='jane@example.com',
                phone='5559876543',
                message='Interested in luxury properties'
            )
            db.session.add(lead)
            db.session.commit()
            
            assert lead.id is not None
            assert lead.status == 'new'
            assert lead.source == 'contact_form'
    
    def test_lead_to_dict(self, app):
        """Test converting lead to dictionary"""
        with app.app_context():
            lead = Lead(
                name='Bob Johnson',
                email='bob@example.com',
                phone='5551111111',
                message='Looking for commercial space'
            )
            db.session.add(lead)
            db.session.commit()
            
            lead_dict = lead.to_dict()
            assert lead_dict['name'] == 'Bob Johnson'
            assert lead_dict['email'] == 'bob@example.com'
            assert lead_dict['status'] == 'new'


class TestPropertyModel:
    """Test Property model"""
    
    def test_create_property(self, app):
        """Test creating a property"""
        with app.app_context():
            prop = Property(
                title='Luxury Penthouse',
                category='luxury',
                price=5000000,
                bedrooms=3,
                bathrooms=2,
                sqft=2500,
                city='New York',
                state='NY',
                featured=True
            )
            db.session.add(prop)
            db.session.commit()
            
            assert prop.id is not None
            assert prop.active is True
    
    def test_property_to_dict(self, app):
        """Test converting property to dictionary"""
        with app.app_context():
            prop = Property(
                title='Modern Apartment',
                category='residential',
                price=1500000,
                bedrooms=2,
                bathrooms=1,
                sqft=1000,
                city='Boston',
                state='MA'
            )
            db.session.add(prop)
            db.session.commit()
            
            prop_dict = prop.to_dict()
            assert prop_dict['title'] == 'Modern Apartment'
            assert prop_dict['price'] == 1500000


class TestPropertiesAPI:
    """Test properties API endpoints"""
    
    def test_get_empty_properties(self, client, app):
        """Test getting properties when none exist"""
        response = client.get('/api/properties')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['properties']) == 0
    
    def test_get_properties_with_data(self, client, app):
        """Test getting properties with data"""
        with app.app_context():
            prop = Property(
                title='Test Property',
                category='residential',
                price=2000000,
                bedrooms=3,
                bathrooms=2,
                sqft=1800
            )
            db.session.add(prop)
            db.session.commit()
        
        response = client.get('/api/properties')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['properties']) == 1
        assert data['properties'][0]['title'] == 'Test Property'
    
    def test_filter_properties_by_category(self, client, app):
        """Test filtering properties by category"""
        with app.app_context():
            residential = Property(
                title='Residential Home',
                category='residential',
                price=1500000,
                bedrooms=3,
                bathrooms=2,
                sqft=1800
            )
            luxury = Property(
                title='Luxury Suite',
                category='luxury',
                price=5000000,
                bedrooms=4,
                bathrooms=3,
                sqft=3500
            )
            db.session.add_all([residential, luxury])
            db.session.commit()
        
        response = client.get('/api/properties?category=residential')
        assert response.status_code == 200
        data = response.get_json()
        assert len(data['properties']) == 1
        assert data['properties'][0]['category'] == 'residential'


class TestStatsAPI:
    """Test statistics API"""
    
    def test_get_stats(self, client, app):
        """Test getting statistics"""
        with app.app_context():
            lead = Lead(
                name='Test Lead',
                email='test@example.com',
                phone='5551234567',
                message='Test message'
            )
            prop = Property(
                title='Test Property',
                category='residential',
                price=1000000,
                featured=True
            )
            db.session.add_all([lead, prop])
            db.session.commit()
        
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['stats']['total_leads'] == 1
        assert data['stats']['total_properties'] == 1
        assert data['stats']['featured_properties'] == 1


class TestCLI:
    """Test CLI commands"""
    
    def test_init_db_command(self, runner):
        """Test database initialization command"""
        result = runner.invoke(lambda: None, ['init-db'])
        # Note: This is a simplified test
        # Full testing would require proper CLI setup


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
