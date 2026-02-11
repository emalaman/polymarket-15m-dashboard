# 📊 Polymarket 15M Dashboard

Dashboard estático (HTML/JS) para monitorar mercados de **15 minutos** de Bitcoin e Ethereum usando a **Gamma API pública**.

**Live Demo:** https://emalaman.github.io/polymarket-15m-dashboard/

---

## ✨ Características

- 🔍 **Filtro automático** por BTC/ETH + 15min (detecta por texto e duração)
- 📈 **Preços YES/NO** em tempo real
- 💡 **Sinal de trading**:
  - 🔥 **COMPRA FORTE** se YES < 0.40
  - ⏳ **AGUARDAR** entre 0.40 e 0.60
  - ⚠️ **VENDA/EVITAR** se YES > 0.60
- 🔄 **Auto-atualização** a cada 30 segundos
- 🚀 **100% estático** - roda no GitHub Pages (sem backend)
- 📱 **Responsivo** - mobile-friendly

---

## 🛠️ Tecnologia

- HTML5 + Vanilla JavaScript
- Tailwind CSS (via CDN)
- Gamma API pública (sem autenticação)

---

## 🚀 Deploy (GitHub Pages)

1. **Crie um repositório** no GitHub (público)
2. **Copie** este `index.html` para o repo
3. **Ative o Pages**: Settings → Pages → Source: `Deploy from a branch` → branch `main` → folder `/ (root)`
4. Acesse: `https://seuuser.github.io/repo-name/`

Done! Não precisa de segredos nem servidor.

---

## 🔍 Como Funciona

1. **Busca** mercados ativos da Gamma API: `https://gamma-api.polymarket.com/markets?active=true&closed=false&limit=500`
2. **Filtra** por:
   - Conter "bitcoin/btc" ou "ethereum/eth" no texto
   - Excluir times de esporte (blacklist)
   - Ter duração total <= 1 hora OU conter "15 min" no texto
3. **Extrai** preços YES/NO de `outcomePrices`
4. **Gera** sinal baseado no preço YES
5. **Atualiza** a cada 30s

---

## 📊 Status Atual

**Mercados encontrados** (exemplo):
- `Will bitcoin hit $1m before GTA VI?` (duration ~1y) - NÃO é 15min
- (Nenhum mercado de 15min detectado no momento)

*A Gamma API pode não retornar os mercados `/crypto/15M` da página do Polymarket. Se não houver eventos de 15min, o dashboard mostrará "Nenhum mercado encontrado".*

---

## 🐛 Problemas Conhecidos

1. **Filtro de 15min**: A Gamma API não tem tag de duração. Detectamos por duração calculada (startDate → endDate) ou pela string "15min". Se o Polymarket usar outro formato, pode não pegar.
2. **Rate limits**: Gamma API tem limite público (~60 req/min). Atualização a cada 30s é segura.
3. **Dados atrasados**: A API pode ter delay de alguns segundos.

---

## 🔧 Customização

- **Intervalo de atualização**: altere `setInterval(run, 30000)` (ms)
- **Limites do sinal**: modifique `suggestAction(price)` (atual: <0.40 compra, >0.60 venda)
- **Filtro de duração**: ajuste `is15MinMarket()` (atual: <=1 hora)
- **Cores/tema**: edite o CSS no `<style>` do cabeçalho

---

## 📝 Notas

- **Sem API Key** - usa endpoint público Gamma
- **Não realiza trades** - apenas exibe dados
- **Funciona offline?** Não, precisa buscar dados da API
- **GitHub Pages** - hospedagem gratuita estática

---

## 🤔 Por que não usar CLOB?

A API CLOB requer autenticação completa (key+secret+passphrase) para leitura de mercados. Como você só tem a API_KEY (pública), a Gamma API é a alternativa. Ela não filtra por duração, então usamos heurísticas.

---

**Made with 🧠 by EmilIA**