import mobdb

print("Content-type: text/html; charset=utf-8")
print()

print('<h2>Таблицы</h2>')
for en_entity, ru_entity in mobdb.entities.items():
    print(f'<a href=/cgi-bin/tableDetail.py?table={en_entity}>{ru_entity}</a><br>')