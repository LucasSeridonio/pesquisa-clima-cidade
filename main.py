from bs4 import BeautifulSoup
from datetime import datetime
import requests

# Página inicial do ClimaTempo com a lista de cidades
pagina = 'https://www.climatempo.com.br/previsao-do-tempo'
conteudo_pagina_inicial = requests.get('https://www.climatempo.com.br/previsao-do-tempo').content

# Utiliza BeautifulSoup para parsear a página
soup = BeautifulSoup(conteudo_pagina_inicial, 'html.parser')

# Método que recebe o nome da cidade e pesquisa no conteúdo da página
def pesquisa_cidade(cidade):
    links = []
    paginas = []
    li_cidades = soup.find_all(class_='-gray _flex _margin-b-10')
    for li_cidade in li_cidades:
        texto_li_cidade = li_cidade.text.lower().split(',')[0].strip()
        if cidade.lower() == texto_li_cidade:
            print('-'*50)
            print(f'Correspondencia encontrada: {li_cidade.text.title()}')
            links.append(li_cidade['href'].replace('/previsao-do-tempo/agora',''))

            extrai_dados_cidade(f"{pagina}{li_cidade['href'].replace('/previsao-do-tempo/agora','')}")
            print('-'*50, '\n')


# Método que recebe o conteúdo da página da cidade pesquisa e extrai os dados
def extrai_dados_cidade(link):
    pagina_cidade = requests.get(link).content

    soup_pagina_cidade = BeautifulSoup(pagina_cidade, 'html.parser')
    temp_minima = soup_pagina_cidade.find(id='min-temp-1')
    temp_maxima = soup_pagina_cidade.find(id='max-temp-1')

    print(f'Resumo meteorológico para hoje - {datetime.today().strftime("%d/%m/%Y")}:')
    print(f'Temperatura mínima: {temp_minima.text}')
    print(f'Temperatura máxima: {temp_maxima.text}')

    spans = soup_pagina_cidade.find_all('span', class_='_margin-l-5')
    for span in spans:
        if 'mm' in span.text.strip():
            precipitacao = span.text.replace('\n','')
    
    print(f'Volume de chuva: {precipitacao.split("-")[0]} - Probabilidade: {precipitacao.split("-")[1]}')


def main():
    print(' > Iniciando aplicação Pesquisa de Clima por Cidade.\n')

    # Recebendo nome da cidade e formatando para que cada palavra do nome seja capitalizada
    cidade = input('Qual cidade deseja saber o clima?\n')
    cidade = cidade.strip().title()

    pesquisa_cidade(cidade)


if __name__ == "__main__":
    main()
