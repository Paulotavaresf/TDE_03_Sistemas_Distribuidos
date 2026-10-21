from datetime import datetime, timedelta

historico_clientes = {}

def avaliar_regras(transacao):
   
    id_cliente = transacao["id_cliente"]
    valor = transacao["valor"]
    cidade_atual = transacao["city"]
    
    try:
        hora_transacao = datetime.fromisoformat(transacao["hora"])
    except ValueError:
        hora_transacao = datetime.now()

    if id_cliente not in historico_clientes:
        historico_clientes[id_cliente] = []

    alertas = []
    if valor >= 10000.00:
        alertas.append("ALTO_VALOR")

    historico_clientes[id_cliente].append({
        "hora": hora_transacao,
        "city": cidade_atual
    })

    limite_60s = hora_transacao - timedelta(seconds=60)
    transacoes_ultimos_60s = [
        t for t in historico_clientes[id_cliente] 
        if t["hora"] >= limite_60s
    ]
    
    historico_clientes[id_cliente] = transacoes_ultimos_60s

    if len(transacoes_ultimos_60s) >= 4:
        alertas.append("TEMPO_60s")

    limite_10m = hora_transacao - timedelta(minutes=10)
    transacoes_ultimos_10m = [
        t for t in historico_clientes[id_cliente] 
        if t["hora"] >= limite_10m
    ]

    cidades_distintas = set(t["city"] for t in transacoes_ultimos_10m)
    if len(cidades_distintas) > 1:
        alertas.append("GEO_10m")

    if alertas:
        return ", ".join(alertas)
    
    return None