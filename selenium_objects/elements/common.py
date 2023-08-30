import time
from typing import ClassVar, Type

from .elements import Element
from .utils import remove_duplicates


class LazyList(Element):
    item_element: ClassVar[Type[Element]]
    lazy_load_wait_time: ClassVar[float] = 0
    scroll_direction: ClassVar[str] = 'down'

    def get_items(self):
        """Returns all the items on the page."""
        items = []
        previous_items = []
        while True:
            loaded_items = self.get_loaded_items()
            if loaded_items == previous_items:
                break
            previous_items = loaded_items
            items.extend(loaded_items)
            self.load_more_items()
        items = remove_duplicates(items)
        return items

    def get_loaded_items(self):
        """Returns the items that are currently loaded on the page."""
        self.driver.implicitly_wait(5)
        items = self.item_element.find_all(self.driver)
        return items

    def load_more_items(self):
        """Loads more items on the page."""
        self.scroll()
        time.sleep(self.lazy_load_wait_time)
    
    def scroll(self):
        """Scrolls the element to the top or bottom of its containing div."""
        if self.scroll_direction == 'down':
            self.scroll_to_bottom()
        elif self.scroll_direction == 'up':
            self.scroll_to_top()
        else:
            raise NotImplementedError('Only up and down scrolling are supported.')