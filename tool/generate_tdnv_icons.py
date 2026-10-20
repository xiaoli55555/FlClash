from pathlib import Path

from PIL import Image, ImageDraw, ImageOps

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / 'android/app/src/main/res'
SOURCE = ROOT / 'assets/images/tdnv.png'

with Image.open(SOURCE) as original:
    original.load()
    if min(original.size) < 512:
        raise ValueError('tdnv.png must be at least 512 pixels on each side')
    image = ImageOps.fit(original.convert('RGB'), (1024, 1024), method=Image.Resampling.LANCZOS)

image.save(ROOT / 'assets/images/icon.png')
image.resize((512, 512), Image.Resampling.LANCZOS).save(
    ROOT / 'android/app/src/main/ic_launcher-playstore.png',
)

for density, size in {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}.items():
    icon = image.resize((size, size), Image.Resampling.LANCZOS)
    folder = RES / f'mipmap-{density}'
    folder.mkdir(parents=True, exist_ok=True)
    icon.save(folder / 'ic_launcher.webp', lossless=True)
    mask = Image.new('L', (size * 4, size * 4))
    ImageDraw.Draw(mask).ellipse((0, 0, size * 4 - 1, size * 4 - 1), fill=255)
    rounded = icon.convert('RGBA')
    rounded.putalpha(mask.resize((size, size), Image.Resampling.LANCZOS))
    rounded.save(folder / 'ic_launcher_round.webp', lossless=True)
    tv_folder = RES / f'mipmap-television-{density}'
    tv_folder.mkdir(parents=True, exist_ok=True)
    icon.save(tv_folder / 'ic_launcher.webp', lossless=True)

background = image.getpixel((0, 0))
adaptive = Image.new('RGB', (432, 432), background)
symbol = image.resize((336, 336), Image.Resampling.LANCZOS)
adaptive.paste(symbol, (48, 48))
drawable = RES / 'drawable-nodpi'
drawable.mkdir(parents=True, exist_ok=True)
adaptive.save(drawable / 'tdnv_launcher.png')
background_hex = '#{:02X}{:02X}{:02X}'.format(*background)
(RES / 'values/ic_launcher_background.xml').write_text(
    f'<resources><color name="ic_launcher_background">{background_hex}</color></resources>\n',
    encoding='utf-8',
)
xml = '''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/tdnv_launcher"/>
</adaptive-icon>
'''
for path in (
    RES / 'mipmap-anydpi-v26/ic_launcher.xml',
    RES / 'mipmap-anydpi-v26/ic_launcher_round.xml',
    RES / 'mipmap-television-anydpi-v26/ic_launcher.xml',
):
    path.write_text(xml, encoding='utf-8')

banner = Image.new('RGB', (320, 180), background)
banner.paste(image.resize((180, 180), Image.Resampling.LANCZOS), (70, 0))
banner.save(RES / 'mipmap-xhdpi/ic_banner.png')
print('Generated tdnv launcher icons, adaptive icons, TV banner and Flutter icon')
