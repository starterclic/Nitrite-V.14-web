"""
Création du logo Ordi Plus pour l'arrière-plan
"""
from PIL import Image, ImageDraw, ImageFont
import os

# Créer une image avec fond transparent - PLUS GRANDE
width, height = 800, 800
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Couleur orange Ordi Plus avec opacité BEAUCOUP PLUS VISIBLE pour l'arrière-plan
orange = (255, 107, 0, 100)  # #FF6B00 avec 100/255 d'opacité (~40%) - TRÈS VISIBLE
bleu = (0, 51, 102, 110)     # #003366 avec 110/255 d'opacité (~43%) - TRÈS VISIBLE

# Dessiner un logo stylisé "O+" plus grand
# Grand cercle pour "O"
circle_center = (400, 400)
circle_radius = 250
draw.ellipse([circle_center[0]-circle_radius, circle_center[1]-circle_radius,
              circle_center[0]+circle_radius, circle_center[1]+circle_radius],
             outline=orange, width=35)

# Deuxième cercle intérieur pour plus d'effet
inner_radius = 200
draw.ellipse([circle_center[0]-inner_radius, circle_center[1]-inner_radius,
              circle_center[0]+inner_radius, circle_center[1]+inner_radius],
             outline=bleu, width=25)

# Petit "+" en haut à droite du cercle
plus_x = 580
plus_y = 220
plus_size = 80
plus_width = 30
# Barre horizontale du +
draw.rectangle([plus_x-plus_size, plus_y-plus_width//2,
                plus_x+plus_size, plus_y+plus_width//2],
               fill=orange)
# Barre verticale du +
draw.rectangle([plus_x-plus_width//2, plus_y-plus_size,
                plus_x+plus_width//2, plus_y+plus_size],
               fill=orange)

# Sauvegarder
output_path = os.path.join(os.path.dirname(__file__), 'logo_ordiplus_bg.png')
img.save(output_path)
print(f"Logo créé : {output_path}")
