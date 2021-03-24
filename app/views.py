"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from .forms import PropertyForm
from werkzeug.utils import secure_filename
from .models import Property



###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Project 1 - Properties")


@app.route('/property', methods=['GET','POST'])
def property():
    """Render the website Property Page"""
    propertyform = PropertyForm()
    if request.method == 'POST':
        if propertyform.validate_on_submit():
            photo = request.files['photo']
            property = Property(request.form['title'], request.form['description'], request.form['rooms'], request.form['bathrooms'], request.form['price'], request.form['type'], request.form['location'], filename)
            filename = secure_filename(photo.filename)

            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            property = Property(title=title, description=description, rooms=rooms, bathrooms=bathrooms, price=price, property_type=property_type, location=location, photo="uploads/"+filename)
            db.session.add(property)
            db.session.commit()

            flash('New Property Added!', 'success')
            return redirect(url_for('properties'))
            else:
                flash_errors(propertyforms)
                flash('Error. Try again.', 'danger')
                return redirect(url_for('home'))

    return render_template('property.html', form=property_page)

@app.route('/properties')
def properties():
    properties=db.session.query(Property).all()
    return render_template('properties.html', properties=properties)


@app.route('/property/<propertyid>')
def show_property(propertyID):
    property = db.session.query(Property).get(propertyID)
    return render_template('viewproperty.html', property=property)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")