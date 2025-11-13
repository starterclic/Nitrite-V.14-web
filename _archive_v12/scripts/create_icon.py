#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de création d'icône pour NiTriTe V12.0
Crée une icône avec "NiTriTe" en arrière-plan et "V12" au premier plan
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_nitrite_icon():
    """Crée l'icône NiTriTe V12.0"""

    # Dimensions de l'icône (256x256 pour haute qualité)
    size = 256

    # Créer une image avec fond transparent
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Couleurs (thème NiTriTe)
    bg_color = (15, 15, 15, 255)  # Noir profond
    orange = (255, 107, 0, 255)   # Orange Ordi Plus
    orange_light = (255, 133, 51, 180)  # Orange clair avec opacité

    # Fond arrondi
    draw.rounded_rectangle([(10, 10), (246, 246)], radius=30, fill=bg_color)

    # Bordure orange
    draw.rounded_rectangle([(10, 10), (246, 246)], radius=30, outline=orange, width=4)

    try:
        # Essayer d'utiliser une police système
        try:
            # Police pour "NiTriTe" (arrière-plan)
            font_back = ImageFont.truetype("arial.ttf", 40)
            # Police pour "V12" (premier plan)
            font_front = ImageFont.truetype("arial.ttf", 80)
        except:
            # Si Arial n'est pas disponible, essayer Segoe UI
            try:
                font_back = ImageFont.truetype("segoeui.ttf", 40)
                font_front = ImageFont.truetype("seguibl.ttf", 80)
            except:
                # Utiliser la police par défaut
                font_back = ImageFont.load_default()
                font_front = ImageFont.load_default()
    except:
        font_back = ImageFont.load_default()
        font_front = ImageFont.load_default()

    # Texte "NiTriTe" en arrière-plan (haut)
    text_back = "NiTriTe"
    bbox_back = draw.textbbox((0, 0), text_back, font=font_back)
    text_width_back = bbox_back[2] - bbox_back[0]
    text_height_back = bbox_back[3] - bbox_back[1]
    x_back = (size - text_width_back) // 2
    y_back = 50

    # Dessiner "NiTriTe" avec ombre
    draw.text((x_back + 2, y_back + 2), text_back, font=font_back, fill=(0, 0, 0, 150))
    draw.text((x_back, y_back), text_back, font=font_back, fill=orange)

    # Texte "V12" au premier plan (centre) avec opacité légère
    text_front = "V12"
    bbox_front = draw.textbbox((0, 0), text_front, font=font_front)
    text_width_front = bbox_front[2] - bbox_front[0]
    text_height_front = bbox_front[3] - bbox_front[1]
    x_front = (size - text_width_front) // 2
    y_front = (size - text_height_front) // 2 + 10

    # Dessiner "V12" avec ombre et opacité
    draw.text((x_front + 3, y_front + 3), text_front, font=font_front, fill=(0, 0, 0, 100))
    draw.text((x_front, y_front), text_front, font=font_front, fill=orange_light)

    # Petit badge en bas
    badge_text = ".0"
    try:
        font_badge = ImageFont.truetype("arial.ttf", 30)
    except:
        font_badge = ImageFont.load_default()

    bbox_badge = draw.textbbox((0, 0), badge_text, font=font_badge)
    text_width_badge = bbox_badge[2] - bbox_badge[0]
    x_badge = (size - text_width_badge) // 2
    y_badge = 180

    draw.text((x_badge + 2, y_badge + 2), badge_text, font=font_badge, fill=(0, 0, 0, 150))
    draw.text((x_badge, y_badge), badge_text, font=font_badge, fill=(255, 214, 0, 200))

    # Sauvegarder en PNG haute qualité
    assets_dir = "assets"
    os.makedirs(assets_dir, exist_ok=True)

    png_path = os.path.join(assets_dir, "icon_nitrite_v12.png")
    img.save(png_path, 'PNG')
    print(f"✅ Icône PNG créée : {png_path}")

    # Créer plusieurs tailles pour l'ICO (Windows)
    sizes = [256, 128, 64, 48, 32, 16]
    images = []

    for s in sizes:
        resized = img.resize((s, s), Image.Resampling.LANCZOS)
        images.append(resized)

    # Sauvegarder en ICO
    ico_path = os.path.join(assets_dir, "icon.ico")
    images[0].save(ico_path, format='ICO', sizes=[(s, s) for s in sizes])
    print(f"✅ Icône ICO créée : {ico_path}")

    print("\n🎨 Icônes créées avec succès !")
    print(f"   📄 PNG : {png_path}")
    print(f"   📄 ICO : {ico_path}")
    print("\nCaractéristiques :")
    print("   - Fond : Noir profond avec bordure orange")
    print("   - Arrière-plan : 'NiTriTe' en orange vif")
    print("   - Premier plan : 'V12' en orange avec opacité légère")
    print("   - Badge : '.0' en jaune or")

if __name__ == "__main__":
    print("=" * 60)
    print("  🎨 Création de l'icône NiTriTe V12.0")
    print("=" * 60)
    print()

    create_nitrite_icon()

    print()
    print("=" * 60)
