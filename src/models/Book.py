from sqlalchemy import Column, Date, Integer, String
from .meta import Base

class Book(Base):
    _tablename_ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    date_publication = Column(Date)


    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'date_publication': self.date_publication,
            }