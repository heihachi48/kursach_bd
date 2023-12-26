import cgi

import mobdb

form = cgi.FieldStorage()
table_name = form.getvalue('table')

conn = mobdb.open_connection()

if form.getvalue('last_row') is not None:
    params = [int(form.getvalue('last_row')) + 1]
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID': continue
        params.append(form.getvalue(tag))
    mobdb.insert(conn, table_name, params)

if form.getvalue('last_upd_row') is not None:
    params = [form.getvalue(x) for x in mobdb.ru_columns[table_name] if x != 'ID']
    mobdb.update_row_form(conn, table_name, params, form.getvalue('upd_row'))

if form.getvalue('del_line') is not None:
    mobdb.delete_row_from(conn, table_name, form.getvalue('del_line'))

data = mobdb.select_all_from(conn, table_name)
# conn.close()

print("Content-type: text/html; charset=utf-8")
print()

print('<table>')

print(f'<caption><h2>{mobdb.entities[table_name]}</h2></caption>')
print('<tr>')
for column in mobdb.ru_columns[table_name]:
    print(f'<th>{column}</th>')
print('<tr>')

for record in data:
    print('<tr>')
    i = -1
    for obj in record:
        print(f'<td>{obj}</td>')
    print(f'<td><a href="/cgi-bin/updateRecord.py?table={table_name}&upd_line={record[0]}">изменить</a></td>')
    print(f'<td><a href="/cgi-bin/tableDetail.py?table={table_name}&del_line={record[0]}">удалить</a></td>')
    print('</tr>')


print('<tr>')
print('<td>-</td>')

print(f'<form action="/cgi-bin/tableDetail.py?table={table_name}&last_row={data[len(data) - 1][0]}" method="POST">')
if table_name == 'rate':
    tags = mobdb.ru_columns[table_name]

    print(f'<td><select name={tags[1]} style="width: 100%;">')
    for equipment in mobdb.select_all_from(conn, 'equipment'):
        print(f'<option value="{equipment[0]}">{f"{equipment[0]} {equipment[4]}"}</option>')
    print('</select></td>')

    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-оборудования': continue
        print(f'<td><input type="text" name="{tag}" /></td>')

elif table_name == 'subscribe':
    tags = mobdb.ru_columns[table_name]

    print(f'<td><select name={tags[1]} style="width: 100%;" >')
    for rate in mobdb.select_all_from(conn, 'rate'):
        print(f'<option value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
    print('</select></td>')

    print(f'<td><select name={tags[2]} style="width: 100%;">')
    for client in mobdb.select_all_from(conn, 'client'):
        print(f'<option value="{client[0]}">{f"{client[0]} {client[2]}"}</option>')
    print('</select></td>')

    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-тарифа' or tag == 'ID-клиента': continue
        print(f'<td><input type="text" name="{tag}" /></td>')

elif table_name == 'price_list':
    tags = mobdb.ru_columns[table_name]

    print(f'<td><select name={tags[1]} style="width: 100%;">')
    for rate in mobdb.select_all_from(conn, 'rate'):
        print(f'<option value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
    print('</select></td>')

    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-тарифа': continue
        print(f'<td><input type="text" name="{tag}" /></td>')


else:
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID': continue
        print(f'<td><input type="text" name="{tag}" /></td>')
print(f'<td><button type="submit">добавить</button></td>')
print('</form>')

print('</tr>')

print('</table>')

print('<br>')
print(f'<a href="/cgi-bin/index.py">На главную</a>')

conn.close()