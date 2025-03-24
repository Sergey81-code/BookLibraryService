import datetime

import pytest
from uuid_extensions import uuid7

from tests.conftest import BOOK_URL, VERSION_URL

from tests.utils_for_tests import create_auth_headers_for_user
from utils.roles import PortalRole



async def test_create_book(
        client, 
        create_object_in_database, 
        get_book_from_database
    ):
    author1_info = {
        "id": uuid7(),
        "name": "Толстой Лев Николаевич",
        "birthday": datetime.date(1855, 4, 22),
        "deathday": datetime.date(1999, 6, 12)
    }
    author2_info = {
        "id": uuid7(),
        "name": "Лермонтов Михаил",
        "birthday": datetime.date(1845, 7, 2),
        "deathday": datetime.date(1989, 3, 18)
    }
    book_info = {
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    author1_id = await create_object_in_database("authors", author1_info)
    author2_id = await create_object_in_database("authors", author2_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})
    
    await create_object_in_database("books", book_info)

    # resp = client.post(
    #     f"{VERSION_URL}{BOOK_URL}", json=book_info,
    #     headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    # )

    # assert resp.status_code == 200
    # data_from_resp = resp.json()

    # assert data_from_resp['name'] == book_info['name']
    # assert data_from_resp['description'] == book_info['description']
    # assert data_from_resp['url'] == book_info['url']
    # assert data_from_resp['year'] == book_info['year']
    # assert data_from_resp['totalAmount'] == book_info['totalAmount']
    # assert data_from_resp['borrowedAmount'] == book_info['borrowedAmount']

    # for author_key in author1_info.keys():
    #     assert str(data_from_resp['authors'][0][author_key]) == str(author1_info[author_key])
    #     assert str(data_from_resp['authors'][1][author_key]) == str(author2_info[author_key])

    # book_from_db = await get_book_from_database(data_from_resp['id'])
    # assert str(book_from_db["id"]) == data_from_resp['id']
    # assert book_from_db["name"] == book_info["name"]
    # assert book_from_db["description"] == book_info["description"]
    # assert book_from_db["url"] == book_info["url"]
    # assert book_from_db["year"] == book_info["year"]
    # assert book_from_db["totalAmount"] == book_info["totalAmount"]
    # assert book_from_db["borrowedAmount"] == book_info["borrowedAmount"]
    # assert [{"id": str(author["author_id"])} for author in book_from_db["authors"]] == book_info["authors"]