from random import choice

from flask import Flask, redirect, render_template, request, url_for

from custom.use_db import UseDB

app = Flask(__name__)

db = UseDB()

@app.after_request
def add_header(response):
    response.cache_control.max_age = 30
    return response


@app.route('/', methods=['GET', 'POST'])
def home():
    try:
        if request.method == 'GET':
            return render_template('home.html', users=db.all_users())
        elif request.method == 'POST':
            random_user = set()
            count_username = request.form.get('count_username')
            if count_username != None:
                random_user.add(choice(db.all_users()))
            else:
                while len(random_user) != count_username:
                    random_user.add(choice(db.all_users()))
            return render_template('home.html',users=db.all_users(),
                                   random_user=random_user)
        return render_template('home.html', users=db.all_users())
    except:
        return redirect(url_for('home'))


@app.route('/user/', methods=['GET', 'POST'])
def user():
    try:
        if request.method == 'POST':
            insert_username = request.form.get('insert_username')
            delete_username = request.form.get('delete_username')
            if insert_username != None:
                insert_username = insert_username.replace(" ", "_")
                db.insert_user(insert_username)
            if delete_username != None:
                delete_username = delete_username.replace(" ", "_")
                db.delete_user(delete_username)
        return render_template("user.html", users=db.all_users())
    except:
        return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()