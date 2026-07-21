# Base de Conhecimento

## Dados Utilizados

| Arquivo | Formato | Utilização no Agente Poupança Poupada |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores para atendimentos futuros |
| `perfil_investidor.json` | JSON | Personalizar recomendações de investimentos |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil do cliente |
| `transacoes.csv` | CSV | Analisar e armazenar padrão de gastos do cliente para usar como referência |


---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

`transacoes.csv`: As categorias e descrições foram ajustadas para deixar em evidencia um saldo de R$ 4.000,00 parado na conta corrente e aportes de R$ 1.000,00 na poupança, fornecendo ao agente os gatilhos necessários para propor o rebalanceamento.
`historico_atendimento.csv`: O conteúdo foi atualizado com dúvidas passadas do cliente sobre liquidez e rentabilidade do CDB vs. Poupança, permitindo que o agente atue de forma mais empática e personalizada.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Existem duas possibilidades: 

Injetar os dados diretamente no prompt (Ctrl + C, Ctrl + V) ou carregar os arquivos via código como no exemplo abaixo: 

```Python
import pandas as pd
import json as js

historico = pd.read_csv(data/historico_atendimento.csv)
transacoes = pd.read_csv(data/transacoes.csv

with open('data/perfil_investidor.json', 'r', enconding = 'utf-8') as f:
    perfil = js.load(f)

with open('data/produtos_financeiros.json', 'r', enconding = 'utf-8') as f:
    produtos = js.load(f)
```

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Para simplificar, podemos injetar os dados no nosso prompt garantindo o melhor contexto possível para o agente, lembrando que em soluções mais robustas é melhor que essas informações sejam carregadas dinâmicamente para ganharmos flexibilidade.

```text

Dados do cliente e perfil (data/perfil_investidor.json):

{
  "nome": "João Silva",
  "idade": 32,
  "profissao": "Analista de Sistemas",
  "renda_mensal": 5000.00,
  "perfil_investidor": "moderado",
  "objetivo_principal": "Construir reserva de emergência",
  "patrimonio_total": 15000.00,
  "reserva_emergencia_atual": 10000.00,
  "aceita_risco": false,
  "metas": [
    {
      "meta": "Completar reserva de emergência",
      "valor_necessario": 15000.00,
      "prazo": "2026-06"
    },
    {
      "meta": "Entrada do apartamento",
      "valor_necessario": 50000.00,
      "prazo": "2027-12"
    }
  ]
}


Transações do cliente (data/transacoes.csv):

data,descricao,categoria,valor,tipo
2026-06-01,Salário,receita,5000.00,entrada
2026-06-02,Aluguel,moradia,1800.00,saida
2026-06-03,Supermercado,alimentacao,650.00,saida
2026-06-05,Netflix,lazer,55.90,saida
2026-06-07,Farmácia,saude,89.00,saida
2026-06-10,Aplicação Poupança,investimento,1000.00,saida
2026-06-12,Uber,transporte,45.00,saida
2026-06-15,Conta de Luz,moradia,180.00,saida
2026-06-18,Academia,saude,99.00,saida
2026-06-20,Saldo Conta Corrente Parado,saldo,4000.00,entrada


Historico do cliente (data/historico_atendimento.csv):

data,canal,tema,resumo,resolvido
2026-05-10,chat,CDB,Cliente perguntou sobre a rentabilidade de CDB em comparação com a poupança,sim
2026-05-28,chat,Liquidez,Cliente informou ter receio de investir em produtos sem resgate imediato,sim
2026-06-01,chat,Tesouro Selic,Cliente pediu explicação simples sobre o funcionamento do Tesouro Direto,sim
2026-06-12,chat,Metas financeiras,Cliente acompanhou o progresso da meta da reserva de emergência,sim
2026-06-15,email,Atualização cadastral,Cliente confirmou e-mail e dados de contato,sim


Produtos disponíveis (data/produtos_financeiros.json):

[
  {
    "nome": "Tesouro Selic",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "100% da Selic",
    "aporte_minimo": 30.00,
    "indicado_para": "Reserva de emergência e iniciantes"
  },
  {
    "nome": "CDB Liquidez Diária",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "102% do CDI",
    "aporte_minimo": 100.00,
    "indicado_para": "Quem busca segurança com rendimento diário"
  },
  {
    "nome": "LCI/LCA",
    "categoria": "renda_fixa",
    "risco": "baixo",
    "rentabilidade": "95% do CDI",
    "aporte_minimo": 1000.00,
    "indicado_para": "Quem pode esperar 90 dias (isento de IR)"
  },
  {
    "nome": "Fundo Multimercado",
    "categoria": "fundo",
    "risco": "medio",
    "rentabilidade": "CDI + 2%",
    "aporte_minimo": 500.00,
    "indicado_para": "Perfil moderado que busca diversificação"
  },
  {
    "nome": "Fundo de Ações",
    "categoria": "fundo",
    "risco": "alto",
    "rentabilidade": "Variável",
    "aporte_minimo": 100.00,
    "indicado_para": "Perfil arrojado com foco no longo prazo"
  }
]

```

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

O exemplo abaixo se baseiam nos dados originais da base de conhecimento porém os cintetisa deixando apenas as informações mais relevantes, otimizando o consumo de TOKENS.

Vale lembrar que, mais importante do que economizar TOKENS é ter todas as informações relevantes disponíveis em seu contexto.
```
Dados do Cliente:
- Nome: João Silva
- Perfil: Moderado
- Saldo disponível: R$ 5.000

Resumo de gastos:
- Aluguel: 1800,00
- Alimentação: 650,00
- Investimento: 1000,00
- Luz: 180,00
- Lazer: 55,90
- Saúde: 89,00 + 99,00 = 188,00
- Transporte: 45,00
Gastos totais: 3.918,9

Produtos disponíveis:
- Tesouro SELIC (Baixo risco)
- CDB liquidez diária (Baixo risco)
- LCI/LCA (Baixo risco)
- Fundo Multimercado (Risco moderado)
- Fundo de ações (Alto risco)

Últimas transações:
- 03/06: Supermercado - R$ 450
- 05/06: Lazer - R$ 55
...
```
