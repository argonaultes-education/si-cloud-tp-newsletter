from flask import Flask, request, redirect, url_for, render_template
from hashlib import md5
import hmac
import sqlite3
import datetime
import os
import re
from prometheus_client import start_http_server, Counter, Gauge

# create tables in sqlite
try:
    os.remove('newsletter.db')
except:
    pass
connection = sqlite3.connect('newsletter.db')
connection.execute('CREATE TABLE subscribers (email varchar(200) unique not null, subscribed_at datetime default current_timestamp)')
connection.commit()
cursor = connection.cursor()
data = [
    ('gael@hotmail.com', datetime.datetime(2023, 1, 31, 10, 20)),
    ('super@msn.com', datetime.datetime(2023, 2, 28, 10, 20)),
    ('james@lycos.fr', datetime.datetime(1987, 1, 31, 10, 20)),
    ('tonton@caramail.fr', datetime.datetime(2010, 1, 31, 10, 20)),
    ('gamer@battle.net', datetime.datetime(2008, 1, 31, 10, 20))
]
cursor.executemany("INSERT INTO subscribers VALUES(?, ?)", data)
connection.commit()
connection.execute('CREATE TABLE newsletters(email varchar(200) references subscribers(email), title varchar(200) not null, send_at datetime not null)')
connection.commit()
data_newsletters = [
    ('gael@hotmail.com', 'nature is wild', datetime.datetime(2023, 3, 29, 10, 20)),
    ('super@msn.com', 'nature is wild', datetime.datetime(2023, 3, 29, 10, 20)),
    ('james@lycos.fr', 'life is tough', datetime.datetime(2011, 6, 13, 10, 00)),
    ('tonton@caramail.fr', 'life is tough', datetime.datetime(2011, 6, 13, 10, 00)),
    ('gamer@battle.net', 'life is tough', datetime.datetime(2011, 6, 13, 10, 00))
]
cursor.executemany("INSERT INTO newsletters VALUES(?, ?, ?)", data_newsletters)
connection.commit()
connection.close()

SECRET_KEY=b'secret'

MAX_QUERIES=300

app_counter = {}

app = Flask(__name__)


# metrics

# root index
@app.route('/')
def index():
    return redirect(url_for('welcome'))

# display welcome page with form identifier
@app.route('/welcome')
def welcome():
    identifier = request.args.get('identifier', '').lower()
    response = identifier
    if (len(identifier) == 2 and re.search('^[a-z]{2}$', identifier)):
        if identifier in app_counter.keys():
            counter = app_counter[identifier]['counter'] + 1
            start_date = app_counter[identifier]['start_date']
            app_counter[identifier]['g'].inc(1.3)
            g = app_counter[identifier]['g']
        else:
            g = Gauge(f'gauge_{identifier}', f'count http requests of {identifier}')
            g.set(1985)
            counter = 0
            start_date = datetime.datetime.now()
        app_counter[identifier] = {
            'counter': counter,
            'start_date': start_date,
            'last_date': datetime.datetime.now(),
            'g': g
        }
        nb_seconds_elapsed = (app_counter[identifier]['last_date'] - app_counter[identifier]['start_date']).total_seconds()
        if app_counter[identifier]['counter'] >= MAX_QUERIES and nb_seconds_elapsed > 300:
            response_hash = hmac.new(SECRET_KEY, identifier.encode('UTF-8'), md5)
            response = response_hash.hexdigest()
            app_counter[identifier]['counter'] = 0
            app_counter[identifier]['start_date'] = datetime.datetime.now()
    return render_template('welcome.html', identifier = response)

# display newsletter form to subscribe
@app.get('/subscribe')
def subscribe():
    email = request.args.get('email', '')
    res_email = ''
    res_sub = ''
    if email:
        with sqlite3.connect('newsletter.db') as conn:
            res = conn.execute(f'SELECT email, subscribed_at FROM subscribers WHERE email = \'{email}\'')
            email_sub = res.fetchone()
            if  email_sub is not None:
                res_email, res_sub = email_sub
            # flash notice
    return render_template('subscribe.html', email = res_email, sub = res_sub)

@app.post('/subscribe')
def subscribe_email():
    email = request.form['email']
    res_subscribed_at = ''
    with sqlite3.connect('newsletter.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO subscribers(email) VALUES (?)', (email,))
        except:
            pass
        cursor.execute('SELECT * FROM subscribers WHERE email = ?', (email,))
        res_email, res_subscribed_at = cursor.fetchone()
        conn.commit()
    return render_template('subscribe.html', email = res_email, sub = res_subscribed_at)

# display newsletter subscription result
start_http_server(int(os.getenv('METRICS_PORT', '9000')))