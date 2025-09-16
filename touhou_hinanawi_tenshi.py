import sys
import pygame
import math
from random import randint
from settings import Settings
from hinanawi_tenshi import HinanawiTenshi
from world_background import PixelWorld
from bullet_ga import BulletGa
from enemy import Dog_1
from game_stats import GameStats
from time import sleep
from button import Button

image_2 = pygame.image.load("/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/g_2.jpg")

class DamageText(pygame.sprite.Sprite):
    def __init__(self, amount, target_rect, font):
        super().__init__()
        self.amount = int(amount)
        self.font = font
        # render once
        self.image = self.font.render(str(self.amount), True, (255, 80, 80))
        self.image = self.image.convert_alpha()
        # start just above the target
        self.anchor = pygame.Vector2(target_rect.centerx, target_rect.top)
        self.rect = self.image.get_rect(midbottom=self.anchor)
        # animation timing
        self.birth_ms = pygame.time.get_ticks()
        self.life_ms = 700      # ms on screen
        self.rise_px = 40       # how far to move up
        self.start_alpha = 255

    def update(self):
        now = pygame.time.get_ticks()
        t = (now - self.birth_ms) / self.life_ms
        if t >= 1.0:
            self.kill()
            return
        # move up and fade out
        y = self.anchor.y - int(self.rise_px * t)
        self.rect.midbottom = (self.anchor.x, y)
        self.image.set_alpha(int(self.start_alpha * (1.0 - t)))

class TouhouHinanawiTenshi:
    def __init__(x):
        pygame.init()
        x.clock = pygame.time.Clock()
        x.settings = Settings()
        x.screen = pygame.display.set_mode((x.settings.screen_width,x.settings.screen_height))
        pygame.display.set_caption("Touhou Hinanawi Tenshi")
        x.stats = GameStats(x)
        # --- font and damage texts ---
        pygame.font.init()
        x.font_damage = pygame.font.Font(None, 28)
        # HUD font and baseline for max life (fallbacks if GameStats doesn't expose it)
        x.font_hud = pygame.font.Font(None, 20)
        x._life_max = getattr(x.stats, "life_max", getattr(x.stats, "max_life", x.stats.life_left))
        x.damage_texts = pygame.sprite.Group()
        x.hinanawi_tenshi = HinanawiTenshi(x)
        x.attack_B_1_right = pygame.sprite.Group()
        x.attack_B_1_left = pygame.sprite.Group()
        x.bullet_gas_right = pygame.sprite.Group()
        x.bullet_gas_left = pygame.sprite.Group()
        x.dogs_1 = pygame.sprite.Group()
        x.screen.fill((255, 255, 255))
        x.last_key = None
        x.left_down = False
        x.right_down = False
        x.flag = None
        x.bullet_flag = None
        x.shot_bulllet_B = False
        x.Background_1__frames = [pygame.transform.scale(pygame.image.load(f"/Users/dog/Desktop/python_work/Touhou_Hinanawi_Tenshi/graphs/Background_1/frame_{i}.jpg"), (x.settings.screen_width, x.settings.screen_height)) for i in range(0,240)]
        x.world = PixelWorld(tile_size=16, chunk_tiles=32, load_radius=2, seed=20250830)
        sw, sh = x.screen.get_size()
        x._cam_anchor = pygame.Vector2(sw * 0.5, sh * 0.5)
        x._cam_last_ms = pygame.time.get_ticks()
        x._ga_emitted = False
        x.GA_RELEASE_FRAME = 6
        x.game_active = False
        x.dog_1_killed_number = 0
        x.play_button = Button(x, "Play")
        x._create_four_dogs_1()
    
    def _draw_hud(x):
        """Draw a simple HP bar at the top-left of the screen."""
        # Resolve max life with sensible fallbacks
        life_max = getattr(x.stats, "life_max", getattr(x.stats, "max_life", getattr(x, "_life_max", 5)))
        if life_max <= 0:
            life_max = 1
        life = max(0, min(getattr(x.stats, "life_left", 0), life_max))

        # Bar geometry
        margin = 10
        bar_w = 600
        bar_h = 30
        bg_rect = pygame.Rect(margin, margin, bar_w, bar_h)

        # Background & border
        pygame.draw.rect(x.screen, (40, 40, 40), bg_rect)
        pygame.draw.rect(x.screen, (255, 255, 255), bg_rect, 2)

        # Fill based on life ratio
        ratio = life / float(life_max)
        fill_w = int((bar_w - 4) * ratio)
        fill_rect = pygame.Rect(margin + 2, margin + 2, fill_w, bar_h - 4)
        # Color shifts from red (low) to green (high)
        fill_color = (int(255 * (1.0 - ratio)), int(255 * ratio), 40)
        if fill_w > 0:
            pygame.draw.rect(x.screen, fill_color, fill_rect)

        # Text label: "HP current/max"
        try:
            label = x.font_hud.render(f"HP {life}/{life_max}", True, (255, 255, 255))
            x.screen.blit(label, (margin + 4, margin + bar_h + 4))
        except Exception:
            pass

    def _draw_kill_counter(x):
        """Draw a compact kill counter badge at the top-right of the screen."""
        # Prepare label
        kills = int(getattr(x, 'dog_1_killed_number', 0))
        text = f"Dog Kills: {kills}"
        surf = x.font_hud.render(text, True, (255, 255, 255))
        tw, th = surf.get_size()

        # Geometry (top-right)
        margin = 10
        padding = 8
        sw, sh = x.screen.get_size()
        bg_rect = pygame.Rect(0, 0, tw + padding * 2, th + padding * 2)
        bg_rect.top = margin
        bg_rect.right = sw - margin

        # Background + border for readability
        pygame.draw.rect(x.screen, (40, 40, 40), bg_rect)
        pygame.draw.rect(x.screen, (255, 255, 255), bg_rect, 2)

        # Text
        x.screen.blit(surf, (bg_rect.left + padding, bg_rect.top + padding))

    def draw_debug_boxes(x):
        # --- Tenshi ---
        if hasattr(x.hinanawi_tenshi, "rect"):
            # cyan rect
            pygame.draw.rect(x.screen, (0, 255, 255), x.hinanawi_tenshi.rect, 2)
            # center crosshair
            cx, cy = x.hinanawi_tenshi.rect.center
            pygame.draw.line(x.screen, (0, 255, 255), (cx - 5, cy), (cx + 5, cy), 1)
            pygame.draw.line(x.screen, (0, 255, 255), (cx, cy - 5), (cx, cy + 5), 1)

            # optional: Tenshi mask outline (yellow)
            if getattr(x.hinanawi_tenshi, "mask", None):
                outline = x.hinanawi_tenshi.mask.outline()
                if outline:
                    pts = [(x.hinanawi_tenshi.rect.left + px,
                            x.hinanawi_tenshi.rect.top  + py) for (px, py) in outline]
                    pygame.draw.lines(x.screen, (255, 255, 0), True, pts, 1)

        # --- Dogs ---
        for d in x.dogs_1.sprites():
            # red rect
            pygame.draw.rect(x.screen, (255, 0, 0), d.rect, 2)

            # light red fill to see coverage
            fill = pygame.Surface(d.rect.size, pygame.SRCALPHA)
            fill.fill((255, 0, 0, 40))
            x.screen.blit(fill, d.rect.topleft)

            # optional: dog mask outline (yellow)
            if getattr(d, "mask", None):
                outline = d.mask.outline()
                if outline:
                    pts = [(d.rect.left + px, d.rect.top + py) for (px, py) in outline]
                    pygame.draw.lines(x.screen, (255, 255, 0), True, pts, 1)

    def _check_events(x):
        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            x._check_play_button(mouse_pos)
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                x.hinanawi_tenshi.moving_right = True
                                x.flag = "right"
                                x.bullet_flag = "right"
                                x.last_key = pygame.K_RIGHT
                                x.right_down = True
                            if event.key == pygame.K_LEFT:
                                x.hinanawi_tenshi.moving_left = True
                                x.flag = "left"
                                x.bullet_flag = "left"
                                x.last_key = pygame.K_LEFT
                                x.left_down = True
                            if event.key == pygame.K_LSHIFT:
                                x.hinanawi_tenshi.moving_fast = True
                            if event.key == pygame.K_z:
                                x.choice = randint(1,2)
                                if x.choice == 1:
                                    x.hinanawi_tenshi.dash_forward_air_A = True
                                if x.choice == 2:
                                    x.hinanawi_tenshi.dash_forward_air_B = True
                            if event.key == pygame.K_x:
                                x.hinanawi_tenshi.attack_B_1 = True
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.sit_down = True
                                x.hinanawi_tenshi.stand_up = False
                                x.hinanawi_tenshi.frame_hinanawi_tenshi_sit_index = 0
                                x.hinanawi_tenshi.frame_hinanawi_tenshi_stand_index = 0
                                try:
                                    x.hinanawi_tenshi.sit_phase = "sit_down"
                                except Exception:
                                    pass
                            if event.key == pygame.K_c:
                                x._ga_emitted = True
                                x.hinanawi_tenshi.shot_B = True
                                x.shot_bulllet_B = True
                            if event.key == pygame.K_a:
                                x.debug_draw = not getattr(x, "debug_draw", False)
                            if event.key == pygame.K_v:
                                x.hinanawi_tenshi.spell_call = True

                                                    

                        elif event.type == pygame.KEYUP:
                            if event.key == pygame.K_RIGHT:
                                x.hinanawi_tenshi.moving_right = False  
                                x.right_down = False   
                            if event.key == pygame.K_LEFT:
                                x.hinanawi_tenshi.moving_left = False
                                x.left_down = False
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.moving_down = False
                            if event.key == pygame.K_UP:
                                x.hinanawi_tenshi.moving_up = False   
                            if event.key == pygame.K_LSHIFT:
                                x.hinanawi_tenshi.moving_fast = False 
                            if event.key == pygame.K_DOWN:
                                x.hinanawi_tenshi.sit_down = False
                                x.hinanawi_tenshi.stand_up = True
                            if event.key == pygame.K_z:
                                x.hinanawi_tenshi.dash_forward_air_A = False
                                x.hinanawi_tenshi.dash_forward_air_B = False




        if x.left_down and x.right_down:
            if x.last_key == pygame.K_RIGHT:
                  x.hinanawi_tenshi.moving_left = False
            if x.last_key == pygame.K_LEFT:
                  x.hinanawi_tenshi.moving_right = False

    def _check_screen(x):
            if x.last_key == None:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
                x.bullet_flag = "right"
            elif x.last_key == pygame.K_LEFT:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_left()
                x.flag = "left"
                x.bullet_flag = "left"
            elif x.last_key == pygame.K_RIGHT:
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
                x.bullet_flag = "right"
            elif x.flag == "right":
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_right()
                x.flag = "right"
                x.bullet_flag = "right"
            elif x.flag == "left":
                x.hinanawi_tenshi_blitme_type = x.hinanawi_tenshi.blitme_left()
                x.flag = "left"
                x.bullet_flag = "left"

    def _check_play_button(x, mouse_pos):
        button_clicked = x.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not x.game_active:
            x.stats.reset_stats()
            x.game_active = True
            pygame.mouse.set_visible(False)
    def _player_screen_center(x):
        rlist = getattr(x.hinanawi_tenshi, "rects_hinanawi_tenshi_dash_forward_air_A", None)
        if rlist:
            idx = getattr(x.hinanawi_tenshi, "frame_hinanawi_tenshi_dash_forward_air_A_index", 0)
            if len(rlist) > 0:
                r = rlist[int(idx) % len(rlist)]
                return float(r.centerx), float(r.centery)

        sw, sh = x.screen.get_size()
        return float(sw) * 0.5, float(sh) * 0.5

    def _update_world_camera_deadzone(x) -> None:

        now = pygame.time.get_ticks()
        last = getattr(x, "_cam_last_ms", now)
        x._cam_last_ms = now
        dt = max(1e-3, (now - last) / 1000.0)

        sx, sy = x._player_screen_center()

        sw, sh = x.screen.get_size()
        DEADZONE_W_RATIO = 0.2
        DEADZONE_H_RATIO = 0.35
        dz_w = int(sw * DEADZONE_W_RATIO)
        dz_h = int(sh * DEADZONE_H_RATIO)
        dz_l = sw // 2 - dz_w // 2
        dz_t = sh // 2 - dz_h // 2
        dz_r = dz_l + dz_w
        dz_b = dz_t + dz_h

        offx = 0.0
        if   sx < dz_l: offx = sx - dz_l
        elif sx > dz_r: offx = sx - dz_r

        offy = 0.0
        if   sy < dz_t: offy = sy - dz_t
        elif sy > dz_b: offy = sy - dz_b

        if offx == 0.0 and offy == 0.0:
            x.world.update_camera(x.world.cam_x, x.world.cam_y)
            return

        CAM_LERP_PER_SEC = 12.0
        alpha = 1.0 - math.exp(-CAM_LERP_PER_SEC * dt)  # 0..1（帧率无关）

        old_cam_x, old_cam_y = x.world.cam_x, x.world.cam_y
        target_cam_x = old_cam_x + offx
        target_cam_y = old_cam_y + offy
        x.world.cam_x = old_cam_x + (target_cam_x - old_cam_x) * alpha
        x.world.cam_y = old_cam_y + (target_cam_y - old_cam_y) * alpha

        dx_cam = x.world.cam_x - old_cam_x
        dy_cam = x.world.cam_y - old_cam_y

        rlist = getattr(x.hinanawi_tenshi, "rects_hinanawi_tenshi_dash_forward_air_A", None)
        if rlist and (dx_cam != 0.0 or dy_cam != 0.0):
            sx_int = int(round(dx_cam))
            sy_int = int(round(dy_cam))
            if sx_int or sy_int:
                for r in rlist:
                    r.move_ip(-sx_int, -sy_int)
        x.world.update_camera(x.world.cam_x, x.world.cam_y)

    def shot_bullet_ga(x):
        new_bullet_ga = BulletGa(x)
        if x.bullet_flag == "right":
            x.bullet_gas_right.add(new_bullet_ga)
        if x.bullet_flag == "left":
            x.bullet_gas_left.add(new_bullet_ga)

    def _create_four_dogs_1(x):
        new_dog_1 = Dog_1(x)
        new_dog_2 = Dog_1(x)
        new_dog_3 = Dog_1(x)
        new_dog_4 = Dog_1(x)
        x.dogs_1.add(new_dog_1)
        x.dogs_1.add(new_dog_2)
        x.dogs_1.add(new_dog_3)
        x.dogs_1.add(new_dog_4)
    
    def _create_one_dogs_1(x):
        new_dog_1 = Dog_1(x)
        x.dogs_1.add(new_dog_1)

    def spawn_damage_text(x, amount, target_rect, size=None):
        font = x.font_damage if size is None else pygame.font.Font(None, int(size))
        dt = DamageText(amount, target_rect, font)
        x.damage_texts.add(dt)

    def _hinanawi_tenshi_hit(x):
        if x.stats.life_left > 0:
            x.stats.life_left -= 1
        else:
            x.game_active = False

    def run_game(x):
        while True:
            x._check_events()
            if x.game_active == True:
                x._update_world_camera_deadzone()
                x.world.draw(x.screen)

                if x.game_active == True:
                    for dog_1 in x.dogs_1.sprites():
                        if dog_1.state == "alive":
                            if dog_1.hurt and dog_1.flag == "left":
                                dog_1.update_dog_1_hurt_left()
                                dog_1.hurt = False
                            elif dog_1.hurt and dog_1.flag == "right":
                                dog_1.update_dog_1_hurt_right()
                                dog_1.hurt = False
                            elif -700 <= x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx <= -300:
                                if dog_1.dog_1_hp >= 3:
                                    dog_1.update_dog_1_walk_left()
                                    dog_1.flag = "left"
                                elif dog_1.dog_1_hp <3:
                                    dog_1.update_dog_1_walk_right()
                                    dog_1.flag = "right"
                            elif 300 <= x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx <= 700:
                                if dog_1.dog_1_hp >= 3:
                                    dog_1.update_dog_1_walk_right()
                                    dog_1.flag = "right"
                                elif dog_1.dog_1_hp < 3:
                                    dog_1.update_dog_1_walk_left()
                                    dog_1.flag = "left"
                            elif x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx < -700:
                                if dog_1.dog_1_hp >= 3 :
                                    dog_1.update_dog_1_idle_left()
                                    dog_1.flag = "left"
                                elif dog_1.dog_1_hp < 3:
                                    dog_1.update_dog_1_walk_right()
                                    dog_1.flag = "right"
                            elif x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx > 700:
                                if dog_1.dog_1_hp >= 3:
                                    dog_1.update_dog_1_idle_right()
                                    dog_1.flag = "right"
                                elif dog_1.dog_1_hp < 3:
                                    dog_1.update_dog_1_walk_left()
                                    dog_1.flag = "left"
                            elif -300 < x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx <= 0:
                                if dog_1.dog_1_hp == 5:
                                    dog_1.update_dog_1_threaten_left()
                                elif 3 <= dog_1.dog_1_hp < 5:
                                    dog_1.update_dog_1_attack_left()
                                    collisions = pygame.sprite.spritecollide(x.hinanawi_tenshi, x.dogs_1, False, pygame.sprite.collide_mask)
                                    if collisions:
                                        x._hinanawi_tenshi_hit()
                                        x.spawn_damage_text(1, x.hinanawi_tenshi.rect, 100)
                                        for d in collisions:
                                            d.wx = d.wx + 150
                                        x.hinanawi_tenshi.gaurd_upper_B = True
                                elif 1 <= dog_1.dog_1_hp < 3:
                                    dog_1.update_dog_1_walk_right()
                                elif dog_1.dog_1_hp < 1:
                                    dog_1.state = "die"
                                    x.dog_1_killed_number += 1
                                dog_1.flag = "left"
                            elif 0 < x.hinanawi_tenshi.rects_hinanawi_tenshi_dash_forward_air_A[x.hinanawi_tenshi.frame_hinanawi_tenshi_dash_forward_air_A_index].x - dog_1.sx <= 300:
                                if dog_1.dog_1_hp == 5:
                                    dog_1.update_dog_1_threaten_right()
                                elif 3 <= dog_1.dog_1_hp < 5:
                                    dog_1.update_dog_1_attack_right()
                                    collisions = pygame.sprite.spritecollide(x.hinanawi_tenshi, x.dogs_1, False, pygame.sprite.collide_mask)
                                    if collisions:
                                        x._hinanawi_tenshi_hit()
                                        x.spawn_damage_text(1, x.hinanawi_tenshi.rect, 100)
                                        for d in collisions:
                                            d.wx = d.wx - 150
                                    x.hinanawi_tenshi.gaurd_upper_B = True
                                elif 1 <= dog_1.dog_1_hp < 3:
                                    dog_1.update_dog_1_walk_left()
                                elif dog_1.dog_1_hp < 1:
                                    dog_1.state = "die"
                                    x.dog_1_killed_number += 1
                                dog_1.flag = "right"

                        if dog_1.state == "die" and dog_1.flag == "right":
                            dog_1.update_dog_1_die_right()
                        if dog_1.state == "die" and dog_1.flag == "left":
                            dog_1.update_dog_1_die_left()
                        if dog_1.state == "die" and dog_1.frame_dog_1_die_index >= len(dog_1.frames_dog_1_die) - 1:
                            if not getattr(dog_1, "corpsed", False):
                                dog_1.corpsed = True
                                x._create_one_dogs_1()

                    if x.shot_bulllet_B:
                        for bullet_ga_1 in x.bullet_gas_right.sprites():
                            bullet_ga_1.draw_bullet_right()

                        for bullet_ga_2 in x.bullet_gas_left.sprites():
                            bullet_ga_2.draw_bullet_left()


                    
                    for bullet_ga_1 in x.bullet_gas_right.sprites():
                        bullet_ga_1.update_right()
                        collisions = pygame.sprite.groupcollide(x.bullet_gas_right, x.dogs_1, True, False, pygame.sprite.collide_mask)
                        if collisions:
                            for dogs in collisions.values():
                                for d in dogs:
                                    d.dog_1_hp = d.dog_1_hp - x.settings.attack_bullet_ga_damage
                                    x.spawn_damage_text(x.settings.attack_bullet_ga_damage, d.rect, 170)
                                    d.hurt = True
                                    if d.dog_1_hp <= 0 and d.state == "alive":
                                        d.state = "die"
                                        x.dog_1_killed_number += 1
                                        d.frame_dog_1_die_index = 0
                                        d.flag = "right" if x.hinanawi_tenshi.rect.centerx >= d.rect.centerx else "left"

                    for bullet_ga_2 in x.bullet_gas_left.sprites():   
                        bullet_ga_2.update_left() 
                        collisions = pygame.sprite.groupcollide(x.bullet_gas_left, x.dogs_1, True, False, pygame.sprite.collide_mask)
                        if collisions:
                            for dogs in collisions.values():
                                for d in dogs:
                                    d.dog_1_hp = d.dog_1_hp - x.settings.attack_bullet_ga_damage
                                    x.spawn_damage_text(x.settings.attack_bullet_ga_damage, d.rect, 170)
                                    d.hurt = True
                                    if d.dog_1_hp <= 0 and d.state == "alive":
                                        d.state = "die"
                                        x.dog_1_killed_number += 1
                                        d.frame_dog_1_die_index = 0
                                        d.flag = "right" if x.hinanawi_tenshi.rect.centerx >= d.rect.centerx else "left"

                    if x.hinanawi_tenshi.shot_B and x.flag == "right":
                        x.hinanawi_tenshi.function_shot_B_right()
                        if x._ga_emitted and x.hinanawi_tenshi.frame_hinanawi_tenshi_shot_B_index == x.GA_RELEASE_FRAME:
                            x.shot_bullet_ga()
                            x._ga_emitted = False
                            x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.shot_B and x.flag == "left":
                        x.hinanawi_tenshi.function_shot_B_left()
                        if x._ga_emitted and x.hinanawi_tenshi.frame_hinanawi_tenshi_shot_B_index == x.GA_RELEASE_FRAME:
                            x.shot_bullet_ga()
                            x._ga_emitted = False
                            x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.spell_call and x.flag == "right":
                        x.hinanawi_tenshi.function_spell_call_right()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)
                    
                    elif x.hinanawi_tenshi.spell_call and x.flag == "left":
                        x.hinanawi_tenshi.function_spell_call_left()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.attack_B_1 == True and x.flag == "right":
                        x.hinanawi_tenshi.function_attack_B_1_right()
                        x.attack_B_1_right.empty()
                        x.attack_B_1_right.add(x.hinanawi_tenshi)
                        collisions = pygame.sprite.groupcollide(x.attack_B_1_right, x.dogs_1, False, False, pygame.sprite.collide_mask)
                        if collisions and 6 >= x.hinanawi_tenshi.frame_hinanawi_tenshi_attack_B_1_index >= 5 and x.flag == "right":
                            for dogs in collisions.values():
                                for d in dogs:
                                    if d.state == "alive":
                                        d.dog_1_hp = d.dog_1_hp - x.settings.attack_B_1_damage
                                        x.spawn_damage_text(x.settings.attack_B_1_damage, d.rect, 100)
                                        d.hurt = True
                                        if d.dog_1_hp <= 0:
                                            d.state = "die"
                                            x.dog_1_killed_number += 1
                                            d.frame_dog_1_die_index = 0
                                            if x.hinanawi_tenshi.rect.centerx >= d.rect.centerx:
                                                d.flag = "right"
                                            else:
                                                d.flag = "left"
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)


                    elif x.hinanawi_tenshi.attack_B_1 == True and x.flag == "left":
                        x.hinanawi_tenshi.function_attack_B_1_left()
                        x.attack_B_1_left.empty()
                        x.attack_B_1_left.add(x.hinanawi_tenshi)
                        collisions = pygame.sprite.groupcollide(x.attack_B_1_left, x.dogs_1, False, False, pygame.sprite.collide_mask)
                        if collisions and 6 >= x.hinanawi_tenshi.frame_hinanawi_tenshi_attack_B_1_index >= 5 and x.flag == "left":
                            for dogs in collisions.values():
                                for d in dogs:
                                    if d.state == "alive":
                                        d.dog_1_hp = d.dog_1_hp - x.settings.attack_B_1_damage
                                        x.spawn_damage_text(x.settings.attack_B_1_damage, d.rect, 100)
                                        d.hurt = True
                                        if d.dog_1_hp <= 0:
                                            d.state = "die"
                                            x.dog_1_killed_number += 1
                                            d.frame_dog_1_die_index = 0
                                            if x.hinanawi_tenshi.rect.centerx >= d.rect.centerx:
                                                d.flag = "right"
                                            else:
                                                d.flag = "left"
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.gaurd_upper_B and x.flag == "right":
                        x.hinanawi_tenshi.function_gaurd_upper_B_right()
                        x.clock.tick(8)
                    
                    elif x.hinanawi_tenshi.gaurd_upper_B and x.flag == "left":
                        x.hinanawi_tenshi.function_gaurd_upper_B_left()
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.dash_forward_air_A and x.hinanawi_tenshi.moving_right:
                        x.hinanawi_tenshi.function_dash_forward_air_A_right()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.dash_forward_air_A and x.hinanawi_tenshi.moving_left:
                        x.hinanawi_tenshi.function_dash_forward_air_A_left()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)
                    
                    elif x.hinanawi_tenshi.dash_forward_air_B and x.hinanawi_tenshi.moving_right:
                        x.hinanawi_tenshi.function_dash_forward_air_B_right()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.dash_forward_air_B and x.hinanawi_tenshi.moving_left:
                        x.hinanawi_tenshi.function_dash_forward_air_B_left()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.sit_down:
                        if x.flag == "right":
                            x.hinanawi_tenshi.function_sit_down_right()
                        elif x.flag == "left":
                            x.hinanawi_tenshi.function_sit_down_left()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.stand_up and x.flag == "right":
                        x.hinanawi_tenshi.function_stand_up_right()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.stand_up and x.flag == "left":
                        x.hinanawi_tenshi.function_stand_up_left()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    elif x.hinanawi_tenshi.moving_right or x.hinanawi_tenshi.moving_left or x.hinanawi_tenshi.moving_up or x.hinanawi_tenshi.moving_down:
                        x.hinanawi_tenshi.update()
                        x.hinanawi_tenshi.gaurd_upper_B = False
                        x.clock.tick(8)

                    else:
                        x._check_screen()
                        x.clock.tick(8)

                x.damage_texts.update()
                x.damage_texts.draw(x.screen)

                # --- HUD (top-left health bar) ---
                x._draw_hud()
                # --- Kill counter (top-right) ---
                x._draw_kill_counter()

                if getattr(x, "debug_draw", False):
                    x.draw_debug_boxes()

            elif x.game_active == False:
                x.screen.blit(pygame.transform.scale(image_2,(x.settings.screen_width,x.settings.screen_height)),(0,0))
                pygame.mouse.set_visible(True)

            if not x.game_active:
                x.play_button.draw_button()

            pygame.display.flip()


if __name__ == '__main__':
    tht = TouhouHinanawiTenshi()
    tht.run_game()