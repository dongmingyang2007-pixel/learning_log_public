
import math
from typing import Dict, Tuple, List, Optional
import pygame

__all__ = ["PixelWorld"]

def _hash(ix: int, iy: int, seed: int = 0) -> float:
    n = ix * 374761393 + iy * 668265263 + seed * 1442695040
    n = (n ^ (n >> 13)) * 1274126177
    n = (n ^ (n >> 16)) & 0xFFFFFFFF
    return n / 0xFFFFFFFF

def _smooth(t: float) -> float:
    return t * t * (3 - 2 * t)

def _value2d(x: float, y: float, seed: int = 0) -> float:
    x0 = math.floor(x); y0 = math.floor(y)
    x1 = x0 + 1;        y1 = y0 + 1
    fx = x - x0;        fy = y - y0
    u = _smooth(fx);    v = _smooth(fy)
    n00 = _hash(x0, y0, seed); n10 = _hash(x1, y0, seed)
    n01 = _hash(x0, y1, seed); n11 = _hash(x1, y1, seed)
    nx0 = n00 * (1 - u) + n10 * u
    nx1 = n01 * (1 - u) + n11 * u
    return nx0 * (1 - v) + nx1 * v

def _fbm1d(x: float, seed: int, octaves: int = 5, lac: float = 2.0, gain: float = 0.5) -> float:
    a = 0.5; f = 1.0; t = 0.0; nrm = 0.0
    for i in range(octaves):
        t   += a * _value2d(x * f, 0.0, seed + 911 * i)
        nrm += a
        a *= gain; f *= lac
    return t / nrm if nrm else 0.0

def _ridged1d(x: float, seed: int) -> float:
    n = _fbm1d(x, seed, octaves=6, lac=2.1, gain=0.5)
    r = 1.0 - abs(2.0 * n - 1.0)
    return r * r

# ==================== PixelWorld ====================
class PixelWorld:

    SKY_TOP     = (214, 208, 224)
    SKY_HORIZON = (236, 216, 210)
    SUN_COLOR   = (255, 174, 122)

    FAR_MOUNT_1 = (56, 72, 94)
    FAR_MOUNT_2 = (46, 64, 82)

    MID_HILL    = (45, 86, 68)
    RIVER       = (178, 197, 205)
    RIVER_EDGE  = (120, 150, 160)
    PAGODA      = (92, 56, 56)
    ROOF        = (138, 90, 90)
    TORII       = (156, 52, 52)

    GROUND      = (66, 80, 70)
    GRASS       = (94, 132, 96)
    TREE_TRUNK  = (92, 66, 48)
    TREE_LEAF   = (66, 112, 74)
    FENCE       = (70, 62, 58)
    LANTERN     = (180, 180, 160)

    # 贴身带颜色
    BUSH_DARK   = (58, 100, 68)
    BUSH_MID    = (72, 124, 82)
    BUSH_LIGHT  = (94, 148, 102)
    FERN        = (64, 136, 94)
    BAMBOO      = (58, 140, 88)
    BAMBOO_LEAF = (70, 160, 96)
    STONE       = (115, 112, 108)
    STONE_LIGHT = (150, 146, 142)
    STUMP_TOP   = (132, 96, 68)
    STUMP_SIDE  = (94, 70, 52)
    FLOWER      = (236, 188, 198)
    GROUND_SHADE= (40, 55, 48)

    def __init__(self, settings=None, tile_size: int = 16, chunk_tiles: int = 32,
                 load_radius: int = 2, seed: int = 0, lock_vertical: bool = True):
        self.settings = settings
        self.tile = int(tile_size)
        self.chunk_tiles = int(chunk_tiles)
        self.chunk_px = self.tile * self.chunk_tiles
        self.load_radius = int(load_radius)
        self.seed = int(seed)
        self.lock_vertical = lock_vertical

        # camera
        self.cam_x = 0.0
        self.cam_y = 0.0

        # layers: (name, parallax)
        self.layers: List[Tuple[str, float]] = [
            ("far",  0.35),
            ("mid",  0.60),
            ("near", 0.95),
            ("fg",   1.15),
        ]
        self._chunks: Dict[str, Dict[Tuple[int, int], pygame.Surface]] = {k: {} for k, _ in self.layers}
        self._view_h: Optional[int] = None

        # ---- Close band parameters ----
        self.CLOSE_HALF_WIDTH = 300     # 覆盖范围
        self.CLOSE_PARALLAX   = 1.25    # 更贴脸
        self.CLOSE_STEP       = 10      # 基础步长（用于采样噪声等）
        self.CLOSE_DENSITY    = 1.15    # 全局密度
        self.CLOSE_SIZE_SCALE = 2.2     # ★ 贴身尺寸放大系数（核心）

        # 固定到底部
        self.CLOSE_BAND_FROM_BOTTOM    = 46
        self.CLOSE_BAND_WAVE_AMPLITUDE = 10
        self.CLOSE_BAND_WAVE_FREQ      = 0.006

    # -------------- Public API --------------
    def update_camera(self, x: float, y: float) -> None:
        self.cam_x = float(x)
        self.cam_y = 0.0 if self.lock_vertical else float(y)
        if self._view_h is None:
            return
        self._ensure_all_layers()

    def draw(self, screen: pygame.Surface) -> None:
        sw, sh = screen.get_size()
        if self._view_h != sh:
            self._view_h = sh
            for d in self._chunks.values():
                d.clear()
            self._ensure_all_layers()

        self._draw_sky(screen)
        self._draw_sun_once(screen)

        # 背景层
        for key, parallax in self.layers:
            d = self._chunks[key]
            cam_l = (self.cam_x - sw * 0.5) * parallax
            for (cx, _cy), surf in d.items():
                world_x = cx * self.chunk_px
                screen.blit(surf, (world_x - cam_l, 0))

        # 贴身后景层（在角色后面）
        #self._draw_close_band(screen, front=False)

    def draw_front(self, screen: pygame.Surface) -> None:
        """如需草丛遮脚：在画完天子后调用本方法。"""
        self._draw_close_band(screen, front=True)

    # -------------- Chunking --------------
    def _ensure_all_layers(self) -> None:
        for key, parallax in self.layers:
            center_cx = int(math.floor((self.cam_x * parallax) / self.chunk_px))
            needed = set()
            r = self.load_radius + 1
            for dx in range(-r, r + 1):
                needed.add((center_cx + dx, 0))
            d = self._chunks[key]
            for pos in needed:
                if pos not in d:
                    d[pos] = self._gen_chunk(key, pos[0], 0)
            for pos in list(d.keys()):
                if pos not in needed:
                    del d[pos]

    def _gen_chunk(self, layer: str, cx: int, cy: int) -> pygame.Surface:
        h = self._view_h if self._view_h else 540
        w = self.chunk_px
        surf = pygame.Surface((w, h), pygame.SRCALPHA).convert_alpha()
        world_x0 = cx * self.chunk_px
        horizon = int(h * 0.60)

        if layer == "far":
            for x in range(w):
                gx = world_x0 + x
                peak2 = int(horizon - (28 + _ridged1d(gx * 0.0032, self.seed + 90) * 100))
                pygame.draw.line(surf, self.FAR_MOUNT_2, (x, peak2), (x, horizon), 1)
                peak1 = int(horizon - (12 + _ridged1d(gx * 0.0046, self.seed + 100) * 70))
                pygame.draw.line(surf, self.FAR_MOUNT_1, (x, peak1), (x, horizon - 6), 1)

        elif layer == "mid":
            for x in range(w):
                gx = world_x0 + x
                ridge = int(horizon - (6 + _fbm1d(gx * 0.006, self.seed + 200) * 36))
                pygame.draw.line(surf, self.MID_HILL, (x, ridge), (x, horizon), 1)
            river_y = int(horizon + 6 + (_fbm1d(world_x0 * 0.001, self.seed + 250) - 0.5) * 10)
            thickness = 10
            pygame.draw.rect(surf, self.RIVER, pygame.Rect(0, river_y, w, thickness))
            pygame.draw.line(surf, self.RIVER_EDGE, (0, river_y), (w, river_y), 1)
            pygame.draw.line(surf, self.RIVER_EDGE, (0, river_y + thickness), (w, river_y + thickness), 1)
            self._scatter_pagodas(surf, world_x0, w, horizon - 2)
            self._scatter_torii_mid(surf, world_x0, w, horizon - 4)

        elif layer == "near":
            ground_base = int(horizon + 28)
            for x in range(w):
                gx = world_x0 + x
                gy = int(ground_base + (_fbm1d(gx * 0.008, self.seed + 300) - 0.5) * 14.0)
                pygame.draw.line(surf, self.GROUND, (x, gy), (x, h), 1)
                if _hash(gx, 0, self.seed + 301) > 0.982:
                    pygame.draw.line(surf, self.GRASS, (x, gy), (x, gy - 7), 1)
            self._scatter_small_trees(surf, world_x0, w, ground_base)
            self._scatter_fence_and_lanterns(surf, world_x0, w, ground_base)

        elif layer == "fg":
            ground = int(horizon + 32)
            self._scatter_big_foreground(surf, world_x0, w, ground)

        return surf

    # -------------- Mid/Near helpers --------------
    def _scatter_pagodas(self, surf: pygame.Surface, world_x0: int, w: int, horizon: int) -> None:
        x = 0
        while x < w:
            gx = world_x0 + x
            chance  = _hash(gx // 64, 0, self.seed + 501)
            spacing = 280 + int(chance * 260)
            if chance > 0.72:
                height = 44 + int(_hash(gx, 1, self.seed + 502) * 54)
                levels = 3  + int(_hash(gx, 2, self.seed + 503) * 3)
                cx = x + int((_hash(gx, 3, self.seed + 504) - 0.5) * 30)
                self._draw_pagoda(surf, cx, horizon, height, levels)
            x += spacing

    def _draw_pagoda(self, surf: pygame.Surface, cx: int, horizon: int, height: int, levels: int) -> None:
        base_y = horizon - 6
        body_w = max(14, int(height * 0.22))
        body_h = int(height * 0.55)
        rect = pygame.Rect(cx - body_w // 2, base_y - body_h, body_w, body_h)
        pygame.draw.rect(surf, self.PAGODA, rect)
        roof_span = body_w + 8
        roof_h = max(3, height // 18)
        for i in range(levels):
            y = rect.top + i * (body_h // max(1, (levels + 1)))
            span = int(roof_span * (1.0 - i * 0.12))
            pts = [(cx - span // 2, y), (cx, y - roof_h), (cx + span // 2, y)]
            pygame.draw.polygon(surf, self.ROOF, pts)
        pygame.draw.line(surf, self.ROOF, (cx, rect.top - roof_h), (cx, rect.top - roof_h - 10), 1)

    def _scatter_torii_mid(self, surf: pygame.Surface, world_x0: int, w: int, horizon: int) -> None:
        x = 40
        while x < w:
            gx = world_x0 + x
            chance  = _hash(gx // 48, 5, self.seed + 520)
            spacing = 120 + int(chance * 180)
            if chance > 0.78:
                width  = 18 + int(_hash(gx, 6, self.seed + 521) * 14)
                height = 16 + int(_hash(gx, 7, self.seed + 522) * 10)
                self._draw_torii(surf, x, horizon, width, height)
            x += spacing

    def _draw_torii(self, surf: pygame.Surface, x: int, horizon: int, width: int, height: int) -> None:
        base_y = horizon - 2
        post_w = max(2, width // 6)
        pygame.draw.rect(surf, self.TORII, pygame.Rect(x, base_y - height, post_w, height))
        pygame.draw.rect(surf, self.TORII, pygame.Rect(x + width - post_w, base_y - height, post_w, height))
        pygame.draw.rect(surf, self.TORII, pygame.Rect(x - 2, base_y - height - 3, width + 4, 4))
        pygame.draw.rect(surf, self.TORII, pygame.Rect(x,     base_y - height - 7, width,     3))

    def _scatter_small_trees(self, surf: pygame.Surface, world_x0: int, w: int, ground: int) -> None:
        x = 0
        while x < w:
            gx = world_x0 + x
            chance  = _hash(gx // 16, 0, self.seed + 601)
            spacing = 14 + int(chance * 20)
            if chance > 0.40:
                h = 28 + int(_hash(gx, 1, self.seed + 602) * 28)
                base_y = ground + 2 + int((_hash(gx, 2, self.seed + 603) - 0.5) * 4)
                self._draw_tree(surf, x, base_y, h)
            x += spacing

    def _draw_tree(self, surf: pygame.Surface, x: int, base_y: int, h: int) -> None:
        trunk_w = max(2, h // 10)
        trunk_h = int(h * 0.55)
        trunk = pygame.Rect(x, base_y - trunk_h, trunk_w, trunk_h)
        pygame.draw.rect(surf, self.TREE_TRUNK, trunk)
        r = max(4, h // 6)
        cy = trunk.top
        pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx, cy), r)
        pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx - r, cy + r // 2), int(r * 0.9))
        pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx + r, cy + r // 2), int(r * 0.9))

    def _scatter_fence_and_lanterns(self, surf: pygame.Surface, world_x0: int, w: int, ground: int) -> None:
        for x in range(0, w, 14):
            gx = world_x0 + x
            if _hash(gx // 14, 9, self.seed + 700) > 0.35:
                y = ground + 3
                pygame.draw.line(surf, self.FENCE, (x, y), (x + 12, y), 1)
                pygame.draw.line(surf, self.FENCE, (x, y - 4), (x + 12, y - 4), 1)
                pygame.draw.line(surf, self.FENCE, (x + 2, y - 6), (x + 2, y + 2), 1)
                pygame.draw.line(surf, self.FENCE, (x + 10, y - 6), (x + 10, y + 2), 1)
        x = 20
        while x < w:
            gx = world_x0 + x
            if _hash(gx // 64, 11, self.seed + 710) > 0.82:
                y = ground + 2
                pygame.draw.line(surf, self.LANTERN, (x, y - 12), (x, y), 1)
                pygame.draw.rect(surf, self.LANTERN, pygame.Rect(x - 3, y - 16, 6, 4))
            x += 60 + int(_hash(gx, 12, self.seed + 711) * 80)

    def _scatter_big_foreground(self, surf: pygame.Surface, world_x0: int, w: int, ground: int) -> None:
        x = 0
        while x < w:
            gx = world_x0 + x
            chance  = _hash(gx // 24, 0, self.seed + 800)
            spacing = 40 + int(chance * 40)
            if chance > 0.45:
                H = 58 + int(_hash(gx, 1, self.seed + 801) * 54)
                base_y = ground + 4 + int((_hash(gx, 2, self.seed + 802) - 0.5) * 6)
                trunk_w = max(3, H // 10)
                trunk_h = int(H * 0.58)
                trunk = pygame.Rect(x, base_y - trunk_h, trunk_w, trunk_h)
                pygame.draw.rect(surf, self.TREE_TRUNK, trunk)
                r = max(7, H // 5)
                cy = trunk.top
                pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx, cy), r)
                pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx - r, cy + r // 2), int(r * 0.9))
                pygame.draw.circle(surf, self.TREE_LEAF, (trunk.centerx + r, cy + r // 2), int(r * 0.9))
            x += spacing

    # -------------- Sky & Sun --------------
    def _draw_sky(self, screen: pygame.Surface) -> None:
        sw, sh = screen.get_size()
        for y in range(sh):
            t = y / max(1, sh - 1)
            r = int(self.SKY_TOP[0] * (1 - t) + self.SKY_HORIZON[0] * t)
            g = int(self.SKY_TOP[1] * (1 - t) + self.SKY_HORIZON[1] * t)
            b = int(self.SKY_TOP[2] * (1 - t) + self.SKY_HORIZON[2] * t)
            pygame.draw.line(screen, (r, g, b), (0, y), (sw, y))

    def _draw_sun_once(self, screen: pygame.Surface) -> None:
        sw, sh = screen.get_size()
        parallax = 0.35
        cam_l = (self.cam_x - sw * 0.5) * parallax
        SUN_REPEAT = 5000
        base   = (int(self.cam_x) // SUN_REPEAT) * SUN_REPEAT
        offset = int((_fbm1d(base * 0.0007, self.seed + 777) * 0.6 + 0.2) * SUN_REPEAT)
        sun_world_x = base + offset
        x_screen = int(sun_world_x - cam_l)
        y_screen = int(sh * 0.22)
        if -50 <= x_screen <= sw + 50:
            pygame.draw.circle(screen, self.SUN_COLOR, (x_screen, y_screen), 18)

    # ==================== Close band (procedural, big, layered) ====================
    def _close_ground_y(self, world_x: float, screen_height: int) -> int:
        """贴身带使用的“地面线”：以屏幕底部为基准 + 轻微起伏。"""
        base = screen_height - int(self.CLOSE_BAND_FROM_BOTTOM)
        wiggle = int((( _fbm1d(world_x * self.CLOSE_BAND_WAVE_FREQ, self.seed + 1990) - 0.5) * 2.0)
                     * self.CLOSE_BAND_WAVE_AMPLITUDE)
        return base + wiggle

    def _draw_close_band(self, screen: pygame.Surface, front: bool) -> None:
        sw, sh = screen.get_size()
        parallax = self.CLOSE_PARALLAX
        cam_l = (self.cam_x - sw * 0.5) * parallax

        half_w = int(self.CLOSE_HALF_WIDTH)
        start_world = self.cam_x - half_w
        end_world   = self.cam_x + half_w

        size_mul = self.CLOSE_SIZE_SCALE * (1.18 if front else 1.0)

        # ——底部暗线，避免“漂浮感”
        gy0 = self._close_ground_y(self.cam_x, sh)
        pygame.draw.line(screen, self.GROUND_SHADE, (0, gy0), (sw, gy0), 1)

        # 用“事件间距”而不是均匀步距，避免形成色块墙
        wx = int(start_world)
        while wx <= end_world:
            gx = wx
            # 确定性随机
            r_main = _hash(gx // 12, 0 if front else 1, self.seed + (930 if front else 920))
            # 动态间距：跟对象体量相关，避免挤成一条带
            base_spacing = 28 + int(r_main * 34)
            spacing = int(base_spacing * (size_mul * 0.8))
            spacing = max(18, spacing)

            x_screen = int(gx * parallax - cam_l)
            gy = self._close_ground_y(gx, sh)

            # 选择类型（按权重）；前景少一点石头，多些叶子，避免挡死画面
            choice = r_main
            if choice > 0.86:
                self._p_rock_poly(screen, x_screen, gy, int((24 + _hash(gx, 11, self.seed) * 32) * size_mul))
            elif choice > 0.72:
                self._p_stump(screen, x_screen, gy,
                              int((28 + _hash(gx, 12, self.seed) * 28) * size_mul),
                              int((14 + _hash(gx, 13, self.seed) * 12) * size_mul))
            elif choice > 0.56:
                self._p_bush_cluster(screen, x_screen, gy,
                                     int((40 + _hash(gx, 14, self.seed) * 48) * size_mul),
                                     int((24 + _hash(gx, 15, self.seed) * 22) * size_mul))
            elif choice > 0.40:
                self._p_grass_tuft(screen, x_screen, gy,
                                   int((28 + _hash(gx, 16, self.seed) * 28) * size_mul))
            elif choice > 0.26:
                self._p_fern(screen, x_screen, gy,
                             int((30 + _hash(gx, 17, self.seed) * 26) * size_mul))
            else:
                self._p_bamboo(screen, x_screen, gy,
                               int((100 + _hash(gx, 18, self.seed) * 90) * size_mul))

            # 地面接触阴影
            pygame.draw.line(screen, self.GROUND_SHADE, (x_screen - 8, gy), (x_screen + 8, gy), 1)
            wx += spacing

        # 点缀小花（稀疏）
        wx = int(start_world)
        while wx <= end_world:
            gx = wx
            if _hash(gx // 8, 5 if front else 4, self.seed + 940) > 0.82:
                xs = int(gx * parallax - cam_l)
                gy = self._close_ground_y(gx, sh)
                screen.fill(self.FLOWER, (xs, gy - 3, 3, 3))
            wx += 22

    # ---------- Procedural brushes (bigger / non-rectangular) ----------
    def _p_bush_cluster(self, surf: pygame.Surface, x: int, ground_y: int, w: int, h: int) -> None:
        """灌木丛：多颗半圆/圆叠加，不再是条状或方块。"""
        w = max(24, w); h = max(16, h)
        n = 4 + (w // 22)
        for i in range(n):
            t = (i / max(1, n - 1)) * w - w * 0.5
            cx = x + int(t) + int((_hash(x + i, i, self.seed) - 0.5) * 8)
            cy = ground_y - int(h * (0.6 + (_hash(x, i, self.seed + 1) * 0.4)))
            r  = max(8, int(h * (0.35 + _hash(x, i, self.seed + 2) * 0.4)))
            pygame.draw.circle(surf, self.BUSH_MID, (cx, cy), r)
            pygame.draw.circle(surf, self.BUSH_DARK, (cx - 3, cy + 2), max(1, r - 3))
            pygame.draw.circle(surf, self.BUSH_LIGHT, (cx + 2, cy - 2), max(1, r - 4))

    def _p_grass_tuft(self, surf: pygame.Surface, x: int, ground_y: int, h: int) -> None:
        """三角草尖簇（更大）"""
        h = max(18, h)
        half = max(12, h // 2)
        pts = [(x, ground_y),
               (x - half, ground_y - h),
               (x + half, ground_y - h)]
        pygame.draw.polygon(surf, self.GRASS, pts)

    def _p_fern(self, surf: pygame.Surface, x: int, ground_y: int, h: int) -> None:
        """蕨类：多层羽叶"""
        h = max(22, h)
        for k in range(5):
            t = ground_y - int(h * (0.22 + 0.15 * k))
            pygame.draw.line(surf, self.FERN, (x, t), (x + 16, t - 6), 1)
            pygame.draw.line(surf, self.FERN, (x, t), (x - 16, t - 2), 1)

    def _p_bamboo(self, surf: pygame.Surface, x: int, ground_y: int, h: int) -> None:
        """竹：更粗更高，带节与叶"""
        h = max(80, h)
        pygame.draw.line(surf, self.BAMBOO, (x, ground_y - h), (x, ground_y), 4)
        for k in range(5):
            y = ground_y - int(h * (0.20 + 0.16 * k))
            pygame.draw.line(surf, self.BAMBOO_LEAF, (x - 7, y), (x + 7, y), 1)
        ly = ground_y - int(h * 0.58)
        pygame.draw.line(surf, self.BAMBOO_LEAF, (x, ly), (x + 20, ly - 6), 1)
        pygame.draw.line(surf, self.BAMBOO_LEAF, (x, ly + 7), (x - 20, ly + 3), 1)

    def _p_rock_poly(self, surf: pygame.Surface, x: int, ground_y: int, size: int) -> None:
        """不规则石头（多边形+顶面高光），避免矩形色块感。"""
        s = max(18, size)
        # 5~7 点多边形
        cnt = 5 + int(_hash(x, 0, self.seed) * 3)
        pts = []
        for i in range(cnt):
            ang = (i / cnt) * math.tau
            rx = (math.cos(ang) * (s * 0.6 + _hash(x, i, self.seed + 10) * s * 0.25))
            ry = (math.sin(ang) * (s * 0.35 + _hash(x, i, self.seed + 11) * s * 0.20))
            pts.append((x + int(rx), ground_y - int(ry)))
        pygame.draw.polygon(surf, self.STONE, pts)
        # 顶部高光
        top = [(px, py - 2) for (px, py) in pts[: max(3, cnt // 2)]]
        if len(top) >= 3:
            pygame.draw.polygon(surf, self.STONE_LIGHT, top)

    def _p_stump(self, surf: pygame.Surface, x: int, ground_y: int, w: int, h: int) -> None:
        """树桩：侧面+椭圆顶"""
        w = max(20, w); h = max(12, h)
        side = pygame.Rect(x - w // 2, ground_y - h, w, h)
        pygame.draw.rect(surf, self.STUMP_SIDE, side)
        top = pygame.Rect(x - w // 2, ground_y - h - 4, w, 6)
        pygame.draw.ellipse(surf, self.STUMP_TOP, top)
