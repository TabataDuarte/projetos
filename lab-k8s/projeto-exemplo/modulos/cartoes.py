"""
Módulo de consulta de cartões do Simulador de Cartões de Crédito.

Contém vulnerabilidades intencionais de SQL Injection: os parâmetros
recebidos da requisição são concatenados diretamente na query SQL,
sem uso de consultas parametrizadas (Prepared Statements).
"""

import sqlite3

from flask import request


def consultar_fatura(numero_cartao):
    """Consulta a fatura de um cartão. VULNERÁVEL: concatenação direta
    do parâmetro na string SQL."""
    conn = sqlite3.connect("cartoes.db")
    query = "SELECT fatura FROM cartoes WHERE numero = '" + numero_cartao + "'"
    cursor = conn.execute(query)
    return cursor.fetchone()


def buscar_cartoes_cliente():
    """Busca todos os cartões associados a um CPF. VULNERÁVEL: uso de
    f-string para montar a query com entrada do usuário."""
    cpf = request.args.get("cpf")
    conn = sqlite3.connect("cartoes.db")
    sql = f"SELECT * FROM cartoes WHERE cpf_titular = '{cpf}'"
    return conn.execute(sql).fetchall()
