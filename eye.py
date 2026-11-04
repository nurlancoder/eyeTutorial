"""
Cosmic Eye Animation - Professional ASCII Art Experience
Powered by Nurlan Mammadli
GitHub: https://github.com/nurlancoder

A generative ASCII art animation that brings a cosmic eye to life:
- Eye opens and blinks with realistic eyelids
- Pupil transforms into a portal to space
- 3,200+ twinkling stars fly toward the camera
- Shooting stars and comet with glowing trails
- Heart-shaped nebula morphs from cosmic clouds
- Advanced bloom, vignette, and color effects
"""

import math as m
import random
import time

import numpy as np

# ============ DISPLAY SETTINGS ============
FONT_SIZE = 8
FRAME_RATE = 30
SUPER_SAMPLE = 2
ASPECT_RATIO = 1.40
MAX_ROW_COUNT = 30
TKINTER_FRAME_BUDGET_MS = 13.0

# ============ TIMELINE CONFIGURATION ============
TIME_EYE_OPEN_START = 0.9
TIME_EYE_OPEN_DURATION = 2.4
TIME_BLINK = 4.0
TIME_ZOOM_START = 5.4
TIME_ZOOM_DURATION = 28.0
ZOOM_FINAL_LEVEL = 14.0
TIME_SPACE_SCENE = TIME_ZOOM_START + TIME_ZOOM_DURATION
TIME_HEART_MORPH_START = TIME_ZOOM_START + 3.5
TIME_HEART_MORPH_DURATION = 26.0

# ============ EYE GEOMETRY ============
EYE_HALF_WIDTH = 0.78
EYELID_UPPER_HEIGHT, EYELID_LOWER_HEIGHT = 0.30, 0.20
IRIS_RADIUS = 0.27
PUPIL_BASE_RADIUS = 0.098
STAR_SPREAD_BASE = 0.085
STAR_SPREAD_MAXIMUM = 1.5

# ============ ASCII CHARACTER RAMP ============
# Characters ordered from dark to bright
BRIGHTNESS_RAMP = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
RAMP_MAX_INDEX = len(BRIGHTNESS_RAMP) - 1
CHARACTER_INDEX_MAP = {c: i for i, c in enumerate(BRIGHTNESS_RAMP)}
COLOR_QUANTIZATION_LEVELS = 24

# ============ RANDOM GENERATORS ============
main_random_generator = np.random.RandomState(5)
physics_random_generator = random.Random(9)


def smooth_step(min_val, max_val, value):
    """Smooth interpolation from min to max using smoothstep curve."""
    t = np.clip((value - min_val) / (max_val - min_val), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def ease_curve(t):
    """Scalar smoothstep easing function (ease in, ease out)."""
    t = min(max(t, 0.0), 1.0)
    return t * t * (3 - 2 * t)


def zoom_progress(t):
    """Calculate zoom progress (0-1) based on timeline."""
    return ease_curve((t - TIME_ZOOM_START) / TIME_ZOOM_DURATION)


def linear_interpolate(a, b, factor):
    """Linear interpolation between two values."""
    return a + (b - a) * factor


def upscale_2d_smooth(base_grid, target_size):
    """Smoothly upscale a small random 2D grid to target size."""
    grid_size = base_grid.shape[0]
    indices = np.arange(target_size) * grid_size / target_size
    idx0 = indices.astype(np.int64) % grid_size
    idx1 = (idx0 + 1) % grid_size
    frac = indices - np.floor(indices)
    frac = (frac * frac * (3 - 2 * frac)).astype(np.float32)
    temp = base_grid[:, idx0] * (1 - frac) + base_grid[:, idx1] * frac
    return temp[idx0, :] * (1 - frac)[:, None] + temp[idx1, :] * frac[:, None]


def normalize_noise(noise_array, k=4.0):
    """Normalize noise into 0-1 range with standard deviation scaling."""
    return np.clip(0.5 + (noise_array - noise_array.mean()) / (noise_array.std() * k + 1e-9), 0, 1).astype(np.float32)


def generate_fractal_texture(size, grid_levels):
    """Generate multi-layer fractal 2D texture from random grids."""
    output = np.zeros((size, size), np.float32)
    amplitude = 1.0
    for grid in grid_levels:
        output += amplitude * upscale_2d_smooth(main_random_generator.rand(grid, grid).astype(np.float32), size)
        amplitude *= 0.55
    return normalize_noise(output)


def generate_1d_noise(length, grid_size):
    """Generate smooth 1D noise from random grid."""
    base = main_random_generator.rand(grid_size)
    indices = np.arange(length) * grid_size / length
    idx0 = indices.astype(np.int64) % grid_size
    idx1 = (idx0 + 1) % grid_size
    frac = indices - np.floor(indices)
    frac = frac * frac * (3 - 2 * frac)
    return (base[idx0] * (1 - frac) + base[idx1] * frac).astype(np.float32)


def bilinear_sample(texture, u, v):
    """Bilinear sampling from texture at given UV coordinates."""
    tex_size = texture.shape[0]
    u0 = np.floor(u)
    v0 = np.floor(v)
    frac_u = u - u0
    frac_v = v - v0
    i0 = u0.astype(np.int32) % tex_size
    j0 = v0.astype(np.int32) % tex_size
    i1 = (i0 + 1) % tex_size
    j1 = (j0 + 1) % tex_size
    return ((texture[j0, i0] * (1 - frac_u) + texture[j0, i1] * frac_u) * (1 - frac_v)
            + (texture[j1, i0] * (1 - frac_u) + texture[j1, i1] * frac_u) * frac_v)


print("Initializing cosmic textures...")
TEXTURE_SKIN = generate_fractal_texture(1024, (6, 20, 64, 200))
TEXTURE_GRAIN = generate_fractal_texture(1024, (8, 24, 64, 160))
TEXTURE_WHITE_NOISE = main_random_generator.rand(512, 512).astype(np.float32)
_base_vein_texture = generate_fractal_texture(512, (5, 12, 30))
TEXTURE_VEIN = 1 - np.abs(2 * _base_vein_texture - 1)
_base_vein_texture2 = generate_fractal_texture(512, (3, 7, 16))
TEXTURE_VEIN2 = 1 - np.abs(2 * _base_vein_texture2 - 1)

# ============ IRIS TEXTURE ARRAYS ============
ANGULAR_NOISE_SIZE = 4096
IRIS_FIBER_1 = normalize_noise(0.5 * generate_1d_noise(ANGULAR_NOISE_SIZE, 900) + 0.3 * generate_1d_noise(ANGULAR_NOISE_SIZE, 300) + 0.2 * generate_1d_noise(ANGULAR_NOISE_SIZE, 120), 3.0)
IRIS_FIBER_2 = normalize_noise(0.5 * generate_1d_noise(ANGULAR_NOISE_SIZE, 700) + 0.3 * generate_1d_noise(ANGULAR_NOISE_SIZE, 200) + 0.2 * generate_1d_noise(ANGULAR_NOISE_SIZE, 80), 3.0)
IRIS_WOBBLE = normalize_noise(generate_1d_noise(ANGULAR_NOISE_SIZE, 13), 3.0)
IRIS_CRYPT = normalize_noise(generate_1d_noise(ANGULAR_NOISE_SIZE, 48), 3.0)

# ============ STAR FIELD ============
STAR_COUNT = 3200
STAR_POS_X = main_random_generator.uniform(-1, 1, STAR_COUNT).astype(np.float32)
STAR_POS_Y = main_random_generator.uniform(-1, 1, STAR_COUNT).astype(np.float32)
STAR_DEPTH = main_random_generator.uniform(0.06, 1.0, STAR_COUNT).astype(np.float32)
STAR_BRIGHTNESS = (0.10 + 0.90 * main_random_generator.rand(STAR_COUNT) ** 3.5).astype(np.float32)
_star_temp = main_random_generator.rand(STAR_COUNT, 1).astype(np.float32)
STAR_COLOR = linear_interpolate(np.array([0.65, 0.85, 1.0], np.float32), np.array([1.0, 0.85, 0.60], np.float32), _star_temp ** 1.5)
STAR_TWINKLE_PHASE = main_random_generator.uniform(0, 6.28, STAR_COUNT).astype(np.float32)
STAR_TWINKLE_FREQ = main_random_generator.uniform(1.0, 3.5, STAR_COUNT).astype(np.float32)

# ============ GAZE KEYFRAMES ============
GAZE_KEYFRAMES = [(0.0, 0.0, 0.0)]
_time_cursor = 1.7
_gaze_random = random.Random(4)
while _time_cursor < 40:
    GAZE_KEYFRAMES.append((_time_cursor, _gaze_random.uniform(-0.045, 0.045), _gaze_random.uniform(-0.022, 0.02)))
    _time_cursor += _gaze_random.uniform(0.9, 2.4)

# ============ EYELASH ARRAYS ============
_lash_random = random.Random(21)
UPPER_LASHES = []
UPPER_LASH_COUNT = 44
for i in range(UPPER_LASH_COUNT):
    UPPER_LASHES.append((-0.92 + 1.84 * i / (UPPER_LASH_COUNT - 1), _lash_random.uniform(0.92, 1.08), 0.0, 1.0))
LOWER_LASHES = []
LOWER_LASH_COUNT = 20
for i in range(LOWER_LASH_COUNT):
    LOWER_LASHES.append((-0.70 + 1.40 * i / (LOWER_LASH_COUNT - 1), _lash_random.uniform(0.90, 1.10), 0.0, 1.0))

# ============ GLOBAL STATE ============
global_state = {}

# ============ SHOOTING STARS ============
shooting_stars = []
world_state = {"last_time": 0.0, "next_shooting_star": 1.0e9, "comet_active": False}


class ShootingStar:
    """Represents a shooting star or comet with position, velocity, and visual properties."""
    def __init__(self, x, y, vx, vy, lifetime, tail_length, color, soft=False):
        self.x, self.y, self.vx, self.vy = x, y, vx, vy
        self.lifetime, self.tail_length, self.color, self.soft = lifetime, tail_length, color, soft
        self.age = 0.0


# ============ GEOMETRY COORDINATES ============
cell_width = 0
cell_height = 0
row_count = 0
col_count = 0
canvas_width = 0
canvas_height = 0
grid_width = 0
grid_height = 0
coord_x = None
coord_y = None
radius_subpixel = None
cell_center_x = None
cell_center_y = None
radius_cell = None
hash_cell = None


def initialize_display(cw, ch, rows):
    """Initialize display size, coordinate grids, and geometry."""
    global cell_width, cell_height, row_count, col_count
    global canvas_width, canvas_height, grid_width, grid_height
    global coord_x, coord_y, radius_subpixel
    global cell_center_x, cell_center_y, radius_cell, hash_cell

    cell_width, cell_height = cw, ch
    row_count = rows
    col_count = int(rows * ch * ASPECT_RATIO / cw) // 2 * 2
    row_count = row_count // 2 * 2
    canvas_width, canvas_height = col_count * cw, row_count * ch
    grid_width, grid_height = col_count * SUPER_SAMPLE, row_count * SUPER_SAMPLE

    xs = (np.arange(grid_width, dtype=np.float32) + 0.5) * (cw / SUPER_SAMPLE)
    ys = (np.arange(grid_height, dtype=np.float32) + 0.5) * (ch / SUPER_SAMPLE)
    coord_x = (((xs - canvas_width / 2) / canvas_height)[None, :] * np.ones((grid_height, 1), np.float32)).astype(np.float32)
    coord_y = (((ys - canvas_height / 2) / canvas_height)[:, None] * np.ones((1, grid_width), np.float32)).astype(np.float32)
    radius_subpixel = np.sqrt(coord_x * coord_x + coord_y * coord_y)

    cx = (np.arange(col_count, dtype=np.float32) + 0.5) * cw
    cy = (np.arange(row_count, dtype=np.float32) + 0.5) * ch
    cell_center_x = (((cx - canvas_width / 2) / canvas_height)[None, :] * np.ones((row_count, 1), np.float32)).astype(np.float32)
    cell_center_y = (((cy - canvas_height / 2) / canvas_height)[:, None] * np.ones((1, col_count), np.float32)).astype(np.float32)
    radius_cell = np.sqrt(cell_center_x * cell_center_x + cell_center_y * cell_center_y)

    rr, cc = np.mgrid[0:row_count, 0:col_count]
    hash_cell = (((rr * 73856093) ^ (cc * 19349663) ^ 0x5bd1e995) % 1009 / 1009.0).astype(np.float32)

    reset_animation()


def blink_curve(t, blink_time=TIME_BLINK):
    """Blink animation curve (0 = open, 1 = closed)."""
    delta = t - blink_time
    if delta < 0 or delta > 0.36:
        return 0.0
    if delta < 0.09:
        return ease_curve(delta / 0.09)
    if delta < 0.12:
        return 1.0
    return 1 - ease_curve((delta - 0.12) / 0.24)


def eyelid_openness(t):
    """Calculate eyelid openness over time (0 = closed, 1 = open)."""
    k = ease_curve((t - TIME_EYE_OPEN_START) / TIME_EYE_OPEN_DURATION)
    k = k * (1 + 0.035 * m.sin(m.pi * k))
    return min(1.0, k) * (1 - 0.985 * blink_curve(t))


def gaze_direction(t, progress):
    """Compute current gaze direction (gx, gy) based on keyframes."""
    prev_gaze = (0.0, 0.0)
    curr_gaze = (0.0, 0.0)
    keyframe_time = 0.0
    for (time_key, gx_key, gy_key) in GAZE_KEYFRAMES:
        if time_key <= t:
            prev_gaze = curr_gaze
            curr_gaze = (gx_key, gy_key)
            keyframe_time = time_key
        else:
            break
    k = ease_curve((t - keyframe_time) / 0.09)
    gx = prev_gaze[0] + (curr_gaze[0] - prev_gaze[0]) * k
    gy = prev_gaze[1] + (curr_gaze[1] - prev_gaze[1]) * k
    gx += 0.003 * m.sin(t * 1.3)
    gy += 0.002 * m.sin(t * 1.1 + 1)
    amplitude = 1 - ease_curve((t - TIME_ZOOM_START) / 2.5)
    gy -= 0.03 * blink_curve(t)
    return gx * amplitude, gy * amplitude


def eyelid_edge_position(u_position, openness):
    """Calculate upper/lower eyelid edge positions at given x coordinate."""
    s = u_position / EYE_HALF_WIDTH
    width_upper = 0.88 if s < -0.12 else 1.12
    curve_upper = max(0.0, 1 - ((s + 0.12) / width_upper) ** 2) ** 0.8
    curve_lower = max(0.0, 1 - (s - 0.08) ** 2) ** 0.9
    v_closed = 0.03 * curve_lower
    v_lower = v_closed + (EYELID_LOWER_HEIGHT * curve_lower - v_closed) * (0.35 + 0.65 * openness)
    v_upper = v_lower + (-EYELID_UPPER_HEIGHT * curve_upper - v_lower) * openness
    return v_upper, v_lower, curve_upper, curve_lower


def heart_nebula_renderer(xs, ys, size, heart_morph, t):
    """Render the heart-shaped nebula cloud in space."""
    hx = xs / size
    hy = -ys / size
    noise_c = bilinear_sample(TEXTURE_GRAIN, hx * 16 + 400, hy * 16 + 100)
    noise_d = bilinear_sample(TEXTURE_GRAIN, hx * 16 + 90, hy * 16 + 530)
    noise_a = bilinear_sample(TEXTURE_GRAIN, hx * 42 + 300, hy * 42 + 700 + t * 0.8)
    noise_b = bilinear_sample(TEXTURE_GRAIN, hx * 110 + 80, hy * 110 + 200)
    wobble = 1 - 0.65 * heart_morph
    hx_warped = hx + wobble * 0.40 * (noise_c - 0.5) + 0.05 * (noise_a - 0.5)
    hy_warped = hy + wobble * 0.40 * (noise_d - 0.5) + 0.05 * (noise_a - 0.5)
    dist_circle = np.sqrt(hx_warped * hx_warped + hy_warped * hy_warped) / 0.80 - 1.0
    hy_heart = hy_warped + 0.12
    heart_equation = (hx_warped * hx_warped + hy_heart * hy_heart - 1.0) ** 3 - hx_warped * hx_warped * hy_heart ** 3
    dist_heart = 0.5 * np.cbrt(heart_equation)
    dist = dist_circle * (1 - heart_morph) + dist_heart * heart_morph
    inside = np.clip(-dist / (0.80 - 0.35 * heart_morph), 0, 1)
    k = 3.0 + 2.5 * heart_morph
    body = np.where(dist < 0, 0.50 + 0.50 * np.sqrt(inside), np.exp(-np.clip(dist, 0, 10) * k) * 0.50)
    texture = 1 + (0.62 + 0.80 * noise_b - 1) * 0.8
    color_deep = np.array([0.85, 0.10, 0.35], np.float32)
    color_light = np.array([1.0, 0.55, 0.75], np.float32)
    heart_color = linear_interpolate(color_deep, color_light, (inside ** 0.8)[..., None])
    color = (body * texture)[..., None] * heart_color

    halo = np.exp(-np.clip(dist, 0, 10) * 1.6) * 0.25 * (0.5 + noise_a) * (dist > 0)
    color = color + halo[..., None] * np.array([0.75, 0.08, 0.25], np.float32)

    rim = np.exp(-((dist + 0.04) / 0.14) ** 2)
    ridge = np.clip((bilinear_sample(TEXTURE_VEIN, hx_warped * 120 + 50, hy_warped * 120 + 300 + t * 0.6) - 0.86) * 7, 0, 1)
    red_accent = np.array([0.90, 0.12, 0.30], np.float32)
    color = color + (rim * (0.25 + 0.95 * ridge) * (0.5 + noise_a))[..., None] * red_accent
    color = color + (ridge * np.clip(-dist, 0, 1) * 0.30)[..., None] * red_accent
    return color.astype(np.float32)


def eye_scene_renderer(t, zoom, openness, gaze_x, gaze_y, pupil_radius, space_image):
    """Render the complete eye scene (sclera, iris, pupil, eyelids, skin)."""
    inv_zoom = 1.0 / zoom
    pixel_size = inv_zoom / grid_height
    u = coord_x * inv_zoom
    v = coord_y * inv_zoom
    near_camera = zoom < 3.4
    pupil_motion_x = u - gaze_x
    pupil_motion_y = v - gaze_y
    radius_from_pupil = np.sqrt(pupil_motion_x * pupil_motion_x + pupil_motion_y * pupil_motion_y)
    distance_to_lid = None

    if near_camera:
        s = u / EYE_HALF_WIDTH
        s_clamped = np.clip(s, -1.3, 1.3)
        width_upper = np.where(s_clamped < -0.12, 0.88, 1.12)
        curve_upper = np.clip(1 - ((s_clamped + 0.12) / width_upper) ** 2, 0, 1) ** 0.8
        curve_lower = np.clip(1 - (s_clamped - 0.08) ** 2, 0, 1) ** 0.9
        v_tilted = v + 0.055 * s
        v_closed = 0.03 * curve_lower
        v_lower = v_closed + (EYELID_LOWER_HEIGHT * curve_lower - v_closed) * (0.35 + 0.65 * openness)
        v_upper = v_lower + (-EYELID_UPPER_HEIGHT * curve_upper - v_lower) * openness
        dist_upper = v_tilted - v_upper
        dist_lower = v_lower - v_tilted
        distance_to_lid = np.minimum(dist_upper, dist_lower)
        mask_inside = np.clip(distance_to_lid / (1.6 * pixel_size) + 0.5, 0, 1)[..., None]

    angle_index = (((np.arctan2(pupil_motion_y, pupil_motion_x) / (2 * m.pi)) % 1.0) * ANGULAR_NOISE_SIZE).astype(np.int32) % ANGULAR_NOISE_SIZE
    normalized_radius = np.clip((radius_from_pupil - pupil_radius) / (IRIS_RADIUS - pupil_radius), 0, 1.3)
    radial_bin = normalized_radius * 14
    idx_bin = np.floor(radial_bin).astype(np.int32)
    frac_bin = radial_bin - idx_bin
    fiber_brightness = 0.55 * IRIS_FIBER_1[angle_index] + 0.45 * (IRIS_FIBER_2[(angle_index + idx_bin * 131) % ANGULAR_NOISE_SIZE] * (1 - frac_bin) + IRIS_FIBER_2[(angle_index + (idx_bin + 1) * 131) % ANGULAR_NOISE_SIZE] * frac_bin)
    angle_norm = (np.arctan2(pupil_motion_y, pupil_motion_x) / (2 * m.pi)) % 1.0
    zigzag = np.abs((angle_norm * 34) % 1.0 - 0.5) * 2 - 0.5
    collarette_radius = 0.34 + 0.20 * (IRIS_WOBBLE[angle_index] - 0.5) + 0.035 * zigzag
    mask_morph = smooth_step(-0.10, 0.22, normalized_radius - collarette_radius)[..., None]
    color_amber = np.array([0.85, 0.50, 0.12], np.float32)
    color_rust = np.array([0.45, 0.22, 0.08], np.float32)
    iris_color = linear_interpolate(color_amber, color_rust, mask_morph)
    iris_color = iris_color * (0.45 + 1.05 * fiber_brightness)[..., None]
    iris_color += np.array([0.25, 0.12, 0.0], np.float32) * (np.exp(-((normalized_radius - collarette_radius) / 0.07) ** 2) * (0.2 + fiber_brightness))[..., None]
    crypt_mask = (IRIS_CRYPT[angle_index] > 0.72) * smooth_step(0.65, 0.18, normalized_radius)
    iris_color *= (1 - 0.55 * crypt_mask)[..., None]
    iris_color *= (1 - 0.82 * smooth_step(0.62, 1.0, normalized_radius))[..., None]
    iris_color *= (0.55 + 0.45 * smooth_step(0, 0.07, normalized_radius))[..., None]
    if near_camera:
        iris_color *= (0.30 + 0.70 * smooth_step(0, 0.16, dist_upper))[..., None]

    if near_camera:
        corner_weight = smooth_step(0.40, 0.95, np.abs(s))
        shade_factor = (0.38 + 0.62 * smooth_step(0, 0.22, dist_upper)) * (0.72 + 0.28 * smooth_step(0, 0.10, dist_lower)) * (1 - 0.30 * corner_weight)
        sclera_color = np.array([0.82, 0.84, 0.88], np.float32) * shade_factor[..., None]
        sclera_color = linear_interpolate(sclera_color, np.array([0.90, 0.55, 0.50], np.float32) * shade_factor[..., None], (corner_weight * 0.35)[..., None])
        vein_mask = np.clip((bilinear_sample(TEXTURE_VEIN2, u * 85 + 40, v * 85 + 70) - 0.925) * 14, 0, 1) * (0.25 + 0.75 * corner_weight) * smooth_step(0.12, 0.32, np.abs(pupil_motion_x))
        sclera_color = linear_interpolate(sclera_color, np.array([0.65, 0.18, 0.16], np.float32), (vein_mask * 0.65)[..., None])
        iris_mask = np.clip((IRIS_RADIUS - radius_from_pupil) / (1.6 * pixel_size) + 0.5, 0, 1)[..., None]
        inside_eye = linear_interpolate(sclera_color, iris_color, iris_mask)
    else:
        inside_eye = iris_color

    pupil_screen_radius = pupil_radius * zoom
    vignette_factor = 0.25 + 0.75 * smooth_step(0, 0.30 * pupil_screen_radius, pupil_screen_radius - radius_subpixel)
    pupil_mask = np.clip((pupil_radius - radius_from_pupil) / (1.6 * pixel_size) + 0.5, 0, 1)
    inside_eye = linear_interpolate(inside_eye, space_image * vignette_factor[..., None], pupil_mask[..., None])

    catchlight_fade = max(0.0, min(1.0, 1 - (zoom - 1.6) / 2.4))
    if catchlight_fade > 0:
        dist_reflection = np.sqrt((pupil_motion_x - 0.075) ** 2 + (pupil_motion_y + 0.040) ** 2)
        window1 = np.clip(1 - (dist_reflection - 0.030) / (1.4 * pixel_size + 0.004), 0, 1)
        dist_reflection2 = np.sqrt((pupil_motion_x + 0.045) ** 2 + (pupil_motion_y - 0.050) ** 2)
        window2 = np.clip(1 - (dist_reflection2 - 0.009) / (1.4 * pixel_size + 0.003), 0, 1) * 0.5
        inside_eye = inside_eye + ((window1 + window2) * catchlight_fade)[..., None] * np.array([1.0, 0.98, 0.95], np.float32) * 1.5

    if not near_camera:
        return inside_eye, pupil_mask

    if zoom < 2.6:
        mid_lid = 0.5 * (v_upper + v_lower)
        is_upper = v_tilted < mid_lid
        dist_upper_edge = np.maximum(v_upper - v_tilted, 0)
        dist_lower_edge = np.maximum(v_tilted - v_lower, 0)
        dist_to_edge = np.where(is_upper, dist_upper_edge, dist_lower_edge)
        skin_texture = bilinear_sample(TEXTURE_SKIN, u * 120 + 100, v * 120 + 100)
        base_skin = np.array([0.65, 0.42, 0.30], np.float32)
        skin_color = base_skin * (0.90 + 0.20 * skin_texture)[..., None]
        shade = 0.50 + 0.50 * smooth_step(0, 0.30, dist_to_edge)
        shade *= 1 + 0.10 * np.exp(-((v + 0.20) / 0.09) ** 2)
        crease_position = 0.075 + 0.03 * (1 - openness)
        shade *= 1 - 0.42 * np.exp(-((dist_upper_edge - crease_position) / 0.020) ** 2) * is_upper
        shade *= 1 + 0.08 * np.exp(-((dist_lower_edge - 0.09) / 0.04) ** 2) * (~is_upper)
        skin_color = skin_color * shade[..., None]
        lid_zone = smooth_step(crease_position, crease_position * 0.4, dist_upper_edge) * is_upper
        skin_color = linear_interpolate(skin_color, np.array([0.70, 0.42, 0.32], np.float32) * shade[..., None], (lid_zone * 0.5)[..., None])

        symmetric_blend = np.clip(1 - np.abs(s), 0, 1)
        eyebrow_mask = np.exp(-((v_tilted + 0.42 + 0.10 * s * s) / (0.040 + 0.012 * symmetric_blend)) ** 2)
        eyebrow_hair = 0.55 + 0.9 * bilinear_sample(TEXTURE_WHITE_NOISE, u * 90, v * 30)
        skin_color = linear_interpolate(skin_color, np.array([0.12, 0.08, 0.05], np.float32), np.clip(eyebrow_mask * eyebrow_hair, 0, 0.92)[..., None])

        lid_line = np.exp(-(dist_upper_edge / 0.010) ** 2) * is_upper
        skin_color = linear_interpolate(skin_color, np.array([0.06, 0.04, 0.025], np.float32), np.clip(lid_line * (1.0 - 0.3 * openness) * 0.9, 0, 1)[..., None])
        waterline = smooth_step(0.014, 0.0, dist_lower_edge) * (~is_upper)
        skin_color = linear_interpolate(skin_color, np.array([0.75, 0.35, 0.32], np.float32), (waterline * 0.7)[..., None])
        gloss = np.exp(-((dist_lower_edge - 0.016) / 0.006) ** 2) * (~is_upper) * (0.35 + 0.65 * bilinear_sample(TEXTURE_WHITE_NOISE, u * 60, v * 60))
        skin_color = skin_color + (gloss * 0.55)[..., None] * np.array([1.0, 0.90, 0.80], np.float32) * smooth_step(0.12, 0.5, openness)
        skin_speckle = (bilinear_sample(TEXTURE_WHITE_NOISE, u * 150 + 7, v * 150 + 3) > 0.985) * 0.35 * (0.4 + skin_texture) * smooth_step(0.0, 0.3, dist_to_edge)
        skin_color = skin_color + skin_speckle[..., None] * np.array([1.0, 0.95, 0.85], np.float32)
        final_color = linear_interpolate(skin_color, inside_eye, mask_inside)

        caruncle = np.exp(-(((u + EYE_HALF_WIDTH * 0.90) / 0.045) ** 2 + ((v_tilted - 0.025) / 0.032) ** 2)) * smooth_step(0.1, 0.5, openness)
        final_color = linear_interpolate(final_color, np.array([0.85, 0.45, 0.40], np.float32), (caruncle * 0.85)[..., None])
        return final_color, pupil_mask
    return inside_eye, pupil_mask


def reset_animation():
    """Reset all animation state to initial values."""
    world_state.update(last_time=0.0, next_shooting_star=1.0e9, comet_active=False)
    shooting_stars.clear()
    STAR_DEPTH[:] = main_random_generator.uniform(0.06, 1.0, STAR_COUNT).astype(np.float32)


def update_world_state(t, dt, progress):
    """Update star positions, shooting stars, and comet."""
    velocity_factor = 0.010 + 0.05 * progress + (0.015 if t > TIME_SPACE_SCENE else 0.0)
    STAR_DEPTH[:] -= velocity_factor * dt
    dead_stars = STAR_DEPTH < 0.06
    if dead_stars.any():
        STAR_DEPTH[dead_stars] += 0.94
        count = int(dead_stars.sum())
        STAR_POS_X[dead_stars] = main_random_generator.uniform(-1, 1, count)
        STAR_POS_Y[dead_stars] = main_random_generator.uniform(-1, 1, count)
    if world_state["next_shooting_star"] > 1e8 and t > TIME_SPACE_SCENE - 4.0:
        world_state["next_shooting_star"] = t + 1.0
    if t > world_state["next_shooting_star"]:
        world_state["next_shooting_star"] = t + physics_random_generator.uniform(2.2, 4.5)
        angle = m.radians(physics_random_generator.uniform(18, 62))
        sign = physics_random_generator.choice((-1, 1))
        speed = physics_random_generator.uniform(0.7, 1.2)
        shooting_stars.append(ShootingStar(physics_random_generator.uniform(-0.7, 0.7), physics_random_generator.uniform(-0.45, -0.15),
                              sign * m.cos(angle) * speed, m.sin(angle) * speed,
                              physics_random_generator.uniform(0.9, 1.4), physics_random_generator.uniform(0.14, 0.26),
                              np.array([0.85, 0.92, 1.0], np.float32)))
    if t > TIME_SPACE_SCENE + 1.5 and not world_state["comet_active"]:
        world_state["comet_active"] = True
        shooting_stars.append(ShootingStar(-0.95, -0.28, 0.030, 0.008, 70.0, 0.22,
                              np.array([0.65, 0.82, 1.0], np.float32), soft=True))
    for star in shooting_stars:
        star.age += dt
    shooting_stars[:] = [star for star in shooting_stars if star.age < star.lifetime]


def place_character(char_indices, foreground_colors, row, col, char, color, alpha=1.0):
    """Safely place a character at given cell position with bounds checking."""
    if 0 <= row < row_count and 0 <= col < col_count:
        char_indices[row, col] = CHARACTER_INDEX_MAP[char]
        foreground_colors[row, col] = color * alpha


def render_shooting_star(star, char_indices, foreground_colors, pupil_mask_cell, vignette_cell):
    """Render a shooting star or comet with character trail."""
    head_x = star.x + star.vx * star.age
    head_y = star.y + star.vy * star.age
    speed = m.hypot(star.vx, star.vy)
    dir_x, dir_y = star.vx / speed, star.vy / speed
    fade = m.sin(m.pi * min(1.0, star.age / star.lifetime)) ** 0.7
    if fade < 0.02:
        return
    if abs(dir_y) < 0.38 * abs(dir_x):
        tail_char = "-"
    elif abs(dir_x) < 0.38 * abs(dir_y):
        tail_char = "|"
    elif dir_x * dir_y > 0:
        tail_char = "\\"
    else:
        tail_char = "/"
    tail_length = max(6, int(star.tail_length * canvas_height / (cell_width * 0.8)))
    for k in range(tail_length):
        fraction = k / tail_length
        col = int((canvas_width / 2 + (head_x - dir_x * star.tail_length * fraction) * canvas_height) / cell_width)
        row = int((canvas_height / 2 + (head_y - dir_y * star.tail_length * fraction) * canvas_height) / cell_height)
        brightness = (1 - fraction) ** 1.3 * fade
        if brightness < 0.08 or not (0 <= row < row_count and 0 <= col < col_count) or pupil_mask_cell[row, col] < 0.5:
            continue
        if k == 0:
            char = "@" if not star.soft else "*"
        elif star.soft:
            char = ":" if brightness > 0.35 else "."
        else:
            char = tail_char if brightness > 0.30 else "."
        place_character(char_indices, foreground_colors, row, col, char, star.color, min(1.0, 0.3 + brightness) * vignette_cell[row, col])


def render_stars(char_indices, foreground_colors, luminance, t, star_scale, amount, pupil_mask_cell, vignette_cell, offset_x, offset_y):
    """Render twinkling stars as characters."""
    if amount <= 0.003:
        return
    depth = STAR_DEPTH
    cols = ((canvas_width * 0.5 + (STAR_POS_X * star_scale / depth + offset_x) * canvas_height) / cell_width).astype(np.int32)
    rows = ((canvas_height * 0.5 + (STAR_POS_Y * star_scale / depth + offset_y) * canvas_height) / cell_height).astype(np.int32)
    alpha = smooth_step(1.0, 0.82, depth) * (0.80 + 0.20 * np.sin(t * STAR_TWINKLE_FREQ + STAR_TWINKLE_PHASE)) * amount
    visible = (cols >= 0) & (cols < col_count) & (rows >= 0) & (rows < row_count) & (alpha > 0.04)
    if not visible.any():
        return
    indices = np.flatnonzero(visible)
    cols, rows = cols[indices], rows[indices]
    brightness = STAR_BRIGHTNESS[indices] * alpha[indices] * (1 + 0.05 / depth[indices])
    mask = pupil_mask_cell[rows, cols] > 0.5
    indices, cols, rows, brightness = indices[mask], cols[mask], rows[mask], brightness[mask]
    keep = brightness > luminance[rows, cols] * 0.7
    indices, cols, rows, brightness = indices[keep], cols[keep], rows[keep], brightness[keep]
    if len(brightness) == 0:
        return
    chars = np.where(brightness < 0.20, CHARACTER_INDEX_MAP["."], np.where(brightness < 0.42, CHARACTER_INDEX_MAP["+"], CHARACTER_INDEX_MAP["*"]))
    char_indices[rows, cols] = chars
    foreground_colors[rows, cols] = STAR_COLOR[indices] * np.clip(0.35 + 0.9 * brightness, 0, 1)[:, None] * vignette_cell[rows, cols][:, None]

    bright_stars = np.flatnonzero(brightness > 0.55)
    for j in bright_stars[:45]:
        cc, rr, bb = int(cols[j]), int(rows[j]), float(brightness[j])
        star_color = STAR_COLOR[indices[j]] * vignette_cell[rr, cc]
        char_indices[rr, cc] = CHARACTER_INDEX_MAP["@"] if bb > 0.85 else CHARACTER_INDEX_MAP["*"]
        ray_length = int(2 + 6 * (bb - 0.5))
        for k in range(1, ray_length + 1):
            ray_alpha = (1 - k / (ray_length + 1)) * bb
            for (dr, dc, ray_char) in ((0, k, "-"), (0, -k, "-"), (k // 2 + (1 if k > 2 else 0), 0, "|"), (-(k // 2 + (1 if k > 2 else 0)), 0, "|")):
                if dr == 0 and dc == 0:
                    continue
                r2, c2 = rr + dr, cc + dc
                if 0 <= r2 < row_count and 0 <= c2 < col_count and pupil_mask_cell[r2, c2] > 0.5 and luminance[r2, c2] < ray_alpha * 0.8:
                    char_indices[r2, c2] = CHARACTER_INDEX_MAP[ray_char if ray_alpha > 0.18 else "."]
                    foreground_colors[r2, c2] = star_color * min(1.0, 0.25 + ray_alpha)


def render_eyelashes(char_indices, foreground_colors, t, zoom, openness, gaze_x, gaze_y):
    """Render eyelashes as characters."""
    if zoom > 2.6 or openness < 0.0:
        return
    closed_amount = 1 - openness ** 0.8

    def to_cell_coords(ue, ve):
        return int((canvas_width / 2 + ue * zoom * canvas_height) / cell_width), int((canvas_height / 2 + ve * zoom * canvas_height) / cell_height)

    def pick_char_from_angle(angle):
        deg = m.degrees(m.atan2(-m.sin(angle), m.cos(angle))) % 180
        if deg < 25 or deg >= 155:
            return "-"
        if deg < 70:
            return "/"
        if deg < 110:
            return "|"
        return "\\"

    def draw_lash(base_u, base_v, start_angle, length, curl, color_root, color_tip, max_segments, tip_char):
        segments = int(max(2, min(max_segments, length * zoom * canvas_height / (cell_width * 0.85))))
        step = length / segments
        ue, ve = base_u, base_v
        for k in range(segments):
            t_param = k / max(1, segments - 1)
            angle = start_angle + curl * t_param * t_param
            ue += m.cos(angle) * step
            ve += m.sin(angle) * step
        col, row = to_cell_coords(ue, ve)
        if not (0 <= row < row_count and 0 <= col < col_count):
            return
        char = tip_char if (k == segments - 1 and segments >= 4) else pick_char_from_angle(angle)
        char_indices[row, col] = CHARACTER_INDEX_MAP[char]
        foreground_colors[row, col] = color_root + (color_tip - color_root) * t_param

    upper_root_color = np.array([0.18, 0.12, 0.08], np.float32)
    upper_tip_color = np.array([0.32, 0.21, 0.15], np.float32)
    lower_root_color = np.array([0.19, 0.13, 0.09], np.float32)
    lower_tip_color = np.array([0.32, 0.22, 0.16], np.float32)

    for (s0, length_factor, phase, curve_var) in UPPER_LASHES:
        u0 = s0 * EYE_HALF_WIDTH
        v_upper, v_lower, curve_upper, curve_lower = eyelid_edge_position(u0, openness)
        base_v = v_upper - 0.055 * s0
        angle_open = m.radians(-90 + 26 * s0)
        angle_closed = m.radians(90 - 20 * s0) if s0 >= 0 else m.radians(-270 - 20 * s0)
        start_angle = angle_open + (angle_closed - angle_open) * curve_lower
        edge_factor = m.sqrt(max(0.0, 1 - s0 * s0))
        lash_height = (0.070 + 0.050 * edge_factor) * length_factor
        curl_amount = m.radians(-22 * s0) * (1 - curve_lower)
        draw_lash(u0, base_v, start_angle, lash_height, curl_amount, upper_root_color, upper_tip_color, 14, "'")
    for (s0, length_factor, phase, curve_var) in LOWER_LASHES:
        u0 = s0 * EYE_HALF_WIDTH
        v_upper, v_lower, curve_upper, curve_lower = eyelid_edge_position(u0, openness)
        base_v = v_lower - 0.055 * s0
        start_angle = m.radians(90 - 20 * s0)
        lash_height = 0.034 * (0.5 + 0.8 * curve_lower) * length_factor
        draw_lash(u0, base_v, start_angle, lash_height, m.radians(12 * (1 if s0 > 0 else -1)), lower_root_color, lower_tip_color, 6, ".")


def apply_bloom(image):
    """Apply bloom/glow effect to bright areas."""
    bright = np.clip(image - 0.45, 0, None)
    output = image
    for scale, weight in ((2, 0.45), (4, 0.35)):
        blurred = bright.reshape(grid_height // scale, scale, grid_width // scale, scale, 3).mean((1, 3))
        for _ in range(2):
            blurred = (blurred * 2 + np.roll(blurred, 1, 0) + np.roll(blurred, -1, 0) + np.roll(blurred, 1, 1) + np.roll(blurred, -1, 1)) / 6
        output = output + weight * np.repeat(np.repeat(blurred, scale, 0), scale, 1)
    return output


def render_frame(t, dt):
    """Render one complete frame and return character + color arrays."""
    world_state["last_time"] = t
    progress = zoom_progress(t)
    idle_progress = ease_curve(t / TIME_ZOOM_START)
    zoom = m.exp(m.log(ZOOM_FINAL_LEVEL) * progress) * (1 + 0.05 * idle_progress + 0.004 * m.sin(t * 0.9))
    zoom_space = zoom if t < TIME_SPACE_SCENE else ZOOM_FINAL_LEVEL * m.exp(0.03 * (t - TIME_SPACE_SCENE))
    star_scale = min(6.0, STAR_SPREAD_BASE * zoom_space ** 1.25)
    nebula_scale = min(1.15, STAR_SPREAD_BASE * zoom ** 1.25)
    openness = eyelid_openness(t)
    gaze_x, gaze_y = gaze_direction(t, progress)

    pupil_radius = PUPIL_BASE_RADIUS * (0.76 + 0.24 * ease_curve((t - 1.8) / 3.5)) * (1 + 0.025 * m.sin(1.9 * t)) * (1 + 0.30 * progress)
    pupil_screen_radius = pupil_radius * zoom
    full_space = pupil_screen_radius * 0.72 > 1.03

    star_visibility = ease_curve((t - (TIME_ZOOM_START + 1.5)) / 4.5)
    nebula_visibility = ease_curve((t - (TIME_ZOOM_START + 3.5)) / 8.0)
    update_world_state(t, dt, progress)

    offset_x, offset_y = gaze_x * zoom, gaze_y * zoom
    space_image = np.empty((grid_height, grid_width, 3), np.float32)
    space_image[:] = (0.003, 0.004, 0.010)
    if nebula_visibility > 0.002:
        drift = ease_curve((t - TIME_SPACE_SCENE) / 20.0)
        heart_morph = ease_curve((t - TIME_HEART_MORPH_START) / TIME_HEART_MORPH_DURATION)
        heartbeat = 1 + 0.03 * m.sin(t * 2.6) * heart_morph * heart_morph
        space_image += heart_nebula_renderer(coord_x - offset_x - 0.03 * drift * m.sin(t * 0.07), coord_y - offset_y,
                           0.17 * nebula_scale * heartbeat, heart_morph, t) * (1.30 * nebula_visibility ** 1.3)

    if full_space:
        image = space_image
        pupil_mask_cell = np.ones((row_count, col_count), np.float32)
        solid_mask = np.zeros((row_count, col_count), bool)
    else:
        image, pupil_mask = eye_scene_renderer(t, zoom, openness, gaze_x, gaze_y, pupil_radius, space_image)
        pupil_mask_cell = pupil_mask.reshape(row_count, SUPER_SAMPLE, col_count, SUPER_SAMPLE).mean((1, 3))
        solid_mask = pupil_mask_cell < 0.5

    image = apply_bloom(image)
    image = 1 - np.exp(-2.2 * np.clip(image, 0, None))
    image = image * (1 - 0.30 * smooth_step(0.4, 1.0, radius_subpixel))[..., None] * ease_curve(t / 1.2)
    cell_colors = image.reshape(row_count, SUPER_SAMPLE, col_count, SUPER_SAMPLE, 3).mean((1, 3))
    luminance = 0.30 * cell_colors[..., 0] + 0.60 * cell_colors[..., 1] + 0.10 * cell_colors[..., 2]
    luminance_adjusted = np.clip(luminance, 0, 1) ** 0.72
    ramp_index = np.clip((luminance_adjusted + (hash_cell - 0.5) * 0.07) * RAMP_MAX_INDEX, 0, RAMP_MAX_INDEX).astype(np.int32)
    ramp_index = np.where(solid_mask, np.maximum(ramp_index, 3), ramp_index)
    char_indices = ramp_index.astype(np.int32)
    foreground_colors = np.clip(cell_colors * 1.20, 0, 1).astype(np.float32)

    vignette_cell = (0.25 + 0.75 * smooth_step(0, 0.30 * pupil_screen_radius, pupil_screen_radius - radius_cell)).astype(np.float32)
    render_stars(char_indices, foreground_colors, luminance_adjusted, t, star_scale, star_visibility, pupil_mask_cell, vignette_cell, offset_x, offset_y)
    for star in shooting_stars:
        render_shooting_star(star, char_indices, foreground_colors, pupil_mask_cell, vignette_cell)
    if not full_space:
        render_eyelashes(char_indices, foreground_colors, t, zoom, openness, gaze_x, gaze_y)

    quantized_color = np.clip((np.clip(foreground_colors, 0, 1) * (COLOR_QUANTIZATION_LEVELS - 0.01)).astype(np.int16), 0, COLOR_QUANTIZATION_LEVELS - 1)
    return char_indices, quantized_color


def plan_cell_updates(char_indices, quantized_color, display_char_indices, display_quantized_color, budget):
    """Determine which cells need redrawing within the performance budget."""
    same_char = char_indices == display_char_indices
    color_delta = np.abs(quantized_color - display_quantized_color).max(axis=2)
    both_blank = (char_indices == 0) & (display_char_indices == 0)
    need_update = (~both_blank) & ((~same_char) | (color_delta >= 2))
    cells_to_update = np.flatnonzero(need_update)
    if len(cells_to_update) > budget:
        priority = ((~same_char).astype(np.int16) * 6 + color_delta).ravel()[cells_to_update]
        top_priority = np.argpartition(-priority, budget)[:budget]
        cells_to_update = cells_to_update[top_priority]
    return cells_to_update


def main():
    """Main entry point - initialize window and start animation loop."""
    import tkinter as tk
    import tkinter.font as tkf

    root = tk.Tk()
    root.title("Cosmic Eye - Powered by Nurlan Mammadli")
    root.resizable(False, False)
    root.bind("<Escape>", lambda e: root.destroy())
    font_families = set(tkf.families())
    monospace_font = next((f for f in ("Cascadia Mono", "Consolas", "Courier New", "DejaVu Sans Mono", "Courier")
                 if f in font_families), "Courier")
    screen_height = root.winfo_screenheight()
    font = tkf.Font(root=root, family=monospace_font, size=FONT_SIZE, weight="bold")
    char_height = font.metrics("linespace")
    char_width = font.measure("M")
    rows = min(MAX_ROW_COUNT, (screen_height - 110) // char_height)
    initialize_display(char_width, char_height, rows)
    root.geometry(f"{canvas_width}x{canvas_height}+{(root.winfo_screenwidth() - canvas_width) // 2}+{max(0, (screen_height - canvas_height) // 2 - 20)}")
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="#000810", highlightthickness=0)
    canvas.pack()

    canvas_items = np.zeros((row_count, col_count), dtype=object)
    canvas_items[:] = 0
    display_char_indices = np.zeros((row_count, col_count), np.int32)
    display_quantized_color = np.zeros((row_count, col_count, 3), np.int16)
    hex_color_cache = {}
    timing_state = {"start_time": time.perf_counter(), "update_budget": 2500, "update_cost": 0.012}

    def rgb_to_hex(rgb):
        """Convert RGB color tuple to hex string with caching."""
        key = (int(rgb[0]), int(rgb[1]), int(rgb[2]))
        cached = hex_color_cache.get(key)
        if cached is None:
            cached = "#%02x%02x%02x" % tuple(v * 255 // (COLOR_QUANTIZATION_LEVELS - 1) for v in key)
            hex_color_cache[key] = cached
        return cached

    def restart_animation(event=None):
        """Restart animation from beginning."""
        timing_state["start_time"] = time.perf_counter()
        reset_animation()

    root.bind("r", restart_animation)
    root.bind("R", restart_animation)

    def animation_tick():
        """Per-frame update and render function."""
        t0 = time.perf_counter()
        t = t0 - timing_state["start_time"]
        dt = min(max(t - world_state["last_time"], 0.0), 0.1)
        char_indices, quantized_color = render_frame(t, dt)
        cells_to_update = plan_cell_updates(char_indices, quantized_color, display_char_indices, display_quantized_color, timing_state["update_budget"])
        t1 = time.perf_counter()
        for cell in cells_to_update:
            row, col = divmod(int(cell), col_count)
            char = BRIGHTNESS_RAMP[char_indices[row, col]]
            fill_color = rgb_to_hex(quantized_color[row, col])
            item = canvas_items[row, col]
            if item == 0:
                if char == " ":
                    display_char_indices[row, col] = 0
                    display_quantized_color[row, col] = quantized_color[row, col]
                    continue
                canvas_items[row, col] = canvas.create_text((col + 0.5) * cell_width, (row + 0.5) * cell_height, text=char, fill=fill_color,
                                               font=font, anchor="center")
            else:
                canvas.itemconfig(item, text=char, fill=fill_color)
            display_char_indices[row, col] = char_indices[row, col]
            display_quantized_color[row, col] = quantized_color[row, col]
        if len(cells_to_update) > 50:
            cost_per_cell = (time.perf_counter() - t1) / len(cells_to_update)
            timing_state["update_cost"] = 0.7 * timing_state["update_cost"] + 0.3 * cost_per_cell
            timing_state["update_budget"] = int(min(12000, max(400, (TKINTER_FRAME_BUDGET_MS / 1000.0) / max(timing_state["update_cost"], 1e-6))))
        elapsed = (time.perf_counter() - t0) * 1000
        root.after(max(1, int(1000 / FRAME_RATE - elapsed)), animation_tick)

    root.after(100, animation_tick)
    root.mainloop()


if __name__ == "__main__":
    main()
