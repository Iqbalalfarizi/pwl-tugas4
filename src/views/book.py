from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from ..models import Book


@view_config(route='books', request_method='POST', renderer='json')
def create_book(request):
    db=request.dbsession
    data=request.json_body

    """Melakukan validasi kelengkapan data inputan"""
    if not all (key in data for key in ('title', 'author', 'date_publication')):
        raise HTTPBadRequest('Semua data wajib diisi')

    """Membuat objek dari nilai inputan"""
    book = Book(title=data['title'], author=data['author'], date_publication=data['date_publication'])

     #Menambahkan data buku baru ke database
    db.add(book)
    #kirim perubahan ke database
    db.flush()

    return book.to_dict()

@view_config(route='book', request_method='GET', renderer='json')
def get_book(request):
    """mendapatkan data buku berdasarkan id"""
    db = request.dbsession
    book_id  =  request.matchdict['id']

    """mengambil data buku yang sesuai"""
    book = db.query(Book).filter(Book.id == book_id).first()

    if Book is not None:
        return book.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route='books', request_method='GET', renderer='json')
def get_books(request):
    """mendapatkan lebih dari satu data buku"""
    db = request.dbsession

    """mendapatkan daftar buku"""
    books = db.query(Book).all()

    
    book_list=[book.to_dict() for book in books]
    """memberikan respon daftar buku"""
    return {
        'books': book_list
    }

@view_config(route='book', request_method='PUT', renderer='json')
def update_book(request):
    """Melakukan update buku yang sesuai dengan ID"""
    db = request.dbsession
    book_id = request.matchdict['id']
    data = request.json_body
    """Mencari buku yang sesuai dengan ID"""
    book = db.query(Book).filter(Book.id == book_id).first()

    """Melakukan update data pada id yang ditemukan"""
    if book is not None:
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'date_publication' in data:
            book.date_publication = data['date_publication']

        """Commit perubahan ke database"""
        db.commit()

        return book.to_dict()
    else:
        raise HTTPNotFound()

@view_config(route_name='book', request_method='DELETE', renderer='json')
def delete_book(request):
    """Menghapus data buku dengan ID"""
    db = request.dbsession
    book_id = request.matchdict['id']
    """Mencari data buku yangs sesuai dengan ID"""
    book = db.query(Book).filter(Book.id == book_id).first()

    if book is not None:
        """Menghapus data buku pada database"""
        db.delete(book)
        db.commit()
        return {'message': 'Data berhasil dihapus'}
    else:
        raise HTTPNotFound()
