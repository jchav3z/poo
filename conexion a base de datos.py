# pip install db-sqlite3

import sqlite3

with sqlite3.connect('tienda.db') as conn:
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT,
            impuesto REAL,
            proveedor TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ventas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_producto TEXT,
            nombre_producto TEXT,
            cantidad INTEGER,
            subtotal REAL
        )
    ''')

    def buscar_producto(codigo):
        cursor.execute('SELECT codigo, nombre, impuesto FROM productos WHERE codigo = ?', (codigo,))
        return cursor.fetchone()

    def agregar_venta(codigo, cantidad):
        producto = buscar_producto(codigo)
        if producto:
            codigo, nombre, impuesto = producto
            subtotal = cantidad * impuesto
            cursor.execute('''
                INSERT INTO ventas (codigo_producto, nombre_producto, cantidad, subtotal)
                VALUES (?, ?, ?, ?)
            ''', (codigo, nombre, cantidad, subtotal))
            conn.commit()
            print("Venta agregada con éxito.")
        else:
            print("Producto no encontrado.")

    def visualizar_venta():
        cursor.execute('SELECT SUM(subtotal) FROM ventas')
        total_venta = cursor.fetchone()[0] or 0 
        iva = total_venta * 0.16
        print(f'Total de la venta: {total_venta:.2f}')
        print(f'Impuesto (IVA): {iva:.2f}')

    def agregar_producto(codigo, nombre, impuesto, proveedor):
        cursor.execute('''
            INSERT INTO productos (codigo, nombre, impuesto, proveedor)
            VALUES (?, ?, ?, ?)
        ''', (codigo, nombre, impuesto, proveedor))
        conn.commit()
        print("Producto agregado con éxito.")

    def cerrar_caja():
        cursor.execute('DELETE FROM ventas')
        conn.commit()
        print("Caja cerrada. Registros de ventas eliminados.")

    agregar_producto('12345', 'Producto A', 0.10, 'Proveedor X')
    agregar_producto('67890', 'Producto B', 0.08, 'Proveedor Y')
    agregar_venta('12345', 5)
    agregar_venta('67890', 3)
    visualizar_venta()
    cerrar_caja()
