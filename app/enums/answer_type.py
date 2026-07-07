from enum import Enum


class AnswerType(str, Enum):

    TEXT = "TEXT"

    NUMBER = "NUMBER"

    PHOTO = "PHOTO"

    PHOTO_TEXT = "PHOTO_TEXT"

    BOOLEAN = "BOOLEAN"

    DATE = "DATE"

    LOCATION = "LOCATION"
