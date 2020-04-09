import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))


@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)


@app.route('/create/', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('creating.jinja2')
    name = request.form['name']
    try:
        amt = int(request.form['amount'])
    except ValueError:
        amt = 0

    try:
        donor = Donor.select().where(Donor.name == name).get()
    except Exception:
        return render_template('creating.jinja2',
                               error=f"No donor named {name}")
    else:

        if amt < 0:
            return render_template('creating.jinja2',
                                   error=f"Don't steal from charity, {name}!")

        Donation(value=amt, donor=donor).save()
        return redirect(url_for('home'))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

