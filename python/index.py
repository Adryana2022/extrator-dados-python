# Autor: Adriana Almeida

#importando as bibliotecas
from bs4 import BeautifulSoup
import requests
import csv


#função para extrair os dados

def extrair_dados_postagem(postagem):
    titulo_elemento = postagem.find("h3")
    titulo = titulo_elemento.text.strip() if titulo_elemento else "N/A"

    data_elemento = postagem.find("span", class_="metaText metaDate")
    data = data_elemento.abbr["title"] if data_elemento else "Nada/consta"

    resumo_elemento = postagem.find("p")
    resumo = resumo_elemento.text.strip() if resumo_elemento else "Nada/consta"

    return {"Título": titulo, "Data": data, "Resumo": resumo}


#tratamento de erros
def extrair_postagens(url, quantidade):
    try:
        resposta = requests.get(url)
        resposta.raise_for_status()  # Verifica se ocorreu algum erro na solicitação HTTP
        soup = BeautifulSoup(resposta.text, "html.parser")
        postagens = soup.find_all("article")[:quantidade]

        lista_postagens = [extrair_dados_postagem(postagem) for postagem in postagens]
        return lista_postagens
    except requests.exceptions.RequestException as e:
        print(f"Erro ao fazer a solicitação HTTP: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

# função para salvar os dados em arquivo csv
def salvar_csv(lista_postagens, nome_arquivo):
    try:
        with open(nome_arquivo, "w", newline="", encoding="utf-8") as arquivo_csv:
            campos = ["Título", "Data", "Resumo"]
            escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos)
            escritor_csv.writeheader()
            escritor_csv.writerows(lista_postagens)
    except IOError as e:
        print(f"Erro ao salvar o arquivo CSV: {e}")


# Configurações de quantidade, url e nome do arquivo
url = "https://gizmodo.uol.com.br/"
quantidade_postagens = 10
nome_arquivo = "postagens.csv"

# Extração das postagens
lista_postagens = extrair_postagens(url, quantidade_postagens)

# Salvando os dados em um arquivo CSV
salvar_csv(lista_postagens, nome_arquivo)

print("Os dados foram extraídos e salvos no arquivo postagens.csv.")
