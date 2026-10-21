import sqlite3
from datetime import datetime

DB_NAME = "transacoes_fraude.db"

def inicializar_banco():
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id_transacao TEXT PRIMARY KEY,
            id_cliente TEXT,
            valor REAL,
            country TEXT,
            city TEXT,
            hora TEXT,
            alerta_gerado TEXT,
            data_processamento TIMESTAMP
        )
    ''')
    
    conexao.commit()
    conexao.close()

def salvar_transacao(transacao, alerta=None):
    """Insere uma transação e o respetivo alerta (se houver) na base de dados."""
    conexao = sqlite3.connect(DB_NAME)
    cursor = conexao.cursor()
    
    cursor.execute('''
        INSERT OR IGNORE INTO transacoes (id_transacao, id_cliente, valor, country, city, hora, alerta_gerado, data_processamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        transacao.get("id_transacao"),
        transacao.get("id_cliente"),
        transacao.get("valor"),
        transacao.get("country"),
        transacao.get("city"),
        transacao.get("hora"),
        alerta,
        datetime.now().isoformat()
    ))
    
    conexao.commit()
    conexao.close()