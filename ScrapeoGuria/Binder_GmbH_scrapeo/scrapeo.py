from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_with_selenium():
    driver = webdriver.Chrome()  # Asegúrate de tener el controlador de Chrome instalado
    driver.get("https://www.binder-world.com/int-es/productos/camaras-climaticas/camaras-clima-constante/lista-productos-clima-constante")
    
    time.sleep(5)  # Espera a que se carguen los datos
    # Encuentra y procesa los elementos relevantes en la página
    products = driver.find_elements(By.CSS_SELECTOR, ".product-item")  # Cambia el selector según el HTML
    prod_list = []
    for product in products:
        print(product.text)
        prod_list.append(product)
    
    driver.quit()
    return prod_list

prod_list = scrape_with_selenium()

df = pd.DataFrame(columns=["Producto"])
df["Producto"] = prod_list
df.head()
