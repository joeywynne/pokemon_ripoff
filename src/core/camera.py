from src.core.settings import DEADZONE_RATIO_WIDTH, DEADZONE_RATIO_HEIGHT
import pygame

class Camera:
    def __init__(self, width, height, map_width, map_height):
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        
        self.look_x = 0
        self.look_y = 0

        self.map_width = map_width
        self.map_height = map_height

        # DeadZone
        margin_x = width // DEADZONE_RATIO_WIDTH
        margin_y = height // DEADZONE_RATIO_HEIGHT
        self.deadzone = (
            margin_x,
            margin_y,
            width - 2 * margin_x,
            height - 2 * margin_y
        )

    def follow(self, target: pygame.Rect, velocity: list[float, float]):
        dz_x, dz_y, dz_w, dz_h = self.deadzone
        vx, vy = velocity

        lookahead_strength = 100
        max_speed = max(1, abs(vx) + abs(vy))
        
        if vx == 0:
            target_look_x = 0
        else:
            target_look_x = (vx / max_speed) * lookahead_strength if max_speed > 0 else 0
        if vy == 0:
            target_look_y = 0
        else:
            target_look_y = (vy / max_speed) * lookahead_strength if max_speed > 0 else 0
        
        look_smoothing = 0.15

        self.look_x += (target_look_x - self.look_x) * look_smoothing
        self.look_y += (target_look_y - self.look_y) * look_smoothing

        adjusted_target = target.move(int(self.look_x), int(self.look_y))
        
        # Convert to World coordinates
        left = self.x + dz_x
        right = self.x + dz_x + dz_w
        top = self.y + dz_y
        bottom = self.y + dz_y + dz_h

        target_x = self.x
        target_y = self.y

        if adjusted_target.left < left:
            target_x = adjusted_target.left - dz_x
        elif adjusted_target.right > right:
            target_x = adjusted_target.right - dz_x - dz_w

        if adjusted_target.top < top:
            target_y = adjusted_target.top - dz_y
        elif adjusted_target.bottom > bottom:
            target_y = adjusted_target.bottom - dz_y - dz_h

        self.smooth(target_x, target_y)
        self.clamp()

    def smooth(self, target_x, target_y):
        smoothing = 0.25
        self.x += (target_x - self.x) * smoothing
        self.y += (target_y - self.y) * smoothing

    def clamp(self):
        self.x = max(0, min(self.x, self.map_width - self.width))
        self.y = max(0, min(self.y, self.map_height - self.height))
