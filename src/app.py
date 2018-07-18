import random
import string
import logging
from flask import Flask, request, render_template, jsonify, redirect, url_for, make_response
from flask import session as login_session
from config import Config
from item_catalog.google_login import connect, disconnect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.database_setup import Base, Category, Item, User


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
    LOGGER.info("catalog login info: %s", login_session)
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
    if request.method == 'GET':
        categories = session.query(Category).all()
        return render_template("new_item.html", categories=categories)
    elif request.method == 'POST':
        if 'user_id' in login_session:
            category_id = request.form.getlist('category')[0]
            category = session.query(Category).filter_by(id=category_id).one()
            user = session.query(User).filter_by(id=login_session['user_id']).one()
            new_item = Item(
                name=request.form.getlist('item_name')[0],
                description=request.form.getlist('item_description')[0],
                category=category,
                user=user
            )
            session.add(new_item)
            session.commit()
            return redirect(url_for('catalog'))
        else:
            return "User was not logged in!"


@app.route('/<category_id>/<item_id>')
def category_item(category_id, item_id):
    category = session.query(Category).filter_by(id=category_id).one()
    item = session.query(Item).filter_by(id=item_id).one()
    return render_template("item_description.html", item=item, category=category)


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
    if user_info.status_code == 200:
        user_info = user_info.json
    else:
        exit()
    if 'google_id' in user_info:
        # If this is a new user add its data to the database
        result = session.query(User).filter_by(google_id=login_session['google_id']).first()
        if result:
            login_session['user_id'] = result.id
        else:
            new_user = User(
                email=login_session['email'],
                google_id=login_session['google_id'],
                picture_url=login_session['picture']
            )
            session.add(new_user)
            session.commit()
            LOGGER.info("new_user object: %s", new_user)
            login_session['user_id'] = new_user.id

        return render_template(
            'logged_in.html',
            picture=user_info['picture'],
            email=user_info['email']
        )
    else:
        return render_template('index.html')


@app.route('/gdisconnect')
def gdisconnect():
    response = disconnect()
    LOGGER.info("Session after disconnect: %s", login_session)
    return response


@app.route('/<category_id>/<item_id>/edit', methods=['GET', 'POST'])
def edit_item(category_id, item_id):
    if request.method == 'GET':
        categories = session.query(Category).all()
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template("edit_item.html", categories=categories, item=item, category_id=category_id)
    elif request.method == 'POST':
        return "editted the item"


@app.route('/<category_id>/<item_id>/delete', methods=['GET', 'POST'])
def delete_item(category_id, item_id):
    if request.method == 'GET':
        item = session.query(Item).filter_by(id=item_id).one()
        return render_template("delete_item.html", item=item)
    elif request.method == 'POST':
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
