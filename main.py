import pygame
import math
import sys
import random
import array

# ==================== SIGURAN HAPTIČKI SUSTAV ZA ANDROID ====================
vibrate_fn = None
try:
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    activity = PythonActivity.mActivity
    Context = autoclass('android.content.Context')
    vibrator_service = activity.getSystemService(Context.VIBRATOR_SERVICE)
    Build_VERSION = autoclass('android.os.Build$VERSION')
    sdk_int = Build_VERSION.SDK_INT
    VibrationEffect = autoclass('android.os.VibrationEffect') if sdk_int >= 26 else None

    def trigger_vibe(ms, strength=255):
        try:
            if vibrator_service and vibrator_service.hasVibrator():
                if VibrationEffect and sdk_int >= 26:
                    eff = VibrationEffect.createOneShot(int(ms), min(255, max(1, int(strength))))
                    vibrator_service.vibrate(eff)
                else:
                    vibrator_service.vibrate(int(ms))
        except Exception:
            pass
    vibrate_fn = trigger_vibe
except Exception:
    vibrate_fn = lambda ms, strength=255: None

def haptic(ms, strength=255):
    if vibrate_fn:
        try:
            vibrate_fn(ms, strength)
        except Exception:
            pass

# ==================== PROCEDURALNI ZVUKOVI ====================
audio_enabled = False
snd_step = None
snd_catch = None
snd_tear = None
snd_chew = None
snd_sting = None
snd_evolve = None
snd_burrow = None
snd_breath = None
snd_slam = None
snd_door = None
snd_charge = None
snd_dna = None
snd_hurt = None

try:
    pygame.mixer.pre_init(22050, -16, 1, 512)
    pygame.init()
    pygame.mixer.init()

    def synthesize_sound(sample_fn, duration_sec, volume=0.7):
        sr = 22050
        n_samples = int(sr * duration_sec)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / sr
            s = sample_fn(t, duration_sec)
            s = max(-1.0, min(1.0, s)) * volume
            buf.append(int(s * 32767))
        return pygame.mixer.Sound(buffer=buf.tobytes())

    snd_step = synthesize_sound(lambda t, dur: (math.sin(2 * math.pi * (140 - t * 2000) * t) * 0.6 + random.uniform(-0.3, 0.3)) * (1.0 - t / dur) ** 2, 0.05, 0.45)
    snd_catch = synthesize_sound(lambda t, dur: (random.uniform(-0.9, 0.9) if t < 0.015 else math.sin(2 * math.pi * 320 * t) * (1.0 - t / dur)), 0.08, 0.75)
    snd_tear = synthesize_sound(lambda t, dur: (random.uniform(-0.7, 0.7) * math.sin(2 * math.pi * 60 * t)) * (1.0 - (t / dur) ** 0.5), 0.14, 0.8)
    snd_chew = synthesize_sound(lambda t, dur: math.sin(2 * math.pi * (260 - t * 800) * t) * (1.0 - t / dur) + random.uniform(-0.25, 0.25) * (1.0 - t / dur), 0.09, 0.65)
    snd_sting = synthesize_sound(lambda t, dur: (math.sin(2 * math.pi * (180 + t * 900) * t) * 0.7 + (random.uniform(-0.8, 0.8) if t > 0.1 else 0)) * (1.0 - t / dur), 0.22, 0.95)
    snd_evolve = synthesize_sound(lambda t, dur: math.sin(2 * math.pi * (110 + t * 650) * t) * math.sin(2 * math.pi * 12 * t) * (1.0 - (t / dur) ** 2), 0.45, 0.9)
    snd_burrow = synthesize_sound(lambda t, dur: (random.uniform(-0.8, 0.8) * math.sin(2 * math.pi * 45 * t)) * (1.0 - t / dur), 0.25, 0.75)
    snd_breath = synthesize_sound(lambda t, dur: (random.uniform(-0.4, 0.4) * (1.0 - math.cos(2 * math.pi * t / dur))) * 0.5, 0.40, 0.35)
    snd_slam = synthesize_sound(lambda t, dur: (math.sin(2 * math.pi * (80 - t * 250) * t) * 0.8 + random.uniform(-0.5, 0.5)) * (1.0 - t / dur), 0.30, 1.0)
    snd_door = synthesize_sound(lambda t, dur: (math.sin(2 * math.pi * 90 * t) + random.uniform(-0.3, 0.3)) * (1.0 - math.cos(2 * math.pi * t / dur)), 0.50, 0.7)
    snd_charge = synthesize_sound(lambda t, dur: math.sin(2 * math.pi * (70 + t * 400) * t) * (1.0 - t / dur), 0.35, 0.9)
    snd_dna = synthesize_sound(lambda t, dur: math.sin(2 * math.pi * (520 + t * 950) * t) * (1.0 - t / dur), 0.18, 0.8)
    snd_hurt = synthesize_sound(lambda t, dur: (math.sin(2 * math.pi * (160 - t * 300) * t) + random.uniform(-0.4, 0.4)) * (1.0 - t / dur), 0.22, 0.85)
    audio_enabled = True
except Exception:
    pygame.init()

def play_snd(snd):
    if audio_enabled and snd:
        try:
            snd.play()
        except Exception:
            pass

# ==================== EKRAN I GRANICE ARENE ====================
info = pygame.display.Info()
WIDTH = info.current_w if info.current_w > 0 else 1080
HEIGHT = info.current_h if info.current_h > 0 else 1920

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if hasattr(pygame, 'FULLSCREEN') else 0)
actual_w, actual_h = screen.get_size()
WIDTH, HEIGHT = actual_w, actual_h

pygame.display.set_caption("APEX TITAN - Pure Biomechanical Edition")
clock = pygame.time.Clock()

HUD_BAR_HEIGHT = max(145, int(HEIGHT * 0.11))
SAFE_PAD_X = max(35, int(WIDTH * 0.045))
SAFE_PAD_BOTTOM = max(40, int(HEIGHT * 0.035))

MIN_X = SAFE_PAD_X
MAX_X = WIDTH - SAFE_PAD_X
MIN_Y = HUD_BAR_HEIGHT + 18
MAX_Y = HEIGHT - SAFE_PAD_BOTTOM

def clamp_x(val, extra=0):
    return max(MIN_X + extra, min(MAX_X - extra, val))

def clamp_y(val, extra=0):
    return max(MIN_Y + extra, min(MAX_Y - extra, val))

NEON_PINK_BORDER = (255, 30, 160)
NEON_PINK_GLOW = (255, 90, 200)

def get_border_rim_tint(x, y, max_dist=75):
    dist_left = x - MIN_X
    dist_right = MAX_X - x
    dist_top = y - MIN_Y
    dist_bottom = MAX_Y - y
    min_d = min(dist_left, dist_right, dist_top, dist_bottom)
    if min_d < max_dist:
        return 1.0 - (max(0, min_d) / float(max_dist))
    return 0.0

# ==================== POMOĆNE GEOMETRIJSKE FUNKCIJE ZA ROTIRANE ELIPSE ====================
def get_rotated_ellipse_pts(cx, cy, rx, ry, angle, segments=14):
    pts = []
    ca = math.cos(angle)
    sa = math.sin(angle)
    for i in range(segments):
        theta = (i / float(segments)) * math.pi * 2.0
        lx = math.cos(theta) * rx
        ly = math.sin(theta) * ry
        wx = cx + lx * ca - ly * sa
        wy = cy + lx * sa + ly * ca
        pts.append((wx, wy))
    return pts

def draw_rotated_ellipse(surf, color, cx, cy, rx, ry, angle, width=0, segments=14):
    pts = get_rotated_ellipse_pts(cx, cy, rx, ry, angle, segments)
    pygame.draw.polygon(surf, color, pts, width)
    return pts

# ==================== PJEŠČANI / ZEMLJANI TERARIJ ====================
terrain_surf = pygame.Surface((WIDTH, HEIGHT))
def generate_terrarium_surface():
    terrain_surf.fill((24, 18, 14))
    for _ in range(4500):
        rx = random.randint(MIN_X, MAX_X)
        ry = random.randint(MIN_Y, MAX_Y)
        grain_color = random.choice([
            (36, 26, 18), (48, 34, 24), (30, 20, 15),
            (60, 42, 28), (18, 12, 9), (72, 50, 34), (88, 66, 46)
        ])
        sz = random.choice([1, 1, 2, 2, 3])
        pygame.draw.rect(terrain_surf, grain_color, (rx, ry, sz, sz))

    for _ in range(75):
        kx = random.randint(MIN_X + 15, MAX_X - 15)
        ky = random.randint(MIN_Y + 15, MAX_Y - 15)
        kr = random.randint(3, 8)
        pygame.draw.ellipse(terrain_surf, (12, 8, 6), (kx - kr, ky - kr // 2 + 2, kr * 2, kr))
        pygame.draw.ellipse(terrain_surf, (68, 52, 40), (kx - kr, ky - kr // 2, kr * 2, kr))
        pygame.draw.ellipse(terrain_surf, (100, 84, 66), (kx - kr + 1, ky - kr // 2, kr, kr // 2))

generate_terrarium_surface()

night_overlay_night = pygame.Surface((WIDTH, HEIGHT))
night_overlay_night.fill((5, 10, 24))
night_overlay_night.set_alpha(110)

night_overlay_twilight = pygame.Surface((WIDTH, HEIGHT))
night_overlay_twilight.fill((24, 10, 18))
night_overlay_twilight.set_alpha(60)

world_surf = pygame.Surface((WIDTH, HEIGHT))

# ==================== PALETE BOJA SKORPIONA ====================
C_GROUND_SHADOW = (6, 4, 6)
C_CHROME = (230, 242, 252)

NORM_PAL = {
    'dark': (14, 11, 15),
    'plate': (30, 24, 30),
    'mid': (50, 38, 48),
    'light': (88, 68, 82),
    'spec': (185, 175, 195),
    'edge': (220, 225, 240),
    'shadow_edge': (8, 6, 9),
    'neon': (255, 30, 75),
    'core': (255, 130, 50),
    'fissure': (180, 30, 45)
}

OD_PAL = {
    'dark': (32, 8, 10),
    'plate': (64, 14, 18),
    'mid': (105, 18, 26),
    'light': (185, 42, 58),
    'spec': (255, 195, 125),
    'edge': (255, 120, 32),
    'shadow_edge': (16, 4, 6),
    'neon': (255, 225, 42),
    'core': (255, 245, 150),
    'fissure': (255, 100, 20)
}

MAGMA_PAL = {
    'dark': (10, 6, 8),
    'plate': (28, 14, 12),
    'mid': (70, 20, 12),
    'light': (170, 40, 12),
    'spec': (255, 150, 35),
    'edge': (255, 90, 18),
    'shadow_edge': (6, 3, 4),
    'neon': (255, 230, 55),
    'core': (255, 255, 190),
    'fissure': (255, 130, 15)
}

# ==================== DNA SUSTAV (GORIVO ZA SLAM) ====================
class DNAPickup:
    def __init__(self, x, y):
        self.x = clamp_x(x, 15)
        self.y = clamp_y(y, 15)
        self.life = 720
        self.pulse = random.uniform(0, math.pi * 2)

    def update(self):
        self.pulse += 0.08
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        fade = min(1.0, self.life / 60.0)
        sz = 13 + math.sin(self.pulse) * 3

        pts1, pts2 = [], []
        steps = 6
        for i in range(steps):
            t = (i / float(steps - 1)) * math.pi * 2
            y_off = (i - steps / 2.0) * 4.5
            x_off1 = math.sin(self.pulse + t) * (sz * 0.7)
            x_off2 = -x_off1
            p1 = (self.x + x_off1, self.y + y_off)
            p2 = (self.x + x_off2, self.y + y_off)
            pts1.append(p1)
            pts2.append(p2)
            pygame.draw.line(surf, (160, 255, 190), p1, p2, 1)

        if len(pts1) > 1:
            pygame.draw.lines(surf, (40, 255, 90), False, pts1, 3)
            pygame.draw.lines(surf, (20, 240, 150), False, pts2, 3)

        pygame.draw.circle(surf, (255, 255, 255), (int(self.x), int(self.y)), max(1, int(3 * fade)))

dna_collected = 45
dna_pickups = []

# ==================== EFEKTI, TRAGOVI I ČESTICE ====================
class BloodDrop:
    def __init__(self, x, y, vx, vy, color, size=4):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.life = 180

    def update(self):
        if abs(self.vx) > 0.08 or abs(self.vy) > 0.08:
            self.x = clamp_x(self.x + self.vx)
            self.y = clamp_y(self.y + self.vy)
            self.vx *= 0.84
            self.vy *= 0.84
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        fade = min(1.0, self.life / 35.0)
        c = (int(self.color[0] * fade), int(self.color[1] * fade), int(self.color[2] * fade))
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), max(1, int(self.size * (0.8 + 0.2 * fade))))

class PheromoneDot:
    def __init__(self, x, y, col):
        self.x = x
        self.y = y
        self.col = col
        self.life = 110
        self.max_life = 110

    def update(self):
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        fade = self.life / float(self.max_life)
        c = (int(self.col[0] * fade), int(self.col[1] * fade), int(self.col[2] * fade))
        pygame.draw.circle(surf, c, (int(self.x), int(self.y)), 1)

class StainedFootprint:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.life = 120
        self.max_life = 120

    def update(self):
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        fade = self.life / float(self.max_life)
        c = (int(self.color[0] * fade), int(self.color[1] * fade), int(self.color[2] * fade))
        pygame.draw.ellipse(surf, c, (int(self.x - self.radius), int(self.y - self.radius * 0.6), int(self.radius * 2), int(self.radius * 1.2)))

class MoltenFootprint:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.life = 90
        self.max_life = 90

    def update(self):
        self.life -= 1
        return self.life > 0

    def draw(self, surf):
        fade = self.life / float(self.max_life)
        col_outer = (int(255 * fade), int(70 * fade), int(15 * fade))
        col_core = (int(255 * fade), int(220 * fade), int(80 * fade))
        r = max(1, int(self.radius * fade))
        pygame.draw.circle(surf, col_outer, (int(self.x), int(self.y)), r + 2)
        pygame.draw.circle(surf, col_core, (int(self.x), int(self.y)), max(1, r // 2))

blood_drops = []
pheromone_dots = []
stained_footprints = []
molten_footprints = []
ground_cracks = []
shockwaves = []
particles = []
boss_projectiles = []

screen_shake = 0
flash_alpha = 0
flash_color = (255, 255, 255)

last_click_time = 0
DOUBLE_CLICK_THRESH = 280

active_boss = None
boss_schedule = [25, 45, 65, 85, 100]
boss_schedule_idx = 0

def add_shake(amount):
    global screen_shake
    screen_shake = max(screen_shake, amount)

def spill_blood(x, y, color, count=22, spread=5.8):
    for _ in range(count):
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(1.2, spread)
        blood_drops.append(BloodDrop(x, y, math.cos(ang) * spd, math.sin(ang) * spd, color, random.randint(2, 5)))

def emit_particles(x, y, color, count=14, speed_mult=1.0):
    for _ in range(count):
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(2.0, 5.5) * speed_mult
        life = random.randint(12, 22)
        particles.append([clamp_x(x), clamp_y(y), math.cos(ang) * spd, math.sin(ang) * spd, life, life, color])

def emit_magma_embers(x, y, count=8):
    for _ in range(count):
        ang = random.uniform(-math.pi * 0.8, -math.pi * 0.2)
        spd = random.uniform(1.5, 4.2)
        life = random.randint(15, 30)
        c = random.choice([(255, 60, 20), (255, 160, 30), (255, 230, 80)])
        particles.append([clamp_x(x), clamp_y(y), math.cos(ang) * spd, math.sin(ang) * spd, life, life, c])

class GroundCrackEffect:
    def __init__(self, x, y, max_radius=145, is_magma=False):
        self.x = clamp_x(x, 15)
        self.y = clamp_y(y, 15)
        self.duration = 150
        self.timer = 150
        self.is_magma = is_magma
        self.branches = []

        num_main = random.randint(5, 8)
        for i in range(num_main):
            base_ang = (i * (2 * math.pi / num_main)) + random.uniform(-0.35, 0.35)
            branch_len = max_radius * random.uniform(0.7, 1.2)
            cur_x, cur_y = self.x, self.y
            steps = random.randint(4, 6)
            step_len = branch_len / steps

            for s in range(steps):
                ang = base_ang + random.uniform(-0.40, 0.40)
                nx = clamp_x(cur_x + math.cos(ang) * step_len, 4)
                ny = clamp_y(cur_y + math.sin(ang) * step_len, 4)
                thick = max(1, 4 - s // 2)
                self.branches.append((cur_x, cur_y, nx, ny, thick))
                cur_x, cur_y = nx, ny

    def update(self):
        self.timer -= 1
        if self.is_magma and random.random() < 0.25:
            emit_magma_embers(self.x + random.uniform(-25, 25), self.y + random.uniform(-25, 25), count=1)
        return self.timer > 0

    def draw(self, surf):
        fade = self.timer / float(self.duration)
        alpha_mult = min(1.0, fade * 1.4)
        if self.is_magma:
            col_outer = (int(90 * alpha_mult), int(18 * alpha_mult), int(10 * alpha_mult))
            col_hot = (int(255 * alpha_mult), int(140 * alpha_mult), int(30 * alpha_mult))
            col_core = (int(255 * alpha_mult), int(240 * alpha_mult), int(120 * alpha_mult))
        else:
            col_outer = (int(50 * alpha_mult), int(12 * alpha_mult), int(18 * alpha_mult))
            col_hot = (int(255 * alpha_mult), int(190 * alpha_mult), int(75 * alpha_mult))
            col_core = None

        for x1, y1, x2, y2, thick in self.branches:
            pygame.draw.line(surf, col_outer, (x1, y1), (x2, y2), thick + 3)
            pygame.draw.line(surf, col_hot, (x1, y1), (x2, y2), max(1, thick + 1))
            if col_core:
                pygame.draw.line(surf, col_core, (x1, y1), (x2, y2), max(1, thick - 1))

def solve_ik(p0_x, p0_y, p2_x, p2_y, l1, l2, flip=1):
    dx = p2_x - p0_x
    dy = p2_y - p0_y
    dist = math.hypot(dx, dy)
    d = min(max(dist, 1e-4), l1 + l2 - 0.001)

    base_angle = math.atan2(dy, dx)
    cos_a = (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)
    cos_a = max(-1.0, min(1.0, cos_a))
    angle_a = math.acos(cos_a)

    joint_angle = base_angle + angle_a * flip
    jx = p0_x + math.cos(joint_angle) * l1
    jy = p0_y + math.sin(joint_angle) * l1
    return jx, jy

def to_world(lx, ly, bx, by, ang, scale_w=1.0, S=1.0):
    c, s = math.cos(ang), math.sin(ang)
    ly *= scale_w
    return int(bx + (lx * c - ly * s) * S), int(by + (lx * s + ly * c) * S)

def lerp(a, b, t):
    return a + (b - a) * t

def draw_electric_arc(surf, p1, p2, col_main, col_core=C_CHROME, segments=3, jitter=4, S=1.0):
    pts = [p1]
    dx = (p2[0] - p1[0]) / float(segments)
    dy = (p2[1] - p1[1]) / float(segments)
    for i in range(1, segments):
        jx = random.uniform(-jitter, jitter) * S
        jy = random.uniform(-jitter, jitter) * S
        pts.append((int(p1[0] + dx * i + jx), int(p1[1] + dy * i + jy)))
    pts.append(p2)
    for i in range(len(pts) - 1):
        pygame.draw.line(surf, col_core, pts[i], pts[i+1], max(1, int(1.2 * S)))
        pygame.draw.line(surf, col_main, pts[i], pts[i+1], max(1, int(2.5 * S)))

def draw_sagging_hose(surf, p1, p2, sag_amt, inertia_x, inertia_y, c_body, c_glow, S=1.0):
    mx = (p1[0] + p2[0]) / 2 + inertia_x
    my = (p1[1] + p2[1]) / 2 + sag_amt + inertia_y
    pts = []
    for i in range(7):
        t = i / 6.0
        bx = (1 - t)**2 * p1[0] + 2 * (1 - t) * t * mx + t**2 * p2[0]
        by = (1 - t)**2 * p1[1] + 2 * (1 - t) * t * my + t**2 * p2[1]
        pts.append((int(bx), int(by)))
    pygame.draw.lines(surf, c_body, False, pts, max(1, int(3.0 * S)))
    pygame.draw.lines(surf, c_glow, False, pts, max(1, int(1.2 * S)))

def draw_coil_spring(surf, p1, p2, compression, c_spring, num_coils=5, S=1.0):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    dist = math.hypot(dx, dy)
    if dist < 2: return
    ux, uy = dx / dist, dy / dist
    nx, ny = -uy, ux
    pygame.draw.line(surf, C_CHROME, p1, p2, max(1, int(2.5 * S)))
    coil_r = (4.0 + (1.0 - compression) * 3.5) * S
    pts = [p1]
    for i in range(1, num_coils * 2):
        t = i / (num_coils * 2.0)
        side = 1 if (i % 2 == 1) else -1
        cx = p1[0] + ux * (dist * t) + nx * (coil_r * side)
        cy = p1[1] + uy * (dist * t) + ny * (coil_r * side)
        pts.append((int(cx), int(cy)))
    pts.append(p2)
    pygame.draw.lines(surf, (15, 15, 18), False, pts, max(1, int(3.8 * S)))
    pygame.draw.lines(surf, c_spring, False, pts, max(1, int(1.8 * S)))

# ==================== EKOSUSTAV MRAVA: MRAVINJACI I IZVORI HRANE ====================
class Anthill:
    def __init__(self, x, y, active=False):
        self.x = clamp_x(x, 60)
        self.y = clamp_y(y, 60)
        self.active = active
        self.grains = 14 if active else 0
        self.grains_needed = 14
        self.radius = 28 if active else 12
        self.food_stored = 0
        self.deposit_pulse = 0.0

    def add_grain(self):
        if not self.active:
            self.grains += 1
            self.radius = 12 + int(16 * (self.grains / float(self.grains_needed)))
            if self.grains >= self.grains_needed:
                self.active = True
                emit_particles(self.x, self.y, (190, 150, 100), count=25)
                add_shake(8)

    def deposit_food(self):
        self.food_stored += 1
        self.deposit_pulse = 1.0
        emit_particles(self.x, self.y, (120, 230, 90), count=6, speed_mult=0.5)

    def draw(self, surf):
        if self.deposit_pulse > 0:
            self.deposit_pulse = max(0.0, self.deposit_pulse - 0.05)

        prog = min(1.0, self.grains / float(self.grains_needed))
        r = self.radius + int(self.deposit_pulse * 4)

        col_base = (75, 52, 36)
        col_top = (115, 88, 62)
        col_hole = (12, 8, 6)

        pygame.draw.ellipse(surf, (15, 10, 8), (self.x - r - 4, self.y - r * 0.6 + 4, (r + 4) * 2, (r * 0.6 + 4) * 2))
        pygame.draw.ellipse(surf, col_base, (self.x - r, self.y - r * 0.6, r * 2, r * 1.2))
        pygame.draw.ellipse(surf, col_top, (self.x - r * 0.7, self.y - r * 0.45, r * 1.4, r * 0.9))

        if self.active:
            pygame.draw.ellipse(surf, col_hole, (self.x - 8, self.y - 6, 16, 12))
            pygame.draw.circle(surf, (32, 22, 16), (int(self.x), int(self.y)), 4)
        else:
            pygame.draw.circle(surf, (180, 145, 95), (int(self.x), int(self.y)), 4)
            bar_w = 32
            bar_x = self.x - bar_w // 2
            bar_y = self.y - r - 8
            pygame.draw.rect(surf, (20, 14, 10), (bar_x, bar_y, bar_w, 4), border_radius=2)
            pygame.draw.rect(surf, (220, 180, 80), (bar_x, bar_y, int(bar_w * prog), 4), border_radius=2)

class FoodCluster:
    """Prirodni izvori hrane u terariju koje mravi pronalaze, režu čeljustima i nose u mravinjak."""
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.x = random.randint(MIN_X + 85, MAX_X - 85)
        self.y = random.randint(MIN_Y + 85, MAX_Y - 85)
        self.kind = random.choice(["leaf", "sugar", "protein"])
        self.charges = random.randint(8, 14)
        self.max_charges = self.charges
        if self.kind == "leaf":
            self.col_main = (55, 190, 50)
            self.col_light = (130, 240, 85)
        elif self.kind == "sugar":
            self.col_main = (210, 235, 250)
            self.col_light = (255, 255, 255)
        else:
            self.col_main = (230, 155, 45)
            self.col_light = (255, 215, 110)

    def harvest(self):
        self.charges -= 1
        emit_particles(self.x, self.y, self.col_light, count=5, speed_mult=0.45)
        if self.charges <= 0:
            self.respawn()

    def draw(self, surf):
        ratio = max(0.3, self.charges / float(self.max_charges))
        r = int(14 * ratio) + 4
        pygame.draw.ellipse(surf, C_GROUND_SHADOW, (int(self.x - r - 2), int(self.y - r * 0.6 + 3), (r + 2) * 2, int(r * 1.3)))
        if self.kind == "leaf":
            draw_rotated_ellipse(surf, (35, 125, 30), self.x, self.y, r * 1.3, r * 0.75, 0.4)
            draw_rotated_ellipse(surf, self.col_main, self.x, self.y, r * 1.1, r * 0.6, 0.4)
            pygame.draw.line(surf, self.col_light, (self.x - r * 0.8, self.y - r * 0.3), (self.x + r * 0.8, self.y + r * 0.3), 2)
        elif self.kind == "sugar":
            for i in range(4):
                ox = math.cos(i * 1.6) * (r * 0.45)
                oy = math.sin(i * 1.6) * (r * 0.45)
                pygame.draw.rect(surf, self.col_main, (int(self.x + ox - 4), int(self.y + oy - 4), 8, 8), border_radius=2)
                pygame.draw.rect(surf, self.col_light, (int(self.x + ox - 2), int(self.y + oy - 2), 4, 4))
        else:
            draw_rotated_ellipse(surf, self.col_main, self.x, self.y, r, r * 0.75, -0.3)
            draw_rotated_ellipse(surf, self.col_light, self.x - 2, self.y - 2, r * 0.55, r * 0.35, -0.3)

anthills = []
anthills.append(Anthill(MIN_X + 110, MIN_Y + 180, active=True))
anthills.append(Anthill(WIDTH // 2, HEIGHT // 2 + 100, active=True))
anthills.append(Anthill(MAX_X - 110, MAX_Y - 220, active=True))

for _ in range(5):
    rx = random.randint(MIN_X + 90, MAX_X - 90)
    ry = random.randint(MIN_Y + 90, MAX_Y - 90)
    anthills.append(Anthill(rx, ry, active=False))

food_clusters = [FoodCluster() for _ in range(4)]

# ==================== MRAVI: REALISTIČNA ANATOMIJA, FIZIKA I PAMETNE ULOGE ====================
class Ant:
    def __init__(self, force_gold=False):
        self.force_gold = force_gold
        self.paralyzed_timer = 0
        self.march_phase = random.uniform(0, 10.0)
        self.target_wx = 0.0
        self.target_wy = 0.0
        self.target_timer = 0

        # Uloge i radnje mrava
        self.role = "FORAGER"          # FORAGER, BUILDER, SOLDIER, QUEEN
        self.task_state = "SEEK_WORK"  # SEEK_WORK, HARVESTING, DELIVER_FOOD, DIGGING_SAND, DELIVER_SAND, PATROL
        self.work_timer = 0
        self.carried_item = None       # None, "leaf", "sugar", "protein", "sand", "egg"
        self.carried_col = (255, 255, 255)
        self.target_anthill = None
        self.target_food = None
        self.comm_timer = 0
        self.comm_partner_pos = None

        # Fizika zglobova i animacije tijela
        self.gaster_angle = 0.0
        self.antenna_phase = random.uniform(0, 6.28)
        self.mandible_open = 0.0
        self.legs = [[0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0] for _ in range(6)]
        self.respawn()

    def get_spawn_anthill(self):
        active_hills = [h for h in anthills if h.active]
        if active_hills:
            return random.choice(active_hills)
        return anthills[0]

    def assign_smart_task(self):
        active_hills = [h for h in anthills if h.active]
        incomplete_hills = [h for h in anthills if not h.active]

        if self.role == "QUEEN":
            # Kraljica prenosi ličinke/jajašca između aktivnih mravinjaka
            self.carried_item = "egg"
            self.carried_col = (250, 248, 235)
            self.target_anthill = random.choice(active_hills) if active_hills else anthills[0]
            self.target_wx = self.target_anthill.x
            self.target_wy = self.target_anthill.y
            self.task_state = "DELIVER_FOOD"
            self.target_timer = 260
            return

        if self.role == "SOLDIER":
            # Vojnik patrolira u radijusu oko aktivnog mravinjaka i čuva ulaz
            home = random.choice(active_hills) if active_hills else anthills[0]
            patrol_ang = random.uniform(0, math.pi * 2)
            patrol_r = random.uniform(45, 115)
            self.target_wx = clamp_x(home.x + math.cos(patrol_ang) * patrol_r, 50)
            self.target_wy = clamp_y(home.y + math.sin(patrol_ang) * patrol_r, 50)
            self.task_state = "PATROL"
            self.target_timer = random.randint(90, 160)
            return

        if self.role == "BUILDER" and incomplete_hills:
            # Graditelj traži pijesak pa ga nosi na gradilište novog mravinjaka
            if self.carried_item == "sand" and self.target_anthill and not self.target_anthill.active:
                self.target_wx = self.target_anthill.x
                self.target_wy = self.target_anthill.y
                self.task_state = "DELIVER_SAND"
                self.target_timer = 240
            else:
                self.target_anthill = random.choice(incomplete_hills)
                self.target_wx = random.randint(MIN_X + 80, MAX_X - 80)
                self.target_wy = random.randint(MIN_Y + 80, MAX_Y - 80)
                self.task_state = "SEEK_SAND"
                self.target_timer = 200
            return

        # FORAGER (Skupljač hrane): Odlazi do najbližeg ili nasumičnog izvora hrane, reže ga i nosi u mravinjak
        if self.carried_item in ("leaf", "sugar", "protein"):
            self.target_anthill = min(active_hills, key=lambda h: math.hypot(h.x - self.x, h.y - self.y)) if active_hills else anthills[0]
            self.target_wx = self.target_anthill.x
            self.target_wy = self.target_anthill.y
            self.task_state = "DELIVER_FOOD"
            self.target_timer = 260
        else:
            self.target_food = random.choice(food_clusters)
            self.target_wx = self.target_food.x
            self.target_wy = self.target_food.y
            self.task_state = "SEEK_FOOD"
            self.target_timer = 240

    def respawn(self):
        spawn_hill = self.get_spawn_anthill()
        self.x = spawn_hill.x + random.uniform(-6, 6)
        self.y = spawn_hill.y + random.uniform(-6, 6)
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)
        self.angle = random.uniform(0, math.pi * 2)
        self.gaster_angle = self.angle
        self.carried_item = None
        self.work_timer = 0
        self.comm_timer = 0

        if self.force_gold or random.random() < 0.12:
            self.type_name = "Zlatna Kraljica"
            self.role = "QUEEN"
            self.color_head = (210, 155, 15)
            self.color_thorax = (240, 185, 20)
            self.color_gaster = (255, 215, 35)
            self.color_accent = (255, 250, 180)
            self.color_legs = (150, 105, 15)
            self.blood_col = (255, 235, 70)
            self.max_spd = 3.9
            self.size = 14
            self.is_gold = True
        else:
            types = [
                {
                    "name": "Šumski Skupljač", "role": "FORAGER",
                    "head": (55, 22, 14), "thorax": (95, 34, 18), "gaster": (42, 16, 12),
                    "accent": (185, 95, 55), "legs": (38, 16, 10), "blood": (235, 45, 25), "spd": 3.6, "sz": 11
                },
                {
                    "name": "Kiselinski Radnik", "role": "FORAGER",
                    "head": (22, 48, 24), "thorax": (32, 85, 38), "gaster": (18, 38, 20),
                    "accent": (130, 245, 90), "legs": (18, 36, 18), "blood": (35, 255, 80), "spd": 3.4, "sz": 11
                },
                {
                    "name": "Pješčani Graditelj", "role": "BUILDER",
                    "head": (75, 42, 18), "thorax": (125, 70, 24), "gaster": (58, 32, 14),
                    "accent": (235, 175, 85), "legs": (52, 30, 14), "blood": (245, 140, 40), "spd": 3.5, "sz": 11
                },
                {
                    "name": "Oklopljeni Vojnik", "role": "SOLDIER",
                    "head": (32, 14, 14), "thorax": (65, 20, 18), "gaster": (24, 12, 14),
                    "accent": (255, 90, 40), "legs": (25, 12, 12), "blood": (255, 40, 30), "spd": 3.2, "sz": 13
                }
            ]
            chosen = random.choice(types)
            self.type_name = chosen["name"]
            self.role = chosen["role"]
            self.color_head = chosen["head"]
            self.color_thorax = chosen["thorax"]
            self.color_gaster = chosen["gaster"]
            self.color_accent = chosen["accent"]
            self.color_legs = chosen["legs"]
            self.blood_col = chosen["blood"]
            self.max_spd = chosen["spd"]
            self.size = chosen["sz"]
            self.is_gold = False

        self.assign_smart_task()

        for i in range(6):
            side = -1 if i % 2 == 0 else 1
            row = i // 2
            ang = self.angle + (math.pi / 2) * side + (row - 1) * 0.45
            self.legs[i][0] = self.x + math.cos(ang) * (self.size * 1.55)
            self.legs[i][1] = self.y + math.sin(ang) * (self.size * 1.55)
            self.legs[i][2] = 1.0
            self.legs[i][3] = self.legs[i][0]
            self.legs[i][4] = self.legs[i][1]
            self.legs[i][5] = self.legs[i][0]
            self.legs[i][6] = self.legs[i][1]

    def update(self, pred_x, pred_y, is_pred_burrowed, all_ants=None):
        self.antenna_phase += 0.25
        if self.paralyzed_timer > 0:
            self.paralyzed_timer -= 1
            return

        dx_p = self.x - pred_x
        dy_p = self.y - pred_y
        dist_p = math.hypot(dx_p, dy_p)
        flee_dist = 0 if is_pred_burrowed else 185

        # 1. Bijeg od škorpiona (ili obrambeni stav vojnika na rubu zone)
        if 0 < dist_p < flee_dist:
            self.work_timer = 0
            self.comm_timer = 0
            flee_x = (dx_p / dist_p) * self.max_spd * 1.45
            flee_y = (dy_p / dist_p) * self.max_spd * 1.45
            self.vx += (flee_x - self.vx) * 0.22
            self.vy += (flee_y - self.vy) * 0.22
            self.mandible_open = 0.7 + math.sin(self.antenna_phase * 2.0) * 0.3
        else:
            # 2. Aktivno rezanje hrane ili kopanje pijeska na mjestu
            if self.work_timer > 0:
                self.work_timer -= 1
                self.vx *= 0.65
                self.vy *= 0.65
                self.mandible_open = 0.5 + math.sin(self.work_timer * 0.65) * 0.45
                if self.work_timer % 10 == 0:
                    head_x = self.x + math.cos(self.angle) * (self.size * 1.2)
                    head_y = self.y + math.sin(self.angle) * (self.size * 1.2)
                    emit_particles(head_x, head_y, self.carried_col, count=2, speed_mult=0.35)
                if self.work_timer == 0:
                    if self.task_state == "HARVESTING" and self.target_food:
                        self.carried_item = self.target_food.kind
                        self.carried_col = self.target_food.col_main
                        self.target_food.harvest()
                    elif self.task_state == "DIGGING_SAND":
                        self.carried_item = "sand"
                        self.carried_col = (215, 175, 115)
                    self.assign_smart_task()
                self._update_kinematics(0.1)
                return

            # 3. Kratka komunikacija ticalima s drugim mravom kad se sretnu
            if self.comm_timer > 0:
                self.comm_timer -= 1
                self.vx *= 0.6
                self.vy *= 0.6
                if self.comm_partner_pos:
                    ang_to_p = math.atan2(self.comm_partner_pos[1] - self.y, self.comm_partner_pos[0] - self.x)
                    diff = (ang_to_p - self.angle + math.pi) % (2 * math.pi) - math.pi
                    self.angle += diff * 0.25
                self._update_kinematics(0.05)
                return

            if all_ants and random.random() < 0.03:
                for other in all_ants:
                    if other is not self and other.comm_timer == 0 and other.work_timer == 0:
                        d_ant = math.hypot(other.x - self.x, other.y - self.y)
                        if d_ant < 24:
                            self.comm_timer = 16
                            other.comm_timer = 16
                            self.comm_partner_pos = (other.x, other.y)
                            other.comm_partner_pos = (self.x, self.y)
                            break

            # 4. Izvršavanje zadatka (kretanje prema hrani, pijesku ili mravinjaku)
            self.target_timer -= 1
            if self.target_timer <= 0:
                self.assign_smart_task()

            dx_t = self.target_wx - self.x
            dy_t = self.target_wy - self.y
            dist_t = math.hypot(dx_t, dy_t)

            if dist_t < 24:
                if self.task_state == "SEEK_FOOD" and self.target_food:
                    self.task_state = "HARVESTING"
                    self.work_timer = 38
                    self.carried_col = self.target_food.col_light
                elif self.task_state == "DELIVER_FOOD" and self.target_anthill:
                    self.target_anthill.deposit_food()
                    self.carried_item = None
                    self.assign_smart_task()
                elif self.task_state == "SEEK_SAND":
                    self.task_state = "DIGGING_SAND"
                    self.work_timer = 34
                    self.carried_col = (215, 175, 115)
                elif self.task_state == "DELIVER_SAND" and self.target_anthill:
                    self.target_anthill.add_grain()
                    self.carried_item = None
                    self.assign_smart_task()
                else:
                    self.assign_smart_task()
            elif dist_t > 0:
                target_vx = (dx_t / dist_t) * (self.max_spd * 0.82)
                target_vy = (dy_t / dist_t) * (self.max_spd * 0.82)
                self.vx += (target_vx - self.vx) * 0.10
                self.vy += (target_vy - self.vy) * 0.10

            # Ispuštanje suptilnog feromonskog traga kad nosi teret prema mravinjaku
            if self.carried_item and random.random() < 0.16 and len(pheromone_dots) < 120:
                pheromone_dots.append(PheromoneDot(
                    self.x - math.cos(self.angle) * self.size,
                    self.y - math.sin(self.angle) * self.size,
                    (110, 210, 120) if self.carried_item != "sand" else (195, 160, 95)
                ))

            self.mandible_open = 0.28 if self.carried_item else 0.08

        # Odbijanje od rubova terarija
        wall_soft = 85
        if self.x < MIN_X + wall_soft:
            self.vx += (MIN_X + wall_soft - self.x) * 0.07
        elif self.x > MAX_X - wall_soft:
            self.vx -= (self.x - (MAX_X - wall_soft)) * 0.07

        if self.y < MIN_Y + wall_soft:
            self.vy += (MIN_Y + wall_soft - self.y) * 0.07
        elif self.y > MAX_Y - wall_soft:
            self.vy -= (self.y - (MAX_Y - wall_soft)) * 0.07

        spd = math.hypot(self.vx, self.vy)
        limit = self.max_spd * 1.45
        if spd > limit:
            self.vx = (self.vx / spd) * limit
            self.vy = (self.vy / spd) * limit

        if spd > 0.20:
            target_ang = math.atan2(self.vy, self.vx)
            diff = (target_ang - self.angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += diff * 0.24

        self.x = clamp_x(self.x + self.vx, 10)
        self.y = clamp_y(self.y + self.vy, 10)
        self._update_kinematics(spd)

    def _update_kinematics(self, spd):
        self.march_phase += 0.12 + spd * 0.09
        # Inercija zatka (gastera) - blago kasni za okretanjem prsišta i njiše se pri hodu
        g_diff = (self.angle - self.gaster_angle + math.pi) % (2 * math.pi) - math.pi
        self.gaster_angle += g_diff * 0.18 + math.sin(self.march_phase) * 0.025

        fwd = self.angle
        perp = self.angle + math.pi / 2
        s = self.size
        tripod_group = [0, 1, 1, 0, 0, 1]
        group_phase = int(self.march_phase // math.pi) % 2

        # 6 nogu pričvršćenih na prsište (mesosomu) s prirodnim kutovima za prednje, srednje i stražnje noge
        row_angles = [-0.62, 0.05, 0.72]
        row_reaches = [1.65, 1.55, 1.85]

        for i in range(6):
            side = -1 if (i % 2 == 0) else 1
            row = i // 2
            offset_fwd = (1 - row) * (s * 0.42)
            hip_x = self.x + math.cos(fwd) * offset_fwd + math.cos(perp) * (side * s * 0.34)
            hip_y = self.y + math.sin(fwd) * offset_fwd + math.sin(perp) * (side * s * 0.34)

            reach = s * row_reaches[row]
            rest_ang = fwd + (side * math.pi / 2) + (row_angles[row] * side)
            ideal_x = hip_x + math.cos(rest_ang) * reach
            ideal_y = hip_y + math.sin(rest_ang) * reach

            cur_leg = self.legs[i]
            dist_to_ideal = math.hypot(cur_leg[0] - ideal_x, cur_leg[1] - ideal_y)

            if dist_to_ideal > reach * 0.55 and cur_leg[2] >= 1.0 and (tripod_group[i] == group_phase or dist_to_ideal > reach * 0.95):
                cur_leg[5] = cur_leg[0]
                cur_leg[6] = cur_leg[1]
                cur_leg[3] = ideal_x + math.cos(fwd) * (spd * 3.2)
                cur_leg[4] = ideal_y + math.sin(fwd) * (spd * 3.2)
                cur_leg[2] = 0.0

            if cur_leg[2] < 1.0:
                cur_leg[2] += 0.32
                t = min(1.0, cur_leg[2])
                cur_leg[0] = cur_leg[5] + (cur_leg[3] - cur_leg[5]) * t
                cur_leg[1] = cur_leg[6] + (cur_leg[4] - cur_leg[6]) * t

    def draw(self, surf):
        fwd = self.angle
        perp = self.angle + math.pi / 2
        s = self.size

        # 0. Realistična sjena ispod dijelova tijela mrava
        draw_rotated_ellipse(surf, C_GROUND_SHADOW, self.x + 2, self.y + 3, s * 1.6, s * 0.75, fwd, segments=10)

        # 1. NOGE MRAVA (3 članka: Femur -> Tibia -> Tarsus/Stopalo)
        for i in range(6):
            side = -1 if (i % 2 == 0) else 1
            row = i // 2
            offset_fwd = (1 - row) * (s * 0.42)
            hip_x = self.x + math.cos(fwd) * offset_fwd + math.cos(perp) * (side * s * 0.32)
            hip_y = self.y + math.sin(fwd) * offset_fwd + math.sin(perp) * (side * s * 0.32)
            foot_x, foot_y = self.legs[i][0], self.legs[i][1]

            l1 = s * 0.92
            l2 = s * 1.10
            flip_dir = -side if row == 0 else side
            jx, jy = solve_ik(hip_x, hip_y, foot_x, foot_y, l1, l2, flip_dir)

            # Podizanje koljena u zrak za 3D dojam članka
            knee_x = jx
            knee_y = jy - 2.5

            # Tarsus (završni članak stopala)
            ankle_x = lerp(knee_x, foot_x, 0.78)
            ankle_y = lerp(knee_y, foot_y, 0.78)

            # Sjena noge na tlu
            pygame.draw.line(surf, C_GROUND_SHADOW, (hip_x + 1, hip_y + 2), (jx + 1, jy + 2), 2)
            pygame.draw.line(surf, C_GROUND_SHADOW, (jx + 1, jy + 2), (foot_x + 1, foot_y + 2), 1)

            # Femur (bedro - deblji segment)
            pygame.draw.line(surf, self.color_legs, (hip_x, hip_y), (knee_x, knee_y), 3)
            # Tibia (potkoljenica)
            pygame.draw.line(surf, self.color_thorax, (knee_x, knee_y), (ankle_x, ankle_y), 2)
            # Tarsus (tanko stopalo s pandžicama)
            pygame.draw.line(surf, self.color_accent, (ankle_x, ankle_y), (foot_x, foot_y), 1)
            pygame.draw.circle(surf, self.color_head, (int(knee_x), int(knee_y)), 2)

        # 2. ČVORASTI STRUK (PETIOLE & POSTPETIOLE - tipičan mravlji uski struk)
        pet1_x = self.x - math.cos(fwd) * (s * 0.75)
        pet1_y = self.y - math.sin(fwd) * (s * 0.75)
        pet2_x = self.x - math.cos(fwd) * (s * 1.02)
        pet2_y = self.y - math.sin(fwd) * (s * 1.02)
        pygame.draw.circle(surf, self.color_head, (int(pet1_x), int(pet1_y)), max(2, int(s * 0.24)))
        pygame.draw.circle(surf, self.color_thorax, (int(pet2_x), int(pet2_y)), max(2, int(s * 0.20)))

        # 3. ZADAK (GASTER) - Kapljičasti rotirani oblik sa segmentnim prugama i 3D sjajem
        g_ang = self.gaster_angle
        g_perp = g_ang + math.pi / 2
        gast_cx = pet2_x - math.cos(g_ang) * (s * 0.92)
        gast_cy = pet2_y - math.sin(g_ang) * (s * 0.92)

        g_rx = s * 1.05
        g_ry = s * 0.74
        draw_rotated_ellipse(surf, self.color_gaster, gast_cx, gast_cy, g_rx, g_ry, g_ang, segments=14)
        # Šiljati stražnji vrh zatka (kako bi bio kapljičast)
        tip_gx = gast_cx - math.cos(g_ang) * (g_rx * 1.18)
        tip_gy = gast_cy - math.sin(g_ang) * (g_rx * 1.18)
        p_left = (gast_cx - math.cos(g_ang) * (g_rx * 0.4) + math.cos(g_perp) * (g_ry * 0.82),
                  gast_cy - math.sin(g_ang) * (g_rx * 0.4) + math.sin(g_perp) * (g_ry * 0.82))
        p_right = (gast_cx - math.cos(g_ang) * (g_rx * 0.4) - math.cos(g_perp) * (g_ry * 0.82),
                   gast_cy - math.sin(g_ang) * (g_rx * 0.4) - math.sin(g_perp) * (g_ry * 0.82))
        pygame.draw.polygon(surf, self.color_gaster, [p_left, p_right, (tip_gx, tip_gy)])

        # Hitinske pruge (tergiti) preko zatka
        for b_off in [-0.35, 0.05, 0.42]:
            bx = gast_cx + math.cos(g_ang) * (g_rx * b_off)
            by = gast_cy + math.sin(g_ang) * (g_rx * b_off)
            bw = g_ry * (0.92 - abs(b_off) * 0.45)
            pygame.draw.line(
                surf, self.color_head,
                (bx + math.cos(g_perp) * bw, by + math.sin(g_perp) * bw),
                (bx - math.cos(g_perp) * bw, by - math.sin(g_perp) * bw), 1
            )

        # 3D odsjaj na gornjoj strani zatka
        spec_gx = gast_cx + math.cos(g_ang) * (s * 0.18) - math.cos(g_perp) * (s * 0.22)
        spec_gy = gast_cy + math.sin(g_ang) * (s * 0.18) - math.sin(g_perp) * (s * 0.22)
        draw_rotated_ellipse(surf, self.color_accent, spec_gx, spec_gy, s * 0.42, s * 0.18, g_ang, segments=8)

        # 4. PRSIŠTE (MESOSOMA / THORAX) - Izduženi dvodijelni segmentirani oklop
        pronotum_x = self.x + math.cos(fwd) * (s * 0.25)
        pronotum_y = self.y + math.sin(fwd) * (s * 0.25)
        mesonotum_x = self.x - math.cos(fwd) * (s * 0.30)
        mesonotum_y = self.y - math.sin(fwd) * (s * 0.30)

        draw_rotated_ellipse(surf, self.color_thorax, mesonotum_x, mesonotum_y, s * 0.55, s * 0.34, fwd, segments=10)
        draw_rotated_ellipse(surf, self.color_thorax, pronotum_x, pronotum_y, s * 0.52, s * 0.42, fwd, segments=10)
        draw_rotated_ellipse(surf, self.color_accent, pronotum_x, pronotum_y, s * 0.25, s * 0.14, fwd, segments=8)

        # 5. GLAVA (HEAD) S FASETIRANIM OČIMA, MANDIBULAMA I PRELOMLJENIM TICALIMA
        head_x = self.x + math.cos(fwd) * (s * 0.98)
        head_y = self.y + math.sin(fwd) * (s * 0.98)

        # Vojnici imaju veću, širu glavu
        h_rx = s * (0.64 if self.role == "SOLDIER" else 0.54)
        h_ry = s * (0.58 if self.role == "SOLDIER" else 0.46)
        draw_rotated_ellipse(surf, self.color_head, head_x, head_y, h_rx, h_ry, fwd, segments=12)
        draw_rotated_ellipse(surf, self.color_thorax, head_x - math.cos(fwd) * 1.5, head_y - math.sin(fwd) * 1.5, h_rx * 0.5, h_ry * 0.4, fwd, segments=8)

        # Nošeni teret u čeljustima (list, kristal šećera, zrno pijeska ili jaje)
        mouth_x = head_x + math.cos(fwd) * (h_rx * 0.95)
        mouth_y = head_y + math.sin(fwd) * (h_rx * 0.95)
        if self.carried_item:
            item_x = mouth_x + math.cos(fwd) * (s * 0.42)
            item_y = mouth_y + math.sin(fwd) * (s * 0.42)
            if self.carried_item == "leaf":
                draw_rotated_ellipse(surf, (45, 200, 45), item_x, item_y, s * 0.55, s * 0.35, fwd + 0.5, segments=8)
                pygame.draw.line(surf, (150, 255, 110), (mouth_x, mouth_y), (item_x, item_y), 1)
            elif self.carried_item == "sugar":
                pygame.draw.circle(surf, (220, 245, 255), (int(item_x), int(item_y)), 4)
                pygame.draw.circle(surf, (255, 255, 255), (int(item_x - 1), int(item_y - 1)), 2)
            elif self.carried_item == "egg":
                draw_rotated_ellipse(surf, (245, 245, 230), item_x, item_y, s * 0.45, s * 0.28, fwd + 1.2, segments=8)
            else:
                pygame.draw.circle(surf, self.carried_col, (int(item_x), int(item_y)), 4)
                pygame.draw.circle(surf, (255, 235, 180), (int(item_x - 1), int(item_y - 1)), 1)

        # Srpaste čeljusti (mandibule) i prelomljena lakatna ticala (antennae)
        for side in [-1, 1]:
            # Mandibule
            m_base_x = mouth_x + math.cos(perp) * (side * h_ry * 0.52)
            m_base_y = mouth_y + math.sin(perp) * (side * h_ry * 0.52)
            m_mid_ang = fwd + side * (0.25 + self.mandible_open * 0.55)
            m_mid_x = m_base_x + math.cos(m_mid_ang) * (s * 0.42)
            m_mid_y = m_base_y + math.sin(m_mid_ang) * (s * 0.42)
            m_tip_ang = fwd - side * (0.35 - self.mandible_open * 0.45)
            m_tip_x = m_mid_x + math.cos(m_tip_ang) * (s * 0.32)
            m_tip_y = m_mid_y + math.sin(m_tip_ang) * (s * 0.32)
            pygame.draw.lines(surf, self.color_accent, False, [(m_base_x, m_base_y), (m_mid_x, m_mid_y), (m_tip_x, m_tip_y)], 2)

            # Fasetirane crne oči sa sjajem
            eye_x = head_x + math.cos(fwd) * (h_rx * 0.15) + math.cos(perp) * (side * h_ry * 0.78)
            eye_y = head_y + math.sin(fwd) * (h_rx * 0.15) + math.sin(perp) * (side * h_ry * 0.78)
            pygame.draw.circle(surf, (10, 8, 12), (int(eye_x), int(eye_y)), 2)
            pygame.draw.circle(surf, (220, 220, 240), (int(eye_x), int(eye_y)), 1)

            # Lakatna ticala (Scape + Funiculus)
            twitch = math.sin(self.antenna_phase + side * 1.4) * (0.28 if self.comm_timer > 0 else 0.12)
            a_elbow_ang = fwd + side * (0.62 + twitch)
            a_elbow_x = mouth_x + math.cos(a_elbow_ang) * (s * 0.65)
            a_elbow_y = mouth_y + math.sin(a_elbow_ang) * (s * 0.65)
            a_tip_ang = fwd + side * (0.22 - twitch * 1.3)
            a_tip_x = a_elbow_x + math.cos(a_tip_ang) * (s * 0.75)
            a_tip_y = a_elbow_y + math.sin(a_tip_ang) * (s * 0.75)
            pygame.draw.line(surf, self.color_legs, (mouth_x, mouth_y), (a_elbow_x, a_elbow_y), 2)
            pygame.draw.line(surf, self.color_accent, (a_elbow_x, a_elbow_y), (a_tip_x, a_tip_y), 1)

# ==================== SEGMENTI I UDOVI TITANA (IGRAČ) ====================
class Segment:
    def __init__(self, x, y, length, radius, angle=0.0):
        self.x = clamp_x(x)
        self.y = clamp_y(y)
        self.length = length
        self.radius = radius
        self.angle = angle

    def follow(self, tx, ty):
        dx = tx - self.x
        dy = ty - self.y
        self.angle = math.atan2(dy, dx)
        self.x = tx - math.cos(self.angle) * self.length
        self.y = ty - math.sin(self.angle) * self.length
        self.x = clamp_x(self.x, self.radius * 0.4)
        self.y = clamp_y(self.y, self.radius * 0.4)

class Limb:
    def __init__(self, creature, seg_idx, side, l1, l2, reach, is_heavy=False, is_overdrive_leg=False):
        self.creature = creature
        self.seg_idx = seg_idx
        self.side = side
        self.l1 = l1
        self.l2 = l2
        self.reach = reach
        self.is_heavy = is_heavy
        self.is_overdrive_leg = is_overdrive_leg

        self.foot_x = 0.0
        self.foot_y = 0.0
        self.target_x = 0.0
        self.target_y = 0.0
        self.step_start_x = 0.0
        self.step_start_y = 0.0
        self.step_progress = 1.0

        self.blood_stain_timer = 0
        self.blood_stain_color = (255, 0, 0)

        hx, hy, ang = self.get_hip()
        init_ang = ang + ((math.pi / 3.0) if is_heavy else (math.pi / 2.2)) * side
        self.foot_x = clamp_x(hx + math.cos(init_ang) * reach)
        self.foot_y = clamp_y(hy + math.sin(init_ang) * reach)

    def get_hip(self):
        seg = self.creature.segments[min(self.seg_idx, len(self.creature.segments) - 1)]
        perp = seg.angle + (math.pi / 2) * self.side
        hip_dist = seg.radius * (1.28 if self.is_heavy else 1.05)
        hx = clamp_x(seg.x + math.cos(perp) * hip_dist)
        hy = clamp_y(seg.y + math.sin(perp) * hip_dist)
        return hx, hy, seg.angle

    def update(self):
        if self.is_overdrive_leg and not self.creature.is_overdrive:
            return

        if self.blood_stain_timer > 0:
            self.blood_stain_timer -= 1

        hx, hy, ang = self.get_hip()

        if self.creature.is_burrowed and not self.is_heavy:
            return

        if not self.is_heavy and self.creature.idle_stretch_timer > 0:
            stretch_t = math.sin((self.creature.idle_stretch_timer / 60.0) * math.pi)
            stretch_ang = ang + (math.pi / 2.0 + stretch_t * 0.4) * self.side
            self.foot_x = clamp_x(hx + math.cos(stretch_ang) * (self.reach * (1.0 + stretch_t * 0.3)))
            self.foot_y = clamp_y(hy + math.sin(stretch_ang) * (self.reach * (1.0 + stretch_t * 0.3)))
            return

        if self.is_heavy and self.creature.is_burrowed:
            t = pygame.time.get_ticks() * 0.003
            spread_ang = ang + (0.55 + math.sin(t + self.side) * 0.14) * self.side
            reach_pulse = self.reach * (0.65 + math.cos(t * 1.5) * 0.08)
            self.foot_x = clamp_x(hx + math.cos(spread_ang) * reach_pulse)
            self.foot_y = clamp_y(hy + math.sin(spread_ang) * reach_pulse)
            return

        if self.is_heavy and self.creature.slam_timer > 0:
            slam_t = (25 - self.creature.slam_timer) / 25.0
            slam_reach = self.reach * (0.8 + math.sin(slam_t * math.pi) * 0.4)
            slam_ang = ang + (0.35 * self.side)
            self.foot_x = clamp_x(hx + math.cos(slam_ang) * slam_reach)
            self.foot_y = clamp_y(hy + math.sin(slam_ang) * slam_reach)
            return

        if (self.is_heavy or self.is_overdrive_leg) and self.creature.is_feasting:
            prey = self.creature.feast_target
            tear_rip = math.sin(pygame.time.get_ticks() * 0.035 + self.side * math.pi) * 16
            self.foot_x = clamp_x(prey[0] + self.side * 18 + tear_rip)
            self.foot_y = clamp_y(prey[1] + math.cos(pygame.time.get_ticks() * 0.025) * 8)
            return

        wall_thresh = 95
        if hx < MIN_X + wall_thresh and self.side == -1:
            self.foot_x = MIN_X + 2
            self.foot_y = clamp_y(hy + math.sin(pygame.time.get_ticks() * 0.003) * 15)
            return
        elif hx > MAX_X - wall_thresh and self.side == 1:
            self.foot_x = MAX_X - 2
            self.foot_y = clamp_y(hy + math.sin(pygame.time.get_ticks() * 0.003) * 15)
            return

        if self.is_heavy and self.creature.is_idle:
            t = pygame.time.get_ticks() * 0.003
            spread_ang = ang + (math.pi / 2.6 + math.sin(t + self.side) * 0.28) * self.side
            reach_pulse = self.reach * (1.1 + math.cos(t * 1.5) * 0.15)
            self.foot_x = clamp_x(hx + math.cos(spread_ang) * reach_pulse)
            self.foot_y = clamp_y(hy + math.sin(spread_ang) * reach_pulse)
            return

        rest_ang = ang + ((math.pi / 3.2) if self.is_heavy else ((math.pi / 2.8) if self.is_overdrive_leg else (math.pi / 2.25))) * self.side
        ideal_x = clamp_x(hx + math.cos(rest_ang) * self.reach)
        ideal_y = clamp_y(hy + math.sin(rest_ang) * self.reach)

        dist = math.hypot(self.foot_x - ideal_x, self.foot_y - ideal_y)
        threshold = self.reach * (0.75 if self.is_heavy else 0.85)

        if dist > threshold and self.step_progress >= 1.0:
            self.step_start_x = self.foot_x
            self.step_start_y = self.foot_y
            stride = 28 if self.is_heavy else 20
            self.target_x = clamp_x(ideal_x + math.cos(ang) * stride)
            self.target_y = clamp_y(ideal_y + math.sin(ang) * stride)
            self.step_progress = 0.0

        if self.step_progress < 1.0:
            speed = 0.30 if (self.creature.is_overdrive or self.is_heavy) else 0.24
            self.step_progress += speed
            t = min(1.0, self.step_progress)
            self.foot_x = clamp_x(self.step_start_x + (self.target_x - self.step_start_x) * t)
            self.foot_y = clamp_y(self.step_start_y + (self.target_y - self.step_start_y) * t)

            if self.step_progress >= 1.0 and not self.creature.is_burrowed:
                if self.creature.is_magma:
                    molten_footprints.append(MoltenFootprint(self.foot_x, self.foot_y, 7 if self.is_heavy else 4))
                else:
                    for drop in blood_drops:
                        if math.hypot(self.foot_x - drop.x, self.foot_y - drop.y) < 18:
                            self.blood_stain_timer = 120
                            self.blood_stain_color = drop.color
                            break

                    if self.blood_stain_timer > 0 and len(stained_footprints) < 90:
                        rad = 6 if self.is_heavy else 3
                        stained_footprints.append(StainedFootprint(self.foot_x, self.foot_y, rad, self.blood_stain_color))

                if self.is_heavy:
                    play_snd(snd_step)
                    haptic(14, 70)

    def draw(self, surf, pal):
        if self.is_overdrive_leg and not self.creature.is_overdrive:
            return
        if self.creature.is_burrowed and not self.is_heavy:
            return

        hx, hy, _ = self.get_hip()
        jx, jy = solve_ik(hx, hy, self.foot_x, self.foot_y, self.l1, self.l2, self.side)
        evo = self.creature.evo_level
        is_magma = self.creature.is_magma

        pygame.draw.ellipse(surf, C_GROUND_SHADOW, (int(self.foot_x - 11), int(self.foot_y - 5), 22, 10))
        joint_color = pal['core'] if is_magma else pal['neon']

        if self.is_heavy:
            v1_dx = jx - hx; v1_dy = jy - hy
            v1_len = max(1e-4, math.hypot(v1_dx, v1_dy))
            n1_x = -v1_dy / v1_len * (10.0 + min(9, evo * 0.10))
            n1_y = v1_dx / v1_len * (10.0 + min(9, evo * 0.10))

            p_femur = [
                (hx - n1_x * 0.7, hy - n1_y * 0.7),
                (hx + n1_x * 1.4, hy + n1_y * 1.4),
                (jx + n1_x * 1.0, jy + n1_y * 1.0),
                (jx - n1_x * 0.5, jy - n1_y * 0.5)
            ]
            pygame.draw.polygon(surf, pal['dark'], p_femur)
            pygame.draw.polygon(surf, pal['plate'], p_femur, 2)
            pygame.draw.lines(surf, pal['edge'], True, p_femur, 1)

            v2_dx = self.foot_x - jx; v2_dy = self.foot_y - jy
            v2_len = max(1e-4, math.hypot(v2_dx, v2_dy))
            n2_x = -v2_dy / v2_len * (9.0 + min(8, evo * 0.09))
            n2_y = v2_dx / v2_len * (9.0 + min(8, evo * 0.09))

            p_shin = [
                (jx - n2_x * self.side * 0.5, jy - n2_y * self.side * 0.5),
                (jx + n2_x * self.side * 1.5, jy + n2_y * self.side * 1.5),
                (self.foot_x + n2_x * self.side * 1.1, self.foot_y + n2_y * self.side * 1.1),
                (self.foot_x, self.foot_y)
            ]
            pygame.draw.polygon(surf, pal['dark'], p_shin)
            pygame.draw.lines(surf, pal['edge'], True, p_shin, 1)

            pygame.draw.circle(surf, pal['plate'], (int(jx), int(jy)), 10 + min(5, evo // 16))
            pygame.draw.circle(surf, joint_color, (int(jx), int(jy)), 5)

            c_ang = math.atan2(self.foot_y - jy, self.foot_x - jx)
            tip_len = 28 + min(20, evo * 0.22)

            pinch_anim = math.sin(pygame.time.get_ticks() * 0.015) * 0.14
            out_ang = c_ang + (0.28 + pinch_anim) * self.side
            tip1_x = clamp_x(self.foot_x + math.cos(out_ang) * tip_len)
            tip1_y = clamp_y(self.foot_y + math.sin(out_ang) * tip_len)

            in_ang = c_ang - (0.36 - pinch_anim) * self.side
            tip2_x = clamp_x(self.foot_x + math.cos(in_ang) * (tip_len * 0.75))
            tip2_y = clamp_y(self.foot_y + math.sin(in_ang) * (tip_len * 0.75))

            claw_poly = [
                (self.foot_x - n2_x * self.side * 0.6, self.foot_y - n2_y * self.side * 0.6),
                (tip1_x, tip1_y),
                (self.foot_x + math.cos(c_ang) * 8, self.foot_y + math.sin(c_ang) * 8),
                (tip2_x, tip2_y)
            ]
            pygame.draw.polygon(surf, pal['dark'], claw_poly)
            pygame.draw.lines(surf, pal['edge'], True, claw_poly, 2)

            for t_step in range(1, 4):
                t_ratio = t_step / 4.0
                tx1 = lerp(self.foot_x, tip1_x, t_ratio)
                ty1 = lerp(self.foot_y, tip1_y, t_ratio)
                tx2 = tx1 - math.sin(out_ang) * (3.5 * self.side)
                ty2 = ty1 + math.cos(out_ang) * (3.5 * self.side)
                tooth_col = (255, 230, 80) if is_magma else pal['spec']
                pygame.draw.line(surf, tooth_col, (tx1, ty1), (tx2, ty2), 2)

            pygame.draw.circle(surf, pal['edge'], (int(tip1_x), int(tip1_y)), 3)
            pygame.draw.circle(surf, pal['edge'], (int(tip2_x), int(tip2_y)), 2)
        else:
            v1_dx = jx - hx; v1_dy = jy - hy
            v1_len = max(1e-4, math.hypot(v1_dx, v1_dy))
            norm1_x = -v1_dy / v1_len * 3.2
            norm1_y = v1_dx / v1_len * 3.2

            femur_poly = [
                (hx - norm1_x, hy - norm1_y),
                (hx + norm1_x, hy + norm1_y),
                (jx + norm1_x * 0.7, jy + norm1_y * 0.7),
                (jx - norm1_x * 0.7, jy - norm1_y * 0.7)
            ]
            pygame.draw.polygon(surf, pal['dark'], femur_poly)
            pygame.draw.lines(surf, pal['edge'], True, femur_poly, 1)

            v2_dx = self.foot_x - jx; v2_dy = self.foot_y - jy
            v2_len = max(1e-4, math.hypot(v2_dx, v2_dy))
            norm2_x = -v2_dy / v2_len * 2.5
            norm2_y = v2_dx / v2_len * 2.5

            tibia_poly = [
                (jx - norm2_x, jy - norm2_y),
                (jx + norm2_x, jy + norm2_y),
                (self.foot_x + norm2_x * 0.4, self.foot_y + norm2_y * 0.4),
                (self.foot_x - norm2_x * 0.4, self.foot_y - norm2_y * 0.4)
            ]
            pygame.draw.polygon(surf, pal['plate'], tibia_poly)
            pygame.draw.lines(surf, pal['edge'], True, tibia_poly, 1)

            knee_spike_x = jx + norm1_x * self.side * 2.2
            knee_spike_y = jy + norm1_y * self.side * 2.2
            pygame.draw.line(surf, pal['edge'], (jx, jy), (knee_spike_x, knee_spike_y), 2)
            pygame.draw.circle(surf, joint_color, (int(jx), int(jy)), 3)

            tarsus_ang = math.atan2(v2_dy, v2_dx)
            claw_tip_x = self.foot_x + math.cos(tarsus_ang) * 5
            claw_tip_y = self.foot_y + math.sin(tarsus_ang) * 5
            pygame.draw.line(surf, (255, 255, 255), (self.foot_x, self.foot_y), (claw_tip_x, claw_tip_y), 2)

# ==================== TITANSKI SKORPION (IGRAČ) ====================
class Scorpion:
    def __init__(self, x, y):
        self.evo_level = 1
        self.xp = 0        # 100 XP za Level Up (Obični mrav = 10 XP, Zlatna Kraljica = 50 XP -> 50% smanjen XP)
        self.max_xp = 100
        self.bugs_eaten = 0
        self.pulse_phase = 0.0

        self.max_hp = 100.0
        self.hp = 100.0
        self.invulnerable_timer = 0

        self.max_hunger = 1800.0
        self.hunger = 1800.0
        self.auto_hunting = False
        self.ambush_timer = 0

        self.heat = 0.0
        self.max_heat = 100.0
        self.is_magma = False
        self.magma_timer = 0.0

        self.dna_fail_timer = 0

        self.is_idle = False
        self.idle_stand_ticks = 0
        self.idle_stretch_timer = 0
        self.tail_whip_timer = 0

        self.is_burrowed = False
        self.is_overdrive = False

        self.is_feasting = False
        self.feast_timer = 0
        self.feast_target = (0, 0)
        self.feast_bug_color = (255, 255, 255)
        self.feasting_gold = False
        self.feasting_boss = None

        self.is_stinging = False
        self.sting_progress = 0.0
        self.sting_target = (0, 0)
        self.ambush_target = None
        self.ambush_cooldown = 0

        self.slam_timer = 0
        self.breath_clock = 0.0

        self.vx = 0.0
        self.vy = 0.0

        self.segments = []
        self.limbs = []
        self.rebuild_skeleton(x, y)

    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.max_xp and self.evo_level < 100:
            self.xp -= self.max_xp
            self.evolve_now()
        if self.evo_level >= 100:
            self.xp = self.max_xp

    def rebuild_skeleton(self, x, y):
        new_num_segments = 30 + min(7, int(self.evo_level * 0.07))
        self.seg_len = 10 + min(4, self.evo_level * 0.04)
        
        old_segs = getattr(self, 'segments', [])
        new_segments = []

        base_r = 16 + min(14, self.evo_level * 0.15)

        tail_root_idx = 15
        total_tail_segs = max(1, new_num_segments - tail_root_idx)

        for i in range(new_num_segments):
            if i < tail_root_idx:
                r = math.sin((i / float(tail_root_idx)) * math.pi) * base_r + 8
            else:
                progress = (i - tail_root_idx) / float(total_tail_segs - 1) if total_tail_segs > 1 else 1.0
                r = (base_r * 0.65) * (1.0 - progress * 0.65) + 3.2

            if i < len(old_segs):
                seg = Segment(old_segs[i].x, old_segs[i].y, self.seg_len, r, old_segs[i].angle)
            elif len(new_segments) > 0:
                prev = new_segments[-1]
                nx = prev.x - math.cos(prev.angle) * self.seg_len
                ny = prev.y - math.sin(prev.angle) * self.seg_len
                seg = Segment(nx, ny, self.seg_len, r, prev.angle)
            else:
                seg = Segment(x, y, self.seg_len, r, 0.0)

            new_segments.append(seg)

        self.num_segments = new_num_segments
        self.segments = new_segments

        f_l1 = 52 + min(22, self.evo_level * 0.22)
        f_l2 = 56 + min(24, self.evo_level * 0.24)
        f_reach = 84 + min(32, self.evo_level * 0.32)

        self.limbs = [
            Limb(self, 1, -1, f_l1, f_l2, f_reach, is_heavy=True),
            Limb(self, 1, 1, f_l1, f_l2, f_reach, is_heavy=True)
        ]

        od_front_l1 = 40 + min(12, self.evo_level * 0.13)
        od_front_l2 = 44 + min(13, self.evo_level * 0.14)
        od_front_reach = 70 + min(18, self.evo_level * 0.19)
        self.limbs.append(Limb(self, 2, -1, od_front_l1, od_front_l2, od_front_reach, is_heavy=False, is_overdrive_leg=True))
        self.limbs.append(Limb(self, 2, 1, od_front_l1, od_front_l2, od_front_reach, is_heavy=False, is_overdrive_leg=True))

        od_l1 = 36 + min(11, self.evo_level * 0.12)
        od_l2 = 40 + min(12, self.evo_level * 0.14)
        od_reach = 62 + min(16, self.evo_level * 0.17)
        self.limbs.append(Limb(self, 4, -1, od_l1, od_l2, od_reach, is_heavy=False, is_overdrive_leg=True))
        self.limbs.append(Limb(self, 4, 1, od_l1, od_l2, od_reach, is_heavy=False, is_overdrive_leg=True))

        b_l1 = 32 + min(11, self.evo_level * 0.12)
        b_l2 = 36 + min(12, self.evo_level * 0.14)
        b_reach = 56 + min(16, self.evo_level * 0.17)

        for s_idx in [6, 9, 12, 14]:
            self.limbs.append(Limb(self, s_idx, -1, b_l1, b_l2, b_reach, is_heavy=False))
            self.limbs.append(Limb(self, s_idx, 1, b_l1, b_l2, b_reach, is_heavy=False))

    def add_heat(self, amount):
        if not self.is_magma:
            self.heat = min(self.max_heat, self.heat + amount)
            if self.heat >= self.max_heat:
                self.trigger_magma_overload()

    def trigger_magma_overload(self):
        self.is_magma = True
        self.magma_timer = 600
        self.heat = self.max_heat
        play_snd(snd_charge)
        add_shake(25)
        haptic(450, 255)
        head = self.segments[0]
        shockwaves.append([head.x, head.y, 0, 320, (255, 120, 20)])
        emit_magma_embers(head.x, head.y, count=35)

    def trigger_slam(self, bugs_list):
        global dna_collected

        if dna_collected < 15:
            self.dna_fail_timer = 30
            play_snd(snd_catch)
            haptic(40, 90)
            return

        dna_collected -= 15
        self.slam_timer = 25
        play_snd(snd_slam)
        haptic(220)
        add_shake(24 if self.is_magma else 20)
        head = self.segments[0]

        impact_reach = 60
        impact_x = clamp_x(head.x + math.cos(head.angle) * impact_reach)
        impact_y = clamp_y(head.y + math.sin(head.angle) * impact_reach)

        if len(ground_cracks) < 8:
            ground_cracks.append(GroundCrackEffect(impact_x, impact_y, max_radius=155, is_magma=self.is_magma))

        self.add_heat(15)

        slam_pull_radius = 260 if self.is_magma else 240
        for b in bugs_list:
            dist = math.hypot(b.x - impact_x, b.y - impact_y)
            if dist < slam_pull_radius:
                b.paralyzed_timer = 200
                pull_ang = math.atan2(impact_y - b.y, impact_x - b.x)
                pull_strength = (1.0 - dist / slam_pull_radius) * 16.0
                b.vx += math.cos(pull_ang) * pull_strength
                b.vy += math.sin(pull_ang) * pull_strength
                if self.is_magma and dist < 120:
                    emit_magma_embers(b.x, b.y, count=4)

        global active_boss
        if active_boss and active_boss.state == "active":
            d_boss = math.hypot(active_boss.x - impact_x, active_boss.y - impact_y)
            if d_boss < 240:
                active_boss.take_slam_hit()

    def trigger_feast(self, bug_x, bug_y, bug_color, is_gold=False):
        global dna_collected
        if self.is_feasting:
            return

        if self.is_burrowed:
            self.unburrow()

        self.is_feasting = True
        self.feasting_boss = None
        self.feast_timer = 35
        self.feast_target = (clamp_x(bug_x), clamp_y(bug_y))
        self.feast_bug_color = bug_color
        self.feasting_gold = is_gold

        self.add_heat(35 if is_gold else 8)
        dna_collected = min(100, dna_collected + (15 if is_gold else 4))

        play_snd(snd_catch)
        haptic(50, 180)
        spill_blood(bug_x, bug_y, bug_color, count=18, spread=5.5)

    def trigger_boss_feast(self, boss):
        global dna_collected
        if self.is_burrowed:
            self.unburrow()

        self.is_feasting = True
        self.feasting_boss = boss
        self.feast_timer = 150
        self.feast_target = (clamp_x(boss.x), clamp_y(boss.y))
        self.feast_bug_color = boss.spec["c_main"]
        self.feasting_gold = False

        self.add_heat(50)
        dna_collected = 100

        play_snd(snd_catch)
        add_shake(18)
        haptic(250)
        spill_blood(boss.x, boss.y, boss.spec["c_main"], count=28, spread=7.0)

    def trigger_sting(self, tx, ty):
        self.is_stinging = True
        self.sting_progress = 0.0
        self.sting_target = (clamp_x(tx), clamp_y(ty))

    def take_damage(self, amount):
        if self.invulnerable_timer <= 0:
            self.hp = max(0.0, self.hp - amount)
            self.invulnerable_timer = 40
            self.add_heat(10)
            add_shake(14)
            haptic(160, 240)
            play_snd(snd_hurt)
            head = self.segments[0]
            spill_blood(head.x, head.y, (255, 30, 40), count=12)

            if self.hp <= 0.0:
                self.respawn_after_death()

    def respawn_after_death(self):
        head = self.segments[0]
        self.hp = self.max_hp * 0.5
        self.hunger = self.max_hunger * 0.5
        self.heat = 0.0
        self.xp = 0
        self.is_magma = False
        self.invulnerable_timer = 180
        self.evo_level = max(1, self.evo_level - 3)
        self.bugs_eaten = max(0, self.bugs_eaten - 2)
        self.is_feasting = False
        self.feasting_boss = None
        self.is_stinging = False
        self.is_burrowed = False
        self.rebuild_skeleton(head.x, head.y)
        emit_particles(head.x, head.y, (255, 30, 40), count=40, speed_mult=2.0)
        shockwaves.append([head.x, head.y, 0, 260, (255, 30, 60)])
        add_shake(28)
        haptic(500, 255)
        play_snd(snd_hurt)

    def unburrow(self):
        if self.is_burrowed:
            self.is_burrowed = False
            head = self.segments[0]
            play_snd(snd_burrow)
            emit_particles(head.x, head.y, (120, 100, 80), count=25, speed_mult=1.5)
            add_shake(12)
            haptic(100, 200)

    def evolve_now(self):
        if self.evo_level < 100:
            self.evo_level += 1
            head = self.segments[0]
            self.rebuild_skeleton(head.x, head.y)

            global flash_alpha, flash_color
            flash_alpha = 200
            flash_color = (255, 215, 0) if self.feasting_gold else (255, 255, 255)
            shockwaves.append([head.x, head.y, 0, 190 + min(300, self.evo_level * 5), (255, 215, 0) if self.feasting_gold else (255, 35, 75)])
            add_shake(26)
            play_snd(snd_evolve)
            haptic(350, 255)

    def update(self, tx, ty, user_touching, bugs_list, dt60=1.0):
        global active_boss

        self.pulse_phase = (self.pulse_phase + 0.40) % (self.num_segments + 6)
        head = self.segments[0]
        tip = self.segments[-1]

        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1
        if self.dna_fail_timer > 0:
            self.dna_fail_timer -= 1

        hunger_pct = self.hunger / self.max_hunger
        if hunger_pct > 0.60 and self.hp < self.max_hp:
            self.hp = min(self.max_hp, self.hp + (5.0 / 60.0) * dt60)

        if self.is_magma:
            self.magma_timer -= dt60
            self.heat = max(0.0, (self.magma_timer / 600.0) * self.max_heat)
            if self.magma_timer <= 0:
                self.is_magma = False
                self.heat = 0.0

            if random.random() < 0.35:
                rand_s = random.choice(self.segments[:16])
                emit_magma_embers(rand_s.x, rand_s.y, count=2)

            for b in bugs_list:
                if math.hypot(b.x - head.x, b.y - head.y) < 65:
                    if random.random() < 0.2:
                        emit_magma_embers(b.x, b.y, count=2)
                        b.paralyzed_timer = max(b.paralyzed_timer, 60)
        else:
            self.heat = max(0.0, self.heat - 0.05 * dt60)

        self.breath_clock += 0.025
        if int(self.breath_clock) % 240 == 0 and not self.is_feasting:
            play_snd(snd_breath)

        tx = clamp_x(tx, 35)
        ty = clamp_y(ty, 35)

        self.hunger = max(0.0, self.hunger - 1.0 * dt60)
        self.is_overdrive = hunger_pct < 0.50

        if hunger_pct <= 0.05:
            self.auto_hunting = True
        elif hunger_pct >= 0.40:
            self.auto_hunting = False

        if user_touching:
            self.ambush_timer = 0
        elif self.ambush_timer > 0:
            self.ambush_timer -= 1

        dist_to_target = math.hypot(tx - head.x, ty - head.y)
        self.is_idle = ((dist_to_target < 25 or (self.ambush_timer > 0 and not user_touching))
                        and not self.is_feasting and not self.auto_hunting)

        if self.is_idle:
            self.idle_stand_ticks += 1
            if self.idle_stand_ticks > 180:
                if random.randint(1, 200) == 1 and self.idle_stretch_timer <= 0:
                    self.idle_stretch_timer = 60
                    self.tail_whip_timer = 45
        else:
            self.idle_stand_ticks = 0

        if self.idle_stretch_timer > 0:
            self.idle_stretch_timer -= 1
        if self.tail_whip_timer > 0:
            self.tail_whip_timer -= 1

        if self.slam_timer > 0:
            self.slam_timer -= 1
        if self.is_idle and not user_touching and hunger_pct > 0.45:
            if not self.is_burrowed and random.random() < 0.012:
                self.is_burrowed = True
                play_snd(snd_burrow)
                emit_particles(head.x, head.y, (100, 85, 70), count=18)
                haptic(60, 120)
        elif user_touching or hunger_pct <= 0.45 or self.auto_hunting:
            if self.is_burrowed and not self.is_stinging:
                self.unburrow()

        if self.is_burrowed and not self.is_stinging and not self.is_feasting:
            self.ambush_cooldown += 1
            if self.ambush_cooldown >= 20:
                self.ambush_cooldown = 0
                tail_reach = 220.0
                candidates = [b for b in bugs_list if math.hypot(b.x - tip.x, b.y - tip.y) < tail_reach]
                if active_boss and active_boss.state == "active" and math.hypot(active_boss.x - tip.x, active_boss.y - tip.y) < tail_reach:
                    candidates.append(active_boss)

                if candidates and random.random() < 0.06:
                    target = random.choice(candidates)
                    self.trigger_sting(target.x, target.y)
                    self.ambush_target = target

        if self.is_feasting:
            self.feast_timer -= 1
            head.x += (self.feast_target[0] - head.x) * 0.25 + random.uniform(-2, 2)
            head.y += (self.feast_target[1] - head.y) * 0.25 + random.uniform(-2, 2)

            f_dx = self.feast_target[0] - head.x
            f_dy = self.feast_target[1] - head.y
            if math.hypot(f_dx, f_dy) > 1.0:
                target_ang = math.atan2(f_dy, f_dx)
                diff = (target_ang - head.angle + math.pi) % (2 * math.pi) - math.pi
                head.angle += diff * 0.35

            if self.feasting_boss:
                if self.feast_timer in [115, 70, 25]:
                    play_snd(snd_tear)
                    add_shake(15); haptic(180)
                    spill_blood(self.feast_target[0], self.feast_target[1], self.feasting_boss.spec["c_main"], count=16)

                if self.feast_timer <= 0:
                    self.is_feasting = False
                    self.feasting_boss = None
                    active_boss = None
                    self.hunger = self.max_hunger
                    # 50% smanjen XP i kod Bossa (250 XP = 2.5 levela umjesto prijašnjih 5)
                    self.gain_xp(250)
                    self.ambush_timer = 0 if user_touching else 180
            else:
                if self.feast_timer in [25, 12]:
                    play_snd(snd_tear); haptic(35, 140)
                    spill_blood(self.feast_target[0], self.feast_target[1], self.feast_bug_color, count=8)
                elif self.feast_timer in [20, 8]:
                    play_snd(snd_chew); haptic(25, 100)

                if self.feast_timer <= 0:
                    self.is_feasting = False
                    self.bugs_eaten += 1

                    # SMANJEN XP ZA 50%: Zlatna Kraljica daje 50 XP (pola levela), obični mrav 10 XP (10 mrava za level)
                    if self.feasting_gold:
                        self.hunger = self.max_hunger
                        self.gain_xp(50)
                    else:
                        self.hunger = min(self.max_hunger, self.hunger + (self.max_hunger / 3.0))
                        self.gain_xp(10)

                    self.ambush_timer = 0 if user_touching else 180
                    self.pulse_phase = 0.0
                    self.feasting_gold = False
        else:
            if not self.is_idle and not self.is_burrowed:
                move_dx = 0.0
                move_dy = 0.0

                if self.is_magma:
                    speed = 0.22 if (dist_to_target < 120 and not user_touching) else 0.13
                    move_dx = (tx - head.x) * speed
                    move_dy = (ty - head.y) * speed
                    head.x += move_dx
                    head.y += move_dy
                elif self.is_overdrive:
                    speed = 0.20 if (dist_to_target < 120 and not user_touching) else 0.12
                    move_dx = (tx - head.x) * speed + math.sin(pygame.time.get_ticks() * 0.06) * 1.5
                    move_dy = (ty - head.y) * speed
                    head.x += move_dx
                    head.y += move_dy
                else:
                    speed = 0.17 if (dist_to_target < 120 and not user_touching) else 0.09
                    move_dx = (tx - head.x) * speed
                    move_dy = (ty - head.y) * speed
                    head.x += move_dx
                    head.y += move_dy

                if math.hypot(move_dx, move_dy) > 0.4:
                    target_ang = math.atan2(move_dy, move_dx)
                    ang_diff = (target_ang - head.angle + math.pi) % (2 * math.pi) - math.pi
                    turn_speed = 0.28 if self.is_magma else (0.30 if self.is_overdrive else 0.20)
                    head.angle += ang_diff * turn_speed

        head.x = clamp_x(head.x, 25)
        head.y = clamp_y(head.y, 25)

        if self.is_stinging:
            if self.sting_progress == 0.0:
                play_snd(snd_sting)
            self.sting_progress += 0.07
            if 0.44 <= self.sting_progress <= 0.52:
                add_shake(10)
                haptic(160, 255)
                emit_particles(self.sting_target[0], self.sting_target[1], (255, 120, 20) if self.is_magma else (255, 20, 60), count=16)

                if self.ambush_target:
                    play_snd(snd_tear)
                    self.add_heat(20 if self.is_magma else 12)

                    if self.ambush_target == active_boss:
                        active_boss.take_stinger_hit(head.x, head.y)
                    elif hasattr(self.ambush_target, 'blood_col'):
                        spill_blood(self.ambush_target.x, self.ambush_target.y, self.ambush_target.blood_col, count=22)

                        if random.random() < 0.15 or self.ambush_target.is_gold:
                            dna_pickups.append(DNAPickup(self.ambush_target.x, self.ambush_target.y))

                        self.bugs_eaten += 1
                        if self.ambush_target.is_gold:
                            self.hunger = self.max_hunger
                            self.gain_xp(50)
                        else:
                            self.hunger = min(self.max_hunger, self.hunger + 350.0)
                            self.gain_xp(10)
                        self.ambush_target.respawn()

                    self.ambush_target = None

            if self.sting_progress >= 1.0:
                self.is_stinging = False
                self.sting_progress = 0.0

        tail_root_idx = 15
        for i in range(1, len(self.segments)):
            self.segments[i].follow(self.segments[i - 1].x, self.segments[i - 1].y)

        if self.tail_whip_timer > 0:
            whip_ang = math.sin((self.tail_whip_timer / 45.0) * math.pi * 3) * 18.0
            for k in range(tail_root_idx, len(self.segments)):
                self.segments[k].x += math.cos(self.segments[k].angle + math.pi / 2) * whip_ang

        if self.is_stinging:
            sp = self.sting_progress
            strike_weight = math.sin(sp * math.pi)
            total_tail_segs = len(self.segments) - tail_root_idx
            tx_st = self.sting_target[0]
            ty_st = self.sting_target[1]
            root_seg = self.segments[tail_root_idx]

            for idx in range(tail_root_idx, len(self.segments)):
                t_rel = (idx - tail_root_idx) / float(total_tail_segs)
                cur_seg = self.segments[idx]
                arc_h = math.sin(t_rel * math.pi) * 110 * strike_weight
                curve_x = (1 - t_rel) * root_seg.x + t_rel * tx_st
                curve_y = (1 - t_rel) * root_seg.y + t_rel * ty_st - arc_h
                cur_seg.x += (curve_x - cur_seg.x) * (0.65 * strike_weight)
                cur_seg.y += (curve_y - cur_seg.y) * (0.65 * strike_weight)

        for limb in self.limbs:
            limb.update()

    def draw(self, surf):
        head = self.segments[0]
        tip = self.segments[-1]
        tail_root_idx = 15

        pal = MAGMA_PAL if self.is_magma else (OD_PAL if self.is_overdrive else NORM_PAL)
        rim_tint = get_border_rim_tint(head.x, head.y)

        if not self.is_burrowed:
            for idx in range(1, tail_root_idx, 2):
                s = self.segments[idx]
                pygame.draw.ellipse(surf, C_GROUND_SHADOW, (int(s.x - s.radius * 1.1 + 3), int(s.y - s.radius * 0.6 + 5), int(s.radius * 2.2), int(s.radius * 1.2)))

            num_tail = len(self.segments) - tail_root_idx
            for t_idx in range(tail_root_idx, len(self.segments)):
                s = self.segments[t_idx]
                rel_t = (t_idx - tail_root_idx) / float(num_tail)
                height_arch = math.sin(rel_t * math.pi) * 22.0
                sh_x = s.x + 5 + height_arch * 0.45
                sh_y = s.y + 7 + height_arch * 0.65
                sh_r = max(2, int(s.radius * (1.1 - height_arch * 0.015)))
                pygame.draw.ellipse(surf, C_GROUND_SHADOW, (int(sh_x - sh_r), int(sh_y - sh_r * 0.5), sh_r * 2, int(sh_r * 1.1)))

        if self.is_burrowed:
            pygame.draw.ellipse(surf, (22, 16, 12), (head.x - 35, head.y - 25, 70, 50))
            pygame.draw.ellipse(surf, (36, 26, 18), (head.x - 25, head.y - 18, 50, 36), 2)

        for limb in self.limbs:
            limb.draw(surf, pal)

        perp = head.angle + math.pi / 2
        fwd_ang = head.angle
        jaw_len = 15 + min(8, self.evo_level * 0.09)
        jaw_pinch = math.sin(pygame.time.get_ticks() * 0.05 if self.is_feasting else self.breath_clock * 3) * 0.22

        for side in [-1, 1]:
            j_base_x = head.x + math.cos(fwd_ang) * (head.radius * 0.8) + math.cos(perp) * (side * 6)
            j_base_y = head.y + math.sin(fwd_ang) * (head.radius * 0.8) + math.sin(perp) * (side * 6)

            jaw_ang = fwd_ang + (0.35 + jaw_pinch) * side
            j_mid_x = j_base_x + math.cos(jaw_ang) * (jaw_len * 0.6)
            j_mid_y = j_base_y + math.sin(jaw_ang) * (jaw_len * 0.6)

            j_tip_ang = jaw_ang - (0.55 * side)
            j_tip_x = j_mid_x + math.cos(j_tip_ang) * (jaw_len * 0.55)
            j_tip_y = j_mid_y + math.sin(j_tip_ang) * (jaw_len * 0.55)

            jaw_poly = [(j_base_x, j_base_y), (j_mid_x, j_mid_y), (j_tip_x, j_tip_y)]
            j_col = (255, 240, 80) if self.is_magma else pal['spec']
            pygame.draw.lines(surf, j_col, False, jaw_poly, 2)
            pygame.draw.circle(surf, (255, 255, 255), (int(j_tip_x), int(j_tip_y)), 1)

        breath_expand = math.sin(self.breath_clock) * 1.5

        for i in range(len(self.segments) - 1, -1, -1):
            if self.is_burrowed and i < len(self.segments) - 2:
                continue

            seg = self.segments[i]
            rot = seg.angle + math.pi / 2
            cos_r = math.cos(rot); sin_r = math.sin(rot)
            a = seg.radius + (breath_expand if i < tail_root_idx else 0)
            b = seg.length * 1.15

            if self.is_overdrive and not self.is_burrowed:
                a *= 1.12

            dist_to_pulse = abs(i - self.pulse_phase)
            energy_factor = max(0.0, 1.0 - (dist_to_pulse / 2.8)) if dist_to_pulse < 2.8 else 0.0

            p1 = (seg.x + (a * 1.05) * cos_r - b * 0.6 * sin_r, seg.y + (a * 1.05) * sin_r + b * 0.6 * cos_r)
            p2 = (seg.x + (a * 0.85) * cos_r + b * 0.9 * sin_r, seg.y + (a * 0.85) * sin_r - b * 0.9 * cos_r)
            p3 = (seg.x - (a * 0.85) * cos_r + b * 0.9 * sin_r, seg.y - (a * 0.85) * sin_r - b * 0.9 * cos_r)
            p4 = (seg.x - (a * 1.05) * cos_r - b * 0.6 * sin_r, seg.y - (a * 1.05) * sin_r + b * 0.6 * cos_r)
            pts = [p1, p2, p3, p4]

            pygame.draw.polygon(surf, pal['dark'], pts)
            pygame.draw.polygon(surf, pal['plate'], pts, max(1, int(2)))

            pygame.draw.line(surf, pal['spec'], p4, p1, 2)
            pygame.draw.line(surf, pal['shadow_edge'], p2, p3, 2)

            if a > 6:
                inner_w = a * 0.58
                inner_l = b * 0.48
                fissure_pts = [
                    (seg.x + inner_w * cos_r, seg.y + inner_w * sin_r),
                    (seg.x + math.cos(seg.angle) * inner_l, seg.y + math.sin(seg.angle) * inner_l),
                    (seg.x - inner_w * cos_r, seg.y - inner_w * sin_r),
                    (seg.x - math.cos(seg.angle) * inner_l, seg.y - math.sin(seg.angle) * inner_l)
                ]
                fissure_color = pal['fissure'] if self.is_magma else pal['mid']
                pygame.draw.polygon(surf, fissure_color, fissure_pts)

            edge_col = NEON_PINK_BORDER if rim_tint > 0.4 else pal['edge']
            pygame.draw.lines(surf, edge_col, True, pts, 1)

            if not self.is_burrowed and 2 <= i <= 14:
                back_ang = seg.angle + math.pi
                sp_len = a + 7 + min(11, self.evo_level * 0.20)
                w_base = 4.8
                for s_sign in [-1, 1]:
                    base_cx = seg.x + cos_r * (a * 0.85) * s_sign
                    base_cy = seg.y + sin_r * (a * 0.85) * s_sign
                    spk_tip_x = clamp_x(seg.x + cos_r * sp_len * s_sign + math.cos(back_ang) * 5)
                    spk_tip_y = clamp_y(seg.y + sin_r * sp_len * s_sign + math.sin(back_ang) * 5)

                    tri = [
                        (base_cx - math.cos(back_ang) * w_base, base_cy - math.sin(back_ang) * w_base),
                        (base_cx + math.cos(back_ang) * w_base, base_cy + math.sin(back_ang) * w_base),
                        (spk_tip_x, spk_tip_y)
                    ]
                    pygame.draw.polygon(surf, pal['dark'], tri)
                    spike_edge_col = (255, 140, 20) if self.is_magma else pal['edge']
                    pygame.draw.lines(surf, spike_edge_col, True, tri, 1)

            if energy_factor > 0.2 or self.is_magma:
                pulse_col = (255, 230, 80) if self.is_magma else pal['core']
                r_size = int(4 + energy_factor * 2) if not self.is_magma else 5
                pygame.draw.circle(surf, pulse_col, (int(seg.x), int(seg.y)), r_size)

        if not self.is_burrowed:
            h_rad = head.radius + 2
            head_pts = [
                (head.x + math.cos(fwd_ang) * (h_rad * 1.40), head.y + math.sin(fwd_ang) * (h_rad * 1.40)),
                (head.x + math.cos(fwd_ang + 0.9) * (h_rad * 1.05), head.y + math.sin(fwd_ang + 0.9) * (h_rad * 1.05)),
                (head.x + math.cos(perp) * h_rad, head.y + math.sin(perp) * h_rad),
                (head.x - math.cos(fwd_ang) * (h_rad * 0.85), head.y - math.sin(fwd_ang) * (h_rad * 0.85)),
                (head.x - math.cos(perp) * h_rad, head.y - math.sin(perp) * h_rad),
                (head.x + math.cos(fwd_ang - 0.9) * (h_rad * 1.05), head.y + math.sin(fwd_ang - 0.9) * (h_rad * 1.05)),
            ]
            pygame.draw.polygon(surf, pal['dark'], head_pts)
            pygame.draw.polygon(surf, pal['plate'], head_pts, 2)
            pygame.draw.lines(surf, NEON_PINK_BORDER if rim_tint > 0.4 else pal['edge'], True, head_pts, 2)

            eye_col = (255, 240, 60) if self.is_magma else pal['neon']
            for s_side in [-1, 1]:
                m_eye_x = head.x + math.cos(fwd_ang) * (h_rad * 0.55) + math.cos(perp) * (s_side * 3.5)
                m_eye_y = head.y + math.sin(fwd_ang) * (h_rad * 0.55) + math.sin(perp) * (s_side * 3.5)
                pygame.draw.circle(surf, eye_col, (int(m_eye_x), int(m_eye_y)), 3)
                pygame.draw.circle(surf, (255, 255, 255), (int(m_eye_x), int(m_eye_y)), 1)

                for e_off in range(3):
                    lat_x = head.x + math.cos(fwd_ang) * (h_rad * 0.15 - e_off * 2.5) + math.cos(perp) * (s_side * (h_rad * 0.75))
                    lat_y = head.y + math.sin(fwd_ang) * (h_rad * 0.15 - e_off * 2.5) + math.sin(perp) * (s_side * (h_rad * 0.75))
                    pygame.draw.circle(surf, eye_col, (int(lat_x), int(lat_y)), 2)

        st_ang = tip.angle + math.pi
        st_len = 22

        amp_x = tip.x + math.cos(st_ang) * (st_len * 0.45)
        amp_y = tip.y + math.sin(st_ang) * (st_len * 0.45)
        amp_r = 7 if not self.is_magma else 9
        pygame.draw.circle(surf, pal['dark'], (int(amp_x), int(amp_y)), amp_r + 2)
        pygame.draw.circle(surf, pal['fissure'] if self.is_magma else pal['plate'], (int(amp_x), int(amp_y)), amp_r)
        pygame.draw.circle(surf, (255, 240, 100) if self.is_magma else pal['neon'], (int(amp_x), int(amp_y)), max(1, amp_r // 2))

        st_x = clamp_x(tip.x + math.cos(st_ang) * st_len)
        st_y = clamp_y(tip.y + math.sin(st_ang) * st_len)
        st_color = (255, 240, 80) if self.is_magma else pal['edge']
        pygame.draw.line(surf, st_color, (amp_x, amp_y), (st_x, st_y), 3)
        pygame.draw.circle(surf, (255, 255, 255), (int(st_x), int(st_y)), 2)

# ==================== MEHANIČKE NOGE ZA CYBER BOSSA ====================
class ModularLeg:
    def __init__(self, boss, side, mount_local, idle_foot, move_foot, group_id, parent_seg, spec):
        self.boss = boss
        self.side = side
        self.mount_local = mount_local
        self.idle_foot = idle_foot
        self.move_foot = move_foot
        self.group_id = group_id
        self.parent_seg = parent_seg
        self.spec = spec
        self.cur_pos = [0.0, 0.0]
        self.tgt_pos = [0.0, 0.0]
        self.start_pos = [0.0, 0.0]
        self.lift = 0.0
        self.step_t = 1.0
        self.compression = 1.0

    def init_pos(self, bx, by, ang):
        S = self.boss.scale
        fx, fy = to_world(self.idle_foot[0], self.idle_foot[1], bx, by, ang, self.spec["scale_w"], S)
        self.cur_pos = [float(fx), float(fy)]
        self.tgt_pos = [float(fx), float(fy)]

    def update(self, bx, by, ang, is_moving, speed, vel_x, vel_y, active_group, stance_blend):
        S = self.boss.scale
        cur_x = lerp(self.idle_foot[0], self.move_foot[0], stance_blend)
        cur_y = lerp(self.idle_foot[1], self.move_foot[1], stance_blend)
        ideal_x, ideal_y = to_world(cur_x, cur_y, bx, by, ang, self.spec["scale_w"], S)
        ideal_x += vel_x * 8.5 * S
        ideal_y += vel_y * 8.5 * S

        dist = math.hypot(ideal_x - self.cur_pos[0], ideal_y - self.cur_pos[1])
        if is_moving and self.step_t >= 1.0 and dist > (28 * S) and self.group_id == active_group:
            self.start_pos = list(self.cur_pos)
            self.tgt_pos = [ideal_x, ideal_y]
            self.step_t = 0.0

        if self.step_t < 1.0:
            self.step_t += 0.22 * max(1.0, speed * 0.45)
            if self.step_t >= 1.0:
                self.step_t = 1.0
                self.cur_pos = list(self.tgt_pos)
                self.lift = 0.0
                emit_particles(self.cur_pos[0], self.cur_pos[1], self.spec["c_spark"], count=3, speed_mult=0.5)
            else:
                t = self.step_t
                self.cur_pos[0] = self.start_pos[0] + (self.tgt_pos[0] - self.start_pos[0]) * t
                self.cur_pos[1] = self.start_pos[1] + (self.tgt_pos[1] - self.start_pos[1]) * t
                self.lift = math.sin(t * math.pi) * (20.0 * S)

        if self.lift > 2.0:
            self.compression = lerp(self.compression, 1.15, 0.2)
        else:
            self.compression = lerp(self.compression, 0.75, 0.25)

    def draw(self, surf, bx, by, ang, h_ix, h_iy, is_shadow=False):
        S = self.boss.scale
        hx, hy = to_world(self.mount_local[0], self.mount_local[1], bx, by, ang, self.spec["scale_w"], S)
        fx = int(self.cur_pos[0] + (14 * S if is_shadow else 0))
        fy = int(self.cur_pos[1] - (0 if is_shadow else self.lift) + (16 * S if is_shadow else 0))

        if is_shadow:
            hx += int(14 * S); hy += int(16 * S)

        dx, dy = fx - hx, fy - hy
        d = math.hypot(dx, dy)
        l1, l2 = 54.0 * S, 66.0 * S
        d_clamped = min(max(10.0, d), l1 + l2 - 5.0)
        base_a = math.atan2(dy, dx)
        cos_v = (l1*l1 + d_clamped*d_clamped - l2*l2) / (2 * l1 * d_clamped)
        knee_out = self.side * math.acos(max(-1.0, min(1.0, cos_v)))
        knee_a = base_a + knee_out
        kx = int(hx + math.cos(knee_a) * l1)
        ky = int(hy + math.sin(knee_a) * l1)

        if is_shadow:
            pygame.draw.line(surf, C_GROUND_SHADOW, (hx, hy), (kx, ky), max(1, int(7 * S)))
            pygame.draw.line(surf, C_GROUND_SHADOW, (kx, ky), (fx, fy), max(1, int(5 * S)))
            return

        pygame.draw.line(surf, self.spec["c_chassis"], (hx, hy), (kx, ky), max(1, int(10 * S)))
        pygame.draw.line(surf, self.spec["c_dark"], (hx, hy), (kx, ky), max(1, int(6 * S)))
        pygame.draw.line(surf, self.spec["c_main"], (hx, hy), (kx, ky), max(1, int(2.0 * S)))

        pygame.draw.circle(surf, self.spec["c_chassis"], (kx, ky), max(1, int(8 * S)))
        pygame.draw.circle(surf, self.spec["c_metal"], (kx, ky), max(1, int(5 * S)))
        pygame.draw.circle(surf, self.spec["c_main"], (kx, ky), max(1, int(2 * S)))

        ankle = (int(kx + (fx - kx) * 0.88), int(ky + (fy - ky) * 0.88))
        draw_coil_spring(surf, (kx, ky), ankle, self.compression, self.spec["c_spring"], S=S)
        draw_sagging_hose(surf, (hx, hy), (kx, ky), 6*S, h_ix*0.4, h_iy*0.4, self.spec["c_chassis"], self.spec["c_main"], S=S)

        ftype = self.spec["foot"]
        if ftype == "blade":
            b_dir = base_a + 0.45 * self.side
            b1 = (int(fx - math.cos(b_dir) * (12 * S)), int(fy - math.sin(b_dir) * (12 * S)))
            b2 = (int(fx + math.cos(base_a) * (8 * S)), int(fy + math.sin(base_a) * (8 * S)))
            pygame.draw.polygon(surf, self.spec["c_chassis"], [(fx, fy), b1, b2])
            pygame.draw.line(surf, self.spec["c_main"], b1, b2, max(1, int(2.2 * S)))
        elif ftype == "heavy_pad":
            pygame.draw.circle(surf, self.spec["c_metal"], (fx, fy), max(2, int(6 * S)))
            pygame.draw.line(surf, self.spec["c_main"], (fx - 4, fy), (fx + 4, fy), max(1, int(3 * S)))
        elif ftype == "stilt":
            tip = (int(fx + math.cos(base_a) * 6), int(fy + math.sin(base_a) * 6))
            pygame.draw.line(surf, self.spec["c_main"], (fx, fy), tip, max(1, int(2.5 * S)))
            pygame.draw.circle(surf, self.spec["c_core"], tip, max(1, int(1.8 * S)))
        elif ftype == "talon":
            for ang_off in [-0.4, 0.4]:
                tx = int(fx + math.cos(base_a + ang_off) * 9 * S)
                ty = int(fy + math.sin(base_a + ang_off) * 9 * S)
                pygame.draw.line(surf, self.spec["c_main"], (fx, fy), (tx, ty), max(1, int(2 * S)))
        else:
            pygame.draw.circle(surf, self.spec["c_core"], (fx, fy), max(1, int(4 * S)))
            pygame.draw.circle(surf, self.spec["c_main"], (fx, fy), max(1, int(2 * S)))

# ==================== 5 SPECIFIČNIH MECH BOSSOVA (BRZINA UBRZANA ZA x1.35!) ====================
BOSS_SPECIES = [
    {
        "id": 0,
        "name": "CRIMSON",
        "title": "APEX ASSASSIN",
        "c_main": (255, 20, 55),
        "c_dark": (140, 10, 25),
        "c_glow": (255, 70, 100),
        "c_core": (255, 245, 248),
        "c_chassis": (16, 18, 22),
        "c_metal": (75, 85, 96),
        "c_spring": (205, 155, 50),
        "c_spark": (255, 40, 70),
        "base_speed": 4.6 * 0.85,   # x1.35 ubrzano (6.21)
        "claw": "mantis",
        "head": "v_visor",
        "tail": "whip_fork",
        "body": "aero_flaps",
        "foot": "blade",
        "scale_w": 1.0
    },
    {
        "id": 1,
        "name": "TITAN",
        "title": "SIEGE JUGGERNAUT",
        "c_main": (255, 180, 10),
        "c_dark": (150, 90, 5),
        "c_glow": (255, 130, 0),
        "c_core": (255, 240, 200),
        "c_chassis": (22, 22, 24),
        "c_metal": (90, 95, 105),
        "c_spring": (70, 75, 85),
        "c_spark": (255, 160, 20),
        "base_speed": 3.4 * 0.85,   # x1.35 ubrzano (4.59)
        "claw": "crusher",
        "head": "bunker",
        "tail": "pile_driver",
        "body": "exhaust_stacks",
        "foot": "heavy_pad",
        "scale_w": 0.85
    },
    {
        "id": 2,
        "name": "PHANTOM",
        "title": "EMP INFILTRATOR",
        "c_main": (0, 225, 255),
        "c_dark": (0, 100, 140),
        "c_glow": (70, 160, 255),
        "c_core": (220, 250, 255),
        "c_chassis": (12, 14, 20),
        "c_metal": (60, 75, 95),
        "c_spring": (0, 180, 220),
        "c_spark": (0, 240, 255),
        "base_speed": 5.0 * 0.85,   # x1.35 ubrzano (6.75)
        "claw": "needle",
        "head": "tri_eye",
        "tail": "emp_orb",
        "body": "stealth_fins",
        "foot": "stilt",
        "scale_w": 0.88
    },
    {
        "id": 3,
        "name": "CORRUPTOR",
        "title": "XENO BIO-PLAGUE",
        "c_main": (50, 255, 75),
        "c_dark": (20, 120, 35),
        "c_glow": (160, 255, 30),
        "c_core": (230, 255, 230),
        "c_chassis": (18, 22, 16),
        "c_metal": (70, 90, 75),
        "c_spring": (120, 180, 40),
        "c_spark": (80, 255, 100),
        "base_speed": 4.1 * 0.85,   # x1.35 ubrzano (5.535)
        "claw": "xeno_jaw",
        "head": "crest",
        "tail": "tri_syringe",
        "body": "acid_vials",
        "foot": "talon",
        "scale_w": 1.05
    },
    {
        "id": 4,
        "name": "SOLARIS",
        "title": "DIVINE SUN-FORGE",
        "c_main": (255, 215, 0),
        "c_dark": (160, 120, 10),
        "c_glow": (255, 145, 0),
        "c_core": (255, 255, 245),
        "c_chassis": (26, 24, 22),
        "c_metal": (195, 185, 170),
        "c_spring": (230, 180, 30),
        "c_spark": (255, 230, 80),
        "base_speed": 4.4 * 0.85,   # x1.35 ubrzano (5.94)
        "claw": "solar_glaive",
        "head": "halo_star",
        "tail": "solar_lance",
        "body": "solar_wings",
        "foot": "strider",
        "scale_w": 1.1
    }
]

class CyberBossScorpion:
    def __init__(self, x, y, species_idx=0):
        self.spec = BOSS_SPECIES[species_idx % len(BOSS_SPECIES)]
        self.species_idx = species_idx
        self.x = float(x)
        self.y = float(y)
        self.angle = math.pi / 2

        self.base_scale = 0.70 * (1.05 ** species_idx)
        self.growth_factor = 1.0
        self.scale = self.base_scale * self.growth_factor

        self.ants_eaten = 0
        self.state = "entering"
        self.target_y = MIN_Y + 120

        self.threat_radius = 210.0 * self.scale

        self.max_hp = 30 + species_idx * 16
        self.hp = float(self.max_hp)

        self.speed = 0.0
        self.max_speed = self.spec["base_speed"]
        self.vel_x = 0.0
        self.vel_y = 0.0

        self.turn_rate = 0.0
        self.body_bend = 0.0
        self.rear_bend = 0.0
        self.head_turn = 0.0
        self.tail_inertia = 0.0

        self.stance_blend = 0.0
        self.hose_ix = 0.0
        self.hose_iy = 0.0
        self.anim_tick = random.uniform(0, 10)
        self.gait_timer = 0.0
        self.active_tripod = 0
        self.aero_flap_open = 0.0
        self.seg_dist = 28.0

        self.attack_timer = 0
        self.contact_cooldown = 0
        self.stun_timer = 0

        self.legs = [
            ModularLeg(self, 1,  (18, -26),  (36, -110), (48, -94), group_id=0, parent_seg=0, spec=self.spec),
            ModularLeg(self, 1,  (0, -32),   (-6, -122), (0, -108), group_id=1, parent_seg=1, spec=self.spec),
            ModularLeg(self, 1,  (-14, -28), (-54, -112), (-46, -96), group_id=0, parent_seg=2, spec=self.spec),
            ModularLeg(self, -1, (18, 26),   (36, 110),  (48, 94),  group_id=1, parent_seg=0, spec=self.spec),
            ModularLeg(self, -1, (0, 32),    (-6, 122),  (0, 108),  group_id=0, parent_seg=1, spec=self.spec),
            ModularLeg(self, -1, (-14, 28),  (-54, 112), (-46, 96), group_id=1, parent_seg=2, spec=self.spec),
        ]
        for leg in self.legs:
            leg.init_pos(self.x, self.y, self.angle)

    def eat_ant(self, ant):
        self.ants_eaten += 1
        spill_blood(ant.x, ant.y, ant.blood_col, count=16)
        play_snd(snd_chew)
        # USPORENO POVEĆANJE BOSSOVA ZA 50% (1.025 umjesto 1.05 svakih 5 pojedenih mrava)
        if self.ants_eaten % 5 == 0:
            self.growth_factor *= 1.025
            self.scale = self.base_scale * self.growth_factor
            self.threat_radius = 210.0 * self.scale
            emit_particles(self.x, self.y, self.spec["c_main"], count=25)
            play_snd(snd_evolve)
            add_shake(10)
        ant.respawn()

    def update(self, player_x, player_y, ants_list, player):
        self.anim_tick += 0.14
        if self.contact_cooldown > 0:
            self.contact_cooldown -= 1

        if self.state in ["entering", "captured"]:
            if self.state == "entering":
                self.y += 3.2
                if self.y >= self.target_y:
                    self.state = "active"
                    add_shake(18); haptic(200); play_snd(snd_slam)
            return

        if self.stun_timer > 0:
            self.stun_timer -= 1
            return

        dx_p = player_x - self.x
        dy_p = player_y - self.y
        dist_to_player = math.hypot(dx_p, dy_p)

        target_pos = None
        is_targeting_player = False

        if dist_to_player < self.threat_radius and not player.is_burrowed:
            target_pos = (player_x, player_y)
            is_targeting_player = True
        else:
            if ants_list:
                closest_ant = min(ants_list, key=lambda a: math.hypot(a.x - self.x, a.y - self.y))
                dist_to_ant = math.hypot(self.x - closest_ant.x, self.y - closest_ant.y)
                if dist_to_ant < (45 * self.scale):
                    self.eat_ant(closest_ant)
                else:
                    target_pos = (closest_ant.x, closest_ant.y)

        is_moving = False
        if target_pos:
            tx, ty = target_pos
            dx, dy = tx - self.x, ty - self.y
            dist = math.hypot(dx, dy)

            if dist > (18 * self.scale):
                is_moving = True
                desired_ang = math.atan2(dy, dx)
                diff = (desired_ang - self.angle + math.pi) % (2 * math.pi) - math.pi

                self.turn_rate = max(-0.16, min(0.16, diff * 0.32))
                self.angle += self.turn_rate

                self.speed = min(self.max_speed, dist * 0.12)
                self.vel_x = math.cos(self.angle) * self.speed
                self.vel_y = math.sin(self.angle) * self.speed
                self.x += self.vel_x
                self.y += self.vel_y

                target_bend = self.turn_rate * 4.6
                self.body_bend += (target_bend - self.body_bend) * 0.19
                self.rear_bend += (target_bend * 1.9 - self.rear_bend) * 0.15
                self.head_turn += (self.turn_rate * 3.0 - self.head_turn) * 0.29
                self.tail_inertia += (-self.turn_rate * 4.0 - self.tail_inertia) * 0.13

                target_flap = min(1.0, (self.speed / self.max_speed) * 0.9 + abs(self.turn_rate) * 4.0)
                self.aero_flap_open += (target_flap - self.aero_flap_open) * 0.22

                self.gait_timer += self.speed * (0.08 / self.scale)
                if self.gait_timer >= 1.0:
                    self.gait_timer = 0.0
                    self.active_tripod = 1 - self.active_tripod
            else:
                self.speed = 0.0; self.turn_rate = 0.0
        else:
            self.speed = 0.0; self.turn_rate = 0.0

        tgt_st = 1.0 if is_moving else 0.0
        self.stance_blend += (tgt_st - self.stance_blend) * 0.07

        self.hose_ix += (-self.vel_x * 2.2 - self.hose_ix) * 0.16
        self.hose_iy += (-self.vel_y * 2.2 - self.hose_iy) * 0.16

        if not is_moving:
            self.body_bend *= 0.85; self.rear_bend *= 0.85
            self.head_turn *= 0.85; self.tail_inertia *= 0.88
            self.aero_flap_open *= 0.85

        if is_targeting_player and dist_to_player < (52 * self.scale) and self.contact_cooldown <= 0:
            player.take_damage(14.0 + self.species_idx * 3)
            self.contact_cooldown = 48
            add_shake(16); haptic(200)

        self.attack_timer += 1
        if is_targeting_player and self.attack_timer >= 110:
            self.attack_timer = 0
            if self.spec["id"] == 1:
                shockwaves.append([self.x, self.y, 0, 180 * self.scale, self.spec["c_main"]])
                add_shake(18); play_snd(snd_slam)
                if dist_to_player < 180 * self.scale:
                    player.take_damage(12.0)
            elif self.spec["id"] == 3:
                ang = math.atan2(player_y - self.y, player_x - self.x)
                boss_projectiles.append([self.x, self.y, math.cos(ang) * 7.5, math.sin(ang) * 7.5, 120])
                play_snd(snd_sting)

        for leg in self.legs:
            sx, sy, sa = self._get_seg_transform(leg.parent_seg)
            leg.update(sx, sy, sa, is_moving, self.speed, self.vel_x, self.vel_y,
                       self.active_tripod, self.stance_blend)

        self.x = clamp_x(self.x, 30)
        self.y = clamp_y(self.y, 30)

    def _get_seg_transform(self, idx):
        S = self.scale
        if idx == 0:
            return self.x, self.y, self.angle
        elif idx == 1:
            ang1 = self.angle - self.body_bend
            return self.x - math.cos(ang1) * (self.seg_dist * S), self.y - math.sin(ang1) * (self.seg_dist * S), ang1
        else:
            ang1 = self.angle - self.body_bend
            ang2 = ang1 - self.rear_bend
            px1 = self.x - math.cos(ang1) * (self.seg_dist * S)
            py1 = self.y - math.sin(ang1) * (self.seg_dist * S)
            return px1 - math.cos(ang2) * (self.seg_dist * S), py1 - math.sin(ang2) * (self.seg_dist * S), ang2

    def take_stinger_hit(self, hx, hy):
        if self.state == "captured": return
        self.hp -= 3
        add_shake(15); haptic(160)
        spill_blood(self.x, self.y, self.spec["c_main"], count=18)
        if self.hp <= 0:
            self.state = "captured"
            scorpion.trigger_boss_feast(self)

    def take_slam_hit(self):
        if self.state == "captured": return
        self.hp -= 4
        add_shake(18); haptic(180)
        spill_blood(self.x, self.y, self.spec["c_main"], count=22)
        if self.hp <= 0:
            self.state = "captured"
            scorpion.trigger_boss_feast(self)

    def draw(self, surf):
        S = self.scale

        rim_tint = get_border_rim_tint(self.x, self.y)
        if rim_tint > 0:
            pygame.draw.circle(surf, NEON_PINK_BORDER, (int(self.x), int(self.y)), int(50 * S), 2)

        self._render(surf, is_shadow=True)
        self._render(surf, is_shadow=False)

        if self.state != "captured":
            bar_w = int(140 * S)
            bar_x = self.x - bar_w // 2
            bar_y = self.y - (56 * S)
            pygame.draw.rect(surf, (25, 10, 15), (bar_x, bar_y, bar_w, 9), border_radius=3)
            hp_ratio = max(0.0, self.hp / float(self.max_hp))
            pygame.draw.rect(surf, self.spec["c_main"], (bar_x, bar_y, int(bar_w * hp_ratio), 9), border_radius=3)
            pygame.draw.rect(surf, (255, 255, 255), (bar_x, bar_y, bar_w, 9), 1, border_radius=3)

    def _render(self, surf, is_shadow):
        S = self.scale
        ox = int(14 * S) if is_shadow else 0
        oy = int(16 * S) if is_shadow else 0
        s0_x, s0_y, s0_a = self._get_seg_transform(0); s0_x += ox; s0_y += oy
        s1_x, s1_y, s1_a = self._get_seg_transform(1); s1_x += ox; s1_y += oy
        s2_x, s2_y, s2_a = self._get_seg_transform(2); s2_x += ox; s2_y += oy

        for leg in self.legs:
            sx = s0_x if leg.parent_seg == 0 else (s1_x if leg.parent_seg == 1 else s2_x)
            sy = s0_y if leg.parent_seg == 0 else (s1_y if leg.parent_seg == 1 else s2_y)
            sa = s0_a if leg.parent_seg == 0 else (s1_a if leg.parent_seg == 1 else s2_a)
            leg.draw(surf, sx, sy, sa, self.hose_ix, self.hose_iy, is_shadow)

        self._draw_claws(surf, s0_x, s0_y, s0_a, is_shadow)
        self._draw_meta_thorax(surf, s2_x, s2_y, s2_a, is_shadow)
        self._draw_meso_thorax(surf, s1_x, s1_y, s1_a, is_shadow)
        self._draw_pro_thorax(surf, s0_x, s0_y, s0_a, is_shadow)
        self._draw_tail(surf, s2_x, s2_y, s2_a, is_shadow)

    def _draw_claws(self, surf, s0_x, s0_y, s0_a, is_shadow):
        S = self.scale
        c_style = self.spec["claw"]
        sp = lerp(0.06, 0.52, self.stance_blend) + math.sin(self.anim_tick * 1.5) * 0.04

        for side in [-1, 1]:
            b_sh = to_world(24, side * 18, s0_x, s0_y, s0_a, self.spec["scale_w"], S)
            b_elb = to_world(52, side * (38 + sp * 26), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
            b_wri = to_world(90, side * (26 + sp * 36), s0_x, s0_y, s0_a, self.spec["scale_w"], S)

            if is_shadow:
                pygame.draw.line(surf, C_GROUND_SHADOW, b_sh, b_elb, max(1, int(12 * S)))
                pygame.draw.line(surf, C_GROUND_SHADOW, b_elb, b_wri, max(1, int(9 * S)))
            else:
                pygame.draw.line(surf, self.spec["c_chassis"], b_sh, b_elb, max(1, int(13 * S)))
                pygame.draw.line(surf, self.spec["c_dark"], b_sh, b_elb, max(1, int(8 * S)))
                pygame.draw.line(surf, self.spec["c_main"], b_sh, b_elb, max(1, int(2.5 * S)))
                pygame.draw.line(surf, self.spec["c_chassis"], b_elb, b_wri, max(1, int(10 * S)))
                pygame.draw.circle(surf, self.spec["c_metal"], b_elb, max(1, int(6 * S)))

            if c_style == "mantis":
                tip = to_world(140, side * (18 + sp * 22), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                mid = to_world(122, side * (42 + sp * 40), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                if is_shadow:
                    pygame.draw.polygon(surf, C_GROUND_SHADOW, [b_wri, mid, tip])
                else:
                    pygame.draw.polygon(surf, self.spec["c_chassis"], [b_wri, mid, tip])
                    pygame.draw.line(surf, self.spec["c_dark"], b_wri, mid, max(1, int(5 * S)))
                    pygame.draw.line(surf, self.spec["c_main"], mid, tip, max(1, int(3.5 * S)))
                    pygame.draw.line(surf, self.spec["c_core"], b_wri, tip, max(1, int(1.5 * S)))

            elif c_style == "crusher":
                box1 = to_world(116, side * (40 + sp * 24), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                box2 = to_world(134, side * (12 + sp * 14), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                if is_shadow:
                    pygame.draw.polygon(surf, C_GROUND_SHADOW, [b_wri, box1, box2])
                else:
                    pygame.draw.polygon(surf, self.spec["c_chassis"], [b_wri, box1, box2])
                    pygame.draw.polygon(surf, self.spec["c_main"], [b_wri, box1, box2], max(1, int(2.5 * S)))
                    z1 = to_world(126, side * 22, s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                    pygame.draw.line(surf, self.spec["c_core"], b_wri, z1, max(1, int(3 * S)))

            elif c_style == "needle":
                tip = to_world(152, side * (12 + sp * 16), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                if is_shadow:
                    pygame.draw.line(surf, C_GROUND_SHADOW, b_wri, tip, max(1, int(5 * S)))
                else:
                    pygame.draw.line(surf, self.spec["c_main"], b_wri, tip, max(1, int(3 * S)))
                    pygame.draw.line(surf, self.spec["c_core"], b_wri, tip, max(1, int(1.2 * S)))
                    pygame.draw.circle(surf, self.spec["c_core"], tip, max(1, int(2 * S)))

            elif c_style == "xeno_jaw":
                tip = to_world(136, side * (26 + sp * 18), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                if is_shadow:
                    pygame.draw.line(surf, C_GROUND_SHADOW, b_wri, tip, max(1, int(8 * S)))
                else:
                    pygame.draw.line(surf, self.spec["c_dark"], b_wri, tip, max(1, int(7 * S)))
                    pygame.draw.line(surf, self.spec["c_main"], b_wri, tip, max(1, int(3 * S)))

            else:
                tip1 = to_world(144, side * (22 + sp * 24), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                tip2 = to_world(120, side * (5 + sp * 10), s0_x, s0_y, s0_a, self.spec["scale_w"], S)
                if is_shadow:
                    pygame.draw.line(surf, C_GROUND_SHADOW, b_wri, tip1, max(1, int(7 * S)))
                else:
                    pygame.draw.line(surf, self.spec["c_main"], b_wri, tip1, max(1, int(5 * S)))
                    pygame.draw.line(surf, self.spec["c_core"], b_wri, tip1, max(1, int(2 * S)))
                    pygame.draw.line(surf, self.spec["c_metal"], b_wri, tip2, max(1, int(3 * S)))

    def _draw_pro_thorax(self, surf, bx, by, ang, is_shadow):
        S = self.scale
        pts = [
            to_world(38, 0, bx, by, ang, self.spec["scale_w"], S),
            to_world(24, 25, bx, by, ang, self.spec["scale_w"], S),
            to_world(-10, 28, bx, by, ang, self.spec["scale_w"], S),
            to_world(-16, 0, bx, by, ang, self.spec["scale_w"], S),
            to_world(-10, -28, bx, by, ang, self.spec["scale_w"], S),
            to_world(24, -25, bx, by, ang, self.spec["scale_w"], S),
        ]
        if is_shadow:
            pygame.draw.polygon(surf, C_GROUND_SHADOW, pts); return

        pygame.draw.polygon(surf, self.spec["c_chassis"], pts)
        pygame.draw.polygon(surf, self.spec["c_dark"], pts, max(1, int(3 * S)))
        pygame.draw.polygon(surf, self.spec["c_main"], pts, max(1, int(1.4 * S)))

        h_style = self.spec["head"]
        if h_style == "v_visor":
            for side in [-1, 1]:
                v1 = to_world(36, side * 3, bx, by, ang, self.spec["scale_w"], S)
                v2 = to_world(26, side * 16, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.line(surf, self.spec["c_core"], v1, v2, max(1, int(2 * S)))
                pygame.draw.line(surf, self.spec["c_main"], v1, v2, max(1, int(4 * S)))
        elif h_style == "bunker":
            s1 = to_world(32, -14, bx, by, ang, self.spec["scale_w"], S)
            s2 = to_world(32, 14, bx, by, ang, self.spec["scale_w"], S)
            pygame.draw.line(surf, self.spec["c_core"], s1, s2, max(1, int(3 * S)))
            pygame.draw.line(surf, self.spec["c_main"], s1, s2, max(1, int(5 * S)))
        elif h_style == "tri_eye":
            for dy in [-10, 0, 10]:
                ep = to_world(30 if dy == 0 else 24, dy, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.circle(surf, self.spec["c_core"], ep, max(1, int(2.2 * S)))
                pygame.draw.circle(surf, self.spec["c_main"], ep, max(1, int(1.2 * S)))
        elif h_style == "crest":
            tip = to_world(44, 0, bx, by, ang, self.spec["scale_w"], S)
            base = to_world(22, 0, bx, by, ang, self.spec["scale_w"], S)
            pygame.draw.line(surf, self.spec["c_main"], base, tip, max(1, int(4 * S)))
            pygame.draw.circle(surf, self.spec["c_glow"], tip, max(1, int(3 * S)))
        else:
            cp = to_world(28, 0, bx, by, ang, self.spec["scale_w"], S)
            pygame.draw.circle(surf, self.spec["c_core"], cp, max(1, int(5 * S)))
            pygame.draw.circle(surf, self.spec["c_main"], cp, max(1, int(2.5 * S)))

    def _draw_meso_thorax(self, surf, bx, by, ang, is_shadow):
        S = self.scale
        pts = [
            to_world(16, -26, bx, by, ang, self.spec["scale_w"], S),
            to_world(16, 26, bx, by, ang, self.spec["scale_w"], S),
            to_world(-16, 28, bx, by, ang, self.spec["scale_w"], S),
            to_world(-16, -28, bx, by, ang, self.spec["scale_w"], S),
        ]
        if is_shadow:
            pygame.draw.polygon(surf, C_GROUND_SHADOW, pts); return

        pygame.draw.polygon(surf, self.spec["c_chassis"], pts)
        pygame.draw.polygon(surf, self.spec["c_dark"], pts, max(1, int(3 * S)))

        b_style = self.spec["body"]
        if b_style == "aero_flaps":
            fl = 26 + self.aero_flap_open * 10
            for side in [-1, 1]:
                f1 = to_world(10, side * 18, bx, by, ang, self.spec["scale_w"], S)
                f2 = to_world(-12, side * fl, bx, by, ang, self.spec["scale_w"], S)
                f3 = to_world(-16, side * 16, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.polygon(surf, self.spec["c_metal"], [f1, f2, f3])
                pygame.draw.line(surf, self.spec["c_main"], f1, f2, max(1, int(2 * S)))
        elif b_style == "exhaust_stacks":
            for side in [-1, 1]:
                p = to_world(-8, side * 22, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.circle(surf, self.spec["c_metal"], p, max(2, int(5 * S)))
                pygame.draw.circle(surf, self.spec["c_glow"], p, max(1, int(2.5 * S)))
        elif b_style == "acid_vials":
            for side in [-1, 1]:
                v1 = to_world(-6, side * 16, bx, by, ang, self.spec["scale_w"], S)
                v2 = to_world(10, side * 16, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.line(surf, self.spec["c_glow"], v1, v2, max(1, int(4 * S)))
                pygame.draw.circle(surf, self.spec["c_core"], v2, max(1, int(2 * S)))
        elif b_style == "solar_wings":
            for side in [-1, 1]:
                w1 = to_world(4, side * 18, bx, by, ang, self.spec["scale_w"], S)
                w2 = to_world(-20, side * 36, bx, by, ang, self.spec["scale_w"], S)
                pygame.draw.line(surf, self.spec["c_main"], w1, w2, max(1, int(3 * S)))
                pygame.draw.line(surf, self.spec["c_core"], w1, w2, max(1, int(1.2 * S)))

        core_c = (bx, by)
        b_r = max(2, int((7 + math.sin(self.anim_tick * 1.5) * 1.2) * S))
        pygame.draw.circle(surf, self.spec["c_dark"], core_c, max(3, int(9 * S)))
        pygame.draw.circle(surf, self.spec["c_main"], core_c, b_r)
        pygame.draw.circle(surf, self.spec["c_core"], core_c, max(1, int(b_r * 0.4)))

    def _draw_meta_thorax(self, surf, bx, by, ang, is_shadow):
        S = self.scale
        pts = [
            to_world(14, -24, bx, by, ang, self.spec["scale_w"], S),
            to_world(14, 24, bx, by, ang, self.spec["scale_w"], S),
            to_world(-22, 16, bx, by, ang, self.spec["scale_w"], S),
            to_world(-22, -16, bx, by, ang, self.spec["scale_w"], S),
        ]
        if is_shadow:
            pygame.draw.polygon(surf, C_GROUND_SHADOW, pts); return
        pygame.draw.polygon(surf, self.spec["c_chassis"], pts)
        pygame.draw.polygon(surf, self.spec["c_dark"], pts, max(1, int(2.5 * S)))
        pygame.draw.polygon(surf, self.spec["c_main"], pts, max(1, int(1.2 * S)))

    def _draw_tail(self, surf, s2_x, s2_y, s2_ang, is_shadow):
        S = self.scale
        cur_rx, cur_ry = to_world(-24, 0, s2_x, s2_y, s2_ang, self.spec["scale_w"], S)
        idle_curl = math.sin(self.anim_tick * 0.8) * 0.12
        tail_ang = lerp(s2_ang + math.pi + idle_curl, s2_ang + math.pi + self.tail_inertia, self.stance_blend)
        vert_pts = [(cur_rx, cur_ry)]

        for v_idx in range(7):
            v_len = int((19 - v_idx * 1.4) * S)
            v_w = max(2, int(max(4, 14 - v_idx * 1.5) * S))
            tail_ang += self.tail_inertia * 0.22 + math.sin(self.anim_tick * 1.2 + v_idx) * 0.04 + lerp(0.03, 0.09, self.stance_blend)
            next_rx = cur_rx + int(math.cos(tail_ang) * v_len)
            next_ry = cur_ry + int(math.sin(tail_ang) * v_len)

            if is_shadow:
                pygame.draw.line(surf, C_GROUND_SHADOW, (cur_rx, cur_ry), (next_rx, next_ry), int(v_w + 2))
            else:
                pygame.draw.line(surf, self.spec["c_chassis"], (cur_rx, cur_ry), (next_rx, next_ry), v_w)
                pygame.draw.line(surf, self.spec["c_main"], (cur_rx, cur_ry), (next_rx, next_ry), max(1, int(v_w * 0.4)))

            cur_rx, cur_ry = next_rx, next_ry
            vert_pts.append((cur_rx, cur_ry))

        t_style = self.spec["tail"]
        st_dir = tail_ang + 1.25
        st_len = int(22 * S)
        tip = (cur_rx + int(math.cos(st_dir) * st_len), cur_ry + int(math.sin(st_dir) * st_len))

        if is_shadow:
            pygame.draw.line(surf, C_GROUND_SHADOW, (cur_rx, cur_ry), tip, max(1, int(6 * S)))
            return

        if t_style == "whip_fork":
            h1 = (int(tip[0] + math.cos(st_dir + 0.6) * 9 * S), int(tip[1] + math.sin(st_dir + 0.6) * 9 * S))
            h2 = (int(tip[0] + math.cos(st_dir - 0.6) * 9 * S), int(tip[1] + math.sin(st_dir - 0.6) * 9 * S))
            pygame.draw.line(surf, C_CHROME, (cur_rx, cur_ry), tip, max(1, int(3 * S)))
            pygame.draw.line(surf, self.spec["c_main"], tip, h1, max(1, int(2 * S)))
            pygame.draw.line(surf, self.spec["c_main"], tip, h2, max(1, int(2 * S)))
            draw_electric_arc(surf, h1, h2, self.spec["c_main"], segments=2, jitter=3, S=S)

        elif t_style == "pile_driver":
            pygame.draw.line(surf, self.spec["c_metal"], (cur_rx, cur_ry), tip, max(1, int(6 * S)))
            pygame.draw.circle(surf, self.spec["c_main"], tip, max(2, int(5 * S)))

        elif t_style == "emp_orb":
            pygame.draw.circle(surf, self.spec["c_dark"], tip, max(2, int(7 * S)))
            pygame.draw.circle(surf, self.spec["c_core"], tip, max(1, int(4 * S)))
            if random.random() < 0.25 and len(vert_pts) >= 2:
                draw_electric_arc(surf, vert_pts[-2], tip, self.spec["c_main"], segments=3, jitter=4, S=S)

        elif t_style == "tri_syringe":
            for off in [-0.3, 0.0, 0.3]:
                sp_tip = (cur_rx + int(math.cos(st_dir + off) * st_len), cur_ry + int(math.sin(st_dir + off) * st_len))
                pygame.draw.line(surf, self.spec["c_main"], (cur_rx, cur_ry), sp_tip, max(1, int(2 * S)))
                pygame.draw.circle(surf, self.spec["c_glow"], sp_tip, max(1, int(2 * S)))

        else:
            pygame.draw.line(surf, self.spec["c_core"], (cur_rx, cur_ry), tip, max(1, int(4 * S)))
            for r_s in [0.4, 0.8]:
                rx = int(cur_rx + (tip[0] - cur_rx) * r_s)
                ry = int(cur_ry + (tip[1] - cur_ry) * r_s)
                pygame.draw.circle(surf, self.spec["c_main"], (rx, ry), max(1, int(4 * S)), 1)

# ==================== JEDINSTVENO IME ŠKORPIONA ====================
SCORPION_NAME = "APEX TITAN"

target_x, target_y = WIDTH // 2, HEIGHT // 2
scorpion = Scorpion(target_x, target_y)
ants = [Ant(force_gold=True)] + [Ant(force_gold=False) for _ in range(7)]

is_user_touching = False
door_open_progress = 0.0

# STANJE IGRE: "START_MENU" (Početni zaslon prije igre) ili "PLAYING" (Aktivna igra)
game_state = "START_MENU"

font_big_logo = pygame.font.SysFont(None, max(64, int(WIDTH * 0.11)), bold=True)
font_sub_logo = pygame.font.SysFont(None, max(28, int(WIDTH * 0.042)), bold=True)
font_btn = pygame.font.SysFont(None, max(44, int(WIDTH * 0.075)), bold=True)
font_title = pygame.font.SysFont(None, 28, bold=True)
font_hud = pygame.font.SysFont(None, 22)
font_bold_hud = pygame.font.SysFont(None, 22, bold=True)

flash_surf = pygame.Surface((WIDTH, HEIGHT))
menu_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
# ==================== START MENU I SETTINGS (POSTAVKE) ====================
settings_open = False
sfx_enabled = True
vibe_enabled = True
_saved_vibrate_fn = vibrate_fn
_audio_hw_ok = audio_enabled

def get_start_button_rect():
    btn_w = min(380, int(WIDTH * 0.68))
    btn_h = max(72, int(HEIGHT * 0.064))
    return pygame.Rect(WIDTH // 2 - btn_w // 2, int(HEIGHT * 0.69) - btn_h // 2, btn_w, btn_h)

def get_settings_button_rect():
    btn_w = min(320, int(WIDTH * 0.56))
    btn_h = max(58, int(HEIGHT * 0.052))
    return pygame.Rect(WIDTH // 2 - btn_w // 2, int(HEIGHT * 0.78) - btn_h // 2, btn_w, btn_h)

def get_sfx_toggle_rect():
    btn_w = min(440, int(WIDTH * 0.74))
    btn_h = max(68, int(HEIGHT * 0.060))
    return pygame.Rect(WIDTH // 2 - btn_w // 2, int(HEIGHT * 0.46) - btn_h // 2, btn_w, btn_h)

def get_vibe_toggle_rect():
    btn_w = min(440, int(WIDTH * 0.74))
    btn_h = max(68, int(HEIGHT * 0.060))
    return pygame.Rect(WIDTH // 2 - btn_w // 2, int(HEIGHT * 0.57) - btn_h // 2, btn_w, btn_h)

def get_back_button_rect():
    btn_w = min(300, int(WIDTH * 0.52))
    btn_h = max(62, int(HEIGHT * 0.055))
    return pygame.Rect(WIDTH // 2 - btn_w // 2, int(HEIGHT * 0.72) - btn_h // 2, btn_w, btn_h)

def draw_start_menu(surf, time_ms):
    menu_overlay.fill((8, 6, 12, 185))
    surf.blit(menu_overlay, (0, 0))

    cx = WIDTH // 2
    cy_logo = int(HEIGHT * 0.22)
    pulse = math.sin(time_ms * 0.004)

    # Dekorativni biomehanički okvir na početnom ekranu
    panel_w = min(680, int(WIDTH * 0.88))
    panel_h = int(HEIGHT * 0.74)
    panel_rect = pygame.Rect(cx - panel_w // 2, int(HEIGHT * 0.12), panel_w, panel_h)
    pygame.draw.rect(surf, (18, 12, 22), panel_rect, border_radius=18)
    pygame.draw.rect(surf, NEON_PINK_BORDER, panel_rect, 3, border_radius=18)
    pygame.draw.rect(surf, (255, 130, 50), panel_rect.inflate(-12, -12), 1, border_radius=14)

    # Glavni naslov igre: APEX TITAN
    title_shadow = font_big_logo.render("APEX TITAN", True, (0, 0, 0))
    title_main = font_big_logo.render("APEX TITAN", True, (255, 45, 95))
    title_glow = font_big_logo.render("APEX TITAN", True, (255, 235, 245))
    surf.blit(title_shadow, (cx - title_main.get_width() // 2 + 4, cy_logo - 35 + 4))
    surf.blit(title_main, (cx - title_main.get_width() // 2 - 2, cy_logo - 35))
    surf.blit(title_glow, (cx - title_glow.get_width() // 2, cy_logo - 37))

    if not settings_open:
        sub_s = font_sub_logo.render("PURE BIOMECHANICAL EDITION", True, (255, 185, 70))
        surf.blit(sub_s, (cx - sub_s.get_width() // 2, cy_logo + 28))

        # Glow krug iza amblema
        emblem_y = int(HEIGHT * 0.40)
        glow_r = int(72 + pulse * 7)
        pygame.draw.circle(surf, (45, 14, 28), (cx, emblem_y), glow_r + 16)
        pygame.draw.circle(surf, (95, 20, 42), (cx, emblem_y), glow_r)
        pygame.draw.circle(surf, NEON_PINK_BORDER, (cx, emblem_y), glow_r, 3)

        # Stilski amblem kliješta i žalca u sredini
        for side in [-1, 1]:
            c1 = (cx + side * 24, emblem_y + 16)
            c2 = (cx + side * 52, emblem_y - 10 + int(pulse * 5))
            c3 = (cx + side * 32, emblem_y - 44)
            c4 = (cx + side * 16, emblem_y - 14)
            pygame.draw.polygon(surf, (230, 235, 245), [c1, c2, c3, c4])
            pygame.draw.polygon(surf, (255, 40, 85), [c1, c2, c3, c4], 2)
        pygame.draw.circle(surf, (255, 210, 60), (cx, emblem_y + 5), 13)
        pygame.draw.circle(surf, (255, 40, 75), (cx, emblem_y - 50), 7)

        # Kratke upute za igranje
        info_lines = [
            "• DRŽI I POVLAČI PRSTOM ZA KRETANJE I LOV MRAVA",
            "• DVOSTRUKI KLIK (DOUBLE TAP) ZA SEIZMIČKI SLAM (15 DNA)",
            "• SKUPLJAJ ENERGIJU, EVOLUIRAJ I PORAZI 5 CYBER BOSSOVA"
        ]
        info_y = int(HEIGHT * 0.53)
        for line in info_lines:
            ls = font_bold_hud.render(line, True, (210, 215, 230))
            surf.blit(ls, (cx - ls.get_width() // 2, info_y))
            info_y += 26

        # Gumb START
        btn_rect = get_start_button_rect()
        btn_inflate = int(pulse * 6)
        anim_rect = btn_rect.inflate(btn_inflate, btn_inflate // 2)

        pygame.draw.rect(surf, (35, 10, 22), anim_rect.move(0, 6), border_radius=16)
        pygame.draw.rect(surf, (220, 25, 75), anim_rect, border_radius=16)
        pygame.draw.rect(surf, (255, 220, 90), anim_rect, 3, border_radius=16)

        btn_txt = font_btn.render("START", True, (255, 255, 255))
        surf.blit(btn_txt, (anim_rect.centerx - btn_txt.get_width() // 2, anim_rect.centery - btn_txt.get_height() // 2))

        # Gumb SETTINGS (ispod START gumba)
        set_rect = get_settings_button_rect()
        pygame.draw.rect(surf, (14, 10, 20), set_rect.move(0, 5), border_radius=14)
        pygame.draw.rect(surf, (45, 32, 58), set_rect, border_radius=14)
        pygame.draw.rect(surf, (190, 170, 220), set_rect, 2, border_radius=14)

        set_txt = font_sub_logo.render("SETTINGS / POSTAVKE", True, (240, 235, 255))
        surf.blit(set_txt, (set_rect.centerx - set_txt.get_width() // 2, set_rect.centery - set_txt.get_height() // 2))

    else:
        # EKRAN POSTAVKI (SETTINGS)
        sub_s = font_sub_logo.render("POSTAVKE / SETTINGS", True, (0, 230, 255))
        surf.blit(sub_s, (cx - sub_s.get_width() // 2, cy_logo + 34))

        # Gumb za ZVUČNE EFEKTE (ON / OFF)
        sfx_rect = get_sfx_toggle_rect()
        sfx_bg = (22, 95, 45) if sfx_enabled else (75, 22, 32)
        sfx_border = (60, 255, 110) if sfx_enabled else (255, 70, 85)
        sfx_state_str = "ON (UKLJUČENO)" if sfx_enabled else "OFF (ISKLJUČENO)"

        pygame.draw.rect(surf, (12, 8, 16), sfx_rect.move(0, 5), border_radius=14)
        pygame.draw.rect(surf, sfx_bg, sfx_rect, border_radius=14)
        pygame.draw.rect(surf, sfx_border, sfx_rect, 3, border_radius=14)

        sfx_txt = font_sub_logo.render(f"ZVUČNI EFEKTI: {sfx_state_str}", True, (255, 255, 255))
        surf.blit(sfx_txt, (sfx_rect.centerx - sfx_txt.get_width() // 2, sfx_rect.centery - sfx_txt.get_height() // 2))

        # Gumb za VIBRACIJU (ON / OFF)
        vibe_rect = get_vibe_toggle_rect()
        vibe_bg = (22, 95, 45) if vibe_enabled else (75, 22, 32)
        vibe_border = (60, 255, 110) if vibe_enabled else (255, 70, 85)
        vibe_state_str = "ON (UKLJUČENO)" if vibe_enabled else "OFF (ISKLJUČENO)"

        pygame.draw.rect(surf, (12, 8, 16), vibe_rect.move(0, 5), border_radius=14)
        pygame.draw.rect(surf, vibe_bg, vibe_rect, border_radius=14)
        pygame.draw.rect(surf, vibe_border, vibe_rect, 3, border_radius=14)

        vibe_txt = font_sub_logo.render(f"VIBRACIJA: {vibe_state_str}", True, (255, 255, 255))
        surf.blit(vibe_txt, (vibe_rect.centerx - vibe_txt.get_width() // 2, vibe_rect.centery - vibe_txt.get_height() // 2))

        # Gumb NAZAD (BACK)
        back_rect = get_back_button_rect()
        pygame.draw.rect(surf, (35, 10, 22), back_rect.move(0, 5), border_radius=14)
        pygame.draw.rect(surf, (210, 35, 80), back_rect, border_radius=14)
        pygame.draw.rect(surf, (255, 215, 90), back_rect, 2, border_radius=14)

        back_txt = font_sub_logo.render("NAZAD / BACK", True, (255, 255, 255))
        surf.blit(back_txt, (back_rect.centerx - back_txt.get_width() // 2, back_rect.centery - back_txt.get_height() // 2))

running = True

# ==================== GLAVNA PETLJA IGRE ====================
while running:
    current_time_ms = pygame.time.get_ticks()

    dt_sec = clock.get_time() / 1000.0
    dt60 = min(dt_sec * 60.0, 3.0)
    if dt60 <= 0.0:
        dt60 = 1.0

    cycle_val = math.sin(current_time_ms * 0.00010)
    day_blend = 0.5 + 0.5 * cycle_val
    is_night = day_blend < 0.35
    is_twilight = 0.35 <= day_blend <= 0.65

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "START_MENU":
                if not settings_open:
                    if get_start_button_rect().inflate(20, 20).collidepoint(event.pos):
                        game_state = "PLAYING"
                        is_user_touching = False
                        last_click_time = 0
                        target_x, target_y = scorpion.segments[0].x, scorpion.segments[0].y
                        play_snd(snd_evolve)
                        haptic(180, 255)
                        flash_alpha = 180
                        flash_color = (255, 40, 95)
                        add_shake(14)
                    elif get_settings_button_rect().inflate(16, 16).collidepoint(event.pos):
                        settings_open = True
                        play_snd(snd_catch)
                        haptic(40, 150)
                else:
                    if get_sfx_toggle_rect().inflate(16, 16).collidepoint(event.pos):
                        sfx_enabled = not sfx_enabled
                        audio_enabled = sfx_enabled and _audio_hw_ok
                        if sfx_enabled:
                            play_snd(snd_dna)
                        haptic(40, 140)
                    elif get_vibe_toggle_rect().inflate(16, 16).collidepoint(event.pos):
                        vibe_enabled = not vibe_enabled
                        vibrate_fn = _saved_vibrate_fn if vibe_enabled else None
                        play_snd(snd_catch)
                        if vibe_enabled:
                            haptic(90, 220)
                    elif get_back_button_rect().inflate(16, 16).collidepoint(event.pos):
                        settings_open = False
                        play_snd(snd_catch)
                        haptic(40, 140)
            else:
                is_user_touching = True
                scorpion.ambush_timer = 0
                if scorpion.is_burrowed:
                    scorpion.unburrow()

                if current_time_ms - last_click_time < DOUBLE_CLICK_THRESH:
                    scorpion.trigger_slam(ants)

                last_click_time = current_time_ms
                target_x = clamp_x(event.pos[0])
                target_y = clamp_y(event.pos[1])

        elif event.type == pygame.MOUSEMOTION:
            if game_state == "PLAYING" and is_user_touching:
                target_x = clamp_x(event.pos[0])
                target_y = clamp_y(event.pos[1])
                scorpion.ambush_timer = 0

        elif event.type == pygame.MOUSEBUTTONUP:
            is_user_touching = False

    # ==================== AŽURIRANJE LOGIKE ====================
    if game_state == "START_MENU":
        # U pozadini početnog ekrana mravi već živo rade i skupljaju hranu
        for ant in ants:
            ant.update(-9999, -9999, True, ants)
        scorpion.pulse_phase = (scorpion.pulse_phase + 0.25) % (scorpion.num_segments + 6)
        scorpion.breath_clock += 0.025
    else:
        if is_user_touching:
            m_pos = pygame.mouse.get_pos()
            target_x = clamp_x(m_pos[0])
            target_y = clamp_y(m_pos[1])
            scorpion.ambush_timer = 0

        head = scorpion.segments[0]

        surv_dna = []
        for d in dna_pickups:
            if d.update():
                if math.hypot(head.x - d.x, head.y - d.y) < 46:
                    dna_collected = min(100, dna_collected + 6)
                    play_snd(snd_dna)
                    haptic(50, 150)
                    emit_particles(d.x, d.y, (40, 255, 90), count=16)
                else:
                    surv_dna.append(d)
        dna_pickups = surv_dna

        if boss_schedule_idx < len(boss_schedule):
            req_lvl = boss_schedule[boss_schedule_idx]
            if scorpion.evo_level >= req_lvl and not active_boss:
                door_open_progress = 1.0
                play_snd(snd_door)
                door_center_x = (MIN_X + MAX_X) // 2

                active_boss = CyberBossScorpion(door_center_x, MIN_Y - 50, species_idx=boss_schedule_idx)
                boss_schedule_idx += 1

        if door_open_progress > 0:
            door_open_progress = max(0.0, door_open_progress - 0.015)

        desired_ant_count = 8
        while len(ants) < desired_ant_count:
            ants.append(Ant(force_gold=False))

        should_hunt = scorpion.auto_hunting and (scorpion.ambush_timer <= 0) and not scorpion.is_burrowed

        if not is_user_touching and not scorpion.is_feasting:
            if active_boss and active_boss.state == "active" and should_hunt:
                target_x, target_y = active_boss.x, active_boss.y
            elif should_hunt and ants:
                closest_ant = min(ants, key=lambda b: math.hypot(head.x - b.x, head.y - b.y))
                target_x, target_y = closest_ant.x, closest_ant.y
            elif not is_user_touching:
                target_x, target_y = head.x, head.y

        if active_boss:
            active_boss.update(head.x, head.y, ants, scorpion)
            d_boss_head = math.hypot(head.x - active_boss.x, head.y - active_boss.y)
            if d_boss_head < (52 * active_boss.scale) and not scorpion.is_feasting and active_boss.state == "active":
                active_boss.take_stinger_hit(head.x, head.y)

        surv_proj = []
        for pr in boss_projectiles:
            pr[0] += pr[2]; pr[1] += pr[3]; pr[4] -= 1
            d_p = math.hypot(head.x - pr[0], head.y - pr[1])
            if d_p < 32:
                scorpion.take_damage(16.0)
                scorpion.hunger = max(0.0, scorpion.hunger - 100.0)
                spill_blood(pr[0], pr[1], (45, 255, 80), count=8)
                continue
            if pr[4] > 0 and (MIN_X < pr[0] < MAX_X) and (MIN_Y < pr[1] < MAX_Y):
                surv_proj.append(pr)
        boss_projectiles = surv_proj

        for ant in list(ants):
            ant.update(head.x, head.y, scorpion.is_burrowed, ants)
            dist = math.hypot(head.x - ant.x, head.y - ant.y)
            can_eat = is_user_touching or scorpion.auto_hunting
            if dist < 45 and not scorpion.is_feasting and can_eat and not scorpion.is_burrowed:
                if random.random() < 0.15 or ant.is_gold:
                    dna_pickups.append(DNAPickup(ant.x, ant.y))

                scorpion.trigger_feast(ant.x, ant.y, ant.blood_col, ant.is_gold)
                ant.respawn()

        scorpion.update(target_x, target_y, is_user_touching, ants, dt60)

    # ==================== ISCRTAVANJE ====================
    world_surf.blit(terrain_surf, (0, 0))

    if is_night:
        world_surf.blit(night_overlay_night, (0, 0))
    elif is_twilight:
        world_surf.blit(night_overlay_twilight, (0, 0))

    surv_phero = []
    for pd in pheromone_dots:
        if pd.update():
            pd.draw(world_surf)
            surv_phero.append(pd)
    pheromone_dots = surv_phero

    for fc in food_clusters:
        fc.draw(world_surf)

    for h in anthills:
        h.draw(world_surf)

    pygame.draw.rect(world_surf, NEON_PINK_BORDER, (MIN_X, MIN_Y, MAX_X - MIN_X, MAX_Y - MIN_Y), 3, border_radius=6)
    pygame.draw.rect(world_surf, NEON_PINK_GLOW, (MIN_X - 1, MIN_Y - 1, MAX_X - MIN_X + 2, MAX_Y - MIN_Y + 2), 1, border_radius=7)

    door_w = 170
    door_x = (MIN_X + MAX_X) // 2 - door_w // 2
    door_shift = int((door_w // 2) * door_open_progress)
    pygame.draw.line(world_surf, (0, 240, 255), (door_x, MIN_Y), (door_x + door_w // 2 - door_shift, MIN_Y), 5)
    pygame.draw.line(world_surf, (0, 240, 255), (door_x + door_w // 2 + door_shift, MIN_Y), (door_x + door_w, MIN_Y), 5)

    surv_gc = []
    for gc in ground_cracks:
        if gc.update():
            gc.draw(world_surf)
            surv_gc.append(gc)
    ground_cracks = surv_gc

    surv_molten = []
    for mf in molten_footprints:
        if mf.update():
            mf.draw(world_surf)
            surv_molten.append(mf)
    molten_footprints = surv_molten

    surv_foot = []
    for fp in stained_footprints:
        if fp.update():
            fp.draw(world_surf)
            surv_foot.append(fp)
    stained_footprints = surv_foot

    surv_drops = []
    for drop in blood_drops:
        if drop.update():
            drop.draw(world_surf)
            surv_drops.append(drop)
    blood_drops = surv_drops

    surv_waves = []
    for w in shockwaves:
        w[2] += 5
        if w[2] < w[3]:
            pygame.draw.circle(world_surf, w[4], (int(w[0]), int(w[1])), int(w[2]), 3)
            surv_waves.append(w)
    shockwaves = surv_waves

    for d in dna_pickups:
        d.draw(world_surf)

    render_queue = []
    for ant in ants:
        render_queue.append((ant.y, ant))
    if active_boss:
        render_queue.append((active_boss.y, active_boss))
    render_queue.append((scorpion.segments[0].y, scorpion))

    render_queue.sort(key=lambda item: item[0])
    for _, entity in render_queue:
        entity.draw(world_surf)

    for pr in boss_projectiles:
        pygame.draw.circle(world_surf, (45, 255, 80), (int(pr[0]), int(pr[1])), 6)

    surv_p = []
    for p in particles:
        p[0] += p[2]; p[1] += p[3]
        p[2] *= 0.90; p[3] *= 0.90
        p[4] -= 1
        if p[4] > 0:
            sz = max(1, int(3.5 * (p[4] / p[5])))
            px = clamp_x(p[0])
            py = clamp_y(p[1])
            pygame.draw.circle(world_surf, p[6], (int(px), int(py)), sz)
            surv_p.append(p)
    particles = surv_p[-60:]

    if screen_shake > 0.5:
        shake_mag = min(screen_shake, 12)
        sx = random.randint(-int(shake_mag), int(shake_mag))
        sy = random.randint(-int(shake_mag), int(shake_mag))
        screen_shake *= 0.85
    else:
        sx = 0
        sy = 0
        screen_shake = 0

    screen.fill((0, 0, 0))
    screen.blit(world_surf, (sx, sy))

    if flash_alpha > 0:
        flash_surf.fill(flash_color)
        flash_surf.set_alpha(int(flash_alpha))
        screen.blit(flash_surf, (0, 0))
        flash_alpha = max(0, flash_alpha - 12)

    # ==================== UI SUČELJE ILI START MENU ====================
    if game_state == "START_MENU":
        draw_start_menu(screen, current_time_ms)
    else:
        pygame.draw.rect(screen, (10, 8, 14), (0, 0, WIDTH, HUD_BAR_HEIGHT))
        pygame.draw.line(screen, (60, 42, 35), (0, HUD_BAR_HEIGHT), (WIDTH, HUD_BAR_HEIGHT), 3)

        lvl_col = (255, 140, 20) if scorpion.is_magma else ((255, 30, 60) if scorpion.is_overdrive else (255, 255, 255))
        prefix = "MAGMA OVERLOAD" if scorpion.is_magma else ("OVERDRIVE" if scorpion.is_overdrive else "EVO")
        title_surf = font_title.render(f"{prefix} [LVL {scorpion.evo_level}/100 | XP {scorpion.xp}%] : {SCORPION_NAME}", True, lvl_col)
        screen.blit(title_surf, (SAFE_PAD_X, 8))

        bar_x, bar_hp_y = SAFE_PAD_X, 36
        bar_w, bar_h = 240, 15
        hp_pct = max(0.0, scorpion.hp / scorpion.max_hp)

        pygame.draw.rect(screen, (40, 12, 16), (bar_x, bar_hp_y, bar_w, bar_h), border_radius=3)
        curr_hp_w = int(bar_w * hp_pct)
        if curr_hp_w > 0:
            pygame.draw.rect(screen, (255, 35, 60), (bar_x, bar_hp_y, curr_hp_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (190, 190, 210), (bar_x, bar_hp_y, bar_w, bar_h), 1, border_radius=3)

        hp_info = font_hud.render(f"HP: {int(scorpion.hp)}/100", True, (240, 240, 255))
        screen.blit(hp_info, (bar_x + bar_w + 10, bar_hp_y - 1))

        bar_hung_y = 56
        hunger_pct = scorpion.hunger / scorpion.max_hunger

        pygame.draw.rect(screen, (35, 20, 12), (bar_x, bar_hung_y, bar_w, bar_h), border_radius=3)
        curr_hung_w = int(bar_w * hunger_pct)
        if curr_hung_w > 0:
            hung_col = (255, 120, 20) if scorpion.is_overdrive else (255, 175, 40)
            pygame.draw.rect(screen, hung_col, (bar_x, bar_hung_y, curr_hung_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (190, 190, 210), (bar_x, bar_hung_y, bar_w, bar_h), 1, border_radius=3)

        status_txt = "UKOPAN" if scorpion.is_burrowed else ("HUNT" if scorpion.auto_hunting else ("OD" if scorpion.is_overdrive else "AKTIVAN"))
        hung_info = font_hud.render(f"GLAD: {int(hunger_pct * 100)}% [{status_txt}]", True, (240, 240, 255))
        screen.blit(hung_info, (bar_x + bar_w + 10, bar_hung_y - 1))

        bar_heat_y = 76
        heat_pct = min(1.0, scorpion.heat / scorpion.max_heat)
        pygame.draw.rect(screen, (32, 10, 8), (bar_x, bar_heat_y, bar_w, bar_h), border_radius=3)
        curr_heat_w = int(bar_w * heat_pct)
        if curr_heat_w > 0:
            heat_c = (255, 220, 60) if scorpion.is_magma else (255, 90, 20)
            pygame.draw.rect(screen, heat_c, (bar_x, bar_heat_y, curr_heat_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (255, 140, 40), (bar_x, bar_heat_y, bar_w, bar_h), 1, border_radius=3)

        heat_title = "MELTDOWN!" if scorpion.is_magma else f"HEAT: {int(heat_pct * 100)}%"
        heat_info = font_bold_hud.render(heat_title, True, (255, 160, 40) if not scorpion.is_magma else (255, 240, 80))
        screen.blit(heat_info, (bar_x + bar_w + 10, bar_heat_y - 2))

        dna_bar_y = 96
        pygame.draw.rect(screen, (12, 34, 18), (bar_x, dna_bar_y, bar_w, 14), border_radius=3)
        curr_dna_w = int(bar_w * (dna_collected / 100.0))
        if curr_dna_w > 0:
            pygame.draw.rect(screen, (40, 255, 90), (bar_x, dna_bar_y, curr_dna_w, 14), border_radius=3)

        dna_border_c = (255, 40, 40) if scorpion.dna_fail_timer > 0 else (100, 220, 140)
        pygame.draw.rect(screen, dna_border_c, (bar_x, dna_bar_y, bar_w, 14), 2 if scorpion.dna_fail_timer > 0 else 1, border_radius=3)

        slams_available = dna_collected // 15
        slam_txt = f"SLAM: {slams_available}/6 ({dna_collected} DNA)"
        dna_txt_surf = font_bold_hud.render(slam_txt, True, (255, 70, 70) if scorpion.dna_fail_timer > 0 else (40, 255, 90))
        screen.blit(dna_txt_surf, (bar_x + bar_w + 10, dna_bar_y - 2))

        if active_boss:
            boss_txt = f"OPASNOST: {active_boss.spec['name']} (x{active_boss.growth_factor:.3f})"
            boss_s = font_bold_hud.render(boss_txt, True, active_boss.spec['c_main'])
            screen.blit(boss_s, (SAFE_PAD_X, 118))
        else:
            active_h_count = sum(1 for h in anthills if h.active)
            total_food_stored = sum(h.food_stored for h in anthills)
            h_txt = f"MRAVINJACI: {active_h_count}/8 AKTIVNO | ZALIHE KOLONIJE: {total_food_stored}"
            h_s = font_hud.render(h_txt, True, (180, 200, 220))
            screen.blit(h_s, (SAFE_PAD_X, 118))

        phase_name = "NOĆ" if is_night else ("DAN" if day_blend > 0.65 else "SUMRAK")
        cycle_col = (140, 200, 255) if is_night else ((255, 220, 80) if day_blend > 0.65 else (255, 140, 180))
        cycle_surf = font_hud.render(f"CIKLUS: {phase_name}", True, cycle_col)
        screen.blit(cycle_surf, (WIDTH - SAFE_PAD_X - cycle_surf.get_width(), 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
