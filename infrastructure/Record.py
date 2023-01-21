class Record:
    def __init__(self, title, value, description=""):
        self.__title = title
        self.__description = description
        self.__value = value

    def __str__(self):
        return f"Title: {self.__title} ; Value: {self.__value} ; Description: {self.__description}"

    def __repr__(self):
        return f"{self.__title};{self.__description};{self.__value}"

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
