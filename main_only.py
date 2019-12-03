"""
Advertência: o código abaixo é apenas *ilustrativo* e somente funciona no site dos autores.
Não é possível rodá-lo em um computador doméstico.
"""
import re
import os
from Model import Model

module_dir = os.path.dirname(os.path.abspath(__file__))

global model

try:
    model = Model(os.path.join(module_dir, 'portuguese-bosque-ud-2.4-190531.udpipe'))
except Exception as e:
    print(str(e))


def classific(texto):

    sentences = model.tokenize(texto)

    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            #frase_position += linha.split("\t")[0] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

            classific = frase.strip()

    return classific

def main_haver(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    ## INÍCIO - LISTA DE REGEX HAVER ----------------------------------------------------------------------------
    verbo_encontrado = re.findall(r'\b[hH][ao]\w+(m|ão)/(VERB)(/\w+/)*(/\w+)*\s', frase.strip())
    aux_encontrado = re.findall(r'\b[hH][ao]\w+m/(AUX)(/\w+/)*(/\w+)*\s', frase.strip())
    haverao = re.findall(r'[Hh]averão/VERB', frase.strip())
    haverao_outro = re.findall(r'[Hh]averão/[^V]', frase.strip())
    outros_casos_1 = re.findall(r'[tT](êm|inham|iveram|erão|ivessem|iverem|erem)\s\bhavido\b', texto)
    outros_casos_2 = re.findall(r'[eE](stão|stavam|stiveram|starão|stivessem|stiverem|starem)\s\bhavendo\b', texto)
    outros_casos_3 = re.findall(r'((([pP][ou]d|[dD]ev)((er)?([ie]a?m)?(ão)?(am)?)?(essem)?)|([iv]r?ão)|[pP]ossam)\s(\w+\s)*\bhaver\b', texto)
    outros_casos_4 = re.findall(r'([cC]ostuma(va)?m)\s(\w+\s)*\bhaver\b', texto)
    outros_casos_5 = re.findall(r'((([pP][ou]d|[dD]ev)((er)?([ie]a?m)?(ão)?(am)?)?(essem)?)|([iIVv]r?ão)|[pP]ossam)\s(\w+\s)*\bestar\b\s\bhavendo\b', texto)
    por_bem = re.findall(r'\bpor\b\s\bbem\b', texto)
    ## FIM - LISTA DE REGEX HAVER

    tipoDeRetorno = ''

    if texto == '':
        return 'Digite algo.'

    elif aux_encontrado:
        tipoDeRetorno = '[HAVER:] - Em branco.'
        #print("")
    elif verbo_encontrado:
        if haverao:
            tipoDeRetorno = 'haverErrado'
        elif por_bem:
            tipoDeRetorno = '[HAVER:] - Em branco.'
        else:
            tipoDeRetorno = 'haverErrado'
    elif outros_casos_1 or outros_casos_2 or outros_casos_3 or outros_casos_4 or outros_casos_5:
        tipoDeRetorno = 'haverErrado'
    elif haverao_outro:
        tipoDeRetorno = '[HAVER:] - Em branco.'
    else:
        tipoDeRetorno = '[HAVER:] - Em branco.'

    return tipoDeRetorno

def main_as_vezes(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    as_vezes = re.findall(r'[Aa]s\S+Art\svezes', frase.strip())
    nao_as_vezes = re.findall(r'(([aA]/ADP/)|(?<=[fF]\w[zrç])\w*/VERB\S+)\sas\S+Art\svezes', frase.strip())

    if as_vezes:
        if nao_as_vezes:
            tipoDeRetorno = "Em branco"
        else:
            tipoDeRetorno = "asVezesErrado"

    return tipoDeRetorno

def main_conc_participio_gen(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    ## INÍCIO - LISTA DE REGEX  ----------------------------------------------------------------------------
    auxiliar = re.findall(r'([Pp]ode|[Dd]eve|[éÉ]|[fF]oi|[Ss]erá|[Ee]st\w+|[Vv]ai|[Ii]a)/AUX/Ind/Sing/3/\w+/Fin', frase.strip())
    participio = re.findall(r'\w+/VERB/Masc/Sing/Part/Pass', frase.strip())
    # Da necessidade da ordem:
    # "O relatório vai ser indicado e as pesquisas também": tem NOUN_PLUR, tem CCONJ e está correto
    cconj = re.findall(r'e/CCONJ', frase.strip())

    prep_fem = re.findall(r'\w+/ADP/\s\w+/[^V]\w+(/\w+)*/Fem/(\w+/)*(\w+/)*Sing', frase.strip())
    noun_fem = re.findall(r'\w+/(DET|PRON|NOUN)/Fem/Sing(/\w+)*', frase.strip())

    ## FIM - LISTA DE REGEX

    tipoDeRetorno = ''

    if auxiliar and participio:

        if prep_fem:
            lista_noun_fem_encontrado =[]
            lista_noun_fem_encontrado.extend(noun_fem) # Lista de NOUN_PLUR encontrados
            num_noun_fem_encontrado = len(lista_noun_fem_encontrado) # Número de ítens NOUN_PLUR encontrado

            lista_prep_fem_encontrado =[]
            lista_prep_fem_encontrado.extend(prep_fem) # Lista de NOUN_PLUR encontrados
            num_prep_fem_encontrado = len(lista_prep_fem_encontrado) # Número de ítens NOUN_PLUR encontrado

            if num_noun_fem_encontrado > num_prep_fem_encontrado:
                if cconj:
                    if num_noun_fem_encontrado > 2:
                        tipoDeRetorno = 'concPartGenErrado'
                    else:
                        tipoDeRetorno = '[CONC_PART_GEN:] - Em branco.'

                else:
                    tipoDeRetorno = 'concPartGenErrado'
            else:
                tipoDeRetorno = '[CONC_PART_GEN:] - Em branco.'
        else:
            if noun_fem:
                tipoDeRetorno = 'concPartGenErrado'
            else:
                tipoDeRetorno = '[CONC_PART_GEN:] - Em branco.'


    return tipoDeRetorno

def main_conc_participio_num(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            #frase_position += linha.split("\t")[0] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    ## INÍCIO - LISTA DE REGEX  ----------------------------------------------------------------------------
    auxiliar = re.findall(r'([Pp]ode|[Dd]eve|[éÉ]|[fF]oi|[Ss]erá|[Ee]st\w+|[Vv]ai|[Ii]a)/AUX/Ind/Sing/3/\w+/Fin', frase.strip())
    participio = re.findall(r'\w+/VERB/\w+/Sing/Part/Pass', frase.strip())
    # INFINITIVO = re.findall(r'\w+/AUX/Inf', frases.strip())
    # Gerúndio: "Estava sendo proposto mudanças"

    # Da necessidade da ordem:
    # "O relatório vai ser indicado e as pesquisas também": tem NOUN_PLUR, tem CCONJ e está correto
    prep_plur = re.findall(r'\w+/ADP/\s(\w+/[^V]\w+/\w+/(\w+/)*Plur|\w+/NUM/Card)', frase.strip())
    noun_plur = re.findall(r'\w+/(DET|PRON|NOUN)/\w+/Plur(/\w+)*', frase.strip())
    cconj = re.findall(r'e/CCONJ', frase.strip())
    ## FIM - LISTA DE REGEX

    tipoDeRetorno = ''

    if auxiliar and participio:
        if prep_plur:
    	    lista_noun_plur_encontrado =[]
    	    lista_noun_plur_encontrado.extend(noun_plur) # Lista de NOUN_PLUR encontrados
    	    num_noun_plur_encontrado = len(lista_noun_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

    	    lista_prep_plur_encontrado =[]
    	    lista_prep_plur_encontrado.extend(prep_plur) # Lista de NOUN_PLUR encontrados
    	    num_prep_plur_encontrado = len(lista_prep_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

    	    if num_noun_plur_encontrado > num_prep_plur_encontrado:
    	        if cconj:
    	            if num_noun_plur_encontrado > 2:
    	                tipoDeRetorno = 'concPartNumErrado'
    	            else:
    	                tipoDeRetorno = '[CONC_PART_NUM:] - Em branco.'
    	        else:
    	            tipoDeRetorno = 'concPartNumErrado'
    	    else:
    	        tipoDeRetorno = '[CONC_PART_NUM:] - Em branco.'
        else:
    	    if noun_plur:
    	        tipoDeRetorno = 'concPartNumErrado'
    	    else:
    	        tipoDeRetorno = '[CONC_PART_NUM:] - Em branco.'

    return tipoDeRetorno

def main_conc_verbal(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    lista_classificacao = []
    for item in frase.strip().split(' '):
	    lista_classificacao.append(item)

    suj_verbo = re.findall(r'(((\w+s/))(DET|PROP?N|NOUN|ADJ)\S*\s)' + r'(\S+/[^V][^U]\S*\s)*' + r'\w+/(AUX|VERB)\S*Sing\S*3\S*', frase.strip())
    suj_verbo_sing = re.findall(r'(((([A-Z])\w*/))(DET|PROP?N|NOUN|ADJ)\S*Sing\S*\s)' + r'(\S+/[^V][^U]\S*\s)*' + r'\w+/(AUX|VERB)\S*Plur\S*3\S*', frase.strip())
    prep = [i for i, item in enumerate(lista_classificacao) if re.search(r'\w+/ADP', item)]
    el_plur_ind = [i for i, item in enumerate(lista_classificacao) if re.search(r'(DET|PRON|NOUN)/\w+/Plur', item)]

    if suj_verbo:
        if not prep:
            tipoDeRetorno = "concVerbErrado"
        else:
            if el_plur_ind > prep:
                tipoDeRetorno = '[CUJO:] - Em branco.' # precisa acrescentar o retorno para esse tipo
    elif suj_verbo_sing:
        tipoDeRetorno = "concVerbErrado"

    return tipoDeRetorno

def main_crase(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    ## INÍCIO - LISTA DE REGEX CRASE ----------------------------------------------------------------------------
    crase_pvd = re.findall(r'\ba/ADP/\sa\S*\s\w+/[PVD]\S*', frase.strip())
    crase_masc = re.findall(r'\ba/ADP/\sa\S*\s\w+/\S*Masc\S*', frase.strip())
    crase_plur = re.findall(r'\ba/ADP/\sa\S*Sing\S*\s\w+/NOUN/Fem/Plur', frase.strip())
    crase_ela = re.findall(r'\ba/ADP/\sa\S*\selas?\S*', frase.strip())
    crase_noun = re.findall(r'\ba/ADP/\sa\S*\s\w+/NOUN/\s', frase.strip())
    ## FIM - LISTA DE REGEX CRASE

    tipoDeRetorno = ''

    if crase_pvd:
	    tipoDeRetorno = 'craseErrado'

    if crase_masc:
	    tipoDeRetorno = 'craseErrado'

    if crase_plur:
	    tipoDeRetorno = 'craseErrado'

    if crase_ela:
	    tipoDeRetorno = 'craseErrado'

    if crase_noun:
        tipoDeRetorno = 'craseErrado'

    return tipoDeRetorno

def main_cujo(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    cujo_maius = re.findall(r'Cuj[oa]s?', frase.strip())
    cujo_minus = re.findall(r'cuj[oa]s?/\w+/\w+/\w+/Rel\s\w+/[^N]\w[^J]', frase.strip())
    cujo_comb1 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Masc)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/(Def/|Ind/)?F\w+/\3', frase.strip())
    cujo_comb2 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Fem)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/M\w+/\3', frase.strip())
    cujo_comb3 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Masc)/(Plur)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/\2/S\w+', frase.strip())
    cujo_comb4 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Fem)/(Plur)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/\2/S\w+', frase.strip())
    cujo_comb5 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Masc)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/F\w+/P\w+', frase.strip())
    cujo_comb6 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Fem)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/M\w+/P\w+', frase.strip())
    cujo_comb7 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Masc)/(Plur)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/F\w+/S\w+', frase.strip())
    cujo_comb8 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Fem)/(Plur)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/M\w+\S\w+', frase.strip())
    cujo_comb9 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Masc)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/\2/P\w+', frase.strip())
    cujo_comb10 = re.findall(r'cuj[oa]s?/(PRON|DET)/(Fem)/(Sing)/Rel\s\w+/(DET|NOUN|ADJ|NUM)/\2/P\w+', frase.strip())
    dito_cujo = re.findall(r'\bdit[oa]s?\b\s\bcuj[oa]s?\b', texto)

    tipoDeRetorno = ''

    if cujo_maius:
        tipoDeRetorno = 'cujoErrado'

    elif cujo_minus:
        tipoDeRetorno = 'cujoErrado'
        if dito_cujo:
            tipoDeRetorno = '[CUJO:] - Em branco.'
        if cujo_comb1 or cujo_comb3 or cujo_comb2 or cujo_comb4 or cujo_comb5 or cujo_comb6 or cujo_comb7 or cujo_comb8 or cujo_comb9 or cujo_comb10:
            tipoDeRetorno = 'cujoErrado'

    elif cujo_comb1 or cujo_comb3 or cujo_comb2 or cujo_comb4 or cujo_comb5 or cujo_comb6 or cujo_comb7 or cujo_comb8 or cujo_comb9 or cujo_comb10:
                tipoDeRetorno = 'cujoErrado'
    else:
        tipoDeRetorno = '[CUJO:] - Em branco.'

    return tipoDeRetorno

def main_ele_acus(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    ele_acusativo = re.findall(r'\w+/VERB/(\w+/)*\w+\sel[ea]s?/PRON', frase.strip())
    if ele_acusativo:
        tipoDeRetorno = "eleAcusErrado"

    return tipoDeRetorno

def main_para_mim(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    para_mim = re.findall(r'[pP]a?ra/ADP/\smim/PRON\S+Prs\s\w+/VERB\S+Inf', frase.strip())
    if para_mim:
        tipoDeRetorno = "paraMimErrado"

    return tipoDeRetorno

def main_proclise(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    proclise = re.findall(r'([MT]e|[OA]s?|Lhes?)/\S*\s\w+/(VERB|AUX)', frase.strip())
    proclise_nos = re.findall(r'Nos/_/\sEm/ADP/\sos\S*\s\w+/(VERB|AUX)', frase.strip())
    mesoclise_se = re.findall(r'Se/SCONJ/\s\w+/(VERB|AUX)(((/Cnd)\S*)|(\S*Fut))', frase.strip())
    proclise_se = re.findall(r'Se/SCONJ/\s\w+/(VERB|AUX)', frase.strip())
    sse_inicio = re.findall(r'\w+[^di]sse/VERB', frase.strip())
    enclise_atrator = re.findall(r'([Nn]ão/ADV/Neg|que/SCONJ/)\s\w+-se(-\w+)*/_/\s\w+/(AUX|VERB)\S*/Fin\sse/(PRON|SCONJ)', frase.strip())
    enclise_plural_de = re.findall(r'\w+/(VERB|AUX)\S*Plur\S*Fin\sse/PRON\S*/Prs\sde/ADP/', frase.strip())

    tipoDeRetorno = ''

    if proclise or proclise_nos:
        tipoDeRetorno = "procliseErrado"

    elif mesoclise_se:
        tipoDeRetorno = "mesocliseErrado"

    elif proclise_se:
        tipoDeRetorno = "procliseErrado" # "Se quer ser grande, estude bastante": o caso do "Se" conjunção mesmo

    elif sse_inicio:
        tipoDeRetorno = "passSintErrado"

    elif enclise_atrator:
        tipoDeRetorno = "encliseErrado"

    elif enclise_plural_de:
        tipoDeRetorno = "passSintErrado"

    return tipoDeRetorno

def main_sao_de(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    sao_de = re.findall(r'[Ss]ão\S+Fin\sde/ADP/\s\w+\S+Plur', frase.strip())
    if sao_de:
        tipoDeRetorno = "saoDeErrado"

    return tipoDeRetorno

def main_se(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    verbo_sing = re.findall(r'\w+/VERB/\w+/Sing/', frase.strip())
    prep_plur = re.findall(r'\w+/ADP/\s(\w+/[^V]\w+/\w+/(\w+/)*Plur|\w+/NUM/Card)', frase.strip())
    noun_plur = re.findall(r'\w+/(DET|PRON|NOUN)/\w+/Plur(/\w+)*', frase.strip())
    se_pron = re.findall(r'se/PRON(/\w+)+/Prs', frase.strip())
    se_conj = re.findall(r'se/SCONJ', frase.strip())
    cconj = re.findall(r'e/CCONJ', frase.strip())
    enclise_mesoclise = re.findall(r'\w+-se', frase.strip())
    verbo_infinitivo = re.findall(r'\w+\S*Inf', frase.strip())

    tipoDeRetorno = ''

    if verbo_sing and enclise_mesoclise:

    	if se_conj or se_pron:

    		if prep_plur:
    		    lista_noun_plur_encontrado =[]
    		    lista_noun_plur_encontrado.extend(noun_plur) # Lista de NOUN_PLUR encontrados
    		    num_noun_plur_encontrado = len(lista_noun_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

    		    lista_prep_plur_encontrado =[]
    		    lista_prep_plur_encontrado.extend(prep_plur) # Lista de NOUN_PLUR encontrados
    		    num_prep_plur_encontrado = len(lista_prep_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

    		    if num_noun_plur_encontrado > num_prep_plur_encontrado:
    		        if cconj:
    		            if num_noun_plur_encontrado > 2:
    		                tipoDeRetorno = 'concVerbErrado'

    		            else:
    		                tipoDeRetorno = '[-SE:] - Em branco.'       # Mas ver "Discute-se os livros e com as pessoas.
    		        else:
    		            if verbo_infinitivo:
    		                tipoDeRetorno = '[-SE:] Em branco'
    		            else:
    		                tipoDeRetorno = 'concVerbErrado'
    		    else:
    		        tipoDeRetorno = '[-SE:] - Em branco.'
    		else:

    		    if noun_plur:
    		        if verbo_infinitivo:
    		            tipoDeRetorno = '[-SE:] Em branco'
    		        else:
    		            tipoDeRetorno = 'concVerbErrado'

    		    else:
    		        tipoDeRetorno = '[-SE:] - Em branco.'
    else:
        tipoDeRetorno = '[-SE:] - Em branco.'

    return tipoDeRetorno

def main_suj_verb_virg(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "


    tipoDeRetorno = ''
    suj_verbo_virgula = re.findall(r'((([A-Z]\w+/|[OA]s?/))(DET|PROP?N|NOUN|ADJ)\S*\s)' + r'(\w+/[^V][^U]\S*\s)*' + r',/PUNCT/\s(\w+\S*\s)?\w+/(AUX|VERB)', frase.strip())
    suj_verbo_virgula_minusc = re.findall(r'Já\S*\s' + r'(\w+/(DET|PROP?N|NOUN|ADJ)\S*\s)' + r'(\w+/[^V][^U]\S*\s)*' + r',/PUNCT/\s(\w+\S*\s)?\w+/(AUX|VERB)', frase.strip())

    if suj_verbo_virgula_minusc:
        tipoDeRetorno = "sujVerbVirgErrado"
    elif suj_verbo_virgula:
        tipoDeRetorno = "sujVerbVirgErrado"

    return tipoDeRetorno

def main_tratam_se(texto):

    sentences = model.tokenize(texto)
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    tipoDeRetorno = ''

    tratam_se = re.findall(r'[Tt]ratam/\S+Fin\sse/PRON\S+Prs\sde/ADP/\s\w+\S+Plur', frase.strip())
    if tratam_se:
        tipoDeRetorno = "tratamSeErrado"

    return tipoDeRetorno

def main_verbo_sujeito(texto):

    sentences = model.tokenize(texto)                           ## CLASSIFICAÇÂO DA FRASE
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")                    ## CLASSIFICAÇÂO DA FRASE
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            #frase_position += linha.split("\t")[0] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    lista_classificacao = []
    for item in frase.strip().split(' '):
    	lista_classificacao.append(item)

    el_sing_ind = [i for i, item in enumerate(lista_classificacao) if re.search(r'(NOUN|PRON)\S*/Sing', item)]
    el_plur_ind = [i for i, item in enumerate(lista_classificacao) if re.search(r'(DET|PRON|NOUN)/\w+/Plur', item)]
    verbo_sing_ind = [i for i, item in enumerate(lista_classificacao) if re.search(r'(acontec|exist|[cs]a[ií]|surg|(des)?aparec|nasc|morr|cheg|v[ei]|transcorr|const|falt|entr|segu)' + r'\w+/VERB/\w+/Sing/', item)]
    virgula = [i for i, item in enumerate(lista_classificacao) if re.search(r',/PUNCT/', item)]

    verbo_sing_comeco = re.findall(r'(Acontec|Exist|[CS]a[ií]|Surg|(Des)?[aA]parec|Nasc|Morr|Cheg|Vei|Vinh|Transcorr|Const|Falt|Entr|Segu)' + r'\w+/VERB/\w+/Sing/3', frase.strip())
    verbo_sing = re.findall(r'(acontec|exist|\b[cs]a[ií]|surg|(des)?aparec|nasc|morr|cheg|\bvei|vinh|transcorr|const|falt|entr|segu)' + r'\w+/VERB/\w+/Sing/3', frase.strip())
    verbo_infinitivo = re.findall(r'(acontec|exist|[cs]a[ií]|surg|(des)?aparec|nasc|morr|cheg|v[ei]|transcorr|const|falt|entr|segu)' + r'\w+/VERB/Inf', frase.strip())
    verbo_participio = re.findall(r'(acontec|exist|[cs]a[ií]|surg|(des)?aparec|nasc|morr|cheg|v[ei]|transcorr|const|falt|entr|segu)' + r'\w+/VERB/Part', frase.strip())
    verbo_gerundio = re.findall(r'(acontec|exist|[cs]a[ií]|surg|(des)?aparec|nasc|morr|cheg|v[ei]|transcorr|const|falt|entr|segu)' + r'\w+/VERB/Ger', frase.strip())
    auxiliar_infinitivo = re.findall(r'\b[Ii]a\b|\b[Vv]ai|[Dd]eve\b|[Pp]ode\b/AUX', frase.strip())
    verbo_ter = re.findall(r'\b[Tt]em\b|\b[Tt]inha\b', frase.strip())
    verbo_esta = re.findall(r'\b[eE]stá\b', frase.strip())
    prep_plur = re.findall(r'\w+/ADP/\s(\w+/[^V]\w+/\w+/(\w+/)*Plur|\w+/NUM/Card)', frase.strip())
    noun_plur = re.findall(r'\w+/(DET|PRON|NOUN)/\w+/Plur(/\w+)*', frase.strip())
    cconj = re.findall(r'e/CCONJ', frase.strip())

    def esq_1():
        if el_plur_ind > verbo_sing_ind:
            if prep_plur:
                lista_noun_plur_encontrado =[]
                lista_noun_plur_encontrado.extend(noun_plur) # Lista de NOUN_PLUR encontrados
                num_noun_plur_encontrado = len(lista_noun_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

                lista_prep_plur_encontrado =[]
                lista_prep_plur_encontrado.extend(prep_plur) # Lista de NOUN_PLUR encontrados
                num_prep_plur_encontrado = len(lista_prep_plur_encontrado) # Número de ítens NOUN_PLUR encontrado

                if num_noun_plur_encontrado > num_prep_plur_encontrado:
                    if cconj:
                        if num_noun_plur_encontrado > 2:
                            tipoDeRetorno = 'verbSujErrado'
                        else:
                            tipoDeRetorno = 'verbSujErrado'
                    else:
                        if el_sing_ind < verbo_sing_ind:
                            if el_sing_ind < virgula < verbo_sing_ind:
                                tipoDeRetorno = "[VERBO SUJ:] - Em branco"
                            else:
                                tipoDeRetorno = "[VERBO SUJ:] - Em branco"
                        else:
                            tipoDeRetorno = "verbSujErrado"
                else:
                    tipoDeRetorno = "[VERB SUJ:] - Em branco"
            else:

                if noun_plur:
                    if el_sing_ind < verbo_sing_ind:
                        if el_sing_ind < virgula < verbo_sing_ind:
                            tipoDeRetorno = "[VERBO SUJ:] - Em branco"
                        else:
                            if virgula:
                                tipoDeRetorno = "[VERBO SUJ:] - Em branco"
                            else:
                                if not el_sing_ind:
                                    tipoDeRetorno = "verbSujErrado"
                    else:
                        tipoDeRetorno = "verbSujErrado"
                else:
                    tipoDeRetorno = "[VERB SUJ:] - Em branco"
                    return tipoDeRetorno

        else:
            tipoDeRetorno = "[VERB SUJ:] - Em branco"

        return tipoDeRetorno

    if verbo_sing_comeco:
            return esq_1()

    if verbo_sing:
            return esq_1() # "Ele segue as regras": não deveria capturar, tem que ter índice

    if verbo_infinitivo and auxiliar_infinitivo:
            return esq_1()

    if verbo_ter and verbo_participio:
            return esq_1()

    if verbo_esta and verbo_gerundio:
            return esq_1()

    if auxiliar_infinitivo and verbo_gerundio:
            return esq_1()

def main_conc_nominal(texto):

    sentences = model.tokenize(texto)                           ## CLASSIFICAÇÂO DA FRASE
    for s in sentences:
        model.tag(s)
    conllu = model.write(sentences, "conllu")                    ## CLASSIFICAÇÂO DA FRASE
    frase = ""
    for linha in conllu.splitlines():
        if linha and not "#" in linha:
            feats = linha.split("\t")[5].split("|") # mudar de 1 para 5
            frase += linha.split("\t")[1] + "/" + linha.split("\t")[3] + "/" + "/".join([x.split("=")[1] for x in feats if "=" in x]) + " "

    concordancia_nominal = re.findall(r'((\w+/(DET|PRON|NOUN|ADJ)\S*/Plur(/\w+)*\s))+(\w+/ADV/\s)*(((\w+/(DET|PRON|NOUN|ADJ)\S*/Sing(/\w+)*\s)|(\w+/VERB\S*/Sing/Part)))', frase.strip())
    concordancia_nominal_numeral = re.findall(r'\w+/NUM/Card\s(e/CCONJ/ uma?/DET/\S*\s)*\w+\S*/Sing', frase.strip())
    concordancia_nominal_extra = re.findall(r'((\w+[^s]/)|([oa]/))DET\S*\s\w+\S*/Plur', frase.strip())

    if concordancia_nominal or concordancia_nominal_numeral:
        tipoDeRetorno = "concNomiErrado"

    elif concordancia_nominal_extra:
        tipoDeRetorno = "concNomiErrado"
    else:
        tipoDeRetorno = ''

    return tipoDeRetorno
