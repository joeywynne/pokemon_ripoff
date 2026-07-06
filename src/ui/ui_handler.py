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
        self.current_modal: UIScreen | None = None

    @property
    def is_open(self) -> bool:
        return (self.current_screen is not None) or (self.current_modal is not None)

    def open_screen(self, screen: UIScreen | None):
        self.current_screen = screen

    def close_screen(self):
        self.current_screen = None
    
    def open_modal(self, modal: UIScreen | None):
        self.current_modal = modal

    @property
    def has_modal(self) -> bool:
        return self.current_modal is not None

    def close_modal(self):
        self.current_modal = None

    def handle_event(self, event):
        if self.current_screen:
            self.current_screen.handle_event(event)
        if self.current_modal:
            self.current_modal.handle_event(event)

    def update(self, keys):
        if self.current_screen:
            self.current_screen.update(keys)
        if self.current_modal:
            self.current_modal.update(keys)

    def render(self, surface):
        if self.current_screen:
            self.current_screen.render(surface)
        if self.current_modal:
            self.current_modal.render(surface)
