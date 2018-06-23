from flask import Flask, request


app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def catalog():
    return "Home page"


@app.route('/<category>/items')
def category_items(category):
    return "specific category items"


@app.route('/<category>/<item>')
def category_item(category, item):
    return "item description"


@app.route('/login')
def login():
    return "login page"


@app.route('/<category>/<item>/edit', methods=['GET', 'PUT'])
def edit_item(category, item):
    if request.method == 'GET':
        return "page to edit items"
    elif request.method == 'PUT':
        return "editted the item"


@app.route('/<category>/<item>/delete', methods=['GET', 'DELETE'])
def delete_item(category, item):
    if request.method == 'GET':
        return "page to delete an item"
    elif request.method == 'DELETE':
        return "deleted item"


@app.route('/catalog')
def json_catalog():
    return "endpoint to return catalog"


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
