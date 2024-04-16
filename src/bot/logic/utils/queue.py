from __future__ import annotations

import dataclasses


@dataclasses.dataclass
class NewsItem:
    link: str
    next: NewsItem | None = dataclasses.field(default=None)


class LinksQueue:
    def __init__(self):
        self.__head = None
        self.__tail = None
        self.__length = 0

    def insert(self, new_link: str) -> None:
        if self.__head is None:
            self.__tail = NewsItem(link=new_link)
            self.__head = self.__tail
        else:
            new_item = NewsItem(link=new_link)
            self.__tail.next = new_item
            self.__tail = new_item

        self.__length += 1

    def pop(self) -> str | None:
        if self.__head is None:
            return None

        del_elem = self.__head
        self.__head = del_elem.next
        self.__length -= 1

        return del_elem.link

    def peek(self) -> str | None:
        if self.__head is None:
            return None

        return self.__head.link
