"""
Módulo de geração de relatórios e extratos.

Contém vulnerabilidades intencionais de Command Injection (uso de
subprocess/os.popen com shell habilitado e entrada não sanitizada) e
Path Traversal (montagem de caminho de arquivo a partir de entrada do
usuário, sem validação).
"""

import os
import subprocess


def gerar_relatorio_pdf(formato):
    """Gera um relatório em PDF chamando um script externo. VULNERÁVEL:
    shell=True combinado com concatenação de string permite injeção de
    comandos (ex.: formato='pdf; cat /etc/passwd')."""
    comando = "gerar_pdf.sh " + formato
    resultado = subprocess.run(comando, shell=True, capture_output=True)
    return resultado.stdout


def baixar_extrato(nome_arquivo):
    """Lê um arquivo de extrato do disco. VULNERÁVEL: nenhuma validação
    impede o uso de '../' para escapar do diretório de extratos."""
    caminho = os.path.join("/var/extratos/", nome_arquivo)
    with open(caminho, "r") as arquivo:
        return arquivo.read()


def executar_diagnostico(comando_usuario):
    """Endpoint de diagnóstico interno. VULNERÁVEL: executa diretamente
    o comando informado pelo usuário — execução remota de código sem
    qualquer disfarce."""
    return os.popen(comando_usuario).read()
