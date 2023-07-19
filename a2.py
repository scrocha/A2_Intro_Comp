import pandas as pd
import matplotlib.pyplot as plt


AUTORES = ["Sillas Rocha da Costa", "Leonardo Alexandre da Silva Ferreira"]


# Dados necessários para as questões:
estados_id = {"11": "RO", "12": "AC", "13" :"AM", "14": "RR", "15": "PA", "16": "AP", "17": "TO",
              "21": "MA", "22": "PI", "23": "CE", "24": "RN", "25": "PB", "26": "PE", "27": "AL", "28": "SE", "29": "BA",
              "31": "MG", "32": "ES", "33": "RJ", "35": "SP",
              "41": "PR", "42": "SC", "43": "RS",
              "50": "MS", "51": "MT", "52": "GO", "53": "DF"}

qnt_municipios = {"RO": 52, "AC": 22, "AM": 62, "RR": 15, "PA": 144, "AP": 16, "TO": 139,
             "MA": 217, "PI": 224, "CE": 184, "RN": 167, "PB": 223, "PE": 184, "AL": 102, "SE": 75, "BA": 417,
             "MG": 853, "ES": 78, "RJ": 92, "SP": 645,
             "PR": 399, "SC": 295, "RS": 497,
             "MS": 79, "MT": 141, "GO": 246, "DF": 1}

# Funções de conversão para as questões:
def converter_id_index_estado_silgas(serie_de_ids):
    lista_estados = []
    # Aqui iremos alterar cada id de estados pela sua silga no dicionário "estados_id":
    for id in serie_de_ids.index:
        id = estados_id[str(id)]
        lista_estados.append(id)
    serie_de_ids.index = lista_estados

    # Então retornaremos uma série pandas com as siglas convertidas:
    return serie_de_ids

def converter_datas(data_base, coluna_conversao, nome_nova_coluna):
    novas_datas = []
    # Ao converter elemento a elemento e adicioná-los a uma lista, teremos o seguinte resultado:
    for cada_data in data_base[coluna_conversao]:
        cada_data = str(cada_data)
        nova_data = cada_data[0:4] + "-" + cada_data[4:6] + "-" + cada_data[6:]
        novas_datas.append(nova_data)

    # Por fim, definindo essa lista como os dados da nova coluna:
    data_base[nome_nova_coluna] = pd.Series(novas_datas)
    # E converteremos essa coluna para o formato data:
    data_base[nome_nova_coluna] = pd.to_datetime(data_base[nome_nova_coluna], format = "%Y/%m/%d")

    return data_base


def questao_1(datapath):
    # Aqui há apenas uma contagem de uma coluna obrigatória a ser preenchida, o que retornará o número de ocorrências.
    dados = pd.read_csv(datapath, low_memory = False)
    resultado = int(dados["TP_NOT"].count())

    return resultado


def questao_2(datapath):
    # Nesta questão haverá uma contagem dos valores por id de município, que retornará uma série do Pandas.
    dados = pd.read_csv(datapath, low_memory = False)
    resultado = dados["ID_MUNICIP"].value_counts()

    return resultado


def questao_3(datapath):
    # Nesta questão, haverá a contagem de valores por gênero dos dados, e, então, eles serão atrelados a duas variáveis.
    dados = pd.read_csv(datapath, low_memory = False)
    generos = dados["CS_SEXO"].value_counts()
    masc = int(generos["M"])
    fem = int(generos["F"])

    # Depois haverá uma verificação de qual é o maior.
    if fem > masc:
        maior = "F"
    else:
        maior = "M"

    return (maior), {"M": masc, "F": fem}


def questao_4(datapath):
    # Nesta questão faremos a média dos valores de idades já convertidos anteriormente.
    dados = pd.read_csv(datapath, low_memory = False)
    resultado = float(dados["IDADE"].mean())

    return resultado


def questao_5(datapath):
    # Nesta questão haverá uma contagem de ocorrência para cada estado.
    dados = pd.read_csv(datapath, low_memory = False)
    estados = dados["SG_UF_NOT"].value_counts()
    resultado = dict()

    # Após isso, haverá a troca dos ids dos estados por suas siglas.
    converter_id_index_estado_silgas(estados)

    # E por fim, tudo será convertido para um dicionário.
    for sigla in estados.index:
        resultado[str(sigla)] = int(estados[sigla])

    return resultado


def questao_6(datapath):
    # Nesta questão haverá uma contagem de ocorrência para cada estado, mas desta vez com a filtragem por gênero masculino.
    # De resto, será tudo igual à questão 5.
    dados = pd.read_csv(datapath, low_memory = False)
    estados_filtro = dados["SG_UF_NOT"][dados["CS_SEXO"] == "M"].value_counts()
    resultado = dict()

    converter_id_index_estado_silgas(estados_filtro)

    for sigla in estados_filtro.index:
        resultado[str(sigla)] = int(estados_filtro[sigla])

    return resultado


def questao_7(datapath):
    dados = pd.read_csv(datapath, low_memory = False)
    casos_nots = dict()
    # Iremos obter apenas os ids dos municípios e colocá-los em uma lista
    # Sendo que haverá apenas a contagem de municípios que não se repetem.
    casos_id = []
    for caso in dados["ID_MUNICIP"].unique():
        municips = str(caso)[:2]
        casos_id.append(municips)

    # Agora converteremos esta lista para uma série do Pandas e faremos a contagem dos valores:
    casos_por_municip = pd.Series(casos_id).value_counts()
    # Então trocaremos seus index de ids para silgas:
    converter_id_index_estado_silgas(casos_por_municip)

    # Por fim, calcularemos a proporção para cada estado
    # Dos municípios que registraram infecção em relação ao total de municípios do estado.
    for estado in casos_por_municip.index:
        proporcao = int(casos_por_municip[estado]) / int(qnt_municipios[estado])
        # Deste modo, gerando o dicionário desejado.
        casos_nots[estado] = proporcao

    return casos_nots


def questao_8(datapath):
    # Para esta questão, precisaremos converter inteiros para o formato aceito pelo `pd.to_datetime`, que é: "YYYY-mm-dd".
    dados = pd.read_csv(datapath, low_memory = False)

    # Verificaremos se os dados estão no formato "YYYYmmdd" e não no formato "YYYY-mm-dd":
    if len(str(dados["DT_NOTIFIC"].iloc[0])) == 8:

        # Então, converteremos as datas se for necessário:
        converter_datas(dados, "DT_NOTIFIC", "DT_NOTIFICACAO")
    # Se já estiverem no formato solicitado, apenas transição para datas:
    else:
        dados["DT_NOTIFICACAO"] = pd.to_datetime(dados["DT_NOTIFIC"], format = "%Y/%m/%d")

    # Faremos o mesmo com a coluna "DT_SIN_PRI" que possui a data da aparição dos sintomas:
    if len(str(dados["DT_SIN_PRI"].iloc[0])) == 8:
        converter_datas(dados, "DT_SIN_PRI", "DT_SINTOMAS")
    else:
        dados["DT_SINTOMAS"] = pd.to_datetime(dados["DT_SIN_PRI"], format = "%Y/%m/%d")

    dados["ATRASO_NOT"] =  dados["DT_NOTIFICACAO"] - dados["DT_SINTOMAS"]

    # Agora, converteremos o atraso em dias e faremos o dataframe requerido
    dados["ATRASO_NOT"] = dados["ATRASO_NOT"].dt.days

    datas_not = dados[["DT_NOTIFICACAO", "DT_SINTOMAS", "ATRASO_NOT"]]

    return datas_not


def questao_9(datapath):
    # Para esta questão, iremos reutilizar os resultados da questão 8 e adicionar a coluna "ATRASO_NOT" à nova base de dados.
    dados = pd.read_csv(datapath, low_memory = False)
    datas_not = questao_8(datapath)
    estados_silga = []
    resultado = dict()

    # Agora, adicionaremos a coluna "SG_UF_NOT" à nossa tabela de atraso de notificações:
    datas_not["SG_UF_NOT"] = dados["SG_UF_NOT"]

    # Agora, iremos converter os ids para as siglas diretamente.
    for id in datas_not["SG_UF_NOT"]:
        id = estados_id[str(id)]
        estados_silga.append(id)

    # E transferí-las para a coluna "SG_UF_NOT".
    datas_not["SG_UF_NOT"] = pd.Series(estados_silga)

    # Por fim, iremos percorrer a lista de silgas dos estados:
    for estado in list(qnt_municipios.keys()):
        # Filtrar as datas que procuramos para cada estado:
        filtro = datas_not["ATRASO_NOT"][datas_not["SG_UF_NOT"] == estado]
        # Calcular a média e desvio padrão.
        media_estado = float(filtro.mean())
        desvio_estado = float(filtro.std())
        # E por fim, adicionar tudo ao dicionário Resultado.
        resultado[estado] = (media_estado, desvio_estado)

    return resultado


def questao_10(datapath):
    dados = pd.read_csv(datapath, low_memory = False)
    datas_not = questao_8(datapath)
    lista_ids = []
    medias_id = []
    quantidade_nots = []

    # Passaremos o id dos municípios para a tabela inicial.
    dados["ID_MUNICIP"] = dados["ID_MUNICIP"].astype(str)

    # Agora, adicionaremos o atraso à tabela inicial.
    dados["ATRASO_NOT"] = datas_not["ATRASO_NOT"]

    # Para cada município, iremos obter os dados procurados:
    for municipio in dados["ID_MUNICIP"].unique():
        lista_ids.append(municipio)
        # Atrasos por município:
        atrasos = dados["ATRASO_NOT"][dados["ID_MUNICIP"] == municipio]
        # Média de atraso por município:
        medias_id.append(int(atrasos.mean()))
        # Contagem de notificações filtrada por município:
        quantidade_nots.append(int(atrasos.count()))

    # E, assim, criar um Data Frame com estas informações:
    notifics = pd.DataFrame()
    notifics["Media_Atraso"] = medias_id
    notifics["Quantidade_Not"] = quantidade_nots
    notifics.index = lista_ids

    # Além de fazer a plotagem desejada:
    notifics.plot.scatter("Quantidade_Not",
                            "Media_Atraso")

    plt.show()

    return notifics["Media_Atraso"]