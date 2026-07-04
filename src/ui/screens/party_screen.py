import pygame
from src.core.game_state import GameState
from src.ui.renderers.party_renderer import PartyRenderer

INITIAL_REPEAT_DELAY = 6
REPEAT_DELAY = 3


class PartyScreen:
    def __init__(self, game_state: GameState, renderer: PartyRenderer, on_close):
        self.game_state = game_state
        self.renderer = renderer
        self.on_close = on_close

        self.buddy_index = game_state.buddy_index
        self.selected_index = max(0, self.buddy_index)
    
        # delay before we do another move
        self.move_timer = 0
        self.first_press = False

    def update(self, keys):
        moving = keys[pygame.K_UP] or keys[pygame.K_DOWN]

        if not moving:
            self.first_press = False
            self.move_timer = 0
            return

        if self.move_timer > 0:
            self.move_timer -= 1

        max_index = len(self.game_state.party) - 1
        if keys[pygame.K_DOWN]:
            self.try_navigate(1, max_index)

        elif keys[pygame.K_UP]:
            self.try_navigate(-1, max_index)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.try_select_buddy()

            elif event.key in (pygame.K_ESCAPE, pygame.K_p):
                self.on_close(self)
                return

    def render(self, surface):
        self.renderer.render(surface, self)

    def try_navigate(self, move_index: int, max_idx):
        if self.move_timer > 0:
            return

        end_idx = self.selected_index + move_index
        self.selected_index = max(0, min(end_idx, max_idx))

        if self.first_press:
            self.move_timer = REPEAT_DELAY
        else:
            self.move_timer = INITIAL_REPEAT_DELAY

        self.first_press = True

    def try_select_buddy(self):
        if self.selected_index != self.buddy_index:
            self.buddy_index = self.selected_index
        else:
            # Deselect buddy
            self.buddy_index = -1
