"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

import os
from app import app, db
from flask import render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
from .models import Property
from .forms import PropertyForm


###
# Routing for your application.
###

UPLOAD_FOLDER = '/app/static/file_uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg'])

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about')
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
            property = Property(request.form['title'], request.form['description'], request.form['rooms'], request.form['bathrooms'], request.form['price'], request.form['property_type'], request.form['location'], photo)
            db.session.add(property)
            db.session.commit()
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo)) #save uploaded photo
            flash('New Property Added!', 'success')
            return redirect(url_for('properties'))
        else:
            flash('Error. Please try again.', 'danger')
            return redirect(url_for('home'))
    return render_template('property.html', form=propertyform)

@app.route('/properties')
def properties():
    props=db.session.query(Property).all()
    return render_template('properties.html', props=props)


@app.route('/property/<propertyid>')
def get_property(propertyID):
    property = db.session.query(Property).get(propertyID)
    return render_template('viewproperty.html', spot=property)
###
# The functions below should be applicable to all Flask apps.
###

@app.route('/uploads/<photo>')
def get_image(photo):
    #sources: https://stackoverflow.com/questions/58526153/how-to-upload-the-images-inside-a-folder-images-instead-of-the-curent-director
    #https://www.bogotobogo.com/python/python_files.php 
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, app.config['UPLOAD_FOLDER']), photo)

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
