import pygame
from src.ui.renderers.text_input_renderer import TextInputRenderer

class TextInputModal:
    def __init__(self, renderer: TextInputRenderer, on_submit):
        self.renderer = renderer
        self.on_submit = on_submit
        self.text = ""
        self.max_length = 25  # Maximum length of the input text

    def update(self, keys):
        pass  # No continuous updates needed for text input modal

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.on_submit(self)

            elif event.key == pygame.K_ESCAPE:
                self.on_submit(None)  # Indicate cancellation
            
            else:
                # Handle text input
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    char = event.unicode
                    if char.isprintable():
                        if len(self.text) < self.max_length:
                            self.text += char

    def render(self, surface):
        self.renderer.render(surface, self.text)
