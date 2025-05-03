import datetime

import pytest
from uuid_extensions import uuid7

from tests.conftest import BOOK_URL, VERSION_URL

from tests.utils_for_tests import create_auth_headers_for_user
from utils.roles import PortalRole



async def test_get_book(
        client, 
        create_book_in_database, 
        create_author_in_database
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
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})
    
    book_id = await create_book_in_database(book_info)

    assert book_id == book_info["id"]

    resp = client.get(
        f"{VERSION_URL}{BOOK_URL}/{book_id}",
    )

    assert resp.status_code == 200
    data_from_resp = resp.json()

    assert data_from_resp['name'] == book_info['name']
    assert data_from_resp['description'] == book_info['description']
    assert data_from_resp['url'] == book_info['url']
    assert data_from_resp['year'] == book_info['year']
    assert data_from_resp['totalAmount'] == book_info['totalAmount']
    assert data_from_resp['borrowedAmount'] == book_info['borrowedAmount']

    for author_key in author1_info.keys():
        assert str(data_from_resp['authors'][0][author_key]) == str(author1_info[author_key])
        assert str(data_from_resp['authors'][1][author_key]) == str(author2_info[author_key])


@pytest.mark.parametrize("book_id, expected_status_code, expected_detail", [
    (
        "",
        422,
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": [
                        "query",
                        "book_name"
                    ],
                    "msg": "Field required",
                    "input": None
                }
            ]
        }
    ),
    (
        "123",
        422,
        {
            "detail": [
                {
                    "type": "uuid_parsing",
                    "loc": [
                        "path",
                        "book_id"
                    ],
                    "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
                    "input": "123",
                    "ctx": {
                        "error": "invalid length: expected length 32 for simple format, found 3"
                    }
                }
            ]
        }
    ),
    (
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        404,
        {
        "detail": "Book with id 3fa85f64-5717-4562-b3fc-2c963f66afa6 not found"
        },
    )
])
async def test_get_book_invalid_id(
        client,
        create_author_in_database,
        create_book_in_database,
        book_id,
        expected_status_code,
        expected_detail,
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
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})
    
    await create_book_in_database(book_info)

    resp = client.get(
        f"{VERSION_URL}{BOOK_URL}/{book_id}",
    )

    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail