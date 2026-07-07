import pygame
from src.ui.renderers.text_input_renderer import TextInputRenderer

class TextInputModal:
    def __init__(self, renderer: TextInputRenderer, on_submit, on_cancel, text: str = ""):
        self.renderer = renderer
        self.on_submit = on_submit
        self.on_cancel = on_cancel
        self.text = text
        self.max_length = 25  # Maximum length of the input text

        self.cursor_visible = True
        self.cursor_timer = 0

    def update(self, keys):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.on_submit(self)

            elif event.key == pygame.K_ESCAPE:
                self.on_cancel()  # Indicate cancellation
            
            else:
                # Handle text input
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    char = event.unicode
                    if char and char.isprintable():
                        if len(self.text) < self.max_length:
                            self.text += char

    def render(self, surface):
        self.renderer.render(surface, self)
