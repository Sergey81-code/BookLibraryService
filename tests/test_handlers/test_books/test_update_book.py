import datetime

import pytest
from uuid_extensions import uuid7

from tests.conftest import BOOK_URL, VERSION_URL

from tests.utils_for_tests import create_auth_headers_for_user
from utils.roles import PortalRole


async def test_update_book(
        client, 
        create_author_in_database, 
        create_book_in_database,
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})


    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    )

    assert resp.status_code == 200
    data_from_resp = resp.json()

    assert data_from_resp['name'] == book_updated_info['name']
    assert data_from_resp['description'] == book_updated_info['description']
    assert data_from_resp['url'] == book_updated_info['url']
    assert data_from_resp['year'] == book_updated_info['year']
    assert data_from_resp['totalAmount'] == book_updated_info['totalAmount']
    assert data_from_resp['borrowedAmount'] == book_updated_info['borrowedAmount']

    for author_key in author1_info.keys():
        assert str(data_from_resp['authors'][0][author_key]) == str(author1_info[author_key])
        if author_key in author3_info.keys():
            assert str(data_from_resp['authors'][1][author_key]) == str(author3_info[author_key])

    book_from_db = await get_book_from_database(data_from_resp['id'])
    assert str(book_from_db["id"]) == data_from_resp['id']
    assert book_from_db["name"] == book_updated_info["name"]
    assert book_from_db["description"] == book_updated_info["description"]
    assert book_from_db["url"] == book_updated_info["url"]
    assert book_from_db["year"] == book_updated_info["year"]
    assert book_from_db["totalAmount"] == book_updated_info["totalAmount"]
    assert book_from_db["borrowedAmount"] == book_updated_info["borrowedAmount"]
    assert [{"id": str(author["author_id"])} for author in book_from_db["authors"]] == book_updated_info["authors"]


async def test_update_book_duplicate_name(
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    book_info_same_name = {
        "id": uuid7(),
        "name": "UpdatedBookName",
        "description": "Descriptions of this book.111",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#151111",
        "year": 2010,
        "totalAmount": 12,
        "borrowedAmount": 3,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})
    book_info_same_name['authors'].append({'id': str(author1_id)})
    book_info_same_name['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)
    await create_book_in_database(book_info_same_name)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})


    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    )

    assert resp.status_code == 400
    assert resp.json() == {"detail": "Book name UpdatedBookName already taken"}



async def test_update_book_not_authenticated(
        client, 
        create_author_in_database,
        create_book_in_database,
        get_project_settings
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})


    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Not authenticated"}
    else:
        assert resp.status_code == 200







async def test_update_book_unauth(
        client, 
        create_author_in_database,
        create_book_in_database,
        get_project_settings
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})


    
    auth_header = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(auth_header)) : next(iter(auth_header.values())) + "a"}


    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers = bad_auth_header,
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Could not validate credentials"}
    else:
        assert resp.status_code == 200




async def test_update_book_no_privilage(
        client, 
        create_author_in_database,
        create_book_in_database,
        get_project_settings
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})



    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_USER]),
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Forbidden: insufficient permissions"}
    else:
        assert resp.status_code == 200





async def test_update_book_bad_cred(
        client, 
        create_author_in_database,
        create_book_in_database,
        get_project_settings
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
    author3_info = {
        "id": uuid7(),
        "name": "Роберт Мартин",
        "birthday": datetime.date(1950, 8, 9)
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

    book_updated_info = {
        "name": "UpdatedBookName",
        "description": "Updated descriptions of this book.",
        "url": "https://updated_archive.org/stream/aliceinwonderlan00carriala#17",
        "year": 2014,
        "totalAmount": 12,
        "borrowedAmount": 5,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    author3_id = await create_author_in_database(author3_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    book_updated_info['authors'].append({'id': str(author1_id)})
    book_updated_info['authors'].append({'id': str(author3_id)})



    auth_header = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(auth_header)) : "Bearer 111"}

    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers=bad_auth_header,
    )
    
    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Could not validate credentials"}
    else:
        assert resp.status_code == 200








@pytest.mark.parametrize(
        "book_updated_info, expected_status_code, expected_detail",
        [
            (
                {},
                422,
                {
                "detail": "At least one parameter for book update info should be proveded"
                }
            ),
            (
                {
                    "totalAmount": 0,
                    "borrowedAmount": 0,
                },
                 422,
                {
                "detail": [
                    {
                    "type": "greater_than",
                    "loc": [
                        "body",
                        "totalAmount"
                    ],
                    "msg": "Input should be greater than 0",
                    "input": 0,
                    "ctx": {
                        "gt": 0
                    }
                    }
                ]
                }
            ),
            (
                {
                    "totalAmount": 1,
                    "borrowedAmount": -2,
                },
                 422,
                {
                "detail": [
                    {
                    "type": "greater_than_equal",
                    "loc": [
                        "body",
                        "borrowedAmount"
                    ],
                    "msg": "Input should be greater than or equal to 0",
                    "input": -2,
                    "ctx": {
                        "ge": 0
                    }
                    }
                ]
                }
            ),
            (
                {
                    "totalAmount": 1,
                    "borrowedAmount": 2,
                },
                422,
                {
                "detail": "borrowedAmount cannot be greater than totalAmount"
                }
            ),
            (
                {
                    "authors": [
                        {
                        "id": "123",
                        }
                    ]
                },
                422,
                {
                "detail": [
                    {
                    "type": "uuid_parsing",
                    "loc": [
                        "body",
                        "authors",
                        0,
                        "id"
                    ],
                    "msg": "Input should be a valid UUID, invalid length: expected length 32 for simple format, found 3",
                    "input": "123",
                    "ctx": {
                        "error": "invalid length: expected length 32 for simple format, found 3"
                    }
                    }
                ]
                },
            ),
            (
                {
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                400,
                {
                "detail": "At least one valid author must be provided to create a book."
                },
            ),
        ])
async def test_update_book_invalid_data(
        client, 
        create_book_in_database,
        create_author_in_database,
        book_updated_info, 
        expected_status_code, 
        expected_detail
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

    resp = client.patch(
        f"{VERSION_URL}{BOOK_URL}/?book_id={book_info["id"]}", json=book_updated_info,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    )

    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail
