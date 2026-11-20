import re, os, sys
from PIL import Image

REPO = '/home/user/Padr-o-/'
S = '/tmp/claude-0/-home-user-Padr-o-/f4cfd31c-08a1-5478-97d3-f6c9c56ebd61/scratchpad/'
IMG = S + 'pdfimg/'
os.makedirs(IMG, exist_ok=True)


def prep(src, name, maxpx=900, q=82):
    p = IMG + name + '.jpg'
    if not os.path.exists(p):
        im = Image.open(REPO + src).convert('RGB')
        im.thumbnail((maxpx, maxpx))
        im.save(p, quality=q, optimize=True)
    return 'file://' + p


def logo(name):
    return 'file://' + REPO + 'assets/logo/' + name + '.png'


# ---------------------------------------------------------------- produtos
P = [
 # (arquivo, nome, marca, categoria, texto)
 ('detailer-balde-separador-18l', 'Balde 18 L com separador de partículas', 'Detailer', 'Baldes',
  'A sujeira que sai da luva fica no fundo, abaixo do separador. Isso ajuda a evitar que ela volte pra luva. Use dois: um com shampoo e um só com água, pra enxaguar a luva.'),
 ('luva-tentaculos-autoamerica', 'Luva de microfibra com tentáculos, 16x25 cm', 'AutoAmerica', 'Luvas',
  'Luva de microfibra azul, de dois lados. Eu uso o mesmo modelo na pintura e nas rodas, mas nunca a mesma luva nas duas.'),
 ('toalha-twist-veneto-sigma', 'Toalha de secagem Twist Veneto, 600 gsm, 60x90 cm', 'Sigma Tools', 'Toalhas de secagem',
  'Toalha grande e felpuda, feita pra secagem. Absorve bastante água, o que reduz o número de passadas na pintura.'),
 ('toalha-sem-costura-cinza-sigma', 'Toalha de secagem sem costura, 340 gsm, 50x90 cm', 'Sigma Tools', 'Toalhas de secagem',
  'Toalha cinza, sem costura. Opção mais leve e mais barata de secagem, boa pra vidros e acabamento.'),
 ('kit-10-flanelas-detailer', 'Kit com 10 flanelas de microfibra, 330 gsm, 37x57 cm', 'Detailer', 'Toalhas para selante',
  'Flanelas de microfibra de acabamento premium. Opção pra espalhar e retirar o selante.'),
 ('bobina-microfibra-detailer', 'Bobina de microfibra, 350 gsm, 28x57 cm', 'Detailer', 'Toalhas para selante',
  'Bobina com 20 toalhas destacáveis. Opção pra espalhar e retirar o selante e trocar de pano com frequência.'),
 ('rolo-50-toalhas-sigma', 'Rolo com 50 toalhas de microfibra, 200 gsm, 30x30 cm', 'Sigma Tools', 'Toalhas para selante',
  'Rolo com 50 toalhas destacáveis. Opção econômica pra espalhar e retirar o selante.'),
 ('metmol-jaca-1500ml', 'MetMol, shampoo de pré-lavagem, 500 ml ou 1,5 L', 'Jaça', 'Pré-lavagem',
  'Shampoo automotivo de pré-lavagem. Serve pra soltar a sujeira antes de encostar na pintura. Dilua conforme o rótulo.'),
 ('v-mol-vonixx-500ml', 'V-Mol, shampoo desincrustante, 500 ml', 'Vonixx', 'Pré-lavagem',
  'Opção equivalente ao MetMol. Shampoo desincrustante, ultraconcentrado e espumante. Dilua conforme o rótulo.'),
 ('bubble-foam-jaca-500ml', 'Bubble Foam, shampoo lava autos, 500 ml', 'Jaça', 'Lavagem',
  'Shampoo lava autos usado nos dois baldes ou no pulverizador de espuma. Dilua conforme o rótulo.'),
 ('v-floc-vonixx-500ml', 'V-Floc, shampoo automotivo neutro, 500 ml ou 1,5 L', 'Vonixx', 'Lavagem',
  'Opção equivalente ao Bubble Foam. Shampoo neutro concentrado, que espuma e deixa a pintura com brilho.'),
 ('black-lemon-jaca-1500ml', 'Black Lemon, condicionador de pneus, 500 ml ou 1,5 L', 'Jaça', 'Pneus e borrachas',
  'Hidratante e revitalizador de pneus e plásticos. Segundo a loja, uma demão dá acabamento acetinado e duas dão mais brilho.'),
 ('reset-protelim-500ml', 'Reset, limpador de pneus e borrachas, 500 ml', 'Protelim', 'Pneus e borrachas',
  'Limpador em spray, de ação rápida e profunda. Remove a sujeira difícil de pneus e borrachas antes de aplicar o condicionador.'),
 ('perl-carpro-500ml', 'Perl, restaurador de plásticos e borrachas, 500 ml', 'CarPro', 'Pneus e borrachas',
  'Condicionador concentrado, que se dilui em água. Deixa acabamento acetinado. Pelo rótulo, dura até 3 meses. Dilua conforme o rótulo.'),
 ('aplicador-pretinho-detailer', 'Aplicador de pretinho, espuma amarela', 'Detailer', 'Aplicadores',
  'Opção mais barata. Aplica o condicionador no pneu. Dura menos que o aplicador tipo pincel.'),
 ('aplicador-pincel-soft-pretinho', 'Aplicador de pneu tipo pincel soft', 'Tipo pincel soft', 'Aplicadores',
  'Opção de mais durabilidade. Custa mais que o de espuma e aplica o condicionador de forma uniforme.'),
 ('escova-pneus-autoamerica', 'Escova para pneus Tire Brush', 'AutoAmerica', 'Escovas',
  'Escova de cerdas firmes pra limpar a lateral do pneu junto com o limpador.'),
 ('escova-furo-roda-longa-sigma', 'Escova longa curvada de microfibra, furo de roda', 'Sigma', 'Escovas',
  'Cabo longo e curvo, com microfibra. Chega ao fundo do aro, onde a luva não alcança.'),
 ('escova-furo-roda-cleaner', 'Escova para furo de roda', 'Cleaner', 'Escovas',
  'Escova azul e macia, pra limpar o interior do aro.'),
 ('kit-5-pincéis-cleaner', 'Kit com 5 pincéis de cerdas macias', 'Cleaner', 'Escovas',
  'Pincéis pra detalhes: emblemas, grades, saídas de ar e frestas, onde a luva não entra.'),
 ('masterfull-toys-for-boys', 'Masterfull Degreaser (alcalino), 500 g', 'Toys for Boys (TFB)', 'Limpeza pesada',
  'Pasta de limpeza pra óleos, graxas, gorduras e insetos. Uso profissional. Siga o rótulo e teste antes numa área pequena.'),
 ('snow-foam-duo-detailer', 'Snow Foam Duo, 2 reservatórios', 'Detailer', 'Espuma e aplicação',
  'Canhão de espuma pra lavadora de pressão, com dois reservatórios: um pra shampoo neutro e outro pra limpeza pesada.'),
 ('ik-foam-pro-2', 'Pulverizador IK Foam Pro 2, 1,9 L', 'IK', 'Espuma e aplicação',
  'Pulverizador manual de compressão prévia, com válvula de segurança e pressão máxima de 3 bar. Faz espuma sem precisar de lavadora.'),
 ('pulverizador-2em1-autoamerica', 'Pulverizador de compressão manual 2 em 1, 2 L', 'AutoAmerica', 'Espuma e aplicação',
  'Opção mais simples de pulverizador manual, pra aplicar produtos diluídos.'),
 ('pulverizador-viton-sigma', 'Pulverizador Viton resistente a químicos, 2 L', 'Sigma Tools', 'Espuma e aplicação',
  'Pulverizador com vedação resistente a produtos químicos mais fortes.'),
 ('lavadora-wap-combate-turbo', 'Lavadora de alta pressão Combate Turbo 2600', 'Wap', 'Equipamentos',
  '2100 psi, 360 L/h, 1700 W, mangueira de 5 m e sistema que desliga o motor ao soltar o gatilho. Confira a voltagem (220 V).'),
 ('aspirador-wap-gtw-inox-20', 'Aspirador de pó e água GTW Inox 20', 'Wap', 'Equipamentos',
  '20 litros, 1600 W, filtro lavável. Aspira o interior do carro. Se o seu modelo tiver saída de ar, também serve pra soprar a água das frestas.'),
 ('sio2-pro-vonixx-500ml', 'SiO2-Pro, selante cerâmico em spray, 500 ml', 'Vonixx', 'Proteção',
  'Pronto pra usar, em áreas de até 60x60 cm. Segundo o fabricante, protege a pintura por até 4 meses. A loja indica reaplicar a cada 30 ou 45 dias.'),
 ('luva-nitrilo-ignite-supermax', 'Luva de nitrilo Ignite, 50 pares, tamanho GG', 'Supermax', 'Proteção das mãos',
  'Luva descartável de nitrilo. Protege as mãos ao usar limpadores e produtos químicos.'),
]
P = [(f.replace('é', 'e'), n, m, c, t) for f, n, m, c, t in P]


def product_img(fn):
    fn = fn.replace('pincéis', 'pinceis')
    if fn == 'kit-5-pinceis-cleaner':
        pass
    return prep('assets/produtos/' + fn + '.jpg', 'p_' + fn, 700)


# ---------------------------------------------------------------- kits (a partir da tabela aprovada)
src = open(S + 'ebook24.html').read()
m = re.search(r'<tr><th>Itens</th><th>Opções</th></tr>(.*?)</table>', src, re.S)
rows = re.findall(r'<tr>(.*?)</tr>', m.group(1), re.S)
kits = []
for r in rows:
    h = re.search(r'colspan="2"[^>]*>(.*?)</td>', r, re.S)
    if h:
        kits.append([h.group(1).strip(), []])
        continue
    tds = re.findall(r'<td>(.*?)</td>', r, re.S)
    item = re.sub(r'</?b>', '', tds[0]).strip()
    opts = [re.sub(r'^•\s*', '', o).strip() for o in tds[1].split('<br>')]
    kits[-1][1].append((item, opts))


def kit_table(items):
    out = '<table class="kit"><tr><th>Itens</th><th>Opções</th></tr>'
    for item, opts in items:
        out += '<tr><td class="it">%s</td><td>%s</td></tr>' % (item, '<br>'.join(opts))
    return out + '</table>'


# ---------------------------------------------------------------- páginas
pages = []  # (classe, html, numerar)


def page(html, cls='', num=True):
    pages.append((cls, html, num))


def head(tag, title, sub=''):
    return '<div class="hd"><span class="eyebrow">%s</span><h2>%s</h2>%s</div>' % (tag, title, ('<p class="sub">%s</p>' % sub) if sub else '')


# 1 capa
page('''
<img class="bg" src="%s">
<div class="shade"></div>
<img class="lg" src="%s">
<div class="ttl"><div class="k">E-book · Tidioli Studio</div><h1>Lavagem<br><b>Segura</b></h1>
<p>Como lavar seu carro em casa com método de profissional, e os produtos que eu uso em cada kit.</p></div>
''' % (prep('assets/fotos/f03-ranger-frente.jpg', 'f03', 1500, 84), logo('vertical-branco')), 'cover', False)

# 2 folha de rosto
page('''
<div class="center">
<img class="lg2" src="%s">
<h3>Lavagem Segura</h3>
<p class="small">E-book do Tidioli Studio, estética automotiva.<br>© 2026 Tidioli Studio. Uso pessoal do comprador. Proibida a revenda e a redistribuição.</p>
<div class="aviso"><b>Leia antes de começar.</b> Este e-book reúne o método e os produtos que eu uso e recomendo. Nenhum método elimina por completo o risco de marcas de lavagem: ele ajuda a reduzi-lo. Siga sempre as instruções do rótulo de cada produto, a diluição indicada e as orientações do fabricante do seu veículo. Em carro com película, pintura fosca ou repintura recente, confirme os cuidados com quem fez o serviço.</div>
<p class="small">Fotos dos produtos: lojas B.Wax, Amazon e Mercado Livre, de caráter ilustrativo. As marcas e as imagens pertencem aos seus titulares. Os preços não constam do e-book porque mudam com frequência: confira o valor atual na loja.</p>
</div>
''' % logo('horizontal-preto'), 'white', False)

# 3 sumário (preenchido depois)
page('@@SUMARIO@@', '', True)

# 4 boas-vindas
page(head('Boas-vindas', 'Oi, eu sou o Matheus') + '''
<div class="two"><div class="col">
<p>Há mais de 6 anos eu trabalho com estética automotiva no Tidioli Studio. Nesse tempo vi o mesmo erro se repetir: carro bonito, dono caprichoso, e uma pintura cheia de riscos circulares que apareciam assim que o sol batia.</p>
<p>Na maioria das vezes o problema não é o carro nem o cuidado do dono. É o jeito de lavar, e os produtos escolhidos.</p>
<p>Este e-book reúne o que eu ensinaria na primeira conversa com um cliente: o método de lavagem, a ordem certa de cada etapa e, o que mais me perguntam, <b>quais produtos usar</b>.</p>
<p>No capítulo 2 eu montei três kits, do Essencial ao Entusiasta, com as opções de cada item e uma ficha com foto de cada produto. Você escolhe o que cabe no seu bolso e no seu nível de dedicação.</p>
<p class="assina">Matheus<br><span>Tidioli Studio · Estética Automotiva</span></p>
</div>
<div class="col ph"><img src="%s"></div></div>
''' % prep('assets/fotos/f10-matheus-politriz.jpg', 'f10', 1000), '', True)

# 5-6 cap 1
page(head('Capítulo 1', 'Por que o carro fica riscado depois de lavar', 'A maior parte dos riscos circulares vem da lavagem, não do tempo.') + '''
<p>A pintura do carro é uma camada fina de verniz. Quando uma partícula dura, como poeira, areia ou terra seca, fica presa na luva, na esponja ou na toalha e é arrastada sobre ela, deixa marcas minúsculas. Cada marca é pequena, mas juntas, e sob a luz do sol, formam aqueles riscos circulares.</p>
<h3>Os 4 erros mais comuns</h3>
<ul class="big">
<li><b>Esponja de cozinha ou de banho.</b> A superfície dela prende a sujeira em vez de deixá-la se soltar.</li>
<li><b>Toalha comum ou flanela velha para secar.</b> Pode carregar sujeira e fibras duras para a pintura.</li>
<li><b>Lavar com o carro quente ou no sol.</b> O shampoo seca antes do enxágue e deixa manchas.</li>
<li><b>Um balde só.</b> A cada vez que você mergulha a luva suja, devolve a sujeira para o shampoo e depois para o carro.</li>
</ul>
<div class="foto"><img src="%s"><span>Riscos circulares na pintura, vistos sob uma luz forte.</span></div>
''' % prep('assets/fotos/f11-micro-riscos.jpg', 'f11', 700), '', True)

page(head('Capítulo 1', 'O que realmente reduz o risco', 'Três coisas pesam mais do que qualquer produto caro.') + '''
<div class="cards3">
<div class="c"><span class="n">1</span><h4>Uma boa pré-lavagem</h4><p>Tirar o máximo de sujeira antes de encostar na pintura. Quanto menos partícula sólida chegar na luva, menor o risco.</p></div>
<div class="c"><span class="n">2</span><h4>Dois baldes com separador</h4><p>Um balde com shampoo e outro só com água, ambos com separador de partículas no fundo. A luva é enxaguada antes de voltar ao shampoo.</p></div>
<div class="c"><span class="n">3</span><h4>Microfibra limpa</h4><p>Luvas e toalhas de microfibra em bom estado, sempre limpas, e nunca a mesma da pintura nas rodas.</p></div>
</div>
<div class="tip"><b>Importante.</b> Nenhuma luva evita sozinha que a sujeira arraste na pintura. O que reduz o risco é o conjunto: pré-lavagem bem feita, balde com separador e microfibra limpa. Mesmo assim, o risco nunca chega a zero. Ele fica menor.</div>
<h3>Como usar este e-book</h3>
<p>O capítulo 2 mostra os kits e os produtos. Os capítulos 3 e 4 ensinam a lavagem, na ordem. O 5 trata da proteção, o 6 desfaz mitos e o 7 traz a rotina de manutenção. No final há um checklist para imprimir.</p>
''', '', True)

# 7 cap 2 intro
page(head('Capítulo 2', 'Os kits e os produtos', 'Escolha pelo quanto você quer se dedicar. Você pode começar pelo Essencial e evoluir.') + '''
<div class="cards3 k">
<div class="c"><h4>Kit Essencial</h4><p>O que não pode faltar pra lavar direito: dois baldes com separador, luvas, toalha de secagem e três produtos.</p></div>
<div class="c"><h4>Kit Dedicado</h4><p>Pra quem já pegou gosto. Soma espuma, pincéis, selante, limpador de pneus e a lavadora de pressão.</p></div>
<div class="c"><h4>Kit Entusiasta</h4><p>Pra quem gosta do assunto e quer ter tudo: escovas de furo de roda, desengraxante, condicionador, pulverizador e aspirador.</p></div>
</div>
<h3>Como ler as listas</h3>
<ul class="big">
<li>Cada kit traz a <b>lista completa</b>, sem depender dos outros.</li>
<li>Onde há mais de uma opção, <b>você escolhe</b>. Por exemplo, o MetMol (Jaça) e o V-Mol (Vonixx) fazem o mesmo papel.</li>
<li>Depois das listas, uma <b>ficha com foto</b> de cada produto, pra você reconhecer na loja.</li>
<li>Não coloquei preços: eles mudam com frequência. Confira sempre o valor atual na loja.</li>
</ul>
<h3>A regra da microfibra</h3>
<p>Luva e toalha de microfibra valem mais do que qualquer produto caro. Tenha sempre uma luva para a pintura e outra, separada, para rodas e caixas de roda. Se uma luva ou toalha cair no chão, ela não volta para o carro até ser lavada.</p>
<div class="foto wide"><img src="%s"><span>Kit montado, com a luva, o balde com separador e o pulverizador.</span></div>
''' % prep('assets/fotos/f13-kit-baldes-editada.jpg', 'f13', 1100), '', True)

# 8-10 tabelas dos kits
descr = {
 'Kit Essencial': 'Para lavar direito, sem gastar com o que você ainda não precisa.',
 'Kit Dedicado': 'Soma ao Essencial mais luvas, espuma, selante e lavadora de pressão.',
 'Kit Entusiasta': 'A lista mais completa, para quem quer ter tudo à mão.',
}
opcional = [k for k in kits if k[0].startswith('Opcional')][0][1]
kits = [k for k in kits if not k[0].startswith('Opcional')]
for name, items in kits:
    if name == 'Kit Entusiasta':
        half = 15
        page(head('Capítulo 2', name, descr[name]) + kit_table(items[:half]), '', True)
        page(head('Capítulo 2', name + ' (continuação)') + kit_table(items[half:]) + '<h3>Opcional, em qualquer kit</h3>' + kit_table(opcional) + '<p class="note">Onde há duas opções, escolha a que preferir. Todas aparecem nas fichas a seguir.</p>', '', True)
    else:
        page(head('Capítulo 2', name, descr[name]) + kit_table(items) + '<p class="note">Onde há duas opções, escolha a que preferir. Todas aparecem nas fichas a seguir.</p>', '', True)

# fichas
cards = ''.join(
    '<div class="pc"><div class="im"><img src="%s"></div><div class="tx"><span class="cat">%s</span><b>%s</b><i>%s</i><p>%s</p></div></div>'
    % (product_img(f), c, n, m_, t) for f, n, m_, c, t in P)
chunks = re.findall(r'<div class="pc">.*?</div></div>', cards, re.S)
for i in range(0, len(chunks), 6):
    page(head('Capítulo 2', 'Fichas dos produtos', 'Reconheça cada item na loja. Os preços ficam de fora porque mudam toda hora.') + '<div class="pgrid">' + ''.join(chunks[i:i + 6]) + '</div>', '', True)

# cap 3
page(head('Capítulo 3', 'Antes de molhar o carro', 'A lavagem começa na preparação.') + '''
<ul class="big">
<li><b>Sombra e lataria fria.</b> Lave com o carro na sombra e frio ao toque. No sol e com a lataria quente, o shampoo seca antes do enxágue e mancha. Se o carro rodou há pouco, espere esfriar.</li>
<li><b>Tudo separado antes de começar.</b> Baldes, luvas, toalhas e produtos ao alcance. Parar no meio da lavagem pra procurar um item faz o shampoo secar.</li>
<li><b>Dois baldes montados.</b> Um com água e o shampoo, diluído como diz o rótulo. O outro só com água limpa, para enxaguar a luva. Os dois com o separador de partículas no fundo.</li>
<li><b>Luvas diferentes para pintura e rodas.</b> A roda é a parte mais suja do carro, e a graxa e o pó de freio não podem ir parar na lataria.</li>
<li><b>Roda fria.</b> Não aplique produto de limpeza em roda quente. Espere esfriar.</li>
</ul>
<div class="tip"><b>Tire os anéis e relógios.</b> Eles podem riscar a pintura sem você perceber durante a lavagem.</div>
<div class="foto wide"><img src="%s"><span>Os dois baldes com separador, a luva e o pulverizador, prontos pra começar.</span></div>
''' % prep('assets/fotos/f13-kit-baldes-editada.jpg', 'f13b', 1100), '', True)

# cap 4
steps1 = [
 ('Rodas e pneus primeiro', 'É a parte mais suja. Com a roda fria, aplique o produto de limpeza indicado no rótulo, passe as escovas e a luva das rodas, e enxágue bem. Se você lavar as rodas por último, pode respingar sujeira na pintura limpa.'),
 ('Enxágue geral', 'De cima para baixo, com bastante água, para tirar o máximo de sujeira solta antes de encostar na pintura. Dê atenção às caixas de roda e às partes baixas.'),
 ('Pré-lavagem', 'Aplique o shampoo de pré-lavagem diluído, de baixo para cima. Deixe agir pelo tempo do rótulo, sem deixar secar, e enxágue de cima para baixo. É aqui que você tira a maior parte da sujeira sem encostar na pintura.'),
 ('Lavagem com dois baldes', 'Mergulhe a luva no balde com shampoo, lave uma área pequena, e antes de voltar ao shampoo enxágue a luva no balde de água, esfregando no separador. Só então volte ao balde de shampoo.'),
]
steps2 = [
 ('Ordem da lavagem', 'Comece pelas partes mais altas e limpas e termine nas mais sujas: teto, vidros, capô, porta-malas, laterais de cima, laterais de baixo e para-choques. Passe a luva em linhas retas, sem fazer força.'),
 ('Enxágue final', 'De cima para baixo. Se quiser, tire o bico da mangueira e deixe a água correr sobre a pintura: ela escorre e sobra menos gota para secar.'),
 ('Secagem', 'Estenda a toalha de secagem sobre a pintura e arraste de leve, sem pressionar. Troque de toalha ou de lado quando ela ficar encharcada. Use o ar para tirar a água de frestas, retrovisores e emblemas.'),
 ('Pneus e acabamento', 'Com o pneu seco e limpo, aplique o condicionador com o aplicador e retire o excesso, pra não escorrer nem respingar na pintura. Plásticos externos podem receber o condicionador próprio, diluído como diz o rótulo.'),
]


def steps_html(lst, start):
    return '<div class="steps">' + ''.join('<div class="st"><span class="n">%d</span><div><h4>%s</h4><p>%s</p></div></div>' % (start + i, t, d) for i, (t, d) in enumerate(lst)) + '</div>'


page(head('Capítulo 4', 'O passo a passo da lavagem', 'Etapas 1 a 4: preparar o carro e lavar.') + steps_html(steps1, 1), '', True)
page(head('Capítulo 4', 'O passo a passo da lavagem', 'Etapas 5 a 8: lavar, enxaguar, secar e finalizar.') + steps_html(steps2, 5), '', True)

# cap 5
page(head('Capítulo 5', 'Proteção rápida', 'Depois de lavar, proteger. É o que deixa a próxima lavagem mais fácil.') + '''
<p>Um selante cria uma camada protetora sobre a pintura. Ela ajuda a repelir a água e a sujeira e deixa a próxima lavagem mais simples. O exemplo abaixo é o SiO2-Pro, da Vonixx, um selante cerâmico em spray.</p>
<div class="steps compact">
<div class="st"><span class="n">1</span><div><h4>Carro limpo, seco e frio</h4><p>Aplique na sombra, com a pintura sem poeira e sem resíduo de água.</p></div></div>
<div class="st"><span class="n">2</span><div><h4>Uma área por vez</h4><p>O fabricante indica áreas de até 60x60 cm. Borrife pouco produto.</p></div></div>
<div class="st"><span class="n">3</span><div><h4>Espalhe e retire</h4><p>Espalhe com uma toalha de microfibra limpa e retire o excesso com outra, também limpa.</p></div></div>
<div class="st"><span class="n">4</span><div><h4>Reaplique no tempo certo</h4><p>Segundo o fabricante, a proteção dura até 4 meses. A loja indica reaplicar a cada 30 ou 45 dias, para manter.</p></div></div>
</div>
<div class="two"><div class="col"><h3>Pneus e plásticos</h3><p>Limpe antes com o limpador próprio. Aplique o condicionador em pouca quantidade e retire o excesso. O acabamento pode ser acetinado ou mais brilhante, conforme o produto e o número de demãos.</p></div>
<div class="col"><h3>Vidros</h3><p>Use um limpador específico para vidros e um pano separado, de microfibra, que não seja usado na pintura.</p></div></div>
<div class="tip"><b>Atenção.</b> Selantes e condicionadores têm modo de uso próprio. Leia o rótulo e siga a diluição, o tempo e o tipo de superfície indicados pelo fabricante.</div>
''', '', True)

# cap 6
page(head('Capítulo 6', 'Mitos e erros que você precisa largar') + '''
<div class="myths">
<div class="m"><span class="x">Mito</span><p><b>"Quanto mais espuma, mais limpa a lavagem."</b></p><p>Espuma ajuda a soltar a sujeira e a lubrificar, mas o que protege a pintura é o método: pré-lavagem, dois baldes e microfibra limpa.</p></div>
<div class="m"><span class="x">Mito</span><p><b>"Toalha que caiu no chão ainda serve."</b></p><p>Ela pegou partículas duras. Separe e lave antes de usar de novo.</p></div>
<div class="m"><span class="x">Mito</span><p><b>"Posto de lavagem é igual a lavar em casa."</b></p><p>Escovas e panos de uso coletivo podem acumular a sujeira de vários carros. Em casa você controla o que encosta na pintura.</p></div>
<div class="m"><span class="x">Mito</span><p><b>"Detergente de cozinha serve de shampoo."</b></p><p>Ele pode remover a proteção da pintura e ressecar plásticos e borrachas. Use shampoo automotivo.</p></div>
<div class="m"><span class="x">Mito</span><p><b>"Lavar toda semana estraga a pintura."</b></p><p>Quem estraga é o método. A sujeira acumulada na pintura é pior do que uma lavagem bem feita.</p></div>
</div>
''', '', True)

# cap 7
page(head('Capítulo 7', 'Rotina de manutenção', 'Uma rotina simples vale mais do que uma lavagem perfeita de vez em quando.') + '''
<div class="cards3">
<div class="c"><h4>A cada 15 dias</h4><p>Lavagem completa: pré-lavagem, dois baldes, secagem e condicionador nos pneus.</p></div>
<div class="c"><h4>A cada 30 a 45 dias</h4><p>Reaplicação do selante, conforme a orientação do fabricante do produto.</p></div>
<div class="c"><h4>A cada 3 meses</h4><p>Revise o kit: troque o que estiver gasto e confira o estado das luvas e toalhas.</p></div>
</div>
<h3>Cuide das suas microfibras</h3>
<ul class="big">
<li>Lave as microfibras separadas de roupas, em água morna ou fria.</li>
<li>Não use amaciante nem alvejante. Eles tiram a capacidade de absorver e de reter sujeira.</li>
<li>Seque sem calor alto.</li>
<li>Separe as de pintura das de rodas e de limpeza pesada, e nunca as misture.</li>
<li>Pano com cheiro, duro ou desfiado deve ser descartado.</li>
</ul>
''', '', True)

# checklist
chk = ['Carro na sombra e lataria fria', 'Dois baldes com separador montados (shampoo e água)', 'Luva da pintura e luva das rodas separadas', 'Rodas e pneus lavados primeiro', 'Enxágue geral, de cima para baixo', 'Pré-lavagem aplicada e enxaguada', 'Lavagem em linhas retas, da parte mais limpa para a mais suja', 'Luva enxaguada no balde de água antes de voltar ao shampoo', 'Enxágue final, de cima para baixo', 'Secagem com toalha de microfibra, sem pressionar', 'Condicionador aplicado no pneu, excesso retirado', 'Selante aplicado, quando for o dia']
page(head('Checklist', 'Checklist da lavagem', 'Imprima ou marque na tela do celular.') + '<ul class="chk">' + ''.join('<li><span class="bx"></span>%s</li>' % c for c in chk) + '</ul>', '', True)

# próximo passo
gal = ''.join('<img src="%s">' % prep('assets/fotos/' + f, f.split('-')[0], 700) for f in ['f05-porsche-traseira.jpg', 'f06-porsche-roda.jpg', 'f08-chery-frente-noite.jpg', 'f01-ranger-roda-detalhe.jpg'])
page(head('Obrigado', 'Agora é com você', 'Lave com calma, siga a ordem e comece pelo kit que cabe no seu momento.') + '''
<p>Se este e-book ajudou, compartilhe o resultado da sua lavagem. Eu adoro ver os carros dos meus leitores brilhando.</p>
<div class="galeria">%s</div>
<p class="small c">Carros cuidados pelo Tidioli Studio.</p>
<div class="aviso"><b>Lembrete.</b> Siga as instruções de cada produto e reduza o risco com um bom método. Em dúvida sobre um produto ou sobre o seu tipo de pintura, procure um profissional.</div>
''' % gal, '', True)

# contracapa
page('<div class="center dark"><img class="lg3" src="%s"><p>Estética Automotiva</p></div>' % logo('horizontal-cor'), 'back', False)

# ---------------------------------------------------------------- sumário
toc_items = [('Boas-vindas', 'Boas-vindas'), ('Capítulo 1', 'Por que o carro fica riscado depois de lavar'), ('Capítulo 2', 'Os kits e os produtos'), ('Capítulo 3', 'Antes de molhar o carro'), ('Capítulo 4', 'O passo a passo da lavagem'), ('Capítulo 5', 'Proteção rápida'), ('Capítulo 6', 'Mitos e erros que você precisa largar'), ('Capítulo 7', 'Rotina de manutenção'), ('Checklist', 'Checklist da lavagem')]
nums = {}
n = 0
for cls, html, num in pages:
    n += 1
    mm = re.search(r'<span class="eyebrow">(.*?)</span>', html)
    if mm and mm.group(1) not in nums:
        nums[mm.group(1)] = n
toc = head('Sumário', 'O que tem aqui') + '<ul class="toc">' + ''.join(
    '<li><span class="t"><small>%s</small>%s</span><span class="pgn">%s</span></li>' % (a if a != b else '', b, nums.get(a, '')) for a, b in toc_items) + '</ul>'

# ---------------------------------------------------------------- HTML
CSS = open(S + 'ebook_pdf.css').read()
out = ['<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Lavagem Segura · Tidioli Studio</title>',
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Saira+Condensed:wght@500;600;800&family=Source+Sans+3:wght@400;500;600;700&display=swap">',
       '<style>' + CSS + '</style></head><body>']
n = 0
for cls, html, num in pages:
    html = html.replace('@@SUMARIO@@', toc)
    n += 1
    if num:
        foot = '<div class="ft"><img src="%s"><span>Lavagem Segura</span><b>%d</b></div>' % (logo('horizontal-preto'), n)
    else:
        foot = ''
    out.append('<section class="page %s">%s%s</section>' % (cls, html, foot))
out.append('</body></html>')
open(S + 'lavagem-segura.html', 'w').write('\n'.join(out))
print('paginas', len(pages), 'numeradas', n, 'produtos', len(P), 'kits', [(k, len(i)) for k, i in kits])
