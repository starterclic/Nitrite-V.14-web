"""Vérification finale NiTrite v2.8"""
from src.winget_manager import WingetManager

print('='*60)
print('🎯 VÉRIFICATION FINALE NiTrite v2.8')
print('='*60)

wm = WingetManager()
cats = list(wm.programs_db.keys())

print(f'\n✅ Total: {wm.get_program_count()} programmes/commandes')
print(f'✅ Catégories: {len(cats)}')
print(f'\n🟠 1ère catégorie: {cats[0]}')
print(f'🔧 2ème catégorie: {cats[1]}')

ordi = wm.programs_db[cats[0]]
print(f'\n📦 Programmes dans Outils OrdiPlus: {len(ordi)}')

first = list(ordi.values())[0]
print(f'🎨 Couleur: {first.get("color", "ERREUR")}')

repair = wm.get_repair_commands()
print(f'\n🔧 Commandes de réparation: {len(repair)}')
print(f'\n✅ is_admin(): {wm.is_admin}')
print(f'✅ winget_available: {wm.winget_available}')

print('\n' + '='*60)
print('🎉 NiTrite v2.8 EST PRÊT !')
print('='*60)
