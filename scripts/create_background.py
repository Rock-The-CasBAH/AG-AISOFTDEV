from PIL import Image, ImageDraw, ImageFilter

# Create a 1920x1080 sepia-toned workplace-anime-style background
W, H = 1920, 1080
base = Image.new('RGB', (W, H), (240, 230, 210))  # light warm base
draw = ImageDraw.Draw(base)

# Soft vertical sepia gradient
for y in range(H):
    t = y / H
    r = int(245 - 30 * t)
    g = int(235 - 40 * t)
    b = int(220 - 60 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# Add subtle vignette
v = Image.new('L', (W, H), 0)
vd = ImageDraw.Draw(v)
vd.ellipse((-W*0.2, -H*0.2, W*1.2, H*1.2), fill=180)
v = v.filter(ImageFilter.GaussianBlur(200))
base = Image.composite(base, Image.new('RGB', (W,H), (200,170,140)), v)

draw = ImageDraw.Draw(base)

# Draw desk
desk_h = int(H * 0.28)
draw.rectangle([(0, H - desk_h), (W, H)], fill=(190,150,110))
# desk shadow
draw.rectangle([(0, H - desk_h), (W, H - desk_h + 20)], fill=(160,120,90))

# Draw monitor
mon_w, mon_h = 520, 300
mon_x, mon_y = W//2 - mon_w//2, H - desk_h - mon_h - 30
draw.rounded_rectangle([(mon_x, mon_y), (mon_x+mon_w, mon_y+mon_h)], radius=20, fill=(245,235,225))
# screen inner
draw.rectangle([(mon_x+20, mon_y+20), (mon_x+mon_w-20, mon_y+mon_h-20)], fill=(210,180,150))
# monitor stand
draw.rectangle([(mon_x+mon_w//2-20, mon_y+mon_h), (mon_x+mon_w//2+20, mon_y+mon_h+60)], fill=(160,120,90))
# base
draw.rectangle([(mon_x+mon_w//2-80, mon_y+mon_h+60), (mon_x+mon_w//2+80, mon_y+mon_h+70)], fill=(140,100,70))

# Draw simple anime-style character silhouette at left
cx, cy = W//2 - 380, H - desk_h - 60
# head
draw.ellipse([(cx-40, cy-160), (cx+40, cy-80)], fill=(60,40,30))
# hair simple spikes
hair = [(cx-48, cy-140), (cx-20, cy-170), (cx+2, cy-150), (cx+26, cy-175), (cx+48, cy-145), (cx+40, cy-120), (cx-40, cy-120)]
draw.polygon(hair, fill=(40,26,20))
# body
draw.rounded_rectangle([(cx-60, cy-80), (cx+60, cy+40)], radius=30, fill=(85,60,45))
# arm resting on desk
draw.rectangle([(cx+60, cy-30), (cx+160, cy+10)], fill=(85,60,45))

# Soft blur to simulate painted background
bg = base.filter(ImageFilter.GaussianBlur(1.2))

# Slight paper texture overlay
import random
tex = Image.new('RGBA', (W, H), (0,0,0,0))
td = ImageDraw.Draw(tex)
for i in range(3000):
    x = random.randint(0, W)
    y = random.randint(0, H)
    td.point((x,y), fill=(255,250,240,int(random.randint(4,12))))

combined = Image.alpha_composite(bg.convert('RGBA'), tex)

# Save
out_path = 'c:\\Users\\labadmin\\Desktop\\AISWE\\AG-AISOFTDEV\\background.png'
combined.convert('RGB').save(out_path, format='PNG')
print('Saved', out_path)
