def book_search_serializer(books):
    data = []
    for book in books:
        obj = {
            'book': {
                    'title': book.title,
                    'authors': book.authors,
                    'genre': book.genre,
                    'id': book.id,
                    },
            'image': book.image,
        }
        data.append(obj)
    return data
