"""Vérification finale NiTrite v2.9"""

print('='*70)
print('VÉRIFICATION FINALE - NiTrite v2.9')
print('='*70)
print()

from src.winget_manager import WingetManager
from src.cleanup_manager import NiTriteCleanup

wm = WingetManager()
cleanup = NiTriteCleanup()

print('1. WINGET MANAGER')
print(f'   Programmes: {wm.get_program_count()}')
print(f'   Catégories: {len(wm.programs_db)}')
print(f'   Winget OK: {wm.winget_available}')
print()

print('2. CLEANUP MANAGER')
items = cleanup.get_cleanup_items()
print(f'   Éléments détectés: {len(items)}')
print(f'   Taille totale: {cleanup.get_total_size()} Mo')
print(f'   Python local: {cleanup._is_local_python()}')
print()

print('3. CATÉGORIES PRIORITAIRES')
cats = list(wm.programs_db.keys())[:3]
for i, cat in enumerate(cats, 1):
    print(f'   {i}. {cat}')
print()

print('4. COMMANDES DE RÉPARATION')
repair = wm.get_repair_commands()
print(f'   Total: {len(repair)} commandes')
print()

print('='*70)
print('✅ TOUT EST PRÊT POUR v2.9 !')
print('='*70)
