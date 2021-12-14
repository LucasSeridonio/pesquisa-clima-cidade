from bs4 import BeautifulSoup
import requests

# Página inicial do ClimaTempo com a lista de cidades
pagina = 'https://www.climatempo.com.br/previsao-do-tempo'
conteudo_pagina_inicial = requests.get('https://www.climatempo.com.br/previsao-do-tempo').content

# Utiliza BeautifulSoup para parsear a página
soup = BeautifulSoup(conteudo_pagina_inicial, 'html.parser')


# Método que recebe o nome da cidade e pesquisa no conteúdo da página
def pesquisa_cidade(cidade):
    li_cidades = soup.find_all(class_='-gray _flex _margin-b-10')
    for li_cidade in li_cidades:
        texto_li_cidade = li_cidade.text.lower().split(',')[0].strip()
        if cidade.lower() == texto_li_cidade:
            print(f'\nCorrespondencia encontrada: {li_cidade.text.title()}')
            link = li_cidade['href'].replace('/previsao-do-tempo/agora','')
    
    if link:
        return f'{pagina}{link}'


def extrai_dados_cidade(link):
    pagina_cidade = requests.get(link).content

    soup_pagina_cidade = BeautifulSoup(pagina_cidade, 'html.parser')
    temp_minima = soup_pagina_cidade.find(id='min-temp-1')
    temp_maxima = soup_pagina_cidade.find(id='max-temp-1')

    print('Resumo:')
    print(f'Temperatura mínima: {temp_minima.text}')
    print(f'Temperatura máxima: {temp_maxima.text}')

def main():
    print(' > Iniciando aplicação Pesquisa de Clima por Cidade.\n')

    # Recebendo nome da cidade e formatando para que cada palavra do nome seja capitalizada
    cidade = input('Qual cidade deseja saber o clima?\n')
    cidade = cidade.strip().title()

    pagina_clima_cidade = pesquisa_cidade(cidade)

    extrai_dados_cidade(pagina_clima_cidade)


if __name__ == "__main__":
    main()
