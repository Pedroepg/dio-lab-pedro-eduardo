import streamlit as st
import json as js
import pandas as pd
import requests

# Configuração
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "llama3"

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

# interface


st.title("Poupança Poupada")

if pergunta := st.chat_input("Sua dúvida de investimento..."):
    st.chat_message("user").write(pergunta)
    with st.spinner("..."):
        st.chat_message("assistant").write(perguntar(pergunta))
