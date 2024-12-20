# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import csv
from datetime import datetime
from flask import jsonify,session

from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///purchases.db'
app.secret_key = 'b1c6e54b2e4d6e6d8e0d4b2caa4a2383'  # Set your secret key here
db = SQLAlchemy(app)




# Flask-Mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your email provider's SMTP server
app.config['MAIL_PORT'] =  587
app.config['MAIL_USERNAME'] = '23mca010@stc.ac.in'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'stc@12345'  # Replace with your email password

app.config['MAIL_USE_TLS'] = True  # Use TLS
app.config['MAIL_USE_SSL'] = False  # Do not use SSL



mail = Mail(app)





class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    package = db.Column(db.String(50), nullable=False)

# Create the database tables within an application context
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/select_package', methods=['POST'])
def select_package():
    # Get the selected package from the form
    package = request.form.get('produt')

    # Check if no package was selected
    if package is None:
        return jsonify({"error": "Please select a package."}), 400  # Return an error response

    # Store the selected package in the session
    session['selected_package'] = package

    # Return a success response
    return jsonify({"success": True, "package": package})
@app.route('/book', methods=['GET', 'POST'])
def book_form():
    if request.method == 'POST':
        first_name = request.form['name']
        last_name = request.form['last_name']
        mobile_number = request.form['cpf']
        email = request.form['email']
        event_date_str = request.form['cep']
        time_str = request.form['number']
        event_name = request.form['place']
        address = request.form['neighborhood']
        city = request.form['city']

        # Retrieve the package from the session
        package = session.get('selected_package')

        # Check if the package is still available
        if package is None:
            return "Please select a package first.", 400

        # Convert the string date to a date object
        event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()

        # Convert the string time to a time object
        time_obj = datetime.strptime(time_str, '%H:%M').time()

        new_purchase = Purchase(
            first_name=first_name,
            last_name=last_name,
            mobile_number=mobile_number,
            email=email,
            event_date=event_date,
            time=time_obj,
            event_name=event_name,
            address=address,
            city=city,
            package=package
        )

        db.session.add(new_purchase)
        db.session.commit()

         # Store the user's email in the session
        session['user_email'] = email

        # Clear the session after purchase
        session.pop('selected_package', None)


        return redirect(url_for('success'))
    return render_template('buy.html')  # Render a separate form template if needed

@app.route('/success')
def success():
    # Get the user's email from the session
    user_email = session.get('user_email', None)
    
    # If the email is not in the session, get it from the latest purchase
    if user_email is None:
        latest_purchase = Purchase.query.order_by(Purchase.id.desc()).first()
        user_email = latest_purchase.email if latest_purchase else None

    # Send a confirmation email if the email exists
    if user_email:
        # Create the email message
        msg = Message('Purchase Confirmation',
                      sender='your-email@gmail.com',
                      recipients=[user_email])

        msg.body = 'Thank you for your purchase! Your order has been successfully placed.'

        # Send the email
        mail.send(msg)

        return "Purchase successful! A confirmation email has been sent."
    
    return "Purchase successful!"




# Branches Page
@app.route('/branches')
def branches():
    return render_template('branches.html')

# Packages Page
@app.route('/packages')
def packages():
    return render_template('packages.html')

# Gallery Page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

# Booking Page
@app.route('/buy')
def buy():
    return render_template('buy.html')

# Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/inquire', methods=['POST'])
def inquire():
    name = request.form.get('destination')
    mobile_no = request.form.get('people')
    event_date = request.form.get('checkin')
    upto_date = request.form.get('checkout')

    # Save inquiry to CSV
    with open('inquiries.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now(), name, mobile_no, event_date, upto_date])

    # Send confirmation email
    msg = Message('Thank You for Your Inquiry!',
                  recipients=[app.config['MAIL_DEFAULT_SENDER']])  # Send to your email
    msg.body = f"Thank you, {name}, for your inquiry!\n\n" \
                f"Mobile No: {mobile_no}\n" \
                f"Event Date: {event_date}\n" \
                f"Upto: {upto_date}"

    # Send the email
    try:
        mail.send(msg)
    except Exception as e:
        print("Failed to send email: ", str(e))  # Log the error for debugging
        flash('There was an issue sending the confirmation email.', 'danger')
        return redirect(url_for('index'))

    flash('Your inquiry has been submitted successfully!', 'success')
    return redirect(url_for('index'))


@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')

    # Save the subscription to a CSV file
    with open('subscriptions.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([datetime.now(), email])

    # Send a thank you email
    msg = Message('Thank You for Subscribing!',
                  sender='your-email@gmail.com',  # Set sender explicitly
                  recipients=[email])
    msg.body = "Thank you for subscribing to our newsletter!"
    
    # Send the email
    try:
        mail.send(msg)
    except Exception as e:
        print("Failed to send email: ", str(e))  # Log the error for debugging
        flash('There was an issue sending the email.', 'danger')
        return redirect(url_for('index'))

    flash('Thank you for subscribing to our newsletter!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)