import streamlit as st

# Configuração da Página
st.set_page_config(
    page_title="LINCE - Guia de Liderança",
    page_icon="🦁", # Usando um leão/lince como representação
    layout="centered"
)

# Estilização CSS para aproximar da identidade visual (Laranja/Cinza Petrobras/Industrial)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        background-color: #F39C12;
        color: white;
        font-weight: bold;
        border-radius: 10px;
    }
    .main-header {
        text-align: center;
        color: #2C3E50;
    }
    .sub-header {
        color: #E67E22;
        font-weight: bold;
    }
    .card {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #E67E22;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- DADOS DO APLICATIVO (Extraídos do PDF e Prompt) ---

DB_CONVERSAS = {
    "1. Feedback de desempenho insatisfatório": {
        "Objetivo": "Alinhar resultados e promover melhoria sem desmotivar.",
        "Riscos": "Ser duro demais, usar rótulos ou comparar pessoas.",
        "Fundamentos": "Comunicação não violenta (observar sem julgar, expressar impacto, propor caminhos).",
        "Exemplo": "“Tenho notado que as entregas dos relatórios têm atrasado. Isso impacta a segurança das operações. Como podemos resolver juntos?”"
    },
    "2. Postura inadequada ou comportamento desrespeitoso": {
        "Objetivo": "Corrigir atitudes preservando a dignidade da pessoa.",
        "Riscos": "Confronto direto, tom punitivo, falta de escuta.",
        "Fundamentos": "Liderança servidora e empática; foco em valores e comportamento observável.",
        "Exemplo": "“Percebi comentários que geraram desconforto na equipe. Podemos conversar sobre como isso foi percebido e o que podemos fazer diferente?”"
    },
    "3. Falta de colaboração entre áreas (OP x SMS x MA)": {
        "Objetivo": "Restabelecer diálogo e confiança mútua.",
        "Riscos": "Defender 'o lado' da própria área, reforçar divisões.",
        "Fundamentos": "Visão sistêmica: 'Temos visões diferentes, mas o mesmo objetivo'.",
        "Exemplo": "“Temos visões diferentes, mas o mesmo objetivo: operar com segurança e eficiência. Como podemos alinhar nossos processos?”"
    },
    "4. Falta de motivação ou sinais de esgotamento": {
        "Objetivo": "Compreender causas e oferecer apoio.",
        "Riscos": "Ignorar o emocional, reduzir tudo a metas.",
        "Fundamentos": "Inteligência emocional + escuta genuína + acolhimento.",
        "Exemplo": "“Tenho percebido que você está mais quieto. Está tudo bem? Algo está te sobrecarregando? Posso ajudar de alguma forma?”"
    },
    "5. Erros recorrentes / falhas operacionais": {
        "Objetivo": "Corrigir com foco no aprendizado e prevenção.",
        "Riscos": "Buscar culpados, gerar medo ou vergonha.",
        "Fundamentos": "Cultura justa + foco em lições aprendidas.",
        "Exemplo": "“O que podemos aprender com esse evento para evitar repetições? Há algo no processo que possamos melhorar?”"
    },
    "6. Discussão sobre promoção ou não promoção": {
        "Objetivo": "Explicar critérios com transparência e orientar desenvolvimento.",
        "Riscos": "Falta de clareza, parecer injusto ou pessoal.",
        "Fundamentos": "Transparência + feedback construtivo + plano de desenvolvimento.",
        "Exemplo": "“A decisão foi baseada nos critérios técnicos e comportamentais. Vamos construir juntos um plano para te preparar para a próxima oportunidade.”"
    },
    "7. Conflitos interpessoais entre liderados": {
        "Objetivo": "Promover reconciliação e cooperação.",
        "Riscos": "Tomar partido, minimizar o conflito.",
        "Fundamentos": "Mediação + escuta ativa + foco em interesses comuns.",
        "Exemplo": "“Ambos têm o mesmo objetivo, que é entregar com segurança e qualidade. Vamos entender o ponto de cada um e buscar um caminho comum.”"
    },
    "8. Mudança de função, reestruturação ou decisão impopular": {
        "Objetivo": "Comunicar com clareza e empatia, preservando o engajamento.",
        "Riscos": "Falar apenas o 'que' sem explicar o 'porquê'.",
        "Fundamentos": "Comunicação transparente + contextualização + empatia.",
        "Exemplo": "“Essa mudança foi pensada para fortalecer a equipe e os resultados. Entendo que gera dúvidas — quero te ouvir sobre isso.”"
    },
    "9. Retorno de afastamento (saúde, licença etc.)": {
        "Objetivo": "Acolher e reintegrar o colaborador de forma respeitosa.",
        "Riscos": "Pressionar por resultados imediatos, ignorar limitações.",
        "Fundamentos": "Liderança empática + cuidado humano.",
        "Exemplo": "“Seja bem-vindo de volta! Como está se sentindo? Vamos alinhar juntos o ritmo do retorno para garantir seu bem-estar e desempenho.”"
    },
    "10. Desenvolvimento e mentoria": {
        "Objetivo": "Ampliar potencial e autoconhecimento.",
        "Riscos": "Focar apenas em falhas; não definir metas.",
        "Fundamentos": "Comunicação empática + foco na dignidade e no aprendizado.",
        "Exemplo": "“Você tem evoluído bem. Vamos definir juntos os próximos passos para continuar crescendo?”"
    }
}

PERFIS = {
    "Colérico": {
        "Desc": "Forte, líder, decidido, direto.",
        "Fortes": "Liderança, iniciativa, foco em resultados, coragem para desafios.",
        "Atencao": "Tendência a dominar conversas, impaciência, dificuldade em ouvir opiniões diferentes."
    },
    "Sanguíneo": {
        "Desc": "Alegre, comunicativo, espontâneo.",
        "Fortes": "Entusiasmo, facilidade de comunicação, rapidez em criar conexões, adaptabilidade.",
        "Atencao": "Impulsividade, falta de foco, dificuldade com rotinas e dispersão."
    },
    "Melancólico": {
        "Desc": "Sensível, profundo, analítico.",
        "Fortes": "Empatia, atenção aos detalhes, análise profunda, busca por sentido e valores.",
        "Atencao": "Perfeccionismo excessivo, autocrítica intensa, procrastinação por medo de errar."
    },
    "Fleumático": {
        "Desc": "Calmo, equilibrado, pacificador.",
        "Fortes": "Serenidade sob pressão, capacidade de mediação, pensamento lógico, paciência.",
        "Atencao": "Passividade, resistência a mudanças, evitar confrontos necessários."
    }
}

# --- NAVEGAÇÃO ---

st.markdown("<h1 class='main-header'>LINCE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Guia Prático de Liderança, Inteligência Interpessoal & Comunicação Eficaz</p>", unsafe_allow_html=True)

aba1, aba2, aba3 = st.tabs(["🧩 Teste de Temperamento", "📋 Checklist Mediação", "💬 Conversas Difíceis"])

# --- MÓDULO 1: TESTE ---
with aba1:
    st.header("Descubra seu Temperamento Predominante")
    st.info("💡 Marque a alternativa que mais se parece com você na prática (não a que gostaria de ser).")

    # Parte 1
    st.markdown("### Parte 1: Reações e Energia")
    q1 = st.radio("1. Em grupo, diante de polêmica:", 
                  ["A) Analiso rapidamente e emito minha opinião!", 
                   "B) Analiso com calma, quase sempre sem dar parecer."], index=None)
    
    q2 = st.radio("2. Diante de um projeto novo:", 
                  ["A) Me empolgo com a novidade/desafio!", 
                   "B) Olho com medo e dúvidas se conseguirei."], index=None)
    
    q3 = st.radio("3. Sua energia mental vai para:", 
                  ["A) Mundo exterior, ação (às vezes sem refletir).", 
                   "B) Mundo interior, reflexão (compreender antes de agir)."], index=None)

    # Parte 2
    st.markdown("---")
    st.markdown("### Parte 2: Relacionamento e Emoção")
    q4 = st.radio("4. Colega prejudicando a equipe (problemas pessoais):", 
                  ["A) Converso ou aciono o gerente. O grupo não pode ser afetado.", 
                   "B) Flexibilizo. A situação pessoal pesa."], index=None)
    
    q5 = st.radio("5. Quando alguém é ingrato:", 
                  ["A) Não relevo fácil, incomoda por muito tempo.", 
                   "B) Fico chateado na hora, mas depois passa."], index=None)
    
    q6 = st.radio("6. Mudam um combinado de duas semanas atrás:", 
                  ["A) Me sinto desrespeitado.", 
                   "B) Não ligo muito, tudo se ajeita."], index=None)

    if st.button("Ver Resultado"):
        if None in [q1, q2, q3, q4, q5, q6]:
            st.error("Por favor, responda todas as perguntas.")
        else:
            # Lógica de Contagem
            r1 = [q1, q2, q3]
            r2 = [q4, q5, q6]
            
            # Conta 'A's na parte 1
            count_a1 = sum(1 for x in r1 if x.startswith("A"))
            letra1 = "A" if count_a1 >= 2 else "B"
            
            # Conta 'A's na parte 2
            count_a2 = sum(1 for x in r2 if x.startswith("A"))
            letra2 = "A" if count_a2 >= 2 else "B"
            
            resultado_chave = ""
            if letra1 == "A" and letra2 == "A": resultado_chave = "Colérico"
            elif letra1 == "A" and letra2 == "B": resultado_chave = "Sanguíneo"
            elif letra1 == "B" and letra2 == "A": resultado_chave = "Melancólico"
            elif letra1 == "B" and letra2 == "B": resultado_chave = "Fleumático"
            
            dados = PERFIS[resultado_chave]
            
            st.success(f"Seu temperamento predominante é: **{resultado_chave.upper()}**")
            st.markdown(f"_{dados['Desc']}_")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### ✅ Pontos Fortes")
                st.write(dados['Fortes'])
            with col2:
                st.markdown("#### ⚠️ Pontos de Atenção")
                st.write(dados['Atencao'])
            
            st.markdown("---")
            st.caption("“Você pode desenvolver habilidades de todos os temperamentos.”")

# --- MÓDULO 2: CHECKLIST ---
with aba2:
    st.header("Checklist de Mediação de Conflitos")
    st.write("Marque as etapas conforme você as completa.")

    st.subheader("1. Antes da Conversa")
    c1 = st.checkbox("Levantei fatos e dados objetivos")
    c2 = st.checkbox("Identifiquei impactos para equipe/REPLAN")
    c3 = st.checkbox("Avaliei meu estado emocional")
    c4 = st.checkbox("Defini o objetivo da conversa")
    c5 = st.checkbox("Antecipei preocupações das partes")
    c6 = st.checkbox("Escolhi local e momento adequados")

    st.subheader("2. Durante a Conversa")
    c7 = st.checkbox("Iniciei com empatia")
    c8 = st.checkbox("Mantive o tom colaborativo")
    c9 = st.checkbox("Pratiquei escuta ativa")
    c10 = st.checkbox("Foquei em interesses comuns")
    c11 = st.checkbox("Evitei julgamentos")
    c12 = st.checkbox("Registrei as ideias")

    st.subheader("3. Após a Conversa")
    c13 = st.checkbox("Plano de ação com prazos definidos")
    c14 = st.checkbox("Comuniquei decisões")
    c15 = st.checkbox("Monitorei ações")
    c16 = st.checkbox("Dei feedback sobre a evolução")

    total = sum([c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16])
    progresso = total / 16
    st.progress(progresso)
    
    if progresso == 1.0:
        st.balloons()
        st.success("Processo de mediação completo!")

    with st.expander("💡 Dicas Rápidas (Toque para abrir)"):
        st.markdown("""
        * **Mantenha a calma**
        * Ataque o problema, **não a pessoa**
        * Valorize diferenças
        * Seja transparente
        * **Conflito = Oportunidade de melhoria**
        """)

# --- MÓDULO 3: CONVERSAS DIFÍCEIS ---
with aba3:
    st.header("Painel de Conversas Difíceis")
    st.markdown("Selecione o cenário para carregar o guia dinâmico do **Notebook LINCE**.")
    
    cenario = st.selectbox("Qual o tipo de conversa?", list(DB_CONVERSAS.keys()))
    
    if cenario:
        data = DB_CONVERSAS[cenario]
        
        st.markdown(f"<div class='card'><h4>🎯 Objetivo</h4>{data['Objetivo']}</div>", unsafe_allow_html=True)
        
        col_risco, col_lince = st.columns(2)
        with col_risco:
            st.warning(f"**⚠️ Riscos / Erros Comuns:**\n\n{data['Riscos']}")
        with col_lince:
            st.info(f"**🦁 Fundamentos LINCE:**\n\n{data['Fundamentos']}")
        
        st.markdown("### 🗣️ Exemplo de Fala Prática")
        st.code(data['Exemplo'], language="text")

# Rodapé
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey; font-size: 0.8em;'>LINCE App v1.0 | Baseado no Programa Escalada REPLAN</p>", unsafe_allow_html=True)
