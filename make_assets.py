"""
Gera os assets do Flapy Bleu Mini App:
  icon.png        200x200
  splash.png      800x533
  screenshots/phase1.png  400x711
  screenshots/phase2.png  400x711
  screenshots/phase3.png  400x711
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
SCREENS = os.path.join(BASE, "screenshots")
os.makedirs(SCREENS, exist_ok=True)

# ── helpers ──────────────────────────────────────────────────────────────────

def lerp_color(a, b, t):
    return tuple(int(a[i] + (b[i]-a[i])*t) for i in range(3))

def sky_gradient(draw, w, h, top=(0,5,15), bot=(0,20,60)):
    for y in range(h):
        t = y/h
        c = lerp_color(top, bot, t)
        draw.line([(0,y),(w,y)], fill=c)

def draw_pipe(draw, x, gap_y, gap, w=52, phase=0):
    colors = [
        (("#1a6632","#0d4420","#25945a"), ("#1a3366","#0d2244","#2555aa")),  # p1 green / blue
        (("#7a4a00","#4a2d00","#c87800"), ("#440044","#2a002a","#880088")),  # p3 gold / purple
        (("#006666","#004444","#00aaaa"), ("#663300","#441100","#aa6600")),  # p5 teal / orange
    ][phase % 3]
    top_c, bot_c = colors[0], colors[1]
    # top pipe
    draw.rectangle([x, 0, x+w, gap_y-10], fill=top_c[0])
    draw.rectangle([x-4, gap_y-26, x+w+4, gap_y-10], fill=top_c[1])
    draw.rectangle([x+2, 0, x+4, gap_y-10], fill=top_c[2])
    # bottom pipe
    draw.rectangle([x, gap_y+gap+10, x+w, 2000], fill=bot_c[0])
    draw.rectangle([x-4, gap_y+gap+10, x+w+4, gap_y+gap+26], fill=bot_c[1])
    draw.rectangle([x+2, gap_y+gap+10, x+4, 2000], fill=bot_c[2])

def draw_bird(draw, cx, cy, r=14, color=(30,180,255)):
    # body
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color)
    # wing
    draw.ellipse([cx-r+2, cy-4, cx+4, cy+r-4], fill=lerp_color(color,(255,255,255),0.3))
    # eye
    draw.ellipse([cx+4, cy-6, cx+10, cy], fill=(255,255,255))
    draw.ellipse([cx+6, cy-5, cx+9, cy-1], fill=(10,10,30))
    # beak
    draw.polygon([(cx+r-2,cy-2),(cx+r+7,cy+1),(cx+r-2,cy+4)], fill=(255,190,0))

def try_font(size):
    """Return a font — tries system fonts, falls back to default."""
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/verdanab.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def text_center(draw, text, y, w, font, fill=(255,255,255), shadow=(0,0,0)):
    bbox = draw.textbbox((0,0), text, font=font)
    tw = bbox[2]-bbox[0]
    x = (w - tw)//2
    draw.text((x+2, y+2), text, font=font, fill=shadow)
    draw.text((x, y), text, font=font, fill=fill)

# ── ICON 200x200 ─────────────────────────────────────────────────────────────

def make_icon():
    W, H = 200, 200
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    # background gradient
    sky_gradient(draw, W, H, (0,5,20), (0,30,80))

    # glow ring
    for r in range(72, 58, -1):
        t = (72-r)/14
        a = int(lerp_color((0,212,255),(0,80,180),t)[0])
        b = int(lerp_color((0,212,255),(0,80,180),t)[1])
        c = int(lerp_color((0,212,255),(0,80,180),t)[2])
        draw.ellipse([W//2-r, H//2-r, W//2+r, H//2+r], outline=(a,b,c), width=2)

    # mini candlestick decorations
    for x,h,up in [(30,30,True),(160,20,False),(40,15,False),(170,25,True)]:
        col = (0,220,100) if up else (220,60,60)
        draw.rectangle([x, 140-h, x+10, 140], fill=col)
        draw.line([(x+5,140-h-8),(x+5,140-h)], fill=col, width=2)
        draw.line([(x+5,140),(x+5,148)], fill=col, width=2)

    # bird
    draw_bird(draw, 100, 95, r=28, color=(30,180,255))

    # title
    font_big = try_font(18)
    font_sm  = try_font(11)
    text_center(draw, "FLAPY", 148, W, font_big, fill=(0,212,255), shadow=(0,0,0))
    text_center(draw, "BLEU", 168, W, font_big, fill=(255,255,255), shadow=(0,0,50))
    text_center(draw, "on BASE", 186, W, font_sm, fill=(100,200,255), shadow=(0,0,0))

    out = os.path.join(BASE, "icon.png")
    img.save(out, "PNG")
    print(f"✓ {out}")

# ── SPLASH 800x533 ────────────────────────────────────────────────────────────

def make_splash():
    W, H = 800, 533
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    sky_gradient(draw, W, H, (0,5,15), (0,25,70))

    # stars
    import random; random.seed(42)
    for _ in range(120):
        sx,sy = random.randint(0,W), random.randint(0,H//2)
        br = random.randint(140,255)
        draw.point((sx,sy), fill=(br,br,br))

    # ground
    draw.rectangle([0, H-60, W, H], fill=(10,40,10))
    draw.rectangle([0, H-60, W, H-55], fill=(20,120,20))

    # pipes
    draw_pipe(draw, 180, 200, 130, w=52, phase=0)
    draw_pipe(draw, 480, 150, 130, w=52, phase=0)
    draw_pipe(draw, 680, 240, 130, w=52, phase=0)

    # bird (center, slight upward angle)
    bx, by = 310, 190
    draw_bird(draw, bx, by, r=22, color=(30,180,255))

    # score
    font_score = try_font(54)
    font_title = try_font(52)
    font_sub   = try_font(22)
    font_tag   = try_font(16)

    text_center(draw, "7", 30, W, font_score, fill=(255,255,255), shadow=(0,0,0))

    # title
    text_center(draw, "FLAPY BLEU", H//2+60, W, font_title, fill=(0,212,255), shadow=(0,0,80))
    text_center(draw, "Flap through Base blockchain", H//2+118, W, font_sub, fill=(180,230,255), shadow=(0,0,0))

    # tagline chips
    for i, tag in enumerate(["🎮 10 PHASES", "⚡ POWER-UPS", "💰 USDC REWARDS"]):
        fx = try_font(14)
        bbox = draw.textbbox((0,0), tag, font=fx)
        tw = bbox[2]-bbox[0]
        tx = 80 + i*220
        draw.rounded_rectangle([tx-8, H-130, tx+tw+8, H-108], radius=8, fill=(0,40,100,200))
        draw.text((tx, H-130), tag, font=fx, fill=(0,212,255))

    out = os.path.join(BASE, "splash.png")
    img.save(out, "PNG")
    print(f"✓ {out}")

# ── SCREENSHOTS 400x711 ───────────────────────────────────────────────────────

PHASE_CONFIGS = [
    dict(label="PHASE 1", score=3,  pipe_phase=0, sky_top=(0,5,20),  sky_bot=(0,30,80),  bird_col=(30,180,255)),
    dict(label="PHASE 5", score=47, pipe_phase=1, sky_top=(20,0,40), sky_bot=(60,0,80),  bird_col=(255,80,200)),
    dict(label="PHASE 10",score=99, pipe_phase=2, sky_top=(40,10,0), sky_bot=(80,20,0),  bird_col=(255,200,30)),
]

def make_screenshot(cfg, fname):
    W, H = 400, 711
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)

    sky_gradient(draw, W, H, cfg["sky_top"], cfg["sky_bot"])

    import random; random.seed(7)
    for _ in range(80):
        sx,sy = random.randint(0,W), random.randint(0,H//2)
        br = random.randint(120,240)
        draw.point((sx,sy), fill=(br,br,br))

    # ground
    draw.rectangle([0, H-50, W, H], fill=(10,40,10))
    draw.rectangle([0, H-50, W, H-44], fill=(20,120,20))

    # pipes
    draw_pipe(draw, 120, 220, 128, w=48, phase=cfg["pipe_phase"])
    draw_pipe(draw, 310, 180, 128, w=48, phase=cfg["pipe_phase"])

    # bird
    draw_bird(draw, 160, 210, r=18, color=cfg["bird_col"])

    # HUD
    font_score  = try_font(42)
    font_phase  = try_font(18)
    font_lives  = try_font(14)

    text_center(draw, str(cfg["score"]), 20, W, font_score, fill=(255,255,255), shadow=(0,0,0))
    text_center(draw, cfg["label"], 68, W, font_phase, fill=(0,212,255), shadow=(0,0,0))

    # hearts
    for i in range(3):
        hx = 10 + i*26
        draw.text((hx, 8), "♥", font=try_font(16), fill=(255,60,60))

    out = os.path.join(SCREENS, fname)
    img.save(out, "PNG")
    print(f"✓ {out}")

# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Gerando assets...")
    make_icon()
    make_splash()
    for i, cfg in enumerate(PHASE_CONFIGS, 1):
        make_screenshot(cfg, f"phase{i}.png")
    print("\n✅ Todos os assets gerados com sucesso!")
