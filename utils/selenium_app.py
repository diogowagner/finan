from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Configuração do WebDriver
driver = webdriver.Chrome()  # Certifique-se de que o ChromeDriver está no PATH ou configure o caminho completo.

try:
    # 1. Acessar a página inicial e fazer login
    driver.get("http://127.0.0.1:8000/")
    
    # Preencha o formulário de login (ajuste os seletores de acordo com o HTML da página de login)
    username_field = driver.find_element(By.NAME, "username")  # Substitua pelo atributo real (id, name, etc.)
    password_field = driver.find_element(By.NAME, "password")  # Substitua pelo atributo real
    
    username_field.send_keys("teste")
    password_field.send_keys("Finanteste@")
    password_field.send_keys(Keys.RETURN)  # Pressiona Enter para submeter o formulário

    # Aguarde o carregamento da página pós-login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "clientebusca_top"))  # Ajuste o seletor para algo que aparece após o login
    )

    # 2. Navegar para a página de adição de receita
    driver.get("http://127.0.0.1:8000/adicionar/RECEITA/")

    # Aguarde o carregamento do formulário
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "lForm"))
    )

    # 3. Preencher o formulário
    # Situação
    driver.find_element(By.ID, "id_situacao_0").click()  # "Pago"
    
    # Data de lançamento
    data_lancamento = driver.find_element(By.ID, "id_data_lancamento")
    data_lancamento.send_keys("18-01-2025")
    
    # Conta
    conta_select = Select(driver.find_element(By.ID, "id_conta"))
    conta_select.select_by_index(1)
    
    # Descrição
    descricao = driver.find_element(By.ID, "id_descricao")
    descricao.send_keys("Descrição de exemplo")
    
    # Valor
    valor = driver.find_element(By.ID, "id_valor")
    valor.send_keys("1000,00")
    
    # Categoria
    categoria_select = Select(driver.find_element(By.ID, "id_categoria"))
    categoria_select.select_by_index(1)

    # Centro de custo/lucro (opcional)
    # centro_custo_select = driver.find_element(By.ID, "id_centro_custo_lucro")
    # centro_custo_select.send_keys(Keys.ARROW_DOWN)  # Ajuste para selecionar a opção correta
    
    # Observações
    observacoes = driver.find_element(By.ID, "id_observacoes")
    observacoes.send_keys("Observação de teste")
    
    # 4. Submeter o formulário
    submit_button = driver.find_element(By.XPATH, "//button[text()='Gravar']")
    submit_button.click()

    # Verifique o redirecionamento ou mensagem de sucesso
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "alert-success"))  # Ajuste para o seletor correto
    )
    print("Formulário preenchido e enviado com sucesso!")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Fechar o navegador
    driver.quit()
