import streamlit as st
import random
import datetime
import pandas as pd

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Home", page_icon="🏠")

# BLOQUEIO DE ACESSO
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.warning("⚠️ Você precisa se cadastrar para acessar esta página.")
    st.stop()

# GARANTIR LISTA DE USUÁRIOS
if "usuarios" not in st.session_state:
    st.session_state.usuarios = []





# noticias.py
import streamlit as st
import feedparser

FEEDS = [
    "https://g1.globo.com/rss/g1/educacao/",   # G1 Educação
    "https://www.bbc.co.uk/portuguese/index.xml"  # BBC Portuguese (exemplo)
]

def page_noticias():
    st.title("📰 Notícias - Educação e Ciência")
    for feed in FEEDS:
        try:
            d = feedparser.parse(feed)
            st.subheader(d.feed.get('title','Feed'))
            for entry in d.entries[:5]:
                st.markdown(f"- [{entry.title}]({entry.link}) — {entry.get('published','')}")
        except Exception as e:
            st.error(f"Erro ao carregar feed {feed}: {e}")
import streamlit as st

def pagina():
    st.title("Cursos Gratuitos Recomendados")

    st.write("Aqui você pode adicionar links reais de cursos gratuitos:")

    st.markdown("""
    ### 📘 Programação
    - [Python para Iniciantes – Curso em Vídeo](https://www.cursoemvideo.com/course/python-3/)
    - [Introdução à Programação – Udemy](https://www.udemy.com/course/introducao-a-programacao/)
    - [Git e GitHub – DIO](https://web.dio.me/course/introducao-ao-git-e-ao-github/learning/)

    ### 📗 Matemática
    - [Matemática Básica – Khan Academy](https://pt.khanacademy.org/math)
    - [Funções – Univesp](https://www.youtube.com/watch?v=t6v5biZdmFw)

    ### 📙 Inglês
    - [Duolingo](https://www.duolingo.com/)
    - [BBC Learning English](https://www.bbc.co.uk/learningenglish)
    """)






# ---------------------------------------------
# DADOS DO SISTEMA
# ---------------------------------------------

areas_principais = [
    "Linguagens",
    "Ciências Humanas",
    "Ciências da Natureza",
    "Matemática",
    "Redação"
]

materias_linguagens = [
    "Língua Portuguesa", "Literatura", "Língua Estrangeira (Inglês e Espanhol)",
    "Artes", "Educação Física"
]

materias_ciencias_humanas = ["História", "Geografia", "Filosofia", "Sociologia"]
materias_ciencias_natureza = ["Biologia", "Química", "Física"]
materias_matematica = ["Álgebra", "Geometria", "Trigonometria"]
materias_redação = ["Acentuação", "Caligrafia", "Estrutura"]

# ---------------------------------------------
# SORTEIO DO FOCO DIÁRIO (matéria e tempo)
# ---------------------------------------------
if "area_do_dia" not in st.session_state or "materia_do_dia" not in st.session_state:
    area_do_dia = random.choice(areas_principais)
    st.session_state.area_do_dia = area_do_dia

    if area_do_dia == "Linguagens":
        materia = random.choice(materias_linguagens)
    elif area_do_dia == "Ciências Humanas":
        materia = random.choice(materias_ciencias_humanas)
    elif area_do_dia == "Ciências da Natureza":
        materia = random.choice(materias_ciencias_natureza)
    elif area_do_dia == "Matemática":
        materia = random.choice(materias_matematica)
    else:
        materia = random.choice(materias_redação)

    st.session_state.materia_do_dia = materia

    min_minutes = 30
    max_minutes = 180
    tempo = random.randint(min_minutes, max_minutes)
    horas = tempo // 60
    minutos = tempo % 60
    st.session_state.tempo_sugerido = f"{horas:02}h {minutos:02}m"

# ---------------------------------------------
# QUIZ COMPLETO POR ÁREA E NÍVEL (ENEM-like, reformulado)
# ---------------------------------------------
quiz = {
    "Linguagens": {
        "Fácil": [
            {"pergunta": "O plural de 'pão' é:", "alternativas": ["Pãos", "Pães", "Pãozes", "Paones"], "correta": "Pães"},
            {"pergunta": "Qual é o antônimo de 'feliz'?", "alternativas": ["Alegre", "Contente", "Triste", "Animado"], "correta": "Triste"},
            {"pergunta": "Qual palavra está escrita corretamente?", "alternativas": ["Exceção", "Exceçãon", "Eceção", "Excesão"], "correta": "Exceção"},
        ],
        "Médio": [
            {"pergunta": "Em: 'Vendem-se casas', o sujeito é:", "alternativas": ["Indeterminado", "Composto", "Oculto", "Inexistente"], "correta": "Indeterminado"},
            {"pergunta": "A frase 'Ela chorou rios' apresenta:", "alternativas": ["Hipérbole", "Metonímia", "Metáfora", "Ironia"], "correta": "Hipérbole"},
            {"pergunta": "Em qual opção o uso da crase está correto?", "alternativas": ["Fui à festa ontem.", "Vi o rapaz à distância.", "Entreguei o livro à ele.", "Cheguei à meia-noite."], "correta": "Fui à festa ontem."},
        ],
        "Difícil": [
            {"pergunta": "A polissemia ocorre em:", "alternativas": ["O banco emprestou dinheiro.", "Ele sentou no banco.", "O banco da praça estava velho.", "Todas as anteriores."], "correta": "Todas as anteriores."},
            {"pergunta": "‘Embora quisesse, não saiu.’ Classificação da oração:", "alternativas": ["Concessiva", "Causal", "Condicional", "Temporal"], "correta": "Concessiva"},
            {"pergunta": "Qual alternativa apresenta erro de regência?", "alternativas": ["Aspirei ao cargo.", "Assisti ao documentário.", "Prefiro sorvete do que bolo.", "Obedeci às regras."], "correta": "Prefiro sorvete do que bolo."},
        ],
    },

    "Ciências Humanas": {
        "Fácil": [
            {"pergunta": "Qual desses é um direito social?", "alternativas": ["Educação", "Lazer", "Votar", "Serviço militar"], "correta": "Educação"},
            {"pergunta": "A capital do Brasil é:", "alternativas": ["Brasília", "Rio de Janeiro", "Salvador", "São Paulo"], "correta": "Brasília"},
            {"pergunta": "O capitalismo é baseado em:", "alternativas": ["Lucro", "Coletivismo", "Economia fechada", "Ausência de mercado"], "correta": "Lucro"},
        ],
        "Médio": [
            {"pergunta": "O Iluminismo defendia:", "alternativas": ["Razão", "Absolutismo", "Feudalismo", "Teocentrismo"], "correta": "Razão"},
            {"pergunta": "A Guerra Fria foi caracterizada por:", "alternativas": ["Disputa ideológica", "Guerras diretas", "Colapso do feudalismo", "Conflito religioso"], "correta": "Disputa ideológica"},
            {"pergunta": "A escravidão no Brasil colonial era sustentada principalmente pela:", "alternativas": ["Mão de obra africana", "Mão de obra assalariada", "Mão de obra indígena", "Automação"], "correta": "Mão de obra africana"},
        ],
        "Difícil": [
            {"pergunta": "O Tratado de Tordesilhas dividia territórios entre:", "alternativas": ["Portugal e Espanha", "Brasil e Portugal", "Inglaterra e Espanha", "França e Portugal"], "correta": "Portugal e Espanha"},
            {"pergunta": "A teoria marxista considera que a história da humanidade é:", "alternativas": ["Luta de classes", "Ciclo religioso", "Naturalismo histórico", "Destino individual"], "correta": "Luta de classes"},
            {"pergunta": "O processo de urbanização acelerada no Brasil intensificou-se devido:", "alternativas": ["Industrialização", "Feudalismo tardio", "Êxodo europeu", "Crise agrária medieval"], "correta": "Industrialização"},
        ],
    },

    "Ciências da Natureza": {
        "Fácil": [
            {"pergunta": "A água ferve a aproximadamente:", "alternativas": ["100°C", "50°C", "150°C", "0°C"], "correta": "100°C"},
            {"pergunta": "As plantas produzem energia por meio da:", "alternativas": ["Fotossíntese", "Respiração celular", "Digestão", "Fermentação"], "correta": "Fotossíntese"},
            {"pergunta": "O átomo é composto por prótons, nêutrons e:", "alternativas": ["Elétrons", "Íons", "Ácidos", "Moléculas"], "correta": "Elétrons"},
        ],
        "Médio": [
            {"pergunta": "A força que puxa os objetos para o centro da Terra é:", "alternativas": ["Gravidade", "Magnetismo", "Atrito", "Empuxo"], "correta": "Gravidade"},
            {"pergunta": "A relação entre massa e volume é chamada de:", "alternativas": ["Densidade", "Pressão", "Velocidade", "Potência"], "correta": "Densidade"},
            {"pergunta": "Uma substância que acelera reações químicas é um:", "alternativas": ["Catalisador", "Oxidante", "Soluto", "Íon"], "correta": "Catalisador"},
        ],
        "Difícil": [
            {"pergunta": "Os ácidos nucleicos são formados por:", "alternativas": ["Nucleotídeos", "Aminoácidos", "Lipídios", "Monossacarídeos"], "correta": "Nucleotídeos"},
            {"pergunta": "A energia potencial gravitacional depende de:", "alternativas": ["Altura, massa e gravidade", "Temperatura", "Pressão atmosférica", "Carga elétrica"], "correta": "Altura, massa e gravidade"},
            {"pergunta": "A ligação que ocorre com compartilhamento de elétrons é:", "alternativas": ["Covalente", "Iônica", "Metálica", "Polarizante"], "correta": "Covalente"},
        ],
    },

    "Matemática": {
        "Fácil": [
            {"pergunta": "Quanto é 8 × 7?", "alternativas": ["56", "64", "48", "58"], "correta": "56"},
            {"pergunta": "A área de um quadrado de lado 4 é:", "alternativas": ["16", "8", "12", "20"], "correta": "16"},
            {"pergunta": "O número π (pi) vale aproximadamente:", "alternativas": ["3,14", "2,14", "4,3", "3,40"], "correta": "3,14"},
        ],
        "Médio": [
            {"pergunta": "A função y = 2x + 3 é:", "alternativas": ["Afim", "Quadrática", "Exponencial", "Constante"], "correta": "Afim"},
            {"pergunta": "A raiz quadrada de 81 é:", "alternativas": ["9", "8", "7", "6"], "correta": "9"},
            {"pergunta": "Uma progressão aritmética cresce adicionando sempre:", "alternativas": ["Uma constante", "Um múltiplo", "Uma potência", "Um quadrado perfeito"], "correta": "Uma constante"},
        ],
        "Difícil": [
            {"pergunta": "A derivada de x² é:", "alternativas": ["2x", "x", "x³", "1/x"], "correta": "2x"},
            {"pergunta": "A solução de log₂(8) é:", "alternativas": ["3", "2", "4", "1"], "correta": "3"},
            {"pergunta": "A matriz identidade possui:", "alternativas": ["1 na diagonal principal", "0 em todas as posições", "Apenas números iguais", "Valores negativos"], "correta": "1 na diagonal principal"},
        ],
    },

    "Redação": {
        "Fácil": [
            {"pergunta": "Qual é a parte inicial de um texto dissertativo?", "alternativas": ["Introdução", "Conclusão", "Título", "Proposta"], "correta": "Introdução"},
            {"pergunta": "O propósito da conclusão é:", "alternativas": ["Encerrar a ideia", "Apresentar fatos novos", "Contradizer argumentos", "Criar suspense"], "correta": "Encerrar a ideia"},
            {"pergunta": "Um argumento é:", "alternativas": ["Uma justificativa", "Um desenho", "Uma opinião solta", "Um verbo"], "correta": "Uma justificativa"},
        ],
        "Médio": [
            {"pergunta": "A tese é:", "alternativas": ["A opinião principal", "Um dado estatístico", "Um exemplo", "Um apelo emocional"], "correta": "A opinião principal"},
            {"pergunta": "A coesão textual se refere a:", "alternativas": ["Ligação entre as partes", "Conteúdo repetitivo", "Velocidade da leitura", "Caracteres especiais"], "correta": "Ligação entre as partes"},
            {"pergunta": "Um conectivo adversativo expressa:", "alternativas": ["Ideia de oposição", "Causa", "Adição", "Condição"], "correta": "Ideia de oposição"},
        ],
        "Difícil": [
            {"pergunta": "Uma intervenção completa no ENEM precisa ter:", "alternativas": ["Ação + agente + modo + efeito", "Apenas uma ação", "Somente citação", "Justificativa emocional"], "correta": "Ação + agente + modo + efeito"},
            {"pergunta": "Citação indireta é:", "alternativas": ["Ideia de outro autor com suas palavras", "Reprodução literal", "Um dado inventado", "Opinião pessoal sem fonte"], "correta": "Ideia de outro autor com suas palavras"},
            {"pergunta": "A norma-padrão exige o uso de:", "alternativas": ["Estruturas formais", "Gírias", "Abreviações informais", "Emojis no texto"], "correta": "Estruturas formais"},
        ],
    },
}

# ---------------------------------------------
# FUNÇÃO DA HOME
# ---------------------------------------------
def page_home():
    st.title("🏠 Página Inicial")
    st.write("Bem-vindo à página principal do sistema!")
    st.write("---")

    st.subheader(f"📅 Data: {datetime.date.today().strftime('%d/%m/%Y')}")
    st.write("---")

    st.markdown("## 🎯 Área Principal do Dia")
    st.markdown(f"**<p style='font-size: 32px; color: #1E90FF;'>{st.session_state.area_do_dia}</p>**", unsafe_allow_html=True)
    st.write("---")

    st.markdown("## 📚 Matéria Sugerida")
    st.markdown(f"**<p style='font-size: 28px; color: #32CD32;'>{st.session_state.materia_do_dia}</p>**", unsafe_allow_html=True)
    st.write("---")

    st.markdown("## 🕘 Tempo de Estudo Sugerido")
    st.markdown(f"**<p style='font-size: 32px; color: #FFD700;'>{st.session_state.tempo_sugerido}</p>**", unsafe_allow_html=True)

    # dificuldade
    st.write("---")
    st.markdown("## 🎚️ Escolha a Dificuldade do Estudo:")
    nivel = st.radio("Selecione:", ["Fácil", "Médio", "Difícil"], index=1)

    if st.button("Confirmar Dificuldade"):
        st.session_state.nivel_estudo = nivel
        st.success(f"Dificuldade confirmada: **{nivel}**")

    if "nivel_estudo" in st.session_state:
        st.info(f"Nível atual definido: **{st.session_state.nivel_estudo}**")

# ---------------------------------------------
# REGISTRO DE ESTUDOS + QUIZ (usa area sorteada)
# ---------------------------------------------
def page_registro():
    st.title("📒 Registro de Estudos — Quiz Diário")

    if "nivel_estudo" not in st.session_state:
        st.warning("⚠️ Defina a dificuldade na Página Inicial primeiro!")
        return

    area = st.session_state.area_do_dia
    nivel = st.session_state.nivel_estudo

    st.subheader(f"Área do dia: **{area}**  —  Dificuldade: **{nivel}**")
    st.write("---")

    # pega as perguntas da área e dificuldade
    perguntas_area = quiz.get(area, {}).get(nivel, [])
    if not perguntas_area:
        st.error("Não há perguntas definidas para essa área e nível.")
        return

    # inicializa armazenamento de respostas se não existir
    if "respostas_quiz" not in st.session_state:
        st.session_state.respostas_quiz = {}

    # renderiza perguntas (usa chaves únicas com area e index)
    for i, q in enumerate(perguntas_area):
        key = f"{area}_{nivel}_{i}"
        escolha = st.radio(q["pergunta"], q["alternativas"], key=key)
        st.session_state.respostas_quiz[key] = escolha

    # botão de envio
    if st.button("Enviar Respostas"):
        score = 0
        detalhes = []
        for i, q in enumerate(perguntas_area):
            key = f"{area}_{nivel}_{i}"
            resposta = st.session_state.respostas_quiz.get(key, None)
            correta = q["correta"]
            acerto = (resposta == correta)
            if acerto:
                score += 1
            detalhes.append({"pergunta": q["pergunta"], "sua": resposta, "certa": correta, "acertou": acerto})
        st.success(f"Você acertou **{score}/{len(perguntas_area)}** perguntas!")
        # mostra feedback detalhado
        with st.expander("Ver detalhes das respostas"):
            for d in detalhes:
                if d["acertou"]:
                    st.markdown(f"✅ **{d['pergunta']}** — Sua resposta: *{d['sua']}* (correta)")
                else:
                    st.markdown(f"❌ **{d['pergunta']}** — Sua resposta: *{d['sua']}* → correta: *{d['certa']}*")

# ---------------------------------------------
# MENU LATERAL
# ---------------------------------------------
st.sidebar.title("Menu Principal")
page = st.sidebar.radio("Navegue entre as páginas:", ["Página Inicial", "Registro"])

if page == "Página Inicial":
    page_home()
else:
    page_registro()
