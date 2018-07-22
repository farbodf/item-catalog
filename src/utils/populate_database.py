from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User, Base

engine = create_engine('sqlite:///../../items_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_and_commit(item, session):
    session.add(item)
    session.commit()


categories = ["Technology", "Programming Language", "Entertainment", "Drink"
              "Politics", "Science", "Movie", "Music", "General"]

# Add a user
example_user = User(email="user@example.com",
                    google_id='1',
                    picture_url="https://openclipart.org/image/80px/svg_to_png/247324/abstract-user-flat-1.png")
add_and_commit(example_user, session)

items = [{"name": "Statistics", "category": "Science"},
         {"name": "Calculus", "category": "Science"},
         {"name": "Physics", "category": "Science"},
         {"name": "Birdman", "category": "Movie"},
         {"name": "Inception", "category": "Movie"},
         {"name": "Microsoft", "category": "Technology"},
         {"name": "Rap", "category": "Music"},
         {"name": "Theater", "category": "Entertainment"},
         {"name": "Senate", "category": "Politics"},
         {"name": "Whiskey", "category": "Drink"},
         {"name": "Wine", "category": "Drink"},
         {"name": "Beer", "category": "Drink"},
         {"name": "Vodka", "category": "Drink"},
         {"name": "Rock", "category": "Music"},
         {"name": "Apple", "category": "Technology"},
         {"name": "Python", "category": "Programming Language"},
         {"name": "Scala", "category": "Programming Language"},
         {"name": "R", "category": "Programming Language"},
         {"name": "Java", "category": "Programming Language"},
         {"name": "C", "category": "Programming Language"},
         {"name": "Rust", "category": "Programming Language"}]

for category_name in categories:
    category = Category(name=category_name)
    add_and_commit(category, session)
    category_items = [item for item in items if item["category"] == category_name]
    for item in category_items:
        item = Item(name=item['name'],
                    description="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce luctus eros in fringilla laoreet. In vel urna ac magna placerat dictum a id tortor. Fusce dignissim scelerisque sodales. Proin aliquam diam vel est dapibus, a tempor orci pellentesque. Suspendisse potenti.",
                    category=category,
                    user=example_user)
        add_and_commit(item, session)
