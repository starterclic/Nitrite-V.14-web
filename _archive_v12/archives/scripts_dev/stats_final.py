#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

d = json.load(open('data/programs.json', encoding='utf-8'))
total = sum(len(p) for p in d.values())
winget = sum(1 for c in d.values() for p in c.values() if p.get('winget_id'))
url = sum(1 for c in d.values() for p in c.values() if p.get('download_url') and p.get('download_url') != 'winget')

print(f'\n🎯 STATISTIQUES FINALES')
print(f'{'='*50}')
print(f'Total: {total} programmes')
print(f'Winget: {winget} ({winget/total*100:.1f}%)')
print(f'URLs directes: {url} ({url/total*100:.1f}%)')
print(f'{'='*50}')
print(f'🏆 SCORE DE QUALITÉ: {(winget+url)/total*100:.1f}%\n')
