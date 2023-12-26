import cgi

import mobdb

form = cgi.FieldStorage()
table_name = form.getvalue('table')
row_number = form.getvalue('upd_line')

conn = mobdb.open_connection()

row_data = mobdb.select_row_from(conn, table_name, row_number)
data = mobdb.select_all_from(conn, table_name)

print("Content-type: text/html; charset=utf-8")
print()

print('<table>')
print(f'<tr><td>{mobdb.ru_columns[table_name][0]}</td><td>{row_number}</td></tr>')

print(f'<form action="/cgi-bin/tableDetail.py?table={table_name}&upd_row={row_number}&last_upd_row={data[0]}" method="POST">')
if table_name == 'rate':
    tags = mobdb.ru_columns[table_name]

    i = 0
    join_row = row_data[1]
    print(f'<tr><td>{mobdb.ru_columns[table_name][1]}</td>')
    print(f'<td><select name={tags[1]} style="width: 100%;">')
    for equipment in mobdb.select_all_from(conn, 'equipment'):
        i += 1
        if i == join_row:
            print(f'<option selected value="{equipment[0]}">{f"{equipment[0]} {equipment[4]}"}</option>')
            continue
        print(f'<option value="{equipment[0]}">{f"{equipment[0]} {equipment[4]}"}</option>')
    print('</select></td></tr>')

    i = 2
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-оборудования': continue
        print(f'<tr><td>{mobdb.ru_columns[table_name][i]}</td><td><input type="text" name="{tag}" value="{row_data[i]}"/></td></tr>')
        i += 1

elif table_name == 'subscribe':
    tags = mobdb.ru_columns[table_name]

    i = 0
    join_row = row_data[1]
    print(f'<tr><td>{mobdb.ru_columns[table_name][1]}</td>')
    print(f'<td><select name={tags[1]} style="width: 100%;" >')
    for rate in mobdb.select_all_from(conn, 'rate'):
        i += 1
        if i == join_row:
            print(f'<option selected value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
        print(f'<option value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
    print('</select></td></tr>')

    i = 0
    join_row = row_data[2]
    print(f'<tr><td>{mobdb.ru_columns[table_name][2]}</td>')
    print(f'<td><select name={tags[2]} style="width: 100%;">')
    for client in mobdb.select_all_from(conn, 'client'):
        i += 1
        if i == join_row:
            print(f'<option selected value="{client[0]}">{f"{client[0]} {client[2]}"}</option>')
        print(f'<option value="{client[0]}">{f"{client[0]} {client[2]}"}</option>')
    print('</select></td></tr>')

    i = 3
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-тарифа' or tag == 'ID-клиента': continue
        print(f'<tr><td>{mobdb.ru_columns[table_name][i]}</td><td><input type="text" name="{tag}" value="{row_data[i]}"/></td></tr>')
        i += 1

elif table_name == 'price_list':
    tags = mobdb.ru_columns[table_name]

    i = 0
    join_row = row_data[1]
    print(f'<tr><td>{mobdb.ru_columns[table_name][1]}</td>')
    print(f'<td><select name={tags[1]} style="width: 100%;">')
    for rate in mobdb.select_all_from(conn, 'rate'):
        i += 1
        if i == join_row:
            print(f'<option selected value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
        print(f'<option value="{rate[0]}">{f"{rate[0]} {rate[3]}"}</option>')
    print('</select></td></tr>')

    i = 2
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID' or tag == 'ID-тарифа': continue
        print(f'<tr><td>{mobdb.ru_columns[table_name][i]}</td><td><input type="text" name="{tag}" value="{row_data[i]}"/></td></tr>')
        i += 1


else:
    i = 1
    for tag in mobdb.ru_columns[table_name]:
        if tag == 'ID': continue
        print(f'<tr><td>{mobdb.ru_columns[table_name][i]}</td><td><input type="text" name="{tag}" value="{row_data[i]}"/></td></tr>')
        i += 1
print(f'<td><button type="submit">Обновить</button></td>')
print('</form>')

print('</tr>')

print('</table>')

print('<br>')
print(f'<a href="/cgi-bin/tableDetail.py?table={table_name}">Назад</a>')

conn.close()