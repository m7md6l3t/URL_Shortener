from flask import Blueprint, redirect
from database import db
from .models import URL


redirection_service_blueprint = Blueprint('redirection_service', __name__)

# This route redirects the user to the long URL
@redirection_service_blueprint.route('/<short_code>')
def redirect_to_long_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        url.visit_count += 1
        db.session.commit()
        return redirect(url.long_url)
    else:
        return "URL not found", 404