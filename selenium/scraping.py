from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

ruta = 'https://as.com/resultados/ficha/deportista/cristiano_ronaldo/14558/'

# Ingreso al sitio
driver = webdriver.Chrome()
driver.get(ruta)
wait = WebDriverWait(driver, 10)
print('Página cargada')

# Omisión del anuncio de Cookies
boton_rechazar = wait.until(
    EC.element_to_be_clickable((By.ID, "didomi-notice-disagree-button"))
)
boton_rechazar.click()
print('Omisión de anuncio de Cookies')

# Scrolleo para Cargado de Labels
contenedor_desplegables = wait.until(
    EC.presence_of_element_located(
        (By.ID, 'stats_selectors')
    )
)
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    contenedor_desplegables
)
print('Scrolleo estratégico')

# Seleccion de Real Madrid en ListOptions
menu_desplegable_team = wait.until(
    EC.element_to_be_clickable((
        By.ID,
        "active_team"
    ))
)
menu_desplegable_team.click()
opcion_equipo = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        '//a[@data-hash-component="real_madrid"]'
    ))
)
opcion_equipo.click()
print('Selección del Club: Real Madrid')

# Seleccion de Champions League en ListOptions
menu_desplegable_competition = wait.until(
    EC.element_to_be_clickable((
        By.ID,
        "active_competition"
    ))
)
menu_desplegable_competition.click()
opcion_competicion = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        '//a[@data-team-related="real_madrid" '
        'and @data-hash-component="champions"]'
    ))
)
opcion_competicion.click()
print('Selección de la Competición: Champions League')

# Selección de Temporada 2014/2015 en ListOptions
menu_desplegable_temporada = wait.until(
    EC.element_to_be_clickable((By.ID, "active_season"))
)
menu_desplegable_temporada.click()
opcion_temporada = wait.until(
    EC.element_to_be_clickable((
        By.XPATH,
        '//a[@data-team-related="real_madrid" '
        'and @data-competition-related="champions" '
        'and @data-hash-component="2014_2015"]'
    ))
)
opcion_temporada.click()
print("Selección de la Temporada: 2014/2015")

# Scrolleo para Cargado de Table
tabla_goleadora = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '/html/body/div[6]/div/div/div[2]/div[4]/div/div/div/table/thead')
    )
)
driver.execute_script(
    "arguments[0].scrollIntoView({block: 'center'});",
    tabla_goleadora
)
print('Scrolleo estratégico')

# Selección de las filas y columnas de la Tabla de Goles
filas_anuales = driver.find_elements(
    By.XPATH,
    "/html/body/div[6]/div/div/div[2]/div[4]/div/div/div/table/tbody/tr"
)
carrera = []
for fila_anual in filas_anuales:
    columnas = fila_anual.find_elements(By.XPATH, "./td | ./th")
    carrera.append([
        columnas[0].text, # Temporada
        columnas[1].text, # Equipo
        columnas[2].text, # Partidos
        columnas[4].text # Goles
    ])
print(carrera)

# Exportación usando Pandas
df_ronaldo = pd.DataFrame(
    carrera,
    columns=['Temporada', 'Equipo', 'Goles', 'Partidos']
)
df_ronaldo = df_ronaldo.replace({
    "M. United": "Manchester United",
    "Sp. Portugal": "Sporting CP"
})
df_ronaldo.to_csv(
    'carrera_ronaldo.csv',
    index=False, # Evita 0,1,2,3,4
    encoding='utf-8-sig' # Carácteres especiales
)
print('Archivo exportado en CSV')

time.sleep(2.5)
driver.quit()
print("Programa terminado")