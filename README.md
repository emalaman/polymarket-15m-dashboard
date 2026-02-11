# 📊 Polymarket 15M Dashboard

Dashboard Streamlit para monitorar mercados de 15 minutos de Bitcoin e Ethereum na Polymarket via API CLOB.

**Live Demo:** (Deploy no Streamlit Community Cloud ou seu próprio servidor)

---

## ✨ Funcionalidades

- 🔗 Conexão direta com **CLOB API** do Polymarket
- ⏱️ **Auto-atualização** a cada 30 segundos
- 🎯 Filtro automático para mercados **15min de BTC e ETH**
- 📈 Preços **YES/NO** em tempo real
- 💡 **Sinal de trading**: COMPRA se YES < 0.40, VENDA/EVITAR se YES > 0.60
- 🚨 Alertas visuais com cores
- 🔗 Links diretos para o Polymarket

---

## 🛠️ Stack

- **Frontend**: Streamlit
- **Backend**: py-clob-client
- **Deploy**: Streamlit Community Cloud (recomendado) ou VPS

---

## 🚀 Quick Start

### Local

```bash
# Clone e instale
cd polymarket-15m-dashboard
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt

# Configure secrets
cp .env.example .env
# Edite .env com suas credenciais CLOB

# Rode
streamlit run app.py
```

Acesse: http://localhost:8501

---

## ☁️ Deploy no Streamlit Community Cloud

1. Faça push deste repositório para o GitHub
2. Vá em https://share.streamlit.io/
3. Clique em "New app"
4. Selecione o repo e branch `main`
5. Em **Secrets**, adicione:
   - `POLYMARKET_API_KEY`
   - `POLYMARKET_API_SECRET`
   - `POLYMARKET_API_PASSPHRASE`
6. Clique em **Deploy!**

---

## 🔐 Configurando Credenciais CLOB

Para obter as credenciais:

1. Acesse https://polymarket.com/
2. Vá em **Settings** → **API**
3. Crie uma nova chave API com permissão de leitura (`read:markets`)
4. Copie a **API Key**, **Secret** e **Passphrase**
5. Adicione como **GitHub Secrets** (se usar GitHub Actions) ou no `.env` (local)

---

## ⚙️ Como Funciona

1. **Conecta** à CLOB API (`https://clob.polymarket.com`)
2. **Busca** todos os mercados ativos (`client.get_markets()`)
3. **Filtra** por texto contendo "bitcoin/btc" ou "ethereum/eth" + "15 min"
4. **Extrai** preços YES/NO de cada mercado
5. **Calcula** sugestão de compra/venda baseada no preço YES:
   - `< 0.40`: 🔥 COMPRA FORTE
   - `0.40 - 0.60`: ⏳ AGUARDAR
   - `> 0.60`: ⚠️ VENDA/EVITAR
6. **Atualiza** a interface a cada 30 segundos

---

## 📦 Estrutura do Projeto

```
polymarket-15m-dashboard/
├── app.py              # Código principal Streamlit
├── requirements.txt    # Dependências Python
├── .github/workflows/ci.yml  # CI (teste de importação)
├── .env.example        # Template para variáveis de ambiente
├── .gitignore
└── README.md
```

---

## ⚠️ Rate Limits & Considerações

- CLOB API rate limits: ~100 requests/min
- Atualização a cada 30s é segura
- Não进行 negociações automáticas (apenas leitura)
- Mercados de 15min podem aparecer/desaparecer rapidamente

---

## 🐛 Troubleshooting

| Problema | Solução |
|----------|---------|
| `API Key invalid` | Verifique se copiou corretamente; recrie a chave |
| `ModuleNotFoundError` | Rode `pip install -r requirements.txt` |
| Mercados não aparecem | Não há mercados de 15min ativos no momento |
| Loop infinito no Streamlit | Use `@st.cache_data` e `time.sleep(30)` como no exemplo |

---

## 🔄 Customização

- **Intervalo de atualização**: ajuste `time.sleep(30)` no final do loop
- **Sinal de trading**: modifique a função `suggest_action(price)`
- **Filtro de tempo**: adicione `market['duration']` se disponível
- **Layout**: mude `st.columns()` para `st.tabs()` ou outro

---

## 📝 License

MIT

---

**Made with 🧠 by EmilIA**