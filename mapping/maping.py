import os

import pandas as pd

try:
    # Cargar los archivos CSV
    softline = pd.read_csv('softline.csv')
    productos = pd.read_csv('productos.csv')

    # Definir el nombre de las columnas de coste y PVP en cada DataFrame
    columna_coste = 'coste'
    columna_pvp = 'pvp'

    # Comprobar si existe el archivo netos.csv
    if os.path.exists('netos.csv'):
        netos = pd.read_csv('netos.csv')
        
        # Realizar la combinación (mapeo) basado en la columna común con netos.csv
        merged_data = pd.merge(softline, productos, on='campo-mapeo', how='left')
        
        if 'campo-mapeo' in netos.columns:
            netos_subset = netos[['campo-mapeo', columna_coste, columna_pvp]]
            netos_subset['EsNeto'] = 'SI'
            merged_data = pd.merge(merged_data, netos_subset, on='campo-mapeo', how='left')
            merged_data['EsNeto'].fillna('NO', inplace=True)
            
            # Asegurar que las columnas de coste y PVP de netos tengan prioridad
            merged_data['coste'] = merged_data.apply(lambda x: x[columna_coste + '_y'] if pd.notnull(x[columna_coste + '_y']) else x[columna_coste + '_x'], axis=1)
            merged_data['pvp'] = merged_data.apply(lambda x: x[columna_pvp + '_y'] if pd.notnull(x[columna_pvp + '_y']) else x[columna_pvp + '_x'], axis=1)
            merged_data.drop([columna_coste + '_x', columna_coste + '_y', columna_pvp + '_x', columna_pvp + '_y'], axis=1, inplace=True)
        
    else:
        # Realizar la combinación (mapeo) basado solo en productos.csv y softline.csv
        merged_data = pd.merge(softline, productos, on='campo-mapeo', how='left')

        # Definir columnas 'coste' y 'pvp' de acuerdo a las prioridades
        merged_data['coste'] = merged_data.apply(lambda x: x[columna_coste + '_y'] if pd.notnull(x[columna_coste + '_y']) else x[columna_coste + '_x'], axis=1)
        merged_data['pvp'] = merged_data.apply(lambda x: x[columna_pvp + '_y'] if pd.notnull(x[columna_pvp + '_y']) else x[columna_pvp + '_x'], axis=1)
        merged_data.drop([columna_coste + '_x', columna_coste + '_y', columna_pvp + '_x', columna_pvp + '_y'], axis=1, inplace=True)

    # Crear columna Softline SI y establecer valores
    merged_data['Softline SI'] = 'NO'
    merged_data.loc[(merged_data['campo-mapeo'].isin(softline['campo-mapeo'])) & 
                    (~merged_data['campo-mapeo'].isin(productos['campo-mapeo'])), 'Softline SI'] = 'SI'

    # Guardar el resultado en un nuevo archivo CSV
    merged_data.to_csv('resultado.csv', index=False)

except Exception as e:
    print(f"Ha ocurrido un error: {str(e)}")

input("Presiona la tecla espacio para salir...")
