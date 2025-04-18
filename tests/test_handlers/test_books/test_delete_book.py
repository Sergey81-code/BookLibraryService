import datetime
import json

import pytest
from uuid_extensions import uuid7

from tests.conftest import BOOK_URL, VERSION_URL

from tests.utils_for_tests import create_auth_headers_for_user
from utils.roles import PortalRole



async def test_delete_book(
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

    book1_info = {
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    book2_info = {
        "id": uuid7(),
        "name": "BookName1",
        "description": "Descriptions of this book.1",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2005,
        "totalAmount": 9,
        "borrowedAmount": 2,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book1_info['authors'].append({'id': str(author1_id)})
    book1_info['authors'].append({'id': str(author2_id)})
    book2_info['authors'].append({'id': str(author1_id)})
    
    book1_id = await create_book_in_database(book1_info)
    book2_id = await create_book_in_database(book2_info)

    assert book1_id == book1_info["id"]
    assert book2_id == book2_info["id"]

    book1_id = str(book1_id)
    book2_id = str(book2_id)

    headers_for_auth = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])

    resp = client.request(
        method="DELETE",
        url=f"{VERSION_URL}{BOOK_URL}",
        data=json.dumps([str(book1_id), str(book2_id)]),
        headers = headers_for_auth,
    )

    assert resp.status_code == 200
    data_from_resp = resp.json()

    assert data_from_resp[0] == book1_id
    assert data_from_resp[1] == book2_id



async def test_delete_book_unauth(
        client, 
        create_author_in_database,
        create_book_in_database
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

    book1_info = {
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    book2_info = {
        "id": uuid7(),
        "name": "BookName1",
        "description": "Descriptions of this book.1",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2005,
        "totalAmount": 9,
        "borrowedAmount": 2,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book1_info['authors'].append({'id': str(author1_id)})
    book1_info['authors'].append({'id': str(author2_id)})
    book2_info['authors'].append({'id': str(author1_id)})
    
    book1_id = await create_book_in_database(book1_info)
    book2_id = await create_book_in_database(book2_info)

    assert book1_id == book1_info["id"]
    assert book2_id == book2_info["id"]

    book1_id = str(book1_id)
    book2_id = str(book2_id)

    headers_for_auth = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(headers_for_auth)) : next(iter(headers_for_auth.values())) + "a"}

    resp = client.request(
        method="DELETE",
        url=f"{VERSION_URL}{BOOK_URL}",
        data=json.dumps([str(book1_id), str(book2_id)]),
        headers = bad_auth_header,
    )

    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


async def test_delete_book_no_privilage(
        client, 
        create_author_in_database,
        create_book_in_database
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

    book1_info = {
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    book2_info = {
        "id": uuid7(),
        "name": "BookName1",
        "description": "Descriptions of this book.1",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2005,
        "totalAmount": 9,
        "borrowedAmount": 2,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book1_info['authors'].append({'id': str(author1_id)})
    book1_info['authors'].append({'id': str(author2_id)})
    book2_info['authors'].append({'id': str(author1_id)})
    
    book1_id = await create_book_in_database(book1_info)
    book2_id = await create_book_in_database(book2_info)

    assert book1_id == book1_info["id"]
    assert book2_id == book2_info["id"]

    book1_id = str(book1_id)
    book2_id = str(book2_id)

    headers_for_auth = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_USER])

    resp = client.request(
        method="DELETE",
        url=f"{VERSION_URL}{BOOK_URL}",
        data=json.dumps([str(book1_id), str(book2_id)]),
        headers = headers_for_auth,
    )

    assert resp.status_code == 403
    assert resp.json() == {"detail": "Forbidden: insufficient permissions"}



async def test_delete_book_bad_cred(
        client, 
        create_author_in_database,
        create_book_in_database
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

    book1_info = {
        "id": uuid7(),
        "name": "BookName",
        "description": "Descriptions of this book.",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2003,
        "totalAmount": 10,
        "borrowedAmount": 0,
        "authors": []
    }

    book2_info = {
        "id": uuid7(),
        "name": "BookName1",
        "description": "Descriptions of this book.1",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#15",
        "year": 2005,
        "totalAmount": 9,
        "borrowedAmount": 2,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book1_info['authors'].append({'id': str(author1_id)})
    book1_info['authors'].append({'id': str(author2_id)})
    book2_info['authors'].append({'id': str(author1_id)})
    
    book1_id = await create_book_in_database(book1_info)
    book2_id = await create_book_in_database(book2_info)

    assert book1_id == book1_info["id"]
    assert book2_id == book2_info["id"]

    book1_id = str(book1_id)
    book2_id = str(book2_id)

    headers_for_auth = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(headers_for_auth)) : "Bearer 111"}

    resp = client.request(
        method="DELETE",
        url=f"{VERSION_URL}{BOOK_URL}",
        data=json.dumps([str(book1_id), str(book2_id)]),
        headers = bad_auth_header,
    )

    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}




@pytest.mark.parametrize("book_ids, expected_status_code, expected_detail", [
    (
        [],
        422,
        {
            "detail": "List of book IDs cannot be empty"
        }
    ),
    (
        ["123", "456"],
        422,
        {
        "detail": [
            {
            "type": "uuid_parsing",
            "loc": [
                "body",
                0
            ],
            "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
            "input": "123",
            "ctx": {
                "error": "invalid length: expected length 32 for simple format, found 3"
            }
            },
            {
            "type": "uuid_parsing",
            "loc": [
                "body",
                1
            ],
            "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
            "input": "456",
            "ctx": {
                "error": "invalid length: expected length 32 for simple format, found 3"
            }
            }
        ]
        }
    ),
    (
        ["3fa85f64-5717-4562-b3fc-2c963f66afa6",
         "3fa85f64-5717-4562-b3fc-2c963f66afa5"],
        404,
        {
            "detail": "The books with your IDs are not found."
        },
    )
])
async def test_delete_book_invalid_id(
        client,
        book_ids,
        expected_status_code,
        expected_detail,
    ):

    headers_for_auth = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])

    resp = client.request(
        method="DELETE",
        url=f"{VERSION_URL}{BOOK_URL}",
        json=book_ids,
        headers = headers_for_auth,
    )

    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail