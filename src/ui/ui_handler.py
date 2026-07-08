from typing import Protocol
import logging

logger = logging.getLogger(__name__)


class UIScreen(Protocol):
    def handle_event(self, event) -> None: ...

    def update(self, keys) -> None: ...

    def render(self, surface) -> None: ...


class UIManager:
    def __init__(self):
        self.ui_stack: list[UIScreen] = []

    @property
    def is_open(self) -> bool:
        return len(self.ui_stack) > 0

    def open_screen(self, screen: UIScreen):
        self.ui_stack.append(screen)

    def close_screen(self):
        if self.ui_stack:
            self.ui_stack.pop()

    def handle_event(self, event):
        if self.ui_stack:
            self.ui_stack[-1].handle_event(event)

    def update(self, keys):
        if self.ui_stack:
            self.ui_stack[-1].update(keys)

    def render(self, surface):
        if self.ui_stack:
            self.ui_stack[-1].render(surface)
