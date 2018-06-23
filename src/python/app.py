from flask import Flask, request, render_template


app = Flask(__name__)


@app.route('/')
@app.route('/categories')
def catalog():
    return render_template("index.html")


@app.route('/<category>/items')
def category_items(category):
    return render_template("category_items.html")


@app.route('/<category>/<item>')
def category_item(category, item):
    return render_template("item_description.html")


@app.route('/login')
def login():
    return render_template("login.html")


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
    app.debug = True
    app.run(host='0.0.0.0', port=8081)
