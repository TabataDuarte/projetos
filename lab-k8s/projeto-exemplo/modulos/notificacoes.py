"""
Módulo de notificações e integrações externas.

Contém três vulnerabilidades intencionais: SSRF (Server-Side Request
Forgery), desserialização insegura via pickle, e uso perigoso de
eval() sobre entrada externa.
"""

import pickle

import requests


def enviar_webhook(url_destino, payload):
    """Envia uma notificação para uma URL de webhook. VULNERÁVEL: a URL
    vem diretamente da requisição do cliente, sem validação por
    allowlist — permite SSRF (ex.: acessar metadados de nuvem interna
    ou serviços da rede que não deveriam ser alcançáveis)."""
    resposta = requests.get(url_destino, timeout=5)
    return resposta.text


def carregar_preferencias_notificacao(dados_serializados):
    """Carrega preferências de notificação enviadas pelo cliente.
    VULNERÁVEL: pickle.loads sobre dado controlado pelo usuário permite
    execução remota de código através de um payload malicioso."""
    return pickle.loads(bytes.fromhex(dados_serializados))


def calcular_limite_credito(expressao):
    """Calcula uma simulação de limite de crédito a partir de uma
    expressão matemática informada pelo usuário. VULNERÁVEL: eval()
    executa qualquer código Python embutido na expressão."""
    return eval(expressao)
