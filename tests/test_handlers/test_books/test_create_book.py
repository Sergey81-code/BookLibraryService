import datetime

import pytest
from uuid_extensions import uuid7

from tests.conftest import BOOK_URL, VERSION_URL

from tests.utils_for_tests import create_auth_headers_for_user
from utils.roles import PortalRole


async def test_create_book(
        client, 
        create_author_in_database, 
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

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
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

    book_from_db = await get_book_from_database(data_from_resp['id'])
    assert str(book_from_db["id"]) == data_from_resp['id']
    assert book_from_db["name"] == book_info["name"]
    assert book_from_db["description"] == book_info["description"]
    assert book_from_db["url"] == book_info["url"]
    assert book_from_db["year"] == book_info["year"]
    assert book_from_db["totalAmount"] == book_info["totalAmount"]
    assert book_from_db["borrowedAmount"] == book_info["borrowedAmount"]
    assert [{"id": str(author["author_id"])} for author in book_from_db["authors"]] == book_info["authors"]


async def test_create_book_duplicate_name(
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

    book_info_same_name = {
        "name": "BookName",
        "description": "Descriptions of this book.111",
        "url": "https://archive.org/stream/aliceinwonderlan00carriala#151111",
        "year": 2010,
        "totalAmount": 12,
        "borrowedAmount": 3,
        "authors": []
    }

    author1_id = await create_author_in_database(author1_info)
    author2_id = await create_author_in_database(author2_info)
    book_info['authors'].append({'id': str(author1_id)})
    book_info['authors'].append({'id': str(author2_id)})
    book_info_same_name['authors'].append({'id': str(author1_id)})
    book_info_same_name['authors'].append({'id': str(author2_id)})

    await create_book_in_database(book_info)

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info_same_name,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    )

    assert resp.status_code == 400
    assert resp.json() == {"detail": "Book with name BookName already exists."}



async def test_create_book_not_authenticated(
        client, 
        create_author_in_database,
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
    book_info = {
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

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Not authenticated"}
    else:
        assert resp.status_code == 200



async def test_create_book_unauth(
        client, 
        create_author_in_database,
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
    book_info = {
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
    auth_header = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(auth_header)) : next(iter(auth_header.values())) + "a"}


    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
        headers = bad_auth_header,
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Could not validate credentials"}
    else:
        assert resp.status_code == 200




async def test_create_book_no_privilage(
        client, 
        create_author_in_database,
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
    book_info = {
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

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
        headers = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_USER]),
    )

    
    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 403
        assert resp.json() == {"detail": "Forbidden: insufficient permissions"}
    else:
        assert resp.status_code == 200





async def test_create_book_bad_cred(
        client, 
        create_author_in_database,
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
    book_info = {
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

    auth_header = await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN])
    bad_auth_header = {next(iter(auth_header)) : "Bearer 111"}

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
        headers=bad_auth_header,
    )

    settings = await get_project_settings()

    if settings.ENABLE_ROLE_CHECK == True:
        assert resp.status_code == 401
        assert resp.json() == {"detail": "Could not validate credentials"}
    else:
        assert resp.status_code == 200







@pytest.mark.parametrize(
        "book_info, expected_status_code, expected_detail",
        [
            (
                {},
                422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "name"
                    ],
                    "msg": "Field required",
                    "input": {}
                    },
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "year"
                    ],
                    "msg": "Field required",
                    "input": {}
                    },
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "totalAmount"
                    ],
                    "msg": "Field required",
                    "input": {}
                    },
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "borrowedAmount"
                    ],
                    "msg": "Field required",
                    "input": {}
                    },
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "authors"
                    ],
                    "msg": "Field required",
                    "input": {}
                    }
                ]
                },
            ),
            (
                {
                    "description": "string",
                    "url": "string",
                    "year": 0,
                    "totalAmount": 1,
                    "borrowedAmount": 0,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                 422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "name"
                    ],
                    "msg": "Field required",
                    "input": {
                        "description": "string",
                        "url": "string",
                        "year": 0,
                        "totalAmount": 1,
                        "borrowedAmount": 0,
                        "authors": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                            },
                        ]
                    }
                    }
                ]
                }
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "totalAmount": 1,
                    "borrowedAmount": 0,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                 422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "year"
                    ],
                    "msg": "Field required",
                    "input": {
                        "name": "String",
                        "url": "string",
                        "totalAmount": 1,
                        "borrowedAmount": 0,
                        "authors": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                            },
                        ]
                    }
                    }
                ]
                },
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "borrowedAmount": 0,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                 422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "totalAmount"
                    ],
                    "msg": "Field required",
                    "input": {
                        "name": "String",
                        "url": "string",
                        "year": 2003,
                        "borrowedAmount": 0,
                        "authors": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                            },
                        ]
                    }
                    }
                ]
                }
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                 422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "borrowedAmount"
                    ],
                    "msg": "Field required",
                    "input": {
                        "name": "String",
                        "url": "string",
                        "year": 2003,
                        "totalAmount": 1,
                        "authors": [
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                            },
                            {
                                "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                            },
                        ]
                    }
                    }
                ]
                }
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "borrowedAmount": 0,
                },
                 422,
                {
                "detail": [
                    {
                    "type": "missing",
                    "loc": [
                        "body",
                        "authors"
                    ],
                    "msg": "Field required",
                    "input": {
                        "name": "String",
                        "url": "string",
                        "year": 2003,
                        "totalAmount": 1,
                        "borrowedAmount": 0
                    }
                    }
                ]
                }
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 0,
                    "borrowedAmount": 0,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
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
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "borrowedAmount": -2,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
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
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "borrowedAmount": 2,
                    "authors": [
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
                        },
                        {
                            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa5"
                        },
                    ]
                },
                422,
                {
                "detail": "borrowedAmount cannot be greater than totalAmount"
                }
            ),
            (
                {
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "borrowedAmount": 0,
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
                    "name": "string",
                    "url": "string",
                    "year": 2003,
                    "totalAmount": 1,
                    "borrowedAmount": 0,
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
async def test_create_book_invalid_data(
        client, 
        book_info, 
        expected_status_code, 
        expected_detail
    ):

    resp = client.post(
        f"{VERSION_URL}{BOOK_URL}", json=book_info,
        headers=await create_auth_headers_for_user([PortalRole.ROLE_PORTAL_ADMIN]),
    )

    assert resp.status_code == expected_status_code
    assert resp.json() == expected_detail
