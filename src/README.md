# Passo a passo

## Setup do Ollama

```bash
# 1. Baixar e instalar o Ollama (ollama.com)
# 2. Instalar o modelo de linguagem
ollama pull llama3

# 3. Testar a aplicação
ollama run llama3 'Olá!'
```

# Código completo

O código está estruturado no arquivo `app.py`

# Como rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests

# 2. Garantir que o Ollama está rodando
ollama serve

# 3. Rodar o app
streamlit run app.py
```

## Estrutura Sugerida

```
src/
├── app.py              # Aplicação principal (Streamlit)

```
