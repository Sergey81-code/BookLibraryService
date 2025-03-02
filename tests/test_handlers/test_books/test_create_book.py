
async def test_create_book(client):
    book_info = {
        "name": "BookName",
        "desc": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }