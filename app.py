import os
import time
import streamlit as st
from py_clob_client.client import ClobClient
from py_clob_client.constants import POLYGON

st.set_page_config(
    page_title="Polymarket 15M Dash",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Polymarket 15M Dash - BTC/ETH")

st.markdown("---")

# Sidebar - Configuração
st.sidebar.header("🔐 Configuração CLOB")
api_key = os.getenv("POLYMARKET_API_KEY", "")
api_secret = os.getenv("POLYMARKET_API_SECRET", "")
api_passphrase = os.getenv("POLYMARKET_API_PASSPHRASE", "")

if not all([api_key, api_secret, api_passphrase]):
    st.sidebar.warning("⚠️ Configure as GitHub Secrets:\n- POLYMARKET_API_KEY\n- POLYMARKET_API_SECRET\n- POLYMARKET_API_PASSPHRASE")
    st.error("🚨 Credenciais CLOB não encontradas. Configure os Secrets no repositório GitHub.")
    st.stop()

# Lógica de recomendação
def suggest_action(price):
    if price < 0.40:
        return "🔥 COMPRA FORTE (Probabilidade Baixa)"
    elif price > 0.60:
        return "⚠️ VENDA/EVITAR (Probabilidade Alta)"
    return "⏳ AGUARDAR"

# Inicializar cliente CLOB
@st.cache_resource(ttl=30)
def get_client():
    return ClobClient(
        "https://clob.polymarket.com",
        chain_id=POLYGON,
        key=api_key,
        secret=api_secret,
        passphrase=api_passphrase
    )

# Buscar mercados
@st.cache_data(ttl=30)
def get_markets():
    client = get_client()
    try:
        markets = client.get_markets(limit=500)
    except Exception as e:
        st.error(f"Erro ao buscar mercados: {e}")
        return []
    return markets

# Filtrar mercados de 15 minutos de BTC e ETH
def filter_15m_crypto(markets):
    targets = []
    for m in markets:
        question = m.get('question', '').lower()
        description = m.get('description', '').lower()
        slug = m.get('slug', '').lower()
        text = question + ' ' + description + ' ' + slug
        
        # Detecta BTC a 15 minutos
        is_btc_15m = ('bitcoin' in text or 'btc' in text) and ('15' in text and ('min' in text or 'm' in text))
        # Detecta ETH a 15 minutos
        is_eth_15m = ('ethereum' in text or 'eth' in text) and ('15' in text and ('min' in text or 'm' in text))
        
        if is_btc_15m or is_eth_15m:
            targets.append(m)
    return targets

def get_outcome_prices(market):
    prices = market.get('outcomePrices')
    if isinstance(prices, str):
        try:
            prices = json.loads(prices)
        except:
            return None, None
    if prices and len(prices) == 2:
        yes = float(prices[0])
        no = float(prices[1])
        return yes, no
    return None, None

def format_price(price):
    if price is None:
        return "N/A"
    return f"{price:.3f}"

def format_url(market):
    market_id = market.get('marketId') or market.get('id')
    if market_id:
        return f"https://polymarket.com/market/{market_id}"
    return "#"

# Main
placeholder = st.empty()

while True:
    with placeholder.container():
        try:
            markets = get_markets()
            crypto_15m = filter_15m_crypto(markets)
            
            st.subheader(f"🎯 Mercados 15min Detectados: {len(crypto_15m)}")
            
            if not crypto_15m:
                st.warning("Nenhum mercado de 15min para BTC/ETH encontrado.")
                st.info("Verifique se a API CLOB está acessível e se existem mercados ativos.")
            else:
                cols = st.columns(2)
                for idx, market in enumerate(crypto_15m[:2]):  # Máximo 2 (BTC e ETH)
                    yes_price, no_price = get_outcome_prices(market)
                    suggestion = suggest_action(yes_price) if yes_price else "N/A"
                    
                    question = market.get('question', 'Sem título')
                    
                    with cols[idx]:
                        st.metric(
                            label="BTC 15m" if 'btc' in question.lower() else "ETH 15m",
                            value=format_price(yes_price),
                            delta=None
                        )
                        st.write(f"**Sugestão:** {suggestion}")
                        st.caption(f"**NO:** {format_price(no_price)}")
                        st.caption(f"[Ver no Polymarket]({format_url(market)})")
                
                # Tabela completa
                st.markdown("### 📋 Lista Completa")
                table_data = []
                for m in crypto_15m:
                    yes, no = get_outcome_prices(m)
                    sug = suggest_action(yes) if yes else "-"
                    table_data.append({
                        "Mercado": m.get('question', 'N/A')[:60] + ("..." if len(m.get('question',''))>60 else ""),
                        "YES": format_price(yes),
                        "NO": format_price(no),
                        "Sugestão": sug,
                        "Link": f"[Abrir]({format_url(m)})"
                    })
                st.table(table_data)
            
            last_update = time.strftime('%H:%M:%S')
            st.caption(f"🔄 Última atualização: {last_update} | Próxima em 30s")
            
        except Exception as e:
            st.error(f"Erro inesperado: {e}")
            import traceback
            st.code(traceback.format_exc())
    
    time.sleep(30)
    st.rerun()
