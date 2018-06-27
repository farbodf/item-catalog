import random
import string
import logging
from flask import Flask, request, render_template
from flask import session as login_session
from config import Config
from item_catalog.google_login import connect, disconnect


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("item_catalog")


app = Flask(__name__, template_folder="./templates")


@app.route('/')
@app.route('/categories')
def catalog():
    return render_template("index.html")


@app.route('/<category>/items')
def category_items(category):
    return render_template("category_items.html")


@app.route('/new_item', methods=['GET', 'POST'])
def add_item():
    return render_template("new_item.html")


@app.route('/<category>/<item>')
def category_item(category, item):
    return render_template("item_description.html")


@app.route('/login')
def login():
    state = ''.join(random.choice(string.ascii_uppercase +
                                  string.ascii_lowercase +
                                  string.digits) for x in range(32))
    login_session['state'] = state
    cfg = Config.get_cfg()
    return render_template(
        'login.html',
        data_clientid=cfg['keys']['google_data_clientid'],
        STATE=state
    )


@app.route('/gconnect', methods=['POST'])
def gconnect():
    user_info = connect()
    return render_template(
        'logged_in.html',
        username=user_info['username'],
        picture=user_info['picture']
    )


@app.route('/gdisconnect')
def gdisconnect():
    return disconnect()


@app.route('/<category>/<item>/edit', methods=['GET', 'PUT'])
def edit_item(category, item):
    if request.method == 'GET':
        return render_template("edit_item.html")
    elif request.method == 'PUT':
        return "editted the item"


@app.route('/<category>/<item>/delete', methods=['GET', 'DELETE'])
def delete_item(category, item):
    if request.method == 'GET':
        return render_template("delete_item.html")
    elif request.method == 'DELETE':
        return "deleted item"


@app.route('/catalog')
def json_catalog():
    return "endpoint to return catalog"


if __name__ == "__main__":
    secret_key = ''.join(random.choice(string.ascii_uppercase +
                                       string.ascii_lowercase +
                                       string.digits) for x in range(32))
    LOGGER.info("secret key is: %s", secret_key)
    app.secret_key = str.encode(secret_key)
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
