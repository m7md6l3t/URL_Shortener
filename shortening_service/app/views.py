from flask import Blueprint, request, render_template, redirect, url_for
from .worker import connect_to_rabbitmq, publish_message
from .models import db, URL
import string
import random

shortening_service_blueprint = Blueprint('shortening_service', __name__)

@shortening_service_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        long_url = request.form['long_url']
        code_length = int(request.form.get('code_length') or 6)
        short_code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=code_length))
        #save the new url in the database
        new_url = URL(long_url=long_url, short_code=short_code)
        db.session.add(new_url)
        db.session.commit()
        #send message to rabbitmq server to add the new url in the redirection service
        channel = connect_to_rabbitmq()
        message = {
            "long_url": long_url,
            "short_code": short_code,
            "created_at": new_url.created_at
        }
        publish_message(channel, exchange="", routing_key="URL_data", message=message)

        return redirect(url_for('shortening_service.shortened_url', short_code=short_code))
    return render_template('index.html')

@shortening_service_blueprint.route('/<short_code>')
def shortened_url(short_code):
    url = URL.query.filter_by(short_code=short_code).first()
    if url:
        return render_template('shortened.html', short_url=request.host_url + short_code)
    else:
        return "URL not found", 404