"""
Advertência: o código abaixo é apenas *ilustrativo* e somente funciona no site dos autores.
Não é possível rodá-lo em um computador doméstico.
"""

from flask import Flask, render_template, request # from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import MySQLdb
from main_only import classific, main_haver, main_cujo, main_se, main_crase, main_verbo_sujeito, main_conc_participio_num, main_conc_participio_gen, main_as_vezes, main_ele_acus, main_proclise, main_sao_de, main_tratam_se, main_para_mim, main_conc_verbal, main_suj_verb_virg, main_conc_nominal


app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="rjlimauerj",
    password="ofuturojacomecou",
    hostname="rjlimauerj.mysql.pythonanywhere-services.com",
    databasename="rjlimauerj$arquivo",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Comment(db.Model):

    __tablename__ = "arquivo"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(4096))
    retorno = db.Column(db.String(12198))
    classific = db.Column(db.String(4096))




@app.route('/', methods=["GET", "POST"])
def adder_page():
    errors = ""

    if request.method == "POST":
        texto = None
        try:
            texto = str(request.form["texto"])
                                                           #         main_verbo_sujeito(texto) Retorno desse tá bugado -- Verificar depois
            arquivo = Comment(texto=request.form["texto"], retorno=main_haver(texto) + main_cujo(texto) + main_se(texto) + main_crase(texto) + main_conc_participio_num(texto)+ main_conc_participio_gen(texto)+ main_as_vezes(texto)+ main_ele_acus(texto)+ main_para_mim(texto)+ main_proclise(texto)+ main_sao_de(texto)+ main_tratam_se(texto)+ main_conc_verbal(texto)+ main_suj_verb_virg(texto)+ main_conc_nominal(texto), classific = classific(texto))
            #arquivo = Comment(texto=request.form["texto"], retorno=main_haver(texto) + main_cujo(texto) + main_se(texto) + main_crase(texto) + main_verbo_sujeito(texto) + main_conc_participio_num(texto)+ main_conc_participio_gen(texto)+ main_as_vezes(texto)+ main_ele_acus(texto)+ main_para_mim(texto)+ main_proclise(texto)+ main_sao_de(texto)+ main_tratam_se(texto)+ main_conc_verbal(texto)+ main_suj_verb_virg(texto))
            #classificar = Comment(classific = classific(texto))
            db.session.add(arquivo)
            #db.session.add(classificar)
            db.session.commit()


        except:
            errors += "<p>{!r} erro...</p>\n".format(request.form["texto"])

        if texto is None or texto is "":
            return '''
                <html>
                    <body>
                        <center>
                        <h1>
                        <p>Digite um texto!</p>
                        <p><a href="/">Voltar</a>
                        </center>
                    </body>
                </html>
            '''

        if texto is not None:

            result_haver = main_haver(texto)
            result_cujo = main_cujo(texto)
            #CUJO = main_cujo(texto)
            result_crase = main_crase(texto)
            result_se = main_se(texto)
            result_verb_suj = main_verbo_sujeito(texto)
            resul_conc_participio_num = main_conc_participio_num(texto)
            result_conc_participio_gen = main_conc_participio_gen(texto)
            result_proclise = main_proclise(texto)
            result_as_vezes = main_as_vezes(texto)
            result_para_mim = main_para_mim(texto)
            resul_ele_acus = main_ele_acus(texto)
            result_tratam_se = main_tratam_se(texto)
            result_sao_de = main_sao_de(texto)
            result_conc_nominal = main_conc_nominal(texto)
            result_suj_veb_virg = main_suj_verb_virg(texto)
            result_conc_verbal = main_conc_verbal(texto)



            if result_haver == "haverErrado" or result_cujo == "cujoErrado" or result_crase == "craseErrado" or result_se == "seErrado" or result_verb_suj == "verbSujErrado" or resul_conc_participio_num == "concPartNumErrado" or result_conc_participio_gen == "concPartGenErrado" or result_proclise == "procliseErrado" or result_proclise == "mesocliseErrado" or result_proclise == "encliseErrado" or result_proclise == "passSintErrado" or result_as_vezes == "asVezesErrado" or result_para_mim == "paraMimErrado" or resul_ele_acus == "eleAcusErrado" or result_tratam_se == "tratamSeErrado" or result_sao_de == "saoDeErrado" or result_conc_nominal == "concNomiErrado" or result_suj_veb_virg == "sujVerbVirgErrado" or result_conc_verbal == "concVerbErrado":
                mensagemPadrao = """
Ops!... Parece que você usou uma expressão que não está de acordo com a norma-padrão da língua
portuguesa. Mas não se preocupe!
Muitas pessoas considerem isso um erro, mas é apenas uma expressão linguisticamente legítima, que você
pode usar em várias situações, mas na norma-padrão não é permitido.
"""
            else:
                mensagemPadrao = "Não há forma divergente da norma padrão em seu texto."

            if result_haver == "haverErrado":
                haver1 = """
Na norma-padrão, o verbo “haver” é considerado impessoal quando tem sentido de “existir” e por isso nem
ele nem qualquer verbo ligado a ele vai para o plural nesse registro, mesmo com elementos no plural
diretamente relacionados a ele. Assim:
"""
                haver2 = """
“Havia pessoas ali” e não “Haviam pessoas ali”.
“Pode haver problemas aqui” e não “Podem haver problemas aqui”.
"""

                haver3 = """
Passe o verbo para o singular para se adequar ao registro escrito em que você está inserido.
De todas as formas de “haver” no sentido de existir no plural, as que são mais estigmatizadas (malvistas)
são “houveram” e “haverão”. Isso acontece porque a diferença entre essas formas e a versão no singular
(“houve” e “haverá”, respectivamente) é maior do que a diferença entre outras formas (veja “haviam” e “havia”; “houvessem” e “houvesse”.
"""

                haver4 = """
Indo além:
A manutenção do verbo “haver” como impessoal e portanto não podendo estar no plural é um artificialismo.
Isso porque (a) ele já não faz parte da gramática natural das crianças em idade pré-escolar e (b) por isso,
não temos consciência de que ele deveria ser impessoal. Se na frase tem um elemento no plural, faz sentido
que o verbo relacionado a ele vá para o plural, ainda mais porque isso é corrigido em situações com outros
verbos. Para qualquer registro que não seja o da norma-padrão, a frase “Chegou dois alunos” é legítima,
mas para esse registro específico, ela deve ser “Chegaram dois alunos”. Assim, pode parecer natural para
você fazer o mesmo com o verbo “haver” e mudar “Havia pessoas ali” para “Haviam pessoas ali”.
"""

                haver5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
o uso do singular ou do plural do verbo “haver” nesses casos poderia ser opcional. Afinal, se até em
dissertações de mestrado e teses de doutorado já encontramos, mesmo que raramente, esse uso no plural,
então talvez lá no fundo da cabeça desses mestres e doutores, não tem problema escrever algo do tipo
“Conforme demonstrado nas entrevistas, quando haviam problemas” (exemplo real de uma dissertação de
mestrado). - Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo
(https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)"""

            else:
                haver1 = ''
                haver2 = ''
                haver3 = ''
                haver4 = ''
                haver5 = ''

            if result_cujo == 'cujoErrado':
                cujo1 = """
O “cujo” é um pronome relativo que deve, na norma-padrão da língua portuguesa, ligar dois substantivos,
sendo que o segundo é parte ou tem uma relação estrita com o primeiro. Mas não é só isso... A forma do
pronome “cujo” deve concordar em gênero e número com a forma do segundo substantivo. E ainda não
acabou... o “cujo” determina alguma coisa, e assim não cabe colocar o artigo depois dele. Agora acaba...: o
verbo depois do segundo substantivo deve estar relacionado somente a esse segundo substantivo e não ao
primeiro ou a outro elemento. Assim:
"""
                cujo2 = """
“O livro cuja capa estragou está na mesa”: a capa (segundo substantivo) é parte do livro (primeiro
substantivo) e é feminino e está no singular, logo o pronome também; por fim, o verbo “estragar” é apenas
sobre o segundo substantivo.
“O pai cujo filho visitou ficou contente”: filho (segundo substantivo) tem uma relação estrita com pai (primeiro
substantivo); o pronome está singular e masculino, como o segundo substantivo; no entanto, o verbo não
está relacionado somente ao segundo substantivo (“filho”) mas também ao primeiro (“pai”). Logo, nesse
registro escrito, esse uso do “cujo” seria considerado inadequado. Nesse caso, exigem que seja “O pai que o
filho visitou está contente” e veja que nesse caso o artigo apareceu.
“O aluno cujo o pai está na sala saiu correndo”: responsável (segundo substantivo) tem uma relação estrita
com aluno (primeiro substantivo); o pronome está no singular e masculino, como o segundo substantivo; o
verbo está relacionado somente ao segundo substantivo (“está na sala”), mas tem um artigo que não
aceitam estar ali e a versão aceita é “O aluno cujo pai está na sala saiu correndo”.
“O menino cujo veio ontem está em casa”: “cujo” não está relacionando dois substantivos, mas um
substantivo (“menino”) e um verbo (“veio”) e nesse registro escrito, esse uso do “cujo” seria considerado
inadequado.
"""

                cujo3 = """
Reveja o que você escreveu e faça a alteração de acordo com o caso:
- Você não relacionou o “cujo” com dois substantivos. Pode ser utilizado o pronome “que”.
- Você não fez a concordância de gênero e/ou número do “cujo” com o segundo substantivo. Observe esse
segundo substantivo e faça a alteração do “cujo”.
- Você colocou aquele “artigo a mais” depois do “cujo”. Retire esse artigo.
- Você começou um período com “cujo”. Lembre-se que os dois substantivos que “cujo” deve ligar, na
norma-padrão da língua portuguesa, precisam estar no mesmo período.
"""

                cujo4 = """
Indo além:
O pronome “cujo” já não é encontrado na fala espontânea de adultos, mesmo os mais escolarizados. A
insistência no seu uso pode-se dever a uma tradição enraizada que considera “ruim” deixar de usar termos
que estão em desuso por medo da língua estar “perdendo” alguma coisa ou “diminuindo”.
No entanto, perdas e mudanças fazem parte da história de todas as línguas (refs). Todos os registros que
usamos empregam o “que” no lugar do “cujo”, como se pode ver na música “Esquadros”, de Adriana
Calcanhotto: “Cores que eu não sei o nome” quando deveria ser “Cores cujo nome eu não sei”.
"""

                cujo5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
aceitar o uso do “que” no lugar do “cujo” ou do “cujo” seria um ato com base científica (refs), inclusivo, e
portanto, benéfico para a sociedade.
- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo
(https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)"""

            else:
                cujo1 = ''
                cujo2 = ''
                cujo3 = ''
                cujo4 = ''
                cujo5 = ''

            if result_crase == 'craseErrado':
                crase1 = """
Na norma-padrão da língua portuguesa, a crase no singular somente é aceita em situações bem
particulares: antes de palavras que sejam substantivos e que sejam feminino e que estejam no singular.
Todas essas condições devem ser obedecidas para a adequação a esse registro. Assim:
"""
                crase2 = """
“Entreguei o livro à menina”: menina (substantivo: confere, feminino: confere, singular: confere).
“O vagão é preferencial à mulheres”: mulheres (substantivo: confere, feminino: confere, singular: não
confere). Saída: não usar a crase ou usar no plural (“às”).
“Voltou à sair com ela”: sair (substantivo: não confere, logo não é admitida a crase).
“Passei à ela as instruções”: ela (substantivo: não confere, logo não é admitida a crase).
"""

                crase3 = """
Reveja o que você escreveu e retire a crase:
- Você usou a crase antes de uma palavra no masculino.
- Você usou a crase antes de uma palavra que não é substantivo.
- Você usou a crase no singular antes de uma palavra que está no plural.
"""

                crase4 = """
Indo além:
A crase simboliza a união gráfica da preposição “a” com o artigo feminino “a”. O crescente desuso dessa
preposição junto com o fato de a ausência da crase não levar a ambiguidades ou confusões (ainda que
possam acontecer, o contexto deve dar conta, e ainda que não dê, mas duvidamos rs, sempre vai ter
situações ambíguas ou confusas na língua, porque toda língua tem disso) fazem com que sua cobrança se
torne uma exigência que só visa a exclusão de quem, por algum motivo, não domina as regras restritivas.
O uso da crase em contextos, digamos, “não permitidos” faz com que o usuário da língua seja penalizado.
"""

                crase5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
tornar a esse uso opcional ou não penalizar pelo seu uso nesses contextos poderia ser uma medida a ser
adotada.
- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo
(https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)"""

            else:
                crase1 = ''
                crase2 = ''
                crase3 = ''
                crase4 = ''
                crase5 = ''

            if result_se == 'concVerbErrado':
                se1 = """
Na norma-padrão da língua portuguesa, na frase “Vende-se uma casa”, se considera que “casa” é o sujeito
do verbo “vender”... Você sente isso? Nem nós... Alguém sente isso? A ver... De qualquer forma, se “casa”
é sujeito, o mesmo acontece quando a frase vai para o plural, e então, pela outra regra da norma-padrão,
que impõe a concordância do verbo com o sujeito, o resultado é “Vendem-se casas”. Assim:
"""
                se2 = """
“Apresenta-se soluções para o problema”: se encaixa no caso acima e o verbo deve estar no plural
“Apresentam”.
“Pode-se discutir as soluções”: aqui, na norma-padrão se considera que “discutir” é o sujeito do verbo “pode”
e portanto esse verbo não precisa ir para o plural
"""

                se3 = """
Passe o verbo que está na expressão com “-se” para o plural.
"""

                se4 = """
Indo além:
Considerar que “casa” é sujeito de “vende-se” pode fazer sentido para um sistema linguístico em que
crianças e qualquer usuário da língua, naturalmente, percebem essa relação. Isso acontece com o espanhol
e com o português europeu hoje, por exemplo, mas não parece valer para o português brasileiro: nossas
crianças não utilizam expressões com “-se” de forma espontânea e expressões como “Pretende-se”
parecem fazer parte de uma lista de expressões congeladas, fixas para determinadas situações (refs).
"""

                se5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
não considerar “casa” como sujeito do verbo “vender” em “vende-se uma casa” não é um crime e em nada
fere a língua portuguesa: trata-se apenas de uma interpretação possível para esse tipo de frase, que é a de

que não sabemos quem está vendendo uma casa (refs). Adotar a versão “Vende-se casas” ao lado de
“Vendem-se casas” vai aliviar o peso na consciência de quem está sendo tachado de desconhecedor de
regras, sem que o fato de que há uma lógica por trás da escolha do singular nesse caso seja trazido à tona.
- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo
(https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                se1 = ''
                se2 = ''
                se3 = ''
                se4 = ''
                se5 = ''

            if result_verb_suj == "verbSujErrado":
                verbSuj1 = """
Uma das “regras de ouro” da norma-padrão da língua portuguesa é a concordância do verbo com o sujeito.
Apesar de existirem exceções, o caso do verbo que vem antes do sujeito em uma frase não é uma delas.
Desse modo, você deve ter em mente o que essa norma-padrão considera como sujeito para fazer essa concordância nesse caso. Assim:
"""
                verbSuj2 = """
“Chegou os meninos”: o verbo “chegar” está relacionado a “meninos”, que é o sujeito, e como o sujeito está no plural, o verbo também deve ir, o que leva a “Chegaram os meninos”.
“Faltou discutir as soluções”: aqui, na norma-padrão, considera-se que “discutir” é o sujeito e como ele está no singular, o verbo vai ficar no singular.
"""

                verbSuj3 = """
Passe o verbo do singular para a sua forma no plural.
"""

                verbSuj4 = """
Indo além:
As pessoas que defendem a visão da norma-padrão argumentam que quem utiliza uma frase como “Chegou os meninos”
deve estar desconhecendo o conceito de sujeito e confundindo ele com o objeto, o que explica a ausência de concordância.
Isso serve apenas para a norma-padrão. Não parece ser legítima, apesar de muitos apoiarem, a ideia de que um usuário da
língua desconhece ou confunde algo. O que pode estar acontecendo é uma reinterpretação dos papéis dos elementos na frase:
o usuário sabe que quem chega são os meninos; mas se sujeito é um conceito sintático, então quem faz o que pode não ser o
que determina quem é o sujeito: quem é o sujeito é quem tem uma relação estrutural com o verbo. E se em “_Chegamos”, a norma-padrão
enxerga um sujeito oculto, que não está ali, por que não enxergar um outro tipo de sujeito oculto em “_Chegou os meninos”?
Claro, a tradição normativa que indica a relação semântica faz com que essa ideia seja considerada absurda. No entanto, se ela
puder ser mantida, então não podemos falar que “meninos” seja o sujeito, não pelo menos no plano sintático. Você pode saber mais sobre isso na indicação do aplicativo abaixo.
"""

                verbSuj5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
ainda que não seja algo que esteja perto de chegar a uma regra, a escolha da forma singular no caso em que o verbo precede o que a
norma-padrão considera como sujeito vem sendo feita em registros escritos formais de usuários escolarizados da língua portuguesa,
tais como trabalhos de conclusão de curso, artigos científicos, documentos internos de universidades, entre outros (refs).

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                verbSuj1 = ''
                verbSuj2 = ''
                verbSuj3 = ''
                verbSuj4 = ''
                verbSuj5 = ''

            if resul_conc_participio_num == "concPartNumErrado":
                concPartNum1 = """
O uso de uma construção com voz passiva (verbo “ser” + verbo principal no particípio) com o que a norma-padrão considera como sujeito
aparecendo depois como em “Foi indicada uma pessoa” não está nas exceções da norma-padrão quando esse sujeito está no plural. Assim:
"""
                concPartNum2 = """
“Foi indicado duas pessoas”: aqui o sujeito é “duas pessoas” e estando no plural leva o verbo “foi” para o plural, resultando em
“Foram indicadas duas pessoas”. Note que o particípio acompanha também a desinência de gênero do sujeito.
“Foi proposto uma solução”: ainda que não exista aqui uma situação de concordância de número, acontece a de concordância de gênero.
Como “solução” é feminino, a desinência do particípio acompanha isso, resultando em “Foi proposta uma solução”.
"""

                concPartNum3 = """
Observe as marcas de número e gênero do termo que vem depois da voz passiva e altere o número do verbo “ser” e do
particípio para o plural, se for o caso, e o gênero do particípio para feminino, se for o caso.
"""

                concPartNum4 = """
Indo além:
Assim como em “Propôs-se uma solução” a norma-padrão enxerga “uma solução” como sujeito, em “Foi proposta uma solução”, “uma solução”
também é sujeito. Disso decorre a necessidade para essa norma-padrão de haver concordância de gênero e número entre os elementos da voz
passiva e o sujeito. No entanto, do mesmo modo que não enxergamos que “uma solução” é o sujeito de “propôs-se”, não enxergamos “uma solução”
como sujeito de “foi proposto”: afinal, alguém propôs uma solução… Em outras palavras, “Foi proposto uma solução”, “Propôs-se uma solução”
podem ser equivalentes a “Propuseram uma solução”, onde evidentemente “uma solução” não é sujeito.
"""

                concPartNum5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
o uso frequente da voz passiva sem as marcas de concordância do elemento considerado como sujeito pela norma-padrão em registros formais escritos
de usuários escolarizados (refs) faz com que uma proposta de que essa possibilidade possa conviver com a indicada pela norma-padrão, com as marcas
de concordância, seja bastante razoável.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                concPartNum1 = ''
                concPartNum2 = ''
                concPartNum3 = ''
                concPartNum4 = ''
                concPartNum5 = ''


            if result_conc_participio_gen == "concPartGenErrado":
                concPartGen1 = """
O uso de uma construção com voz passiva (verbo “ser” + verbo principal no particípio) com o que a norma-padrão considera como sujeito
aparecendo depois como em “Foi indicada uma pessoa” não está nas exceções da norma-padrão quando esse sujeito está no plural. Assim:
"""
                concPartGen2 = """
“Foi indicado duas pessoas”: aqui o sujeito é “duas pessoas” e estando no plural leva o verbo “foi” para o plural, resultando em
“Foram indicadas duas pessoas”. Note que o particípio acompanha também a desinência de gênero do sujeito.
“Foi proposto uma solução”: ainda que não exista aqui uma situação de concordância de número, acontece a de concordância de gênero.
Como “solução” é feminino, a desinência do particípio acompanha isso, resultando em “Foi proposta uma solução”.
"""

                concPartGen3 = """
Observe as marcas de número e gênero do termo que vem depois da voz passiva e altere o número do verbo “ser” e do
particípio para o plural, se for o caso, e o gênero do particípio para feminino, se for o caso.
"""

                concPartGen4 = """
Indo além:
Assim como em “Propôs-se uma solução” a norma-padrão enxerga “uma solução” como sujeito, em “Foi proposta uma solução”, “uma solução”
também é sujeito. Disso decorre a necessidade para essa norma-padrão de haver concordância de gênero e número entre os elementos da voz
passiva e o sujeito. No entanto, do mesmo modo que não enxergamos que “uma solução” é o sujeito de “propôs-se”, não enxergamos “uma solução”
como sujeito de “foi proposto”: afinal, alguém propôs uma solução… Em outras palavras, “Foi proposto uma solução”, “Propôs-se uma solução”
podem ser equivalentes a “Propuseram uma solução”, onde evidentemente “uma solução” não é sujeito.
"""

                concPartGen5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
o uso frequente da voz passiva sem as marcas de concordância do elemento considerado como sujeito pela norma-padrão em registros formais escritos
de usuários escolarizados (refs) faz com que uma proposta de que essa possibilidade possa conviver com a indicada pela norma-padrão, com as marcas
de concordância, seja bastante razoável.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                concPartGen1 = ''
                concPartGen2 = ''
                concPartGen3 = ''
                concPartGen4 = ''
                concPartGen5 = ''

            if result_proclise == "procliseErrado":
                proclise1 = """
“Não pode começar frase com pronome átono”. É tudo o que os defensores da norma-padrão podem e sabem dizer.
Por que essa proibição existe? A resposta não é simples, e está logo abaixo. Antes, alguns exemplos:
"""
                proclise2 = """
“Se propõe, nesse texto, uma solução para o problema”: Esse “se” é um pronome átono e sua presença no começo da frase está violando
aquela Lei ali de cima, então “Propõe-se, nesse texto, uma solução…”
“O indiquei para o cargo”: O “O” é um pronome átono e de acordo com a regra que proíbe que esse pronome esteja no começo da frase,
deve ficar assim “Indiquei-o para o cargo”.
"""

                proclise3 = """
Coloque o pronome logo após o verbo que está no começo da frase, separando os dois com um hífen.
"""

                proclise4 = """
Indo além:
Senta que lá vem história… Durante séculos, desde antes do descobrimento do Brasil e durante os 400 anos seguintes a esse
evento histórico, a colocação do pronome átono no começo de frase foi algo natural na língua portuguesa (refs). No século XIX,
a língua portuguesa falada em Portugal passou por mudanças e uma delas fez com que a vogal dos pronomes átonos ficasse ainda
mais fraca. Nesse cenário, de fato, começar frase com pronome átono não faz muito sentido. Mas aqui no Brasil, a vogal do
pronome átono sempre permaneceu, assim como no Espanhol, onde, aliás, começar frase com pronome átono é permitido, claro…
Foi quando se estabeleceu que a norma-padrão brasileira seguiria o modelo português do século XIX (refs) que importamos essa
regra, artificial e estranha à nossa história linguística, e que perdura, sem que as pessoas saibam porque, até hoje…
"""

                proclise5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
entendemos que, por ser uma das regras mais conhecidas e que mais se persegue quem a viola em textos formais escritos, a aceitação
da versão em que se pode começar frase com pronome átono pode ser bastante difícil. No entanto, se isso começar em uma escala, em
que gradualmente vai se chegando aos textos mais formais, os que buscam estar mais em acordo com a norma-padrão, o costume de ver
esse tipo de situação, tão natural para nós brasileiros, pode gerar mais empatia para que “Se propõe, nesse texto, uma solução”
possa um dia estar ao lado de “Propõe-se, nesse texto, uma solução” no tipo de registro escrito que você está utilizando.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                proclise1 = ''
                proclise2 = ''
                proclise3 = ''
                proclise4 = ''
                proclise5 = ''

            if result_proclise == "mesocliseErrado":
                mesoclise1 = """
Verbos no futuro simples e no futuro do pretérito têm um status diferente quando a regra de “Não comece frase com pronome átono”
deve ser aplicada. A indicação que consta da norma-padrão é que nesses tempos verbais, o pronome vai aparecer… no meio do verbo
(por isso o nome mesóclise, que tem a ver com mesopotâmia, que significa no meio dos rios). Assim:
"""
                mesoclise2 = """
“Se proporá uma solução”: como o verbo está no futuro, o pronome deve aparecer no meio do verbo, entre o radical e a marca de futuro,
assim “Propor-se-á uma solução”.
“Se poderia dizer que…”: o verbo está no futuro do pretérito e o pronome deve aparecer no meio do verbo, entre o radical e a marca de
futuro, assim “Poder-se-ia dizer que…”

"""

                mesoclise3 = """
Coloque o pronome no meio do verbo, obedecendo a algumas exigências: deve estar sempre entre hifens, sempre depois do radical do verbo e,
quando for o caso, adaptar a forma do radical e do pronome, como se faz na ênclise, assim “O indicarei para o cargo” fica “Indicá-lo-ei para o cargo”.
"""

                mesoclise4 = """
Indo além:
Mesóclise faz sentido… Se você fala uma língua que, natural e espontaneamente, permite separar as partes do verbo. Sabe o hino do Flamengo,
“Flamengo sempre eu hei de ser”, olha as partes de “serei” separadas em “hei” e “ser”. Pois é, a língua portuguesa já foi assim, separando
essas partes(refs). Hoje… Não, a não ser no hino e em algumas expressões congeladas, não separa mais. Então, não fazer, não saber, achar
estranho a mesóclise é natural.
"""

                mesoclise5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
mesóclise é algo tão estranho que seu uso pode ter efeitos de pedantismo, soberba, etc., vide os episódios recentes do ex-presidente Temer.
A solução “Poderia-se” soa artificial enquanto “Se poderia” está mais em acordo com o que é natural, inclusive para usuários escolarizados da
língua portuguesa. O uso progressivo dessa solução em textos que vão se aproximando do registro escrito que mais se aproxima da norma-padrão
pode vir a desfazer barreiras quanto à sua presença nesse registro.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                mesoclise1 = ''
                mesoclise2 = ''
                mesoclise3 = ''
                mesoclise4 = ''
                mesoclise5 = ''

            if result_proclise == "encliseErrado":
                enclise1 = """
O uso da ênclise é considerado, na norma-padrão, a regra. Porém, seguindo o ditado de que “para toda a regra existe uma exceção”, algumas situações
fazem com que a ênclise seja rejeitada e a próclise é que seja aceita. Dois desses casos são ilustrados abaixo:
"""
                enclise2 = """
“Ele não apresentou-se bem”: advérbios de negação são consideradas como “permitidores” da próclise, o que resulta em “Ele não se apresentou bem”.
“Ele disse que apresentou-se bem”: o pronome relativo “que” é outro elemento que permite a próclise, resultando em “Ele disse que se apresentou bem”.
"""

                enclise3 = """
Coloque o pronome átono antes do verbo.
"""

                enclise4 = """
Indo além:
Por que certos elementos permitem a próclise? O debate continua... (refs). Há algumas ideias, como a de que se trata de “elementos atratores”, mas
sem se saber ao certo por que eles seriam atratores e outros não, e mesmo assim essas ideias não são consensuais.
"""

                enclise5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
o uso da ênclise nos casos acima é vista na norma-padrão como um caso de hipercorreção, ou seja, quando alguém aplica uma regra que não deveria.
Na fala espontânea, o uso da próclise nesses casos parece ser o natural. O uso da ênclise, de qualquer forma, não parece implicar nenhum efeito
grave na frase, podendo acontecer junto ao uso da próclise.
"""

            else:
                enclise1 = ''
                enclise2 = ''
                enclise3 = ''
                enclise4 = ''
                enclise5 = ''

            if result_proclise == "passSintErrado":
                passSint1 = """
A passiva sintética é o resultado da forma verbal acrescentada do pronome “se” com o hífen unindo esses dois elementos. Portanto, a grafia oficialmente
aceita na norma-padrão é  “Vende-se uma casa”. Assim:
"""
                passSint2 = """
“Discutesse esse resultado”: como se trata de uma passiva sintética, a grafia deve ser “Discute-se esse resultado”.
“Apresentasse uma solução”: nesse caso, dificilmente um corretor ortográfico vai apresentar uma correção, porque a forma “apresentasse” é a grafia oficial
do pretérito do subjuntivo do verbo “apresentar”. Ainda assim, a forma verbal para esse caso é “Apresenta-se uma solução”.

"""

                passSint3 = """
Reveja a grafia que você usou e troque o “sse” por “-se”.
"""

                passSint4 = """
Indo além:
O uso raro da passiva sintética faz com que as pessoas não tenham consciência da grafia oficial. Grafias divergentes fizeram parte da história da língua
portuguesa durante séculos (refs) e registros informais não possuem uma rigidez de cobrança em relação a isso. Note que mesmo no caso em que a forma existe
com outro sentido (“Apresentasse”), o contexto faz com que esse outro sentido não esteja disponível.
"""

                passSint5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
em teoria, o uso da forma com “sse” poderia acompanhar o uso da forma “-se”. No entanto, por se tratar de convenção ortográfica, essa proposta é bem mais difícil
de ser aceita pelos setores da sociedade que defendem a manutenção da versão da norma-padrão sem alteração ou concessões.
"""

            else:
                passSint1 = ''
                passSint2 = ''
                passSint3 = ''
                passSint4 = ''
                passSint5 = ''

            if result_as_vezes == "asVezesErrado":
                asVezes1 = """
Essa expressão denota frequência e é, assim, considerada uma locução adverbial. Assim:
"""
                asVezes2 = """
“A menina, às vezes, gostava de sair”
“Ele fez as vezes de pai para ela”: nesse caso, a expressão “as vezes” não denota tempo e sim o papel que “Ele” cumpriu e portanto não é necessária a crase.
"""

                asVezes3 = """
Acrescente a crase ao “as”.
"""

                asVezes4 = """
Indo além:
Por conta da existência do uso de “as vezes” como em “Ele fez as vezes de pai”, pode-se justificar a presença da crase em “A menina, às vezes, gostava de sair”.
No entanto, perceba que o contexto dá conta de diferenciar esses dois usos.
"""

                asVezes5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
a expressão “às vezes” está bastante consagrada nos registros escritos que seguem a norma-padrão. Ainda que a ausência da crase não cause confusão, uma proposta
que indique que a versão sem a crase possa existir ao lado da versão com crase parece ter poucas chances de ser bem-sucedida.
"""

            else:
                asVezes1 = ''
                asVezes2 = ''
                asVezes3 = ''
                asVezes4 = ''
                asVezes5 = ''

            if result_para_mim == "paraMimErrado":
                paraMim1 = """
Na norma-padrão, considera-se que em “Esse livro é para eu ler”, o verbo “ler” está em uma forma chamada infinitivo flexionado: percebemos isso utilizando outro
pronome como em “Esse livro é para eles lerem”. Assim:
"""
                paraMim2 = """
“Esse livro é para mim ler”: por conta de ser um infinitivo flexionado, a forma do pronome de primeira pessoa singular deve ser a do caso reto, logo “Esse livro é para eu ler”.
"""

                paraMim3 = """
Troque o pronome “mim” pelo pronome “eu”.
"""

                paraMim4 = """
Indo além:
A consideração principal a ser feita é sobre o status do verbo que segue o pronome. Na norma-padrão, ele é analisado como sendo um infinitivo flexionado por conta do
caso “Esse livro é para eles lerem”. No entanto, devemos notar que mesmo nesse caso registramos o uso “Esse livro é para eles ler” e como se pode perceber não há flexão
do infinitivo. Ainda que se mantenha o uso de “lerem”, é possível analisar o “ler” em “Esse livro é para eu ler” como não estando flexionado – afinal, não há nenhuma
flexão visível ali. Portanto, se um usuário da língua interpretar “ler” como não estando flexionado, não há motivo para a forma “eu” para o pronome de primeira pessoa
do singular, sobrando a opção “mim”, motivada pela presença da preposição.
"""

                paraMim5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
a forma “para mim” seguida de verbo no infinitivo é uma das mais estigmatizadas da língua portuguesa. Pensar que existe um caminho e uma possibilidade para que essa forma
possa estar ao lado da forma “para eu” seguida de verbo no infinitivo é, atualmente, uma utopia.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                paraMim1 = ''
                paraMim2 = ''
                paraMim3 = ''
                paraMim4 = ''
                paraMim5 = ''

            if resul_ele_acus == "eleAcusErrado":
                eleAcus1 = """
Na norma-padrão, existem quadros pronominais bastante rígidos. Eles indicam a forma “o/a/os/as” como sendo os equivalentes átonos das formas “ele/ela/eles/elas”.
Quando um verbo antecede uma forma pronominal na função de objeto direto, a versão átona é a selecionada pela norma-padrão. Assim:
"""
                eleAcus2 = """
“Vi ele na rua”: há um verbo e em seguida um pronome objeto direto e segundo a norma-padrão, é a versão átona que deve ser usada, portanto “Vi-o na rua”.
“Encontrei ela falando com um amigo”: aqui, ainda que “ela” seja sujeito de falando, na norma-padrão, o que sobressai é a função de objeto, portanto “Encontrei-a
falando com um amigo”.

"""

                eleAcus3 = """
Troque o pronome pela sua versão átona da norma-padrão fazendo a correspondência necessária: “ele-o”, “eles-os”, “ela-a”, “elas-as”.
"""

                eleAcus4 = """
Indo além:
Já tem sido bastante estudada a situação linguística do português brasileiro (refs), que já há muito tempo não conta em sua gramática interna as formas átonas
“o/a/os/as” - se você duvida, basta prestar atenção na fala espontânea de crianças e de qualquer adulto em situação informal. Contribui para a não utilização
das formas átonas a presença dos pronomes “você” e “a gente”, que podem ser usados em suas formas tônicas nos casos acima (“Vi você na rua”, “Ele viu a gente
na rua”), fazendo com que o mesmo aconteça com os pronomes “ele/ela/eles/elas”. Ainda, note que “Vi-o sair”, a forma aceita na norma-padrão, exibe um pronome
que não está no caso reto como sujeito do verbo infinitivo, exatamente a situação que se proíbe em “Esse livro é para mim ler”.
"""

                eleAcus5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
embora utilizada por qualquer usuário da língua portuguesa, mesmo os mais escolarizados (refs), a forma “ele/ela/eles/elas” como objeto direto encontra resistências
nos registros em que se exige a norma-padrão. Ainda é um uso marcado nesse ambiente, e a jornada para que ele possa ser legítimo como o outro, de “o/a/os/as”, parece longa e árdua.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                eleAcus1 = ''
                eleAcus2 = ''
                eleAcus3 = ''
                eleAcus4 = ''
                eleAcus5 = ''

            if result_tratam_se == "tratamSeErrado":
                tratamSe1 = """
Na norma-padrão, relações de concordância entre sujeito e verbo não podem ser intermediadas por elementos como a preposição. Portanto, ainda que o elemento relacionado
ao verbo esteja no plural, o verbo permanece no singular. Assim:
"""
                tratamSe2 = """
“Tratam-se de pessoas importantes”: o verbo “tratar” se relaciona com “pessoas”, que está no plural, mas por causa da preposição, a concordância não é estabelecida.
A frase fica “Trata-se de pessoas importantes”.
"""

                tratamSe3 = """
Passe o verbo que vem antes da preposição “de” para o singular.
"""

                tratamSe4 = """
Indo além:
A relação semântica entre o verbo e o sujeito e a insistência da norma-padrão em corrigir a ausência da marca de concordância podem ser motivos para que os verbos
nesses casos fiquem no plural.
"""

                tratamSe5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
esse é um caso em que a marca de concordância, indevida segundo a norma-padrão, parece ser pouco percebida desse modo. Não parece, portanto, ser um caso estigmatizado,
e poderia acompanhar a versão da norma-padrão, em que não aparece a marca de concordância.
"""

            else:
                tratamSe1 = ''
                tratamSe2 = ''
                tratamSe3 = ''
                tratamSe4 = ''
                tratamSe5 = ''

            if result_sao_de == "saoDeErrado":
                saoDe1 = """
Na norma-padrão, relações de concordância entre sujeito e verbo não podem ser intermediadas por elementos como a preposição. Portanto, ainda que o elemento relacionado
ao verbo esteja no plural, o verbo permanece no singular. Assim:
"""
                saoDe2 = """
“São de pessoas assim que precisamos”: o verbo “ser” se relaciona com “pessoas”, que está no plural, mas por causa da preposição, a concordância não é estabelecida.
A frase fica “É de pessoas assim que precisamos”.
"""

                saoDe3 = """
Passe o verbo que vem antes da preposição “de” para o singular.
"""

                saoDe4 = """
Indo além:
A relação semântica entre o verbo e o sujeito e a insistência da norma-padrão em corrigir a ausência da marca de concordância podem ser motivos para que os verbos
nesses casos fiquem no plural.
"""

                saoDe5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
esse é um caso em que a marca de concordância, indevida segundo a norma-padrão, parece ser pouco percebida desse modo. Não parece, portanto, ser um caso estigmatizado,
e poderia acompanhar a versão da norma-padrão, em que não aparece a marca de concordância.
"""

            else:
                saoDe1 = ''
                saoDe2 = ''
                saoDe3 = ''
                saoDe4 = ''
                saoDe5 = ''

            if result_conc_nominal == "concNomiErrado":
                concNomi1 = """
Uma vez que um elemento do sintagma nominal (conjunto de palavras ao redor do substantivo: artigos, adjetivos e pronomes) recebe a marca de concordância por estar no plural,
os demais elementos do sintagma nominal vão receber também a marca de concordância. Assim:
"""
                concNomi2 = """
“Os menino bonito”: o sintagma nominal tem como núcleo o substantivo “menino”. Com o artigo “os” no plural, os demais elementos do sintagma vão para o plural também: “Os meninos bonitos”.
“As pessoas triste”: não basta o núcleo do sintagma nominal estar no plural, todos os elementos desse sintagma também devem estar no plural, assim “As pessoas tristes”.
"""

                concNomi3 = """
Observe os elementos do sintagma nominal e passe para o plural.
"""

                concNomi4 = """
Indo além:
A ausência da marca de concordância no sintagma nominal no português brasileiro já vem sendo estudada há algumas décadas (refs). Característica de um grupo social, é uma das situações
mais estigmatizadas por grandes setores da sociedade. Uma possível explicação para essa ausência pode estar na busca pela solução de um conflito entre “forças” distintas e independentes:
por um lado, é razoável marcar todos os elementos tendo em vista uma maior clareza e poupando o ouvinte de prestar atenção na única marca disponível, o que inevitavelmente gera um maior
esforço por parte do falante, ao ter que marcar cada elemento; por outro lado, marcar apenas uma vez poupa o falante desse esforço, mas tem o preço de fazer o ouvinte ter que prestar atenção
na única marca disponível. Como todos somos falantes e ouvintes, a balança sempre vai pesar ora para um lado, ora para outro: como falantes, queremos passar a mensagem usando menos energia,
levando à escolha de marcar apenas uma vez; como ouvintes, queremos ser poupados de prestar atenção na única marca, levando à escolha de ter muitas marcas de concordância. Na norma-padrão,
a escolha recaiu por privilegiar o ponto de vista do ouvinte, e na outra versão, o ponto de vista do falante é privilegiado.
"""

                concNomi5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
por conta do imenso estigma que acompanha a ausência de marca de concordância no sintagma nominal, é inimaginável que essa opção possa sequer ser sugerida como uma opção ao lado da versão
com as marcas de concordância nos registros que exigem a norma-padrão.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                concNomi1 = ''
                concNomi2 = ''
                concNomi3 = ''
                concNomi4 = ''
                concNomi5 = ''

            if result_suj_veb_virg == "sujVerbVirgErrado":
                sujVerbVirg1 = """
Para a norma-padrão, sujeito e predicado verbal formam uma unidade. Desse modo, seguindo essa lógica, não é permitido separar essas duas unidades com o uso da vírgula. Assim:
"""
                sujVerbVirg2 = """
“A realidade dos fatos, é inegável”: o predicado verbal é a parte que contém o verbo e os elementos a ele relacionados, logo “é inegável”; o que se relaciona com o predicado verbal é o sujeito:
“a realidade dos fatos”. Com a noção de unidade, o que temos é a ausência da vírgula preconizada pela norma-padrão: “A realidade dos fatos é inegável”.
“Tenho dois irmãos, Pedro e João. Pedro é alto. Já João, é baixo”: nesse último período, o predicado verbal é constituído por “é baixo”, sendo o sujeito “João”. Com essas duas unidades sem poder
ser separadas por vírgula, o resultado é “Já o João é baixo”.
"""

                sujVerbVirg3 = """
Retire a vírgula que separa o sujeito do predicado verbal.
"""

                sujVerbVirg4 = """
Indo além:
“Nada na língua é por acaso”. O título do livro do linguista Marcos Bagno pode ser ilustrado nesse caso em questão: por que o usuário da língua coloca uma vírgula onde, digamos, “não deveria”?
Alguma razão há, não pode ser por acaso. Percebe que, nos exemplos acima, temos duas situações distintas, mas que levam ao mesmo lugar. Na primeira, o sujeito é longo “a realidade dos fatos” e
a vírgula pode representar nada mais do que a pausa que fazemos. Na segunda, o sujeito é curto, mas perceba que se trata de um contraste que está sendo feito com a frase anterior. Na fala, marcamos
esse contraste com a entonação. Na escrita… podemos marcar com a vírgula. Agora, vejamos a seguinte frase: “Um belo dia, João acordou assustado”. Faz sentido colocar a vírgula ali, entre o sujeito
“João” e o predicado verbal “acordou assustado”? O sujeito não é longo e nem existe contraste. E sim, parece que ninguém pensa em colocar a vírgula ali. (refs).
"""

                sujVerbVirg5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
a vírgula quando posta separando sujeito e predicado verbal faz sentido. Em nada prejudica a comunicação. Se há casos de ambiguidade, devem ser raros e contexto pode dar conta. No entanto, aceitar
que a vírgula possa estar ali significa, para os defensores da norma-padrão, uma alteração nas regras que ao que parece eles não estão dispostos a aceitar. Uma pena, pois se trata de uma construção
legítima, com lógica e com uso frequente.

- Veja mais informações sobre outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                sujVerbVirg1 = ''
                sujVerbVirg2 = ''
                sujVerbVirg3 = ''
                sujVerbVirg4 = ''
                sujVerbVirg5 = ''

            if result_conc_verbal == "concVerbErrado":
                concVerb1 = """
A marca de número no verbo deve seguir a marca de número do núcleo sujeito. Com raras exceções, essa regra é aplicada na norma-padrão. Assim:
"""
                concVerb2 = """
“Os amigos do vizinho chegou hoje”: o sujeito da frase é “os amigos do vizinho”; o núcleo do sujeito é sempre um substantivo e não acompanhado de preposição. Assim, nesse caso, é “os amigos”. Estando
o núcleo com marca de plural, o verbo também estará, logo “Os amigos do vizinho chegaram hoje”.
“A realidade dos fatos nas últimas décadas são inegáveis”: ainda que existam vários elementos no plural, o núcleo do sujeito é “A realidade” e contando com a marca de singular, a mesma vai para o verbo
resultando em “A realidade dos fatos nas últimas décadas é inegável”.
"""

                concVerb3 = """
Troque a marca de número do verbo do singular para o plural ou vice-versa, conforme o caso.
"""

                concVerb4 = """
Indo além:
Alguma coisa deve estar acontecendo para que nas frases de exemplo, o verbo “chegar” tenha recebido a marca de número de singular e o verbo “ser” tenha recebido a marca de número de plural. Ao que
parece, a presença de elementos no plural pode estar tendo alguma influência. Ainda, veja o caso de “A vida das pessoas não valem nada”: além do elemento no plural entre o núcleo e o verbo, existe
o fato de que estamos falando de mais de uma vida… Uma ideia de plural em um elemento no singular… (refs). Isso é conhecido na norma-padrão, que aceita “A maioria das pessoas vieram”: o núcleo está
evidentemente no singular; porém, há um elemento no plural e o núcleo tem ideia de plural. Sim, essa é a explicação oficial para a marca de plural no verbo ser aceita nesse caso.
"""

                concVerb5 = """
Aonde nenhum gramático normativo jamais esteve: Não vai cair na sua prova mas pensamos que
perguntamos, então, por que não em outros casos? Já há alguma documentação, ainda que não oficial, de que esse tipo de construção vem ganhando espaço em textos escritos em que se exige o registro da
norma-padrão. Sendo assim, a situação descrita nesse item poderia conviver com a da marca do verbo que segue estritamente o que está no núcleo do sujeito.

- Veja mais informações sobre essa e outras formas linguísticas nesse aplicativo (https://play.google.com/store/apps/details?id=isso.nao.e.uma.gramatica.ling)
"""

            else:
                concVerb1 = ''
                concVerb2 = ''
                concVerb3 = ''
                concVerb4 = ''
                concVerb5 = ''










            #result_se = main_se(texto)
            #result_verbo_sujeito = main_verbo_sujeito(texto)
            #result_conc_participio_num = main_conc_participio_num(texto)
            #result_conc_participio_gen = main_conc_participio_gen(texto)
            #result_as_vezes = main_as_vezes(texto)
            #result_para_mim = main_para_mim(texto)
            #result_proclise = main_proclise(texto)
            #result_sao_de = main_sao_de(texto)
            #result_tratam_se = main_tratam_se(texto)
            #result_conc_verbal = main_conc_verbal(texto)
           # result_suj_verb_virg = main_suj_verb_virg(texto)
            #result_conc_nominal = main_conc_nominal(texto)

            return '''
                <html>
                <title>V.G.S.O.</title>
                    <body background="https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-03.jpg">
                        <center>
                        <h1><b>Verificador Gramatical Sociolinguisticamente Orientado - Versão 1.0</b></h1>
                        <p>
                        <table border="1" width="60%">

            <thead>
                <tr><td>
                    <p><b>Resultado:</b></p>
                        <p><b>Frase digitada:</b> {texto}</p>

                        <p>{mensagemPadrao}</p>

                        <p>{haver1}</p>
                        <p>{haver2}</p>
                        <p><b>{haver3}</b></p>
                        <p>{haver4}</p>
                        <p><i>{haver5}</i></p>

                        <p>{cujo1}</p>
                        <p>{cujo2}</p>
                        <p><b>{cujo3}</b></p>
                        <p>{cujo4}</p>
                        <p><i>{cujo5}</i></p>

                        <p>{crase1}</p>
                        <p>{crase2}</p>
                        <p><b>{crase3}</b></p>
                        <p>{crase4}</p>
                        <p><i>{crase5}</i></p>

                        <p>{se1}</p>
                        <p>{se2}</p>
                        <p><b>{se3}</b></p>
                        <p>{se4}</p>
                        <p><i>{se5}</i></p>

                        <p>{verbSuj1}</p>
                        <p>{verbSuj2}</p>
                        <p><b>{verbSuj3}</b></p>
                        <p>{verbSuj4}</p>
                        <p><i>{verbSuj5}</i></p>

                        <p>{concPartNum1}</p>
                        <p>{concPartNum2}</p>
                        <p><b>{concPartNum3}</b></p>
                        <p>{concPartNum4}</p>
                        <p><i>{concPartNum5}</i></p>

                        <p>{concPartGen1}</p>
                        <p>{concPartGen2}</p>
                        <p><b>{concPartGen3}</b></p>
                        <p>{concPartGen4}</p>
                        <p><i>{concPartGen5}</i></p>

                        <p>{proclise1}</p>
                        <p>{proclise2}</p>
                        <p><b>{proclise3}</b></p>
                        <p>{proclise4}</p>
                        <p><i>{proclise5}</i></p>

                        <p>{mesoclise1}</p>
                        <p>{mesoclise2}</p>
                        <p><b>{mesoclise3}</b></p>
                        <p>{mesoclise4}</p>
                        <p><i>{mesoclise5}</i></p>

                        <p>{enclise1}</p>
                        <p>{enclise2}</p>
                        <p><b>{enclise3}</b></p>
                        <p>{enclise4}</p>
                        <p><i>{enclise5}</i></p>

                        <p>{passSint1}</p>
                        <p>{passSint2}</p>
                        <p><b>{passSint3}</b></p>
                        <p>{passSint4}</p>
                        <p><i>{passSint5}</i></p>

                        <p>{asVezes1}</p>
                        <p>{asVezes2}</p>
                        <p><b>{asVezes3}</b></p>
                        <p>{asVezes4}</p>
                        <p><i>{asVezes5}</i></p>

                        <p>{paraMim1}</p>
                        <p>{paraMim2}</p>
                        <p><b>{paraMim3}</b></p>
                        <p>{paraMim4}</p>
                        <p><i>{paraMim5}</i></p>

                        <p>{eleAcus1}</p>
                        <p>{eleAcus2}</p>
                        <p><b>{eleAcus3}</b></p>
                        <p>{eleAcus4}</p>
                        <p><i>{eleAcus5}</i></p>

                        <p>{tratamSe1}</p>
                        <p>{tratamSe2}</p>
                        <p><b>{tratamSe3}</b></p>
                        <p>{tratamSe4}</p>
                        <p><i>{tratamSe5}</i></p>

                        <p>{saoDe1}</p>
                        <p>{saoDe2}</p>
                        <p><b>{saoDe3}</b></p>
                        <p>{saoDe4}</p>
                        <p><i>{saoDe5}</i></p>

                        <p>{concNomi1}</p>
                        <p>{concNomi2}</p>
                        <p><b>{concNomi3}</b></p>
                        <p>{concNomi4}</p>
                        <p><i>{concNomi5}</i></p>

                        <p>{sujVerbVirg1}</p>
                        <p>{sujVerbVirg2}</p>
                        <p><b>{sujVerbVirg3}</b></p>
                        <p>{sujVerbVirg4}</p>
                        <p><i>{sujVerbVirg5}</i></p>

                        <p>{concVerb1}</p>
                        <p>{concVerb2}</p>
                        <p><b>{concVerb3}</b></p>
                        <p>{concVerb4}</p>
                        <p><i>{concVerb5}</i></p>






                        <p><a href="/">Digitar nova frase</a>

                </td></tr>

            </thead>

            <tfoot>
 	        <tr><td>
 	        <center>
            <h3>
 	        Então, o que achou?
            Conta pra gente se deu tudo certo, se teve algum problema ou qualquer observação que você queira fazer.
            Pode escrever pra gente por e-mail <u>rjlimauerj@gmail.com</u>. Obrigado!
            </h3>


            </center>
            </td></tr>
            <tr><td>
            <center>

            <b>Projeto de Iniciação Científica (UERJ) - Coord. Prof. Ricardo Joseh Lima (rjlimauerj@gmail.com) - 2019</b>


            </td></tr>

            </tfoot>
            </center>

                    </body>
                </html>
            '''.format(mensagemPadrao=mensagemPadrao, haver1=haver1, haver2=haver2, haver3=haver3, haver4=haver4, haver5=haver5,
            cujo1=cujo1, cujo2=cujo2, cujo3=cujo3, cujo4=cujo4, cujo5=cujo5,
            crase1=crase1, crase2=crase2, crase3=crase3, crase4=crase4, crase5=crase5,
            se1=se1, se2=se2, se3=se3, se4=se4, se5=se5,
            verbSuj1=verbSuj1, verbSuj2=verbSuj2, verbSuj3=verbSuj3, verbSuj4=verbSuj4, verbSuj5=verbSuj5,
            concPartNum1=concPartNum1, concPartNum2=concPartNum2, concPartNum3=concPartNum3, concPartNum4=concPartNum4, concPartNum5=concPartNum5,
            concPartGen1=concPartGen1, concPartGen2=concPartGen2, concPartGen3=concPartGen3, concPartGen4=concPartGen4, concPartGen5=concPartGen5,
            proclise1=proclise1, proclise2=proclise2, proclise3=proclise3, proclise4=proclise4, proclise5=proclise5,
            mesoclise1=mesoclise1, mesoclise2=mesoclise2, mesoclise3=mesoclise3, mesoclise4=mesoclise4, mesoclise5=mesoclise5,
            enclise1=enclise1, enclise2=enclise2, enclise3=enclise3, enclise4=enclise4, enclise5=enclise5,
            passSint1=passSint1, passSint2=passSint2, passSint3=passSint3, passSint4=passSint4, passSint5=passSint5,
            asVezes1=asVezes1, asVezes2=asVezes2, asVezes3=asVezes3, asVezes4=asVezes4, asVezes5=asVezes5,
            paraMim1=paraMim1, paraMim2=paraMim2, paraMim3=paraMim3, paraMim4=paraMim4, paraMim5=paraMim5,
            eleAcus1=eleAcus1, eleAcus2=eleAcus2, eleAcus3=eleAcus3, eleAcus4=eleAcus4, eleAcus5=eleAcus5,
            tratamSe1=tratamSe1, tratamSe2=tratamSe2, tratamSe3=tratamSe3, tratamSe4=tratamSe4, tratamSe5=tratamSe5,
            saoDe1=saoDe1, saoDe2=saoDe2, saoDe3=saoDe3, saoDe4=saoDe4, saoDe5=saoDe5,
            concNomi1=concNomi1, concNomi2=concNomi2, concNomi3=concNomi3, concNomi4=concNomi4, concNomi5=concNomi5,
            sujVerbVirg1=sujVerbVirg1, sujVerbVirg2=sujVerbVirg2, sujVerbVirg3=sujVerbVirg3, sujVerbVirg4=sujVerbVirg4, sujVerbVirg5=sujVerbVirg5,
            concVerb1=concVerb1, concVerb2=concVerb2, concVerb3=concVerb3, concVerb4=concVerb4, concVerb5=concVerb5,
            texto=texto)

    return '''
    <html>
    <title>V.G.S.O.</title>
    <center>
    <body background="https://visme.co/blog/wp-content/uploads/2017/07/50-Beautiful-and-Minimalist-Presentation-Backgrounds-03.jpg">
    <h1><b>Verificador Gramatical Sociolinguisticamente Orientado - Versão 1.0</b></h1>
        <p>
        <table border="1" width="60%">
            <thead>
     	        <tr><td>
     	            <center>



                    <p><b>Digite uma frase:</b></p>
                    <p><b><h3>(Leia as instruções abaixo)</h3></b></p>
                <form method="post" action=".">
                    <p><input name="texto" placeholder="Digite uma frase..."/></p>
                    <p><input type="submit" value="Verificar frase" /></p>

                </form>
                    </center>
                </td></tr>

            </thead>

            <tfoot>
 	        <tr><td>
 	        <center>

            <b>Projeto de Iniciação Científica (UERJ) - Coord. Prof. Ricardo Joseh Lima (rjlimauerj@gmail.com) - 2019</b>


            </center>
            </td></tr>
            </tfoot>


            <!-- DESCOMENTAR PARA EXIBIR ARQUIVO E DELETAR ARQUIVO -->
            <!--
            <tbody>
     	        <tr><td>
                    <center>
                    <form method="post" action="/arquivo/">
                        <input type="submit" value="Ver arquivo">
                    </form>
                    <form method="post" action="/Delarquivo/">
                        <input type="submit" value="Deletar arquivo">
                    </form>
                    </center>
                </td></tr>
            </tbody>
            -->
            <!-- DESCOMENTAR PARA EXIBIR ARQUIVO E DELETAR ARQUIVO -->

        </table>
        <p>

        <table border="1" width="60%">
        <tr><td>

        <p><b> O que é um Verificador Gramatical Sociolinguisticamente Orientado (VGSO)?<p></b>
        <p>Um corretor gramatical se preocupa, como seu nome diz, em corrigir o que pode ser considerado um erro.
        Um verificador gramatical vai apontar uma palavra ou expressão que é considerada como inadequada em determinado
        registro. Isso é feito utilizando uma linguagem simples e com informações de uma corrente linguística que
        busca dar explicações sobre a palavra ou expresão inadequada.<p>
        <p><b> Por que e para quem é a versão 1.0 do Verificador Gramatical Sociolinguisticamente Orientado (VGSO)?<p></b>
        <p>Em algumas situações, o usuário apenas precisa saber a versão correta da palavra ou expressão. Para isso,
        servem os corretores gramaticais. No entanto, desde, pelo menos a versão de 2007 do Word, o português brasileiro
        não conta com um corretor gramatical eficiente. Além disso, para muitos usuários, pode (ou deve) ser importante
        o esclarecimento do porque da inadequação, para fins de aprendizado. O VGSO também é uma ferramenta de divulgação
        científica, pois disponibiliza, de modo gratuito, informações que têm origem no ambiente acadêmico.
        Essa versão 1.0 se destina a dar a um possível público-alvo (alunos de nível fundamental e médio) e a interessados
        no tema (profissionais de sociolinguística, profissionais de computação) um conjunto de regras para experimentação e avaliação.<p>
        <p><b>Como você pode contribuir com o VGSO?<p></b>
        <p>A partir da lista de regras abaixo, você pode fazer vários testes e depois contar pra gente o que achou e se existe alguma
        situação em que a verificação não está sendo bem aplicada ou que deveria ser aplicada. Mas, <b>atenção</b>: observe bem as regras listadas
        abaixo, pois <b>essa versão do VGSO foi feita para capturar esses casos, e não outros</b>. Além disso, <b>não use muitas frases, nem muito menos
        textos</b>, pois isso pode sobrecarregar o programa, que foi feito, nessa versão, para testar frases curtas.Você pode fazer comentários sobre o retorno
        que estamos fornecendo sobre cada regra. Você também pode sugerir outras regras. Por fim, você pode querer saber mais sobre esse projeto
        e participar das outras versões.<p>
        <p><b><center>Regras da versão 1.0</center><p></b>
        <p>Verbo "Haver" no plural com sentido de existir ("<b>Haviam</b> pessoas ali.")<p>
        <p>Pronome relativo "cujo" ("O livro <b>cujo a</b> capa."; "O menino <b>cujo veio</b>.")<p>
        <p>Concordância com a passiva sintética ("<b>Discute-se</b>, nessa seção, os resultados</b>.")<p>
        <p>Uso da crase ("Dei o livro <b>à pessoas</b> queridas.")<p>
        <p>Concordância de verbo antecedendo o sujeito ("<b>Chegou os alunos</b>.")<p>
        <p>Concordância de número com particípio ("<b>Foi enviado dois recados</b>.")<p>
        <p>Concordância de gênero com particípio ("<b>Foi proposto uma solução</b>.")<p>
        <p>Uso da crase na expressão "às vezes" ("Ela, <b>às vezes</b>, gostava de sair.")<p>
        <p>Pronome de 3a pessoa como objeto direto ("A menina <b>viu ele</b> saindo.")<p>
        <p>Forma do pronome de 1a pessoa antes de infinitivo ("Ele pediu <b>para mim ler</b> o livro.")<p>
        <p>Colocação pronominal ("<b>Se poderia</b> dizer que sim."; "<b>Não pode-se</b> dizer isso.")<p>
        <p>Uso da expressão "são de" ("<b>São de</b> pessoas assim que o Brasil precisa.")<p>
        <p>Uso de plural em 'falsas' passivas sintéticas ("<b>Precisam-se de trabalhadores</b>.")<p>
        <p>Concordância verbal ("<b>As propostas do autor vai</b>..."; "<b>A realidade dos fatos são</b>...")<p>
        <p>Uso de vírgula entre sujeito e verbo ("<b>Já o João, saiu</b>."; "<b>A Clara, ela cozinha</b> bem.")<p>
        <p>Concordância Nominal ("<b>Os meninos muito bonito</b> chegaram."; "Ela viu <b>os meninos atrasado</b>.")<p>



        </td></tr>
        </table>
        <table border="0" width="60%">
            <thead>
     	        <tr><td>
     	        <center>
         <a href="http://www.hitwebcounter.com" target="_blank">
        <img src="http://hitwebcounter.com/counter/counter.php?page=7156321&style=0006&nbdigits=7&type=page&initCount=0" title="free hits" Alt="free hits"   border="0" >
        </a>                                        <br/>
                                        <!-- hitwebcounter.com --><a href="http://www.hitwebcounter.com" title=""
                                        target="_blank" style="font-family: ;
                                        font-size: px; color: #; text-decoration:  ;"></>
                                        </a>   <p><div id="disqus_thread"></div>
        <script>

        /**
        *  RECOMMENDED CONFIGURATION VARIABLES: EDIT AND UNCOMMENT THE SECTION BELOW TO INSERT DYNAMIC VALUES FROM YOUR PLATFORM OR CMS.
        *  LEARN WHY DEFINING THESE VARIABLES IS IMPORTANT: https://disqus.com/admin/universalcode/#configuration-variables*/
        /*
        var disqus_config = function () {
        this.page.url = PAGE_URL;  // Replace PAGE_URL with your page's canonical URL variable
        this.page.identifier = PAGE_IDENTIFIER; // Replace PAGE_IDENTIFIER with your page's unique identifier variable
        };
        */
        (function() { // DON'T EDIT BELOW THIS LINE
        var d = document, s = d.createElement('script');
        s.src = 'https://http-rjlimauerj-pythonanywhere-com.disqus.com/embed.js';
        s.setAttribute('data-timestamp', +new Date());
        (d.head || d.body).appendChild(s);
        })();
        </script>
        <noscript>Please enable JavaScript to view the <a href="https://disqus.com/?ref_noscript">comments powered by Disqus.</a></noscript>
        <p></td></tr>


    </center>
    <script id="dsq-count-scr" src="//http-rjlimauerj-pythonanywhere-com.disqus.com/count.js" async></script>
    </body>
    </html>
    '''


@app.route("/comentarios/", methods=['POST'])
def move_comentarios():
    return render_template("main_page.html", comments=Comment.query.all());


@app.route("/arquivo/", methods=['POST'])
def arquivo():

    db = MySQLdb.connect("rjlimauerj.mysql.pythonanywhere-services.com","rjlimauerj","ofuturojacomecou","rjlimauerj$arquivo" )

    cursor = db.cursor()

    query_string = "SELECT texto, retorno, classific FROM arquivo"
    cursor.execute(query_string)

    data = cursor.fetchall()

    db.close()
    print(data)
    return render_template('arquivo.html', records=data)

@app.route("/Delarquivo/", methods=['POST'])
def Delarquivo():

    db = MySQLdb.connect("rjlimauerj.mysql.pythonanywhere-services.com","rjlimauerj","ofuturojacomecou","rjlimauerj$arquivo" )

    cursor = db.cursor()

    query_string = "TRUNCATE TABLE arquivo"
    cursor.execute(query_string)

    data = cursor.fetchall()

    db.close()
    print(data)
    return render_template('arquivo.html', records=data)
