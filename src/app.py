import streamlit as st
import json as js
import pandas as pd
import requests

# Configuração
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

st.set_page_config(
    page_title="Poupança Poupada",
    page_icon="💰",
    layout="centered",
)

# ---------- Estilo (tema vermelho Bradesco) ----------
st.markdown("""
    <style>
        :root {
            --bradesco-red: #CC092F;
            --bradesco-red-dark: #9C0722;
        }

        .stApp {
            background: linear-gradient(180deg, var(--bradesco-red) 0%, var(--bradesco-red-dark) 100%);
        }

        [data-testid="stSidebar"] {
            background-color: #7a0619;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        .titulo-agente {
            text-align: center;
            color: #ffffff;
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 0;
        }

        .subtitulo-agente {
            text-align: center;
            color: #f3d0d6;
            font-size: 1rem;
            margin-top: 0;
            margin-bottom: 1.5rem;
        }

        [data-testid="stChatMessage"] {
            background-color: #ffffff;
            border-radius: 14px;
            padding: 0.5rem 0.9rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] div {
            color: #111111 !important;
        }

        [data-testid="stChatInput"] textarea {
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Carregamento de dados
historico = pd.read_csv('data/historico_atendimento.csv')
transacoes = pd.read_csv('data/transacoes.csv')

with open('data/perfil_investidor.json', 'r', encoding='utf-8') as f:
    perfil = js.load(f)

with open('data/produtos_financeiros.json', 'r', encoding='utf-8') as f:
    produtos = js.load(f)

# Criando contexto para o agente
contexto = f"""
Cliente: {perfil['nome']}, {perfil['idade']} anos, Perfil - {perfil['perfil_investidor']} 
Objetivo: {perfil['objetivo_principal']}
Patrimônio: {perfil['patrimonio_total']} | Reserva: {perfil['reserva_emergencia_atual']}

Transações recentes:
{transacoes.to_string(index=False)}

Atendimentos anteriores:
{historico.to_string(index=False)}

Produtos disponíveis:
{js.dumps(produtos, indent=2, ensure_ascii=False)}
"""

# Definição de um prompt para o agente
system_prompt = """
Você é um agente especializado em indicações seguras de investimentos para pessoas leigas sobre investimentos que tem seu dinheiro guardado na conta poupança.

Objetivo: Seu objetivo é identificar valores guardados na conta poupança dos clientes e indicar investimentos seguros para aplicações.

REGRAS:
1. Sempre baseie suas respostas nos dados fornecidos para dar indicações
2. Nunca invente informações financeiras
3. Se não souber algo, não invente informações falsas e ofereça alternativas
4. Utilize uma linguagem simples e encorajadora
5. Nunca forneça dados sensíveis sobre clientes como senhas e logins
6. Responda de forma direta e explicativa.
7. Não responda perguntas fora do escopo financeiro ou de temas aleatórios

"""


# Chamando Ollama
def perguntar(msg):
    prompt = f"""
    {system_prompt}

    Contexto do cliente:
    {contexto}

    Pergunta: {msg}"""

    r = requests.post(OLLAMA_URL, json={
                      "model": MODELO, "prompt": prompt, "stream": False})
    return r.json()["response"]


# ---------- Sidebar com o perfil do cliente ----------
with st.sidebar:
    st.markdown("### 👤 Perfil do cliente")
    st.write(f"**Nome:** {perfil['nome']}")
    st.write(f"**Idade:** {perfil['idade']} anos")
    st.write(f"**Perfil de investidor:** {perfil['perfil_investidor'].capitalize()}")
    st.write(f"**Objetivo:** {perfil['objetivo_principal']}")
    st.markdown("---")
    st.write(f"**Patrimônio total:** R$ {perfil['patrimonio_total']:,.2f}")
    st.write(f"**Reserva de emergência:** R$ {perfil['reserva_emergencia_atual']:,.2f}")

# ---------- Interface principal ----------
st.markdown('<p class="titulo-agente">💰 Poupança Poupada</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo-agente">Seu consultor de investimentos seguros</p>', unsafe_allow_html=True)

if pergunta := st.chat_input("Sua dúvida de investimento..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("Consultando as melhores opções para você..."):
        st.chat_message("assistant").write(perguntar(pergunta))
