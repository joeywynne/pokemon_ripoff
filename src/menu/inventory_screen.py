# This may become a menu later...
import pygame


class InventoryScreen():
    def __init__(self):
        self.selected_index = 0
        self.visible = False
        # delay before we do another move
        self.move_timer = 0
        self.move_delay = 6
        self.subsequent_move_delay = 3
        self.first_press = False


    def update(self, keys, game_state):
        moving = (
            keys[pygame.K_UP] or
            keys[pygame.K_DOWN]
        )

        if not moving:
            self.first_press = False
            self.move_timer = 0
            return
    
        if self.move_timer > 0:
            self.move_timer -= 1
    
        max_index = len(game_state.party) - 1
        if keys[pygame.K_DOWN]:
            direction = 1

        elif keys[pygame.K_UP]:
            direction = -1
        
        self.try_navigate(direction, max_index)

    def try_navigate(self, move_index: int, max_idx):
        if self.move_timer > 0:
            return
        
        end_idx = self.selected_index + move_index
        self.selected_index = max(0, min(end_idx, max_idx))

        if self.first_press:
            self.move_timer = self.subsequent_move_delay
        else:
            self.move_timer = self.move_delay

        self.first_press = True
