import json
from kafka import KafkaConsumer
from database import inicializar_banco, salvar_transacao
from rules import avaliar_regras

TOPICO = 'transacoes-bancarias'

def iniciar_consumidor():
    inicializar_banco()
    print(" Banco de dados inicializado com sucesso.")

    consumidor = KafkaConsumer(
        TOPICO,
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', 
        enable_auto_commit=True,
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    print(f" Consumidor ligado ao tópico '{TOPICO}'. À escuta de transações...")
    print("-" * 60)

    try:
        for mensagem in consumidor:
            transacao = mensagem.value
            
            id_transacao = transacao.get("id_transacao")
            id_cliente = transacao.get("id_cliente")
            valor = transacao.get("valor")
            cidade = transacao.get("city")
            pais = transacao.get("country")
            hora = transacao.get("hora")

            alerta = avaliar_regras(transacao)

            salvar_transacao(transacao, alerta=alerta)

            if alerta:
                print(f" [ALERTA DE FRAUDE DETETADA: {alerta}]")
                print(f"   ↳ ID Transação: {id_transacao}")
                print(f"   ↳ Cliente     : {id_cliente}")
                print(f"   ↳ Valor       : R$ {valor:.2f}")
                print(f"   ↳ Local       : {cidade} ({pais})")
                print(f"   ↳ Hora        : {hora}")
                print("-" * 60)
            else:
                print(f" Transação Normal | Cliente: {id_cliente[:8]}... | Valor: R$ {valor:.2f} | Local: {cidade}")

    except KeyboardInterrupt:
        print("\n Consumidor interrompido pelo utilizador.")
        consumidor.close()

if __name__ == "__main__":
    iniciar_consumidor()