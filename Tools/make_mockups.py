"""Generates the interface mock-up previews in Media/Screenshots.

These are illustrative renders of the CyberFlow UI layout (not captures from a Vita).
Usage: python Tools/make_mockups.py   (needs Pillow)
"""
import math
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "Media", "Screenshots")
FONT = os.path.join(ROOT, "DATA", "Rajdhani-SemiBold.ttf")
THEMES = os.environ.get("CYBERFLOW_THEMES", os.path.join(ROOT, "..", "..", "themes"))
LOGO = os.path.join(ROOT, "Media", "Logo", "logo_cyberflow.png")
S = 2  # supersampling factor
W, H = 960, 544

CYAN = (92, 228, 244)
INFO_CYAN = (84, 220, 244)
RED = (214, 54, 66)
ITEM_RED = (232, 70, 70)
YELLOW = (248, 208, 80)
TEXT = (226, 248, 252)
LABEL = (168, 200, 212)
FOOT_RED = (240, 88, 72)
ACCENT = (0, 255, 200)  # Dogtown accent

_fonts = {}


def font(size):
    if size not in _fonts:
        _fonts[size] = ImageFont.truetype(FONT, int(size * S * 1.18))
    return _fonts[size]


class Canvas:
    def __init__(self, background):
        self.img = background.convert("RGBA")

    def rect(self, x1, y1, x2, y2, color):
        x1, y1, x2, y2 = [int(round(v * S)) for v in (x1, y1, x2, y2)]
        if x2 <= x1 or y2 <= y1:
            return
        layer = Image.new("RGBA", (x2 - x1, y2 - y1), color if len(color) == 4 else color + (255,))
        self.img.alpha_composite(layer, (x1, y1))

    def poly(self, points, fill=None, outline=None, width=1):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        pts = [(x * S, y * S) for x, y in points]
        if fill is not None:
            d.polygon(pts, fill=fill if len(fill) == 4 else fill + (255,))
        if outline is not None:
            d.line(pts + [pts[0]], fill=outline if len(outline) == 4 else outline + (255,), width=width * S, joint="curve")
        self.img.alpha_composite(layer)

    def line(self, x1, y1, x2, y2, color, width=1):
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        ImageDraw.Draw(layer).line([(x1 * S, y1 * S), (x2 * S, y2 * S)], fill=color if len(color) == 4 else color + (255,), width=max(1, int(width * S)))
        self.img.alpha_composite(layer)

    def text(self, x, y, s, size, color, anchor="l"):
        f = font(size)
        layer = Image.new("RGBA", self.img.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        w = d.textlength(s, font=f) / S
        if anchor == "m":
            x -= w / 2
        elif anchor == "r":
            x -= w
        d.text((x * S, y * S), s, font=f, fill=color if len(color) == 4 else color + (255,))
        self.img.alpha_composite(layer)
        return w

    def width(self, s, size):
        return ImageDraw.Draw(self.img).textlength(s, font=font(size)) / S

    def paste(self, im, x, y):
        self.img.alpha_composite(im.convert("RGBA"), (int(round(x * S)), int(round(y * S))))

    def save(self, name):
        os.makedirs(OUT, exist_ok=True)
        out = self.img.convert("RGB").resize((W, H), Image.LANCZOS)
        out.save(os.path.join(OUT, name), optimize=True)
        print("wrote", name)


def background(theme_file, dim=0.55, blur=1.2):
    im = Image.open(os.path.join(THEMES, theme_file)).convert("RGB")
    scale = max(W * S / im.width, H * S / im.height)
    im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    left = (im.width - W * S) // 2
    top = (im.height - H * S) // 2
    im = im.crop((left, top, left + W * S, top + H * S))
    im = im.filter(ImageFilter.GaussianBlur(blur * S))
    return Image.blend(im, Image.new("RGB", im.size, (0, 0, 0)), dim)


def settings_backdrop(c):
    for band in range(68):
        edge = abs(band / 67 - 0.5) * 2
        c.rect(0, band * 8, 960, band * 8 + 8, (20, 3, 11, int(120 + 95 * edge * edge)))
    for strip in range(10):
        a = int(120 * (1 - strip / 10))
        c.rect(strip * 12, 0, strip * 12 + 12, 544, (10, 0, 5, a))
        c.rect(960 - strip * 12 - 12, 0, 960 - strip * 12, 544, (10, 0, 5, a))


def chamfer(c, x, y, w, h, c1, c2, fill):
    pts = [(x + c1, y), (x + w, y), (x + w, y + h - c2), (x + w - c2, y + h), (x, y + h), (x, y + c1)]
    c.poly(pts, fill=fill)


def chamfer_outline(c, x, y, w, h, c1, c2, color, width=1):
    pts = [(x + c1, y), (x + w, y), (x + w, y + h - c2), (x + w - c2, y + h), (x, y + h), (x, y + c1)]
    c.poly(pts, outline=color, width=width)


def key_icon(c, x, y, symbol):
    cx, cy = x + 10, y + 10
    layer = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse(((cx - 9.5) * S, (cy - 9.5) * S, (cx + 9.5) * S, (cy + 9.5) * S), fill=(6, 18, 30, 235), outline=INFO_CYAN + (245,), width=S)
    col = INFO_CYAN + (245,)
    if symbol == "cross":
        d.line(((cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S), fill=col, width=2 * S)
        d.line(((cx - 4) * S, (cy + 4) * S, (cx + 4) * S, (cy - 4) * S), fill=col, width=2 * S)
    elif symbol == "circle":
        d.ellipse(((cx - 4.5) * S, (cy - 4.5) * S, (cx + 4.5) * S, (cy + 4.5) * S), outline=col, width=2 * S)
    elif symbol == "square":
        d.rectangle(((cx - 4) * S, (cy - 4) * S, (cx + 4) * S, (cy + 4) * S), outline=col, width=2 * S)
    elif symbol == "triangle":
        d.polygon([(cx * S, (cy - 5) * S), ((cx + 5) * S, (cy + 4) * S), ((cx - 5) * S, (cy + 4) * S)], outline=col, width=2 * S)
    c.img.alpha_composite(layer)


def footer_entries(c, entries, color):
    cursor = 928
    for label, symbol in entries:
        w = c.width(label, 20)
        tx = cursor - w
        c.text(tx, 504, label, 20, color)
        if symbol == "R1":
            ix = tx - 28
            c.rect(ix, 512, ix + 24, 513, INFO_CYAN)
            c.rect(ix, 527, ix + 24, 528, INFO_CYAN)
            c.rect(ix, 512, ix + 1, 528, INFO_CYAN)
            c.rect(ix + 23, 512, ix + 24, 528, INFO_CYAN)
            c.text(ix + 5, 511, "R1", 11, INFO_CYAN)
            cursor = ix - 22
        else:
            key_icon(c, tx - 28, 510, symbol)
            cursor = tx - 50


def logo(c, y=8):
    lg = Image.open(LOGO).convert("RGBA")
    lg = lg.resize((lg.width * S, lg.height * S), Image.LANCZOS)
    c.paste(lg, 480 - lg.width / S / 2, y)


def ram_bar(c, label, fill):
    c.text(275, 11, "CYBERDECK RAM: " + label, 22, (86, 228, 255, 230))
    for seg in range(41):
        x = 275 + seg * 10
        col = (78, 220, 255, 235) if seg < fill else (236, 62, 82, 88)
        c.rect(x, 42, x + 8, 60, col)
        c.rect(x + 1, 60, x + 7, 64, col)


# ----------------------------------------------------------------- fake game covers
GAMES = [
    ("NEON RUNNER", (0, 200, 255), (120, 0, 200)),
    ("CHROME DRIFT", (255, 90, 60), (60, 0, 40)),
    ("DATA HEIST", (250, 220, 40), (20, 20, 60)),
    ("BLADE CIRCUIT", (255, 40, 120), (30, 0, 50)),
    ("SYNTHWAVE 84", (120, 80, 255), (10, 0, 40)),
    ("DOGTOWN BRAWL", (0, 255, 190), (0, 40, 50)),
    ("GRID BREAKER", (255, 150, 30), (40, 10, 0)),
    ("ECHO PROTOCOL", (80, 255, 120), (0, 30, 20)),
    ("RED SECTOR", (255, 50, 50), (20, 0, 0)),
]


def make_cover(index, w=190, h=270):
    title, c1, c2 = GAMES[index % len(GAMES)]
    rnd = random.Random(index * 91 + 7)
    im = Image.new("RGB", (w * S, h * S))
    d = ImageDraw.Draw(im)
    for y in range(h * S):
        t = y / (h * S)
        d.line([(0, y), (w * S, y)], fill=tuple(int(c2[i] * (1 - t) + c1[i] * 0.55 * t) for i in range(3)))
    # sun / grid / skyline
    cx, cy = w * S // 2, int(h * S * 0.52)
    for r in range(70 * S, 0, -4):
        a = 1 - r / (70 * S)
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=tuple(int(c1[i] * (0.25 + 0.75 * a)) for i in range(3)))
    for i in range(14):
        bw = rnd.randint(10, 26) * S
        bh = rnd.randint(30, 95) * S
        bx = i * (w * S // 14)
        d.rectangle((bx, h * S - bh - 40 * S, bx + bw, h * S), fill=(8, 6, 16))
        for _ in range(4):
            wx, wy = bx + rnd.randint(2, max(3, bw - 4)), h * S - bh - 36 * S + rnd.randint(0, bh)
            d.rectangle((wx, wy, wx + 2 * S, wy + 2 * S), fill=c1)
    for i in range(0, w * S, 18 * S):
        d.line([(i, h * S), (w * S // 2 + (i - w * S // 2) * 0.2, h * S - 40 * S)], fill=c1, width=1)
    d.rectangle((0, 0, w * S, 30 * S), fill=(0, 0, 0))
    d.text((8 * S, 3 * S), "PS VITA", font=font(13), fill=(235, 235, 235))
    d.rectangle((0, 0, w * S - 1, h * S - 1), outline=tuple(int(v * 0.8) for v in c1), width=2 * S)
    words = title.split()
    ty = int(h * S * 0.64)
    for word in words:
        f = font(26)
        tw = d.textlength(word, font=f)
        d.text(((w * S - tw) / 2 + 2 * S, ty + 2 * S), word, font=f, fill=(0, 0, 0))
        d.text(((w * S - tw) / 2, ty), word, font=f, fill=(255, 255, 255))
        ty += 30 * S
    return im


def persp(im, left_h_ratio, right_h_ratio, out_w):
    """Squash an image into a quad whose left/right edge heights differ (coverflow tilt)."""
    w, h = im.size
    ow = int(out_w * S)
    big = max(left_h_ratio, right_h_ratio)
    oh = int(h * big)
    lh, rh = h * left_h_ratio, h * right_h_ratio
    # destination quad (TL, BL, BR, TR) -> map back via QUAD data (source corners for dest rect)
    # PIL QUAD maps output rect corners to the given source quad; instead warp with a mesh of columns
    out = Image.new("RGBA", (ow, oh), (0, 0, 0, 0))
    for x in range(ow):
        t = x / max(1, ow - 1)
        col_h = lh + (rh - lh) * t
        sx = int(t * (w - 1))
        strip = im.crop((sx, 0, sx + 1, h)).resize((1, max(1, int(col_h))), Image.BILINEAR).convert("RGBA")
        out.paste(strip, (x, (oh - int(col_h)) // 2))
    return out


def draw_coverflow(c, selected):
    floor_y = 396
    items = []
    for offset in range(-4, 5):
        items.append(offset)
    items.sort(key=lambda o: -abs(o))
    for offset in items:
        cover = make_cover(selected + offset)
        if offset == 0:
            wpx, tilt = 196, (1.0, 1.0)
            x = 480 - wpx / 2
            im = persp(cover, 1.0, 1.0, wpx)
        else:
            sign = 1 if offset > 0 else -1
            wpx = 70
            x = 480 + sign * (118 + (abs(offset) - 1) * 62) - (wpx / 2 if sign > 0 else wpx / 2)
            hi, lo = 1.0, 0.82
            im = persp(cover, hi if sign > 0 else lo, lo if sign > 0 else hi, wpx)
        top_y = floor_y - im.height / S
        # reflection
        refl = im.transpose(Image.FLIP_TOP_BOTTOM)
        fade = Image.new("L", refl.size, 0)
        fd = ImageDraw.Draw(fade)
        for yy in range(refl.height):
            fd.line([(0, yy), (refl.width, yy)], fill=int(95 * max(0, 1 - yy / (refl.height * 0.55))))
        r, g, b, a = refl.split()
        a = Image.composite(fade, Image.new("L", refl.size, 0), a)
        refl.putalpha(a)
        c.paste(refl, x, floor_y + 2)
        c.paste(im, x, top_y)
        if offset == 0:
            chamfer_outline(c, x - 4, top_y - 4, wpx + 8, im.height / S + 8, 8, 8, CYAN + (230,), 1)


def make_floor_glow(c):
    for i in range(20):
        c.rect(0, 396 + i * 1.4, 960, 396 + (i + 1) * 1.4, ACCENT + (int(26 * (1 - i / 20)),))


# ------------------------------------------------------------------ screens
def screen_start():
    c = Canvas(background("Dogtown.png", dim=0.5))
    make_floor_glow(c)
    draw_coverflow(c, 3)
    ram_bar(c, "PS VITA", 8)
    # status cluster
    c.text(726, 30, "21:37", 20, (86, 228, 255))
    c.text(806, 30, "76%", 20, (86, 228, 255))
    layer = Image.new("RGBA", c.img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for r in (4, 8, 12):
        d.arc(((792 - r) * S, (46 - r) * S, (792 + r) * S, (46 + r) * S), 225, 315, fill=(86, 228, 255, 255), width=2 * S)
    d.ellipse((791 * S, 45 * S, 793 * S, 47 * S), fill=(86, 228, 255, 255))
    c.img.alpha_composite(layer)
    c.rect(884, 36, 912, 48, (86, 228, 255, 255))
    c.rect(886, 38, 910, 46, (4, 14, 22, 255))
    c.rect(887, 39, 903, 45, (86, 228, 255, 255))
    # name band + footer
    c.rect(0, 424, 960, 496, (0, 0, 0, 255))
    c.text(480, 432, "Blade Circuit", 24, (130, 235, 255), "m")
    c.text(480, 462, "4 of 64", 16, (200, 230, 240), "m")
    c.rect(0, 496, 960, 544, ACCENT + (128,))
    c.rect(0, 496, 960, 498, ACCENT + (255,))
    footer_entries(c, [("Launch", "cross"), ("Details", "triangle"), ("Category", "square"), ("View", "circle")], (240, 252, 255))
    c.save("start_menu.png")


def screen_info():
    c = Canvas(background("Dogtown.png", dim=0.6))
    settings_backdrop(c)
    corner = RED + (150,)
    c.line(18, 40, 150, 40, corner)
    c.line(780, 52, 872, 52, corner)
    c.line(91, 469, 182, 469, corner)
    c.line(780, 469, 872, 469, corner)
    ram_bar(c, "PS VITA", 8)
    # rotating box art in the centre
    cover = make_cover(3, 190, 270)
    box = persp(cover, 1.0, 0.93, 170)
    refl = box.transpose(Image.FLIP_TOP_BOTTOM)
    fade = Image.new("L", refl.size, 0)
    fd = ImageDraw.Draw(fade)
    for yy in range(refl.height):
        fd.line([(0, yy), (refl.width, yy)], fill=int(80 * max(0, 1 - yy / (refl.height * 0.5))))
    refl.putalpha(Image.composite(fade, Image.new("L", refl.size, 0), refl.split()[3]))
    bx, by = 395, 125
    c.paste(refl, bx, by + box.height / S + 2)
    c.paste(box, bx, by)
    side = Image.new("RGBA", (22 * S, int(box.height * 0.93)), (30, 20, 50, 255))
    c.paste(side, bx + 170, by + 9)
    # name tag
    name = "BLADE CIRCUIT"
    tw = c.width(name, 16) + 28
    sx = 480 - tw / 2
    hx, hy, r = sx + 9, 106, 9
    pts = [(hx - r, hy), (hx - r / 2, hy - r * 0.87), (hx + r / 2, hy - r * 0.87), (hx + r, hy), (hx + r / 2, hy + r * 0.87), (hx - r / 2, hy + r * 0.87)]
    c.poly(pts, outline=INFO_CYAN + (245,), width=1)
    c.text(sx + 28, 90, name, 16, TEXT)
    # quickhack buttons
    c.text(96, 112, "AVAILABLE ACTIONS:", 14, TEXT)

    def hack(x, y, w, h, selected, title, pills):
        body = (8, 30, 48, 224) if selected else (12, 30, 48, 205)
        line = INFO_CYAN + (245,) if selected else (52, 104, 140, 235)
        chamfer(c, x, y, w, h, 8, 10, body)
        chamfer_outline(c, x, y, w, h, 8, 10, line)
        if selected:
            chamfer_outline(c, x + 1, y + 1, w - 2, h - 2, 7, 9, line)
        box = h - 12
        bx2 = x + w - box - 16
        c.poly([(bx2, y + 6), (bx2 + box, y + 6), (bx2 + box, y + 6 + box), (bx2, y + 6 + box)], outline=line)
        c.text(x + 14, y - 1, title, 16, TEXT)
        px = x + 14
        for text, col in pills:
            pw = c.width(text, 11) + 10
            c.rect(px, y + h - 17, px + pw, y + h - 4, (6, 18, 30, 235))
            c.poly([(px, y + h - 17), (px + pw, y + h - 17), (px + pw, y + h - 4), (px, y + h - 4)], outline=col)
            c.text(px + 5, y + h - 18, text, 11, col)
            px += pw + 5

    pill_text = (206, 232, 240)
    hack(112, 144, 244, 38, True, "DOWNLOAD COVER", [("READY", pill_text), ("ONLINE", YELLOW)])
    hack(90, 188, 244, 38, False, "OVERRIDE CATEGORY", [("READY", pill_text), ("< PS VITA >", YELLOW)])
    # DATA / CONSOLE panel
    px, py, pw, tabH, bodyH = 656, 112, 276, 26, 214
    y0 = py + tabH
    half = pw // 2
    c.rect(px, y0, px + pw, y0 + bodyH, (8, 30, 48, 224))
    c.rect(px, py, px + half, y0 + 1, (8, 30, 48, 224))
    c.line(px, py, px + half, py, INFO_CYAN + (245,), 2)
    c.line(px, py, px, y0, INFO_CYAN + (245,), 2)
    c.line(px + half - 1, py, px + half - 1, y0, INFO_CYAN + (245,), 2)
    c.poly([(px + half, py + 8), (px + pw - 8, py), (px + pw, py + 8), (px + pw, y0), (px + half, y0)], fill=(136, 28, 42, 218), outline=RED + (240,))
    c.text(px + 14, py + 3, "DATA", 16, TEXT)
    c.text(px + half + 14, py + 3, "CONSOLE", 16, (255, 140, 140))
    c.line(px + half, y0, px + pw, y0, INFO_CYAN + (245,), 2)
    c.line(px, y0 + bodyH - 2, px + pw, y0 + bodyH - 2, INFO_CYAN + (245,), 2)
    c.line(px, y0, px, y0 + bodyH, INFO_CYAN + (245,), 2)
    c.line(px + pw - 2, y0, px + pw - 2, y0 + bodyH, INFO_CYAN + (245,), 2)
    rows = [("GAME", "Blade Circuit", YELLOW), ("PLATFORM", "PS Vita", INFO_CYAN), ("APP ID", "PCSE00042", INFO_CYAN), ("VERSION", "01.02", INFO_CYAN), ("SIZE", "1.2 GB", INFO_CYAN)]
    for i, (label, value, col) in enumerate(rows):
        ry = y0 + 12 + i * 31
        c.text(px + 16, ry - 2, label, 12, LABEL)
        c.text(px + 16, ry + 8, value, 18, col)
    footer_entries(c, [("Select", "cross"), ("Options", "triangle"), ("Switch Tab", "R1"), ("Close", "circle")], FOOT_RED + (255,))
    c.save("game_info.png")


def menu_panel(c, title):
    left, right = 190, 770
    for strip in range(68):
        y = strip * 8
        edge = abs(strip / 67 - 0.5) * 2
        fade = max(0, min(1, min(y + 4, 544 - y - 4) / 80))
        c.rect(left, y, right, y + 8, (88, 12, 24, int((122 + 40 * edge) * fade)))
        c.rect(left, y, left + 2, y + 8, RED + (int(235 * fade),))
        c.rect(right - 1, y, right, y + 8, RED + (int(120 * fade),))
    for y in range(6, 540, 12):
        fade = max(0, min(1, min(y, 544 - y) / 80))
        c.rect(left + 3, y, right - 2, y + 1, (255, 90, 90, int(22 * fade)))
    logo(c)
    c.text(218, 112, title, 16, CYAN + (255,))
    c.rect(left + 14, 138, right - 14, 139, CYAN + (110,))


def menu_rows(c, rows, selected):
    for i, row in enumerate(rows):
        y = 156 + i * 36
        if i == selected:
            x, w, h = 200, 560, 33
            chamfer(c, x, y - 7, w, h, 4, 10, (8, 30, 44, 225))
            chamfer_outline(c, x, y - 7, w, h, 4, 10, CYAN + (240,))
            chamfer_outline(c, x + 1, y - 6, w - 2, h - 2, 3, 9, CYAN + (240,))
            c.rect(x + w - 30, y + 4, x + w - 18, y + 6, CYAN)
            c.rect(x + w - 30, y + 9, x + w - 18, y + 11, CYAN)
            c.rect(x + w - 30, y + 14, x + w - 22, y + 16, CYAN)
        c.text(218, y - 6, row, 18, CYAN + (255,) if i == selected else ITEM_RED + (255,))


def screen_help():
    c = Canvas(background("Dogtown.png", dim=0.55, blur=2))
    settings_backdrop(c)
    menu_panel(c, "HELP")
    menu_rows(c, ["< Back", "Adding games", "Why did I get an Adrenaline warning?", "Custom game covers & backgrounds", "Custom wallpaper & music", "Control shortcuts", "About"], 1)
    footer_entries(c, [("Select", "cross"), ("Close", "circle")], CYAN + (255,))
    c.save("help_menu.png")


def screen_about():
    c = Canvas(background("Dogtown.png", dim=0.55, blur=2))
    settings_backdrop(c)
    menu_panel(c, "ABOUT")
    menu_rows(c, ["< Back", "CyberFlow Launcher (RetroFlow 8.4.1)"], 0)
    body = [
        "CyberFlow Mod created by badmanwazzy37.",
        "",
        "Credits to CDPROJEKT RED for creating such a",
        "breathtaking game, Cyberpunk 2077's legacy will",
        "live on forever.",
        "",
        "Credits to Claude Sonnet 5.5 & Opus 5.5 for making",
        "the vision happen.",
        "",
        "Credits to jimbob4000 & VitaHex for their initial and",
        "ongoing work on RetroFlow & HexFlow.",
    ]
    for i, line in enumerate(body):
        c.text(218, 224 + i * 21, line, 18, (206, 234, 244))
    footer_entries(c, [("Close", "circle")], CYAN + (255,))
    c.save("about_credits.png")


THEME_LIST = [
    ("Classic", "Dogtown.png"),
    ("Arasaka", "arasaka.png"),
    ("Dogtown", "Dogtown.png"),
    ("Night City", "night city.png"),
    ("Arasaka Tower", "arasaka tower.png"),
    ("Ending", "ending.jpg"),
    ("Johnny Silverhand", "johnny silverhand.png"),
    ("Main Theme", "main theme.png"),
    ("Mikoshi", "mikoshi.png"),
    ("Militech", "militech.jpg"),
    ("Alt Cunningham", "alt cunningham.png"),
    ("Just Another Weapon: Phantom Liberty", "JUST ANOTHER WEAPON PHANTOM LIBERTY.png"),
    ("Nocturne OP55N1", "Nocturne Op55N1.png"),
]


def screen_themes(selected=2, active=2):
    c = Canvas(background(THEME_LIST[selected][1], dim=0.62, blur=2.5))
    settings_backdrop(c)
    logo(c)
    left, right, body_y = 150, 810, 156
    rows, row_h = 7, 34
    chamfer(c, left, 106, right - left, 32, 0, 10, (118, 22, 34, 225))
    chamfer_outline(c, left, 106, right - left, 32, 0, 10, RED + (235,))
    c.rect(left, 106, left + 4, 128, RED + (235,))
    c.text(left + 18, 108, "CYBERPUNK THEME", 18, CYAN + (255,))
    tag = "%02d / %02d" % (selected + 1, len(THEME_LIST))
    c.text(right - 24, 112, tag, 12, CYAN + (240,), "r")
    # preview box
    box_w, box_h = 238, rows * row_h
    prev = Image.open(os.path.join(THEMES, THEME_LIST[selected][1])).convert("RGB")
    sc = max(box_w * S / prev.width, box_h * S / prev.height)
    prev = prev.resize((int(prev.width * sc), int(prev.height * sc)), Image.LANCZOS)
    prev = prev.crop(((prev.width - box_w * S) // 2, (prev.height - box_h * S) // 2, (prev.width + box_w * S) // 2, (prev.height + box_h * S) // 2))
    c.paste(prev, left, body_y)
    c.rect(left, body_y + box_h - 30, left + box_w, body_y + box_h, (4, 6, 10, 200))
    c.line(left, body_y, left + box_w, body_y, RED + (120,))
    c.line(left, body_y + box_h, left + box_w, body_y + box_h, RED + (120,))
    c.line(left + box_w, body_y, left + box_w, body_y + box_h, RED + (120,))
    c.rect(left, body_y, left + 3, body_y + box_h, RED + (235,))
    c.text(left + box_w / 2, body_y + box_h - 25, THEME_LIST[selected][0].upper(), 13, CYAN + (255,), "m")
    # list
    list_x = left + 254
    list_w = right - list_x - 24
    scroll = max(0, min(len(THEME_LIST) - rows, selected - 3))
    for row in range(rows):
        idx = scroll + row
        ry = body_y + row * row_h
        sel = idx == selected
        name = THEME_LIST[idx][0].upper()
        if len(name) > 22:
            name = name[:19] + "..."
        if sel:
            chamfer(c, list_x, ry, list_w, row_h - 2, 0, 10, CYAN + (255,))
        glyph = (6, 22, 30, 255) if sel else RED + (120,)
        c.rect(list_x + 8, ry + 11, list_x + 18, ry + 13, glyph)
        c.rect(list_x + 8, ry + 16, list_x + 18, ry + 18, glyph)
        c.rect(list_x + 8, ry + 21, list_x + 14, ry + 23, glyph)
        c.text(list_x + 32, ry + 3, name, 18, (6, 22, 30, 255) if sel else ITEM_RED + (255,))
        if idx == active:
            c.text(list_x + list_w - 22, ry + 8, "ACTIVE", 12, (6, 22, 30, 255) if sel else CYAN + (255,), "r")
    track_x = right - 10
    c.rect(track_x, body_y, track_x + 3, body_y + box_h, RED + (60,))
    thumb_h = int(box_h * rows / len(THEME_LIST))
    thumb_y = body_y + int((box_h - thumb_h) * scroll / max(1, len(THEME_LIST) - rows))
    c.rect(track_x, thumb_y, track_x + 3, thumb_y + thumb_h, RED + (235,))
    c.line(left, 456, right, 456, RED + (120,))
    footer_entries(c, [("Select", "cross"), ("Close", "circle")], CYAN + (255,))
    c.save("theme_menu.png")


if __name__ == "__main__":
    screen_start()
    screen_info()
    screen_themes()
    screen_help()
    screen_about()
