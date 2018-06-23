from flask import Flask


app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def categories():
    return "Home page"


@app.route('/catalog/<category_id>/items')
def category_items(category_id):
    return "specific category items"


@app.route('/catalog/<category_id>/<item_id>')
def category_item(category_id, item_id):
    return "item description"


@app.route('/login')
def login():
    return "login page"


@app.route('/catalog/<item_id>/edit')
def edit_item(item_id):
    return "page to edit items"


@app.route('/catalog/<item_id>/delete')
def delete_item(item_id):
    return "page to delete an item"


@app.route('/catalog')
def json_catalog():
    return "endpoint to return catalog"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
