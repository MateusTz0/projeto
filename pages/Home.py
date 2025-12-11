import streamlit as st
import random
import datetime
import pandas as pd
import feedparser

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Home", page_icon="🏠")

# BLOQUEIO DE ACESSO
if "autenticado" not in st.session_state or not st.session_state.autenticado:
    st.warning("⚠️ Você precisa se cadastrar para acessar esta página.")
    st.stop()

if "usuarios" not in st.session_state:
    st.session_state.usuarios = []
if "respostas_quiz" not in st.session_state:
    st.session_state.respostas_quiz = {}
if "historico" not in st.session_state:
    st.session_state.historico = []

# ----------------
# DADOS DO SISTEMA
# ----------------

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

# ----------------------
# SORTEIO DA MATÉRIA DO DIA
# ----------------------
if "area_do_dia" not in st.session_state:
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

    tempo = random.randint(30, 180)
    horas = tempo // 60
    minutos = tempo % 60
    st.session_state.tempo_sugerido = f"{horas:02}h {minutos:02}m"

# --------
# QUESTÕES
# --------

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
            {"pergunta": "Qual é a parte inicial de um texto dissertativo?",
             "alternativas": ["Introdução", "Conclusão", "Título", "Proposta"],
             "correta": "Introdução"},
            {"pergunta": "O propósito da conclusão é:",
             "alternativas": ["Encerrar a ideia", "Apresentar fatos novos", "Criar suspense", "Confundir o leitor"],
             "correta": "Encerrar a ideia"},
            {"pergunta": "Um argumento é:",
             "alternativas": ["Uma justificativa", "Um verbo", "Um desenho", "Uma opinião solta"],
             "correta": "Uma justificativa"},
        ],
        "Médio": [
            {"pergunta": "A tese é:",
             "alternativas": ["A opinião principal", "Um dado estatístico", "Um exemplo", "Uma metáfora"],
             "correta": "A opinião principal"},
            {"pergunta": "A coesão textual se refere a:",
             "alternativas": ["Ligação entre as partes", "Repetições aleatórias", "Velocidade da leitura", "Número de parágrafos"],
             "correta": "Ligação entre as partes"},
            {"pergunta": "Um conectivo adversativo expressa:",
             "alternativas": ["Oposição", "Adição", "Causa", "Conclusão"],
             "correta": "Oposição"},
        ],
        "Difícil": [
            {"pergunta": "Uma intervenção completa no ENEM precisa ter:",
             "alternativas": ["Ação + agente + modo + efeito", "Apenas ação", "Somente citação", "Exemplos pessoais"],
             "correta": "Ação + agente + modo + efeito"},
            {"pergunta": "Citação indireta é:",
             "alternativas": ["Ideia de outro autor com suas palavras", "Cópia literal", "Opinião sem fonte", "Fato inventado"],
             "correta": "Ideia de outro autor com suas palavras"},
            {"pergunta": "A norma-padrão exige o uso de:",
             "alternativas": ["Estruturas formais", "Gírias", "Emojis", "Abreviações informais"],
             "correta": "Estruturas formais"},
        ]
    }
}

# ------------------------------------
# PÁGINAS: Notícias e Cursos (via RSS)
# ------------------------------------

def page_noticias():
    st.title("📰 Notícias - Atualidades do Dia")
    st.write("Notícias reais e atualizadas automaticamente (via RSS).")

    feeds = {
        "G1 - Brasil": "https://g1.globo.com/rss/g1/brasil/",
        "G1 - Mundo": "https://g1.globo.com/rss/g1/mundo/",
        "BBC Brasil": "https://feeds.bbci.co.uk/portuguese/rss.xml",
        "UOL Notícias": "https://rss.uol.com.br/feed/noticias.xml",
    }

    for nome, url in feeds.items():
        st.subheader(f"🌍 {nome}")
        try:
            noticias = feedparser.parse(url)
            if hasattr(noticias, "entries") and noticias.entries:
                for item in noticias.entries[:7]:
                    published = item.get('published', item.get('pubDate', ''))
                    st.markdown(f"- [{item.title}]({item.link}) — {published}")
            else:
                st.info(f"Nenhuma notícia encontrada em {nome}.")
        except Exception as e:
            st.error(f"Erro ao carregar {nome}: {e}")

        st.write("---")

def page_cursos():
    st.title("📘 Cursos & Oportunidades — Notícias Reais")
    st.write("Acompanhe novidades sobre cursos, educação técnica, bolsas e oportunidades.")

    feeds = {
        "Ministério da Educação (MEC)": "https://www.gov.br/mec/pt-br/assuntos/noticias/rss",
        "G1 - Educação": "https://g1.globo.com/rss/g1/educacao/",
        "Educação Profissional": "https://www.gov.br/pt-br/noticias/educacao-e-pesquisa/RSS",
    }

    for nome, url in feeds.items():
        st.subheader(f"📌 {nome}")
        try:
            noticias = feedparser.parse(url)
            if hasattr(noticias, "entries") and noticias.entries:
                for item in noticias.entries[:6]:
                    published = item.get('published', item.get('pubDate', ''))
                    st.markdown(f"- [{item.title}]({item.link}) — {published}")
            else:
                st.info(f"Nenhuma notícia encontrada em {nome}.")
        except Exception as e:
            st.error(f"Erro ao carregar {nome}: {e}")
        st.write("---")

    st.write("### 🎁 Em breve: recomendação inteligente de cursos personalizados!")

# --------------
# PÁGINA INICIAL
# --------------
def page_home():
    st.title("🏠 Página Inicial")
    st.subheader(f"📅 Data: {datetime.date.today().strftime('%d/%m/%Y')}")
    st.write("---")

    st.markdown("## 🎯 Área Principal do Dia")
    st.markdown(f"<h2 style='color:#1E90FF'>{st.session_state.area_do_dia}</h2>", unsafe_allow_html=True)

    st.markdown("## 📚 Matéria Sugerida")
    st.markdown(f"<h2 style='color:#32CD32'>{st.session_state.materia_do_dia}</h2>", unsafe_allow_html=True)

    st.markdown("## 🕘 Tempo Sugerido")
    st.markdown(f"<h2 style='color:#FFD700'>{st.session_state.tempo_sugerido}</h2>", unsafe_allow_html=True)

    st.write("---")
    st.markdown("## 🎚️ Escolha a Dificuldade:")

    nivel = st.radio("Selecione:", ["Fácil", "Médio", "Difícil"], index=1)

    if st.button("Confirmar"):
        st.session_state.nivel_estudo = nivel
        st.success(f"Nível definido: **{nivel}**")

def page_questões():
    st.title("📒 Bem vindo ao nosso — Quiz Diário")

    if "nivel_estudo" not in st.session_state:
        st.warning("⚠️ Defina a dificuldade na Página Inicial primeiro!")
        return

    area = st.session_state.area_do_dia
    nivel = st.session_state.nivel_estudo
    perguntas = quiz.get(area, {}).get(nivel, [])

    st.subheader(f"Área: **{area}** — Dificuldade: **{nivel}**")
    st.write("---")

    # --------------------------
    # BARRA DE PROGRESSO DO QUIZ
    # --------------------------
    total_perguntas = len(perguntas)
    respostas_dadas = sum(
        1 for i in range(total_perguntas)
        if st.session_state.respostas_quiz.get(f"{area}_{nivel}_{i}") is not None
    )

    progresso = respostas_dadas / total_perguntas if total_perguntas > 0 else 0
    st.progress(progresso)

    # -----------------------
    # EMBARALHAMENTO DAS QUESTÕES
    # -----------------------
    for i, q in enumerate(perguntas):
        key = f"{area}_{nivel}_{i}"

        if f"map_{key}" not in st.session_state:
            alternativas_embaralhadas = q["alternativas"][:]
            random.shuffle(alternativas_embaralhadas)

            st.session_state[f"map_{key}"] = {
                "correta": q["correta"],
                "alternativas": alternativas_embaralhadas
            }

        alternativas = st.session_state[f"map_{key}"]["alternativas"]

        st.session_state.respostas_quiz[key] = st.radio(
            q["pergunta"],
            alternativas,
            key=key
        )

    # -----------------
    # BOTÃO DE ENVIAR
    # -----------------
    if st.button("Enviar Respostas"):
        score = 0
        detalhes = []

        for i, q in enumerate(perguntas):
            key = f"{area}_{nivel}_{i}"
            resp = st.session_state.respostas_quiz.get(key, None)
            correta = st.session_state[f"map_{key}"]["correta"]
            acerto = (resp == correta)

            detalhes.append({"pergunta": q["pergunta"], "sua": resp, "certa": correta, "acertou": acerto})
            if acerto:
                score += 1

        # Resultado
        st.success(f"Você acertou **{score}/{len(perguntas)}**!")

        # -------------------------
        # ESTATÍSTICAS DE DESEMPENHO
        # -------------------------
        percentual = (score / len(perguntas)) * 100
        st.subheader("📊 Estatísticas do Desempenho")

        col1, col2, col3 = st.columns(3)
        col1.metric("Acertos", score)
        col2.metric("Total", len(perguntas))
        col3.metric("Desempenho (%)", f"{percentual:.1f}%")

        if percentual == 100:
            st.success("🎉 Perfeito! Você gabaritou!")
        elif percentual >= 70:
            st.info("👏 Bom trabalho! Continue assim.")
        else:
            st.warning("💡 Você pode melhorar! Tente novamente mais tarde.")

        # Salvar no histórico
        st.session_state.historico.append({
            "data": datetime.date.today().strftime('%d/%m/%Y'),
            "area": area,
            "nivel": nivel,
            "materia": st.session_state.materia_do_dia,
            "score": score,
            "total": len(perguntas),
            "detalhes": detalhes,
            "percentual": percentual
        })

# ----------
# HISTÓRICO
# ---------
def page_historico():
    st.title("📜 Registro de Estudos")

    if not st.session_state.historico:
        st.info("Nenhum estudo registrado ainda.")
        return

    for item in st.session_state.historico:
        st.write("---")
        st.subheader(f"📅 {item['data']} — {item['area']} ({item['nivel']})")
        st.write(f"Matéria: **{item['materia']}**")
        st.write(f"Resultado: **{item['score']} / {item['total']}**")

        with st.expander("Ver detalhes"):
            for d in item["detalhes"]:
                if d["acertou"]:
                    st.markdown(f"✅ **{d['pergunta']}** — {d['sua']}")
                else:
                    st.markdown(f"❌ **{d['pergunta']}** — Sua: {d['sua']} / Correta: {d['certa']}")

# ------------
# MENU LATERAL
# -------------
st.sidebar.title("Menu Principal")

page = st.sidebar.radio(
    "Navegue entre as páginas:",
    ["Página Inicial", "Questões", "Histórico", "Notícias", "Cursos"]
)

# Controle das páginas
if page == "Página Inicial":
    page_home()

elif page == "Questões":
    page_questões()

elif page == "Histórico":
    page_historico()

elif page == "Notícias":
    page_noticias()

elif page == "Cursos":
    page_cursos()
