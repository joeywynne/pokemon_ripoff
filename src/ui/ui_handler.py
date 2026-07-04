from typing import Protocol
import logging

logger = logging.getLogger(__name__)


class UIScreen(Protocol):
    def handle_event(self, event) -> None: ...

    def update(self, keys) -> None: ...

    def render(self, surface) -> None: ...


class UIManager:
    def __init__(self):
        self.current_screen: UIScreen | None = None

    @property
    def has_screen(self) -> bool:
        return self.current_screen is not None

    def open(self, screen: UIScreen | None):
        self.current_screen = screen

    def close(self):
        self.current_screen = None

    def handle_event(self, event):
        if self.has_screen:
            self.current_screen.handle_event(event)

    def update(self, keys):
        if self.has_screen:
            self.current_screen.update(keys)

    def render(self, surface):
        if self.has_screen:
            self.current_screen.render(surface)
