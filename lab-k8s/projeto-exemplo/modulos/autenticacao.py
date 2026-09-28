"""
Módulo de autenticação do Simulador de Cartões de Crédito.

Contém vulnerabilidades intencionais: hash criptográfico fraco (MD5)
para senhas e geração de token de sessão com gerador de números
pseudoaleatórios não criptográfico (random, em vez de secrets).
"""

import hashlib
import random
import string

# Base de usuários simplificada para fins do laboratório.
# A senha abaixo corresponde ao hash MD5 de "password".
USUARIOS = {
    "admin": "5f4dcc3b5aa765d61d8327deb882cf99",
}


def gerar_hash_senha(senha):
    """Gera o hash da senha usando MD5 — algoritmo criptograficamente fraco."""
    return hashlib.md5(senha.encode()).hexdigest()


def validar_login(usuario, senha):
    """Valida as credenciais informadas contra a base de usuários."""
    hash_informado = gerar_hash_senha(senha)
    return USUARIOS.get(usuario) == hash_informado


def gerar_token_sessao():
    """Gera um token de sessão usando o módulo random — previsível,
    não deve ser usado para fins de segurança."""
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(32))
