from src.winget_manager import WingetManager

wm = WingetManager()

print("=" * 70)
print(f"✅ TOTAL: {wm.get_program_count()} PROGRAMMES")
print("=" * 70)
print()

for category, programs in wm.programs_db.items():
    print(f"\n📁 {category.upper()} ({len(programs)} programmes)")
    print("-" * 70)
    for name in sorted(programs.keys()):
        print(f"  ✓ {name}")

print("\n" + "=" * 70)
print(f"✅ TOUS LES PROGRAMMES ONT ÉTÉ AJOUTÉS AVEC SUCCÈS !")
print("=" * 70)
