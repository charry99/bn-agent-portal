# Contributing to Billions Network Agent Portal

Thank you for your interest in contributing! We welcome contributions from the community. This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and professional in all interactions. We're committed to creating a welcoming environment for all contributors.

## Getting Started

### 1. Fork the Repository
```bash
git clone https://github.com/yourusername/bn-agent-portal.git
cd bn-agent-portal
```

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

Use descriptive branch names:
- `feature/add-property-search` - for new features
- `bugfix/fix-contact-form` - for bug fixes
- `docs/update-readme` - for documentation updates

### 3. Set Up Development Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask init-db
```

## Development Workflow

### Code Style

We follow PEP 8 for Python and ES6+ for JavaScript.

#### Python Code Style
```python
# Use type hints where appropriate
def validate_contact_form(data: dict) -> list:
    """Validate contact form data.
    
    Args:
        data: Dictionary containing form data
        
    Returns:
        List of validation errors
    """
    errors = []
    # Implementation
    return errors


# Use meaningful variable names
database_connection = get_db_connection()  # Good
db_conn = get_db_connection()              # Acceptable
dc = get_db_connection()                   # Avoid

# Use context managers for resource management
with app.app_context():
    users = User.query.all()
```

#### JavaScript Code Style
```javascript
// Use const by default, let if reassignment needed
const USER_ROLE_ADMIN = 'admin';
let currentPage = 1;

// Use arrow functions
const filterProperties = (properties, category) => {
    return properties.filter(p => p.category === category);
};

// Use descriptive function names
const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
};
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific test file
pytest test_app.py

# Run specific test function
pytest test_app.py::TestContactForm::test_valid_contact_submission

# Run with verbose output
pytest -v

# Run only fast tests
pytest -m "not slow"
```

### Code Quality Tools

Format code before committing:
```bash
# Format Python code
black app.py config.py

# Check for style issues
flake8 app.py config.py

# Sort imports
isort app.py config.py
```

### Database Migrations

When modifying database models:

```python
# app.py - Define or modify model
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
```

Then generate migration:
```bash
flask db migrate -m "Add new model"
flask db upgrade
```

## Git Workflow

### Commit Messages

Write clear, descriptive commit messages:

```bash
# Good
git commit -m "Add property filter functionality"
git commit -m "Fix contact form validation for international phone numbers"

# Bad
git commit -m "Updates"
git commit -m "WIP"
git commit -m "Fixed stuff"
```

Format:
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit to 50 characters for the subject line
- Add detailed explanation in the body if needed

Example:
```
Add advanced property search functionality

- Implement full-text search across property titles and descriptions
- Add price range filter with slider UI
- Add location-based filtering using coordinates
- Update API endpoint /api/properties to support new query parameters

Closes #123
```

### Pull Requests

When submitting a pull request:

1. **Update your branch**
   ```bash
   git fetch origin
   git rebase origin/main
   ```

2. **Push changes**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create PR on GitHub**
   - Write a clear description
   - Reference any related issues (`Closes #123`)
   - Include screenshots for UI changes
   - Ensure all tests pass

4. **PR Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Unit tests added
   - [ ] Integration tests added
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Comments added for complex logic
   - [ ] Documentation updated
   - [ ] No breaking changes
   
   ## Related Issues
   Closes #123
   ```

## Adding Features

### Frontend Features

1. **HTML** - Add semantic markup in `templates/index.html`
2. **CSS** - Add styles to `static/css/style.css`
3. **JavaScript** - Add functionality to `static/js/main.js`
4. **Testing** - Add manual testing steps in PR

Example:
```html
<!-- templates/index.html -->
<section id="new-section" class="py-20 bg-white">
    <div class="container mx-auto px-6">
        <h2>New Feature</h2>
        <!-- Content -->
    </div>
</section>
```

```css
/* static/css/style.css */
#new-section {
    animation: slideInUp 0.8s ease-out;
}
```

```javascript
// static/js/main.js
function initNewFeature() {
    // Feature implementation
}
```

### Backend Features

1. **Models** - Add database models in `app.py`
2. **Routes** - Add Flask routes in `register_blueprints()`
3. **Validation** - Add input validation functions
4. **Tests** - Add tests in `test_app.py`

Example:
```python
# app.py - Add model
class NewModel(db.Model):
    """Description of the model"""
    __tablename__ = 'new_models'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def to_dict(self):
        return {'id': self.id, 'name': self.name}


# app.py - Add route
@api_bp.route('/new-endpoint', methods=['GET'])
def new_endpoint():
    """Description of endpoint"""
    return jsonify({'success': True}), 200


# test_app.py - Add test
def test_new_endpoint(client):
    response = client.get('/api/new-endpoint')
    assert response.status_code == 200
```

## Documentation

### Docstring Format

```python
def calculate_property_price_adjustment(price, adjustment_percent):
    """Calculate adjusted property price based on percentage.
    
    This function takes a base price and calculates the new price
    after applying a percentage adjustment (positive for increase,
    negative for decrease).
    
    Args:
        price (float): Base property price
        adjustment_percent (float): Adjustment percentage (-100 to 100)
        
    Returns:
        float: Adjusted price
        
    Raises:
        ValueError: If adjustment_percent is outside valid range
        TypeError: If price is not numeric
        
    Example:
        >>> calculate_property_price_adjustment(1000000, 10)
        1100000.0
        >>> calculate_property_price_adjustment(1000000, -5)
        950000.0
    """
    if not isinstance(price, (int, float)):
        raise TypeError(f"Price must be numeric, got {type(price)}")
    
    if adjustment_percent < -100 or adjustment_percent > 100:
        raise ValueError(f"Adjustment must be -100 to 100, got {adjustment_percent}")
    
    return price * (1 + adjustment_percent / 100)
```

### Inline Comments

```python
# Use comments to explain WHY, not WHAT
# Good
# Cache results to avoid repeated database queries
cached_properties = cache.get('featured_properties') or load_featured_properties()

# Bad
# Get featured properties from cache or database
cached_properties = cache.get('featured_properties') or load_featured_properties()
```

## Reporting Issues

When reporting bugs:

1. **Use a clear title** - "Contact form validation not working for international numbers"
2. **Describe the issue** - What were you doing? What happened?
3. **Provide steps to reproduce** - Be specific and detailed
4. **Share error messages** - Include full error trace
5. **Environment info** - Python version, browser, OS, etc.
6. **Suggested fix** (optional) - If you have an idea

Example issue:
```markdown
## Bug: Contact form rejects valid phone numbers

### Description
The contact form is rejecting valid international phone numbers from Canada (+1 area codes).

### Steps to Reproduce
1. Navigate to the contact form
2. Enter a valid Canadian phone number (e.g., +1 (555) 123-4567)
3. Try to submit the form

### Expected Behavior
Form should accept valid international phone numbers

### Actual Behavior
Form shows error: "Please enter a valid phone number"

### Environment
- Python 3.11
- Flask 2.3.3
- Chrome 119
- macOS 14.1

### Screenshots
[Attach screenshots if helpful]
```

## Review Process

1. **Code Review** - At least one maintainer will review your PR
2. **Tests** - All tests must pass
3. **Documentation** - Changes should be documented
4. **Performance** - No significant performance regressions
5. **Approval** - PR must be approved before merging

## Community

- **Questions?** Open a GitHub discussion
- **Feature requests?** Open an issue with the `enhancement` label
- **Security issues?** Email security@billionsnetwork.com (don't open public issues)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation

Thank you for contributing! 🚀

---

For more information, see:
- [README.md](README.md) - Project overview
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) - Community guidelines (if available)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
