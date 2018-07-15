import random
import string
import logging
from flask import Flask, request, render_template, jsonify, make_response
from flask import session as login_session
from config import Config
from item_catalog.google_login import connect, disconnect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.database_setup import Base, Category, Item


logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger("item_catalog")

engine = create_engine('sqlite:///items_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__, template_folder="./templates")


@app.route('/')
@app.route('/categories')
def catalog():
    categories = session.query(Category).all()
    items = session.query(Item).order_by(Item.id.desc()).all()
    items_list = [{"name": item.name,
                   "id": item.id,
                   "category_id": item.category_id}
                  for item in items[0:(10 if len(items) > 10 else len(items))]]
    for item in items_list:
        category = session.query(Category).filter_by(id=item["category_id"]).one()
        item['category_name'] = category.name
    return render_template("index.html", categories=categories, items=items_list)


@app.route('/<category_id>/items')
def category_items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category.id).all()
    return render_template("category_items.html",
                           categories=categories,
                           category=category,
                           items=items,
                           items_num=len(items))


@app.route('/new_item', methods=['GET', 'POST'])
def add_item():
    return render_template("new_item.html")


@app.route('/<category_id>/<item_id>')
def category_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template("item_description.html", item=item)


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
    categories = session.query(Category).all()
    catalog = []
    for category in categories:
        category_dict = {'id': category.id, "name": category.name, "items": []}
        items = session.query(Item).filter_by(category_id=category.id).all()
        for item in items:
            category_dict["items"].append({"id": item.id,
                                      "name": item.name,
                                      "description": item.description})
        catalog.append(category_dict)
    return jsonify(catalog)


if __name__ == "__main__":
    secret_key = ''.join(random.choice(string.ascii_uppercase +
                                       string.ascii_lowercase +
                                       string.digits) for x in range(32))
    LOGGER.info("secret key is: %s", secret_key)
    app.secret_key = str.encode(secret_key)
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
