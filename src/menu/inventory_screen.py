# This may become a menu later...
import pygame


class InventoryScreen():
    def __init__(self):
        self.selected_index = 0
        self.buddy_index = -1
        self.visible = False
        # delay before we do another move
        self.move_timer = 0
        self.move_delay = 6
        self.subsequent_move_delay = 3
        self.first_press = False


    def update(self, keys, game_state):
        if not self.visible:
            return
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
            self.try_navigate(1, max_index)

        elif keys[pygame.K_UP]:
            self.try_navigate(-1, max_index)
    
    def handle_event(self, event):
        if event.key == pygame.K_i:
            self.visible = not self.visible
            return
        
        if not self.visible:
            return
        if event.key == pygame.K_SPACE:
            self.try_select_buddy() 

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

    def try_select_buddy(self):
        if self.selected_index != self.buddy_index:
            self.buddy_index = self.selected_index
        else:
            # Deselect buddy
            self.buddy_index = -1
