import csv
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService


def process_products(driver, category_link, current_page, writer):
    while True:
        # Construye la URL de la página de producto actual
        product_url = f"{category_link}page/{current_page}/"

        # Abre la página de producto en Microsoft Edge
        driver.get(product_url)

        try:
            # Encuentra todos los enlaces de los productos en la página
            product_links = [
                a.get_attribute("href")
                for a in driver.find_elements(
                    By.CSS_SELECTOR, "a.woocommerce-LoopProduct-link"
                )
            ]

            if not product_links:
                break  # Si no hay más productos en la página, sal del bucle

            for product_link in product_links:
                # Abre la página del producto individual
                driver.get(product_link)
                time.sleep(2)

                try:
                    # Encuentra el identificador y la URL de la imagen del producto
                    identificador_element = driver.find_element(By.CLASS_NAME, "sku")
                    img_element = driver.find_element(
                        By.CLASS_NAME, "attachment-shop_single"
                    )

                    identificador = (
                        identificador_element.text.strip()
                        if identificador_element
                        else ""
                    )
                    img_url = img_element.get_attribute("src") if img_element else ""

                    writer.writerow(
                        {
                            "identificador": identificador,
                            "URL de la imagen": img_url,
                        }
                    )

                    print(f"Introducido {identificador} con IMAGEN {img_url} en el CSV")

                except Exception as e:
                    print(f"Error al obtener información del producto: {str(e)}")

            current_page += 1  # Avanza a la siguiente página

        except Exception as e:
            print(f"Error al obtener información de la página {product_url}: {str(e)}")


# URL de la página web
base_url = "https://sateliterover.com/categoria-producto/mas-productos-sin-categoria/"
current_page = 1

# Nombre del archivo CSV a exportar
namecsvexport = "productos-con-imagen.csv"

# Configura el controlador de Microsoft Edge
edge_options = EdgeOptions()
edge_options.use_chromium = True
edge_driver_path = "C:/Users/danim/Desktop/CHROMEDRIVER/msedgedriver.exe"

# Crea una instancia del controlador de Microsoft Edge
try:
    driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=edge_options)
except Exception as e:
    print(f"Error al iniciar el controlador de Microsoft Edge: {str(e)}")
    exit()

try:
    with open(namecsvexport, mode="w", newline="") as csv_file:
        fieldnames = ["identificador", "URL de la imagen"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        # Navega a la página principal
        driver.get(base_url)

        # Encuentra todos los elementos de categorías
        category_elements = driver.find_elements(By.CLASS_NAME, "product-category")

        if category_elements and len(category_elements) > 1:
            # Si existen categorías y hay más de una, procesa cada categoría
            category_links = [
                category_element.find_element(By.TAG_NAME, "a").get_attribute("href")
                for category_element in category_elements
            ]

            for category_link in category_links:
                # Abre la página de categoría individual
                driver.get(category_link)
                time.sleep(2)
                current_page = 1

                process_products(driver, category_link, current_page, writer)

        else:
            # Si no hay categorías o solo hay una, procesa directamente los productos en la página base
            current_page = 1
            process_products(driver, base_url, current_page, writer)

        print(f"Los datos se han exportado a {namecsvexport}")

except Exception as e:
    print(f"Error: {str(e)}")

# Cierra el navegador
driver.quit()
