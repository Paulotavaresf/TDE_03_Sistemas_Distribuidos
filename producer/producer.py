import json
import time
import random
from datetime import datetime
from uuid import uuid4
from kafka import KafkaProducer
from faker import Faker

fake = Faker('pt_BR')

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
)

TOPICO = 'transacoes-bancarias'

CIDADES = [
    ("São Paulo", "BR"),
    ("Rio de Janeiro", "BR"),
    ("Belo Horizonte", "BR"),
    ("Curitiba", "BR"),
    ("Brasília", "BR")
]

CLIENTES_FIXOS = [str(uuid4()) for _ in range(5)]

print("🚀 Produtor de transações iniciado. A enviar a cada 3 segundos...")

try:
    while True:
        id_cliente = random.choice(CLIENTES_FIXOS)
        
        cidade_info = random.choice(CIDADES)
        
        if random.random() < 0.2:
            valor = round(random.uniform(10000.00, 25000.00), 2)
        else:
            valor = round(random.uniform(50.00, 9500.00), 2)

        transacao = {
            "id_transacao": str(uuid4()),
            "id_cliente": id_cliente,
            "valor": valor,
            "country": cidade_info[1],
            "city": cidade_info[0],
            "hora": datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        }

        producer.send(TOPICO, value=transacao)
        print(f"📤 Transação enviada | Cliente: {id_cliente[:8]}... | Valor: R$ {valor:.2f} | Local: {cidade_info[0]}")

        time.sleep(3)

except KeyboardInterrupt:
    print("\n🛑 Produtor interrompido pelo utilizador.")
    producer.close()