import json

d = json.load(open('/Users/jens/Documents/git/beamtenanwaertertool/besoldungsdaten.json'))

compact = {}
for bl, entries in d.items():
    bl_data = []
    for e in entries:
        if e['grundbezuege'] == 0:
            continue
        bl_data.append([
            e['dienstgrad'],
            e['besoldungsgruppe'],
            round(e['grundbezuege'], 2),
            round(e['famZuschlag'], 2),
            round(e['vl'], 2),
            round(e['lst_ledig'], 2),
            round(e['soli_ledig'], 2),
            round(e['kist_ledig'], 2),
            round(e['lst_verh'], 2),
            round(e['soli_verh'], 2),
            round(e['kist_verh'], 2),
        ])
    compact[bl] = bl_data

result = json.dumps(compact, ensure_ascii=False, separators=(',', ':'))
print(f'Compact size: {len(result)} chars')
print(f'Entries: {sum(len(v) for v in compact.values())}')

with open('/Users/jens/Documents/git/beamtenanwaertertool/besoldung_compact.json', 'w') as f:
    f.write(result)
