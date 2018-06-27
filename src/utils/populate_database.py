from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Item, User, Base

engine = create_engine('sqlite:///../items_catalog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


def add_and_commit(item, session):
    session.add(item)
    session.commit()


# Add a few categories
technology_category = Category(name="Technology")
add_and_commit(technology_category, session)

music_category = Category(name="Music Genres")
add_and_commit(music_category, session)

general_category = Category(name="General")
add_and_commit(general_category, session)

# Add a user
example_user = User(email="user@example.com",
                    picture_url="https://openclipart.org/image/80px/svg_to_png/247324/abstract-user-flat-1.png")
add_and_commit(example_user, session)

# Add a few polls
music_item = Item(
    name="Rock",
    description="Rock music is a broad genre of popular music that originated as 'rock and roll' in the United States in the early 1950s, and developed into a range of different styles in the 1960s and later, particularly in the United Kingdom and in the United States",
    category=music_category,
    user=example_user
)
add_and_commit(music_item, session)

tech_item = Item(
    name="OS X",
    description="macOS is a series of graphical operating systems developed and marketed by Apple Inc. since 2001. It is the primary operating system for Apple's Mac family of computers. Within the market of desktop, laptop and home computers, and by web usage, it is the second most widely used desktop OS, after Microsoft Windows.",
    category=technology_category,
    user=example_user
)
add_and_commit(tech_item, session)
