"""Error handlers for HTTP and API errors."""
from flask import jsonify, render_template

from . import app, db


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 Not Found errors."""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 Internal Server errors with DB rollback."""
    db.session.rollback()
    return render_template('500.html'), 500


class InvalidAPIUsage(Exception):
    """Custom exception for API validation errors."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Convert exception to JSON-serializable dictionary."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(error):
    """Handle InvalidAPIUsage exceptions and return JSON response."""
    return jsonify(error.to_dict()), error.status_code
