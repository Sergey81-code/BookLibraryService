import enum


class BookStatuses(enum.StrEnum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    RESERVED = "reserved"
