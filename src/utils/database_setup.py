from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    def __repr__(self):
        return "<Category(name='{}')>".format(self.name)


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    picture_url = Column(String(250))


class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user = relationship(User)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __repr__(self):
        return "<Item(name='{}', description='{}')>".format(
            self.name, self.description
        )


engine = create_engine('sqlite:///../../items_catalog.db', echo=True)
Base.metadata.create_all(engine)
