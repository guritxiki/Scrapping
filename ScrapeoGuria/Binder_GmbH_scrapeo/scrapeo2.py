from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_with_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get("https://www.binder-world.com/int-es/productos/incubadoras/incubadoras-estandar/producto/b-28")
    
    # Esperar un poco a que la página cargue
    time.sleep(5)

    # Buscar todos los elementos que contienen el <span class="accordion-icon">
    accordion_icons = driver.find_elements(By.CLASS_NAME, "accordion-icon")
    
    # Verificar si se encuentran los iconos
    if not accordion_icons:
        print("No se encontraron elementos con la clase 'accordion-icon'.")
    else:
        print(f"Se encontraron {len(accordion_icons)} iconos de acordeón.")
    
    # Inicializar ActionChains
    action = ActionChains(driver)

    for icon in accordion_icons:
        try:
            # Desplazar al <span class="accordion-icon">
            driver.execute_script("arguments[0].scrollIntoView(true);", icon)
            time.sleep(1)  # Esperar para asegurar que el desplazamiento ha terminado
            action.move_to_element(icon).click().perform()  # Usar ActionChains para hacer clic
            print("Se hizo clic en el icono de acordeón.")
            time.sleep(2)  # Esperar un poco más para asegurar que el contenido se carga
        except Exception as e:
            print(f"Error al interactuar con el icono de acordeón: {e}")
    
    # Espera adicional para asegurarse de que las interacciones hayan cargado nuevos contenidos
    time.sleep(3)
    
    # Ahora, proceder a extraer las tablas
    tables = driver.find_elements(By.TAG_NAME, "table")
    
    # Verificar si se encontraron tablas
    if not tables:
        print("No se encontraron tablas en la página.")
    else:
        print(f"Se encontraron {len(tables)} tablas en la página.")
    
    # Crear una lista para almacenar los DataFrames de las tablas
    table_data = []
    
    for table in tables:
        # Extraer las filas de la tabla
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Procesar las filas y extraer los datos
        table_rows = []
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            cols_text = [col.text.strip() for col in cols if col.text.strip()]  # Filtrar celdas vacías
            if cols_text:  # Añadir solo las filas que contienen datos
                table_rows.append(cols_text)
        
        # Crear un DataFrame con las filas de la tabla
        if table_rows:
            df = pd.DataFrame(table_rows)
            table_data.append(df)
    
    driver.quit()
    return table_data

# Llamar a la función y obtener las tablas
tables = scrape_with_selenium()

# Mostrar cada tabla completa
if tables:
    for i, table in enumerate(tables):
        print(f"\nTabla {i+1}:")
        print(table)
else:
    print("No se encontraron tablas.")
