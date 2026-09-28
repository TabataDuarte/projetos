# Simulador de Cartões de Crédito — Projeto de Exemplo

Este é um projeto Flask criado **exclusivamente para fins didáticos**,
usado como alvo de análise no laboratório de instalação e uso do
SonarQube. O código contém vulnerabilidades **intencionais**,
distribuídas entre os módulos, para que o SonarQube tenha o que
encontrar durante a análise.

## Não faça isso em produção

Este projeto não deve ser:
- Implantado em qualquer ambiente acessível pela internet;
- Usado como referência de como escrever código seguro;
- Executado em uma rede compartilhada com sistemas reais.

Ele deve rodar apenas dentro da VM isolada do laboratório.

## Estrutura

```
projeto-exemplo/
├── app.py                      # Aplicação Flask principal (rotas + /saude)
├── config.py                   # Configurações — contém segredos hardcoded
├── Dockerfile                  # Containeriza a aplicação (laboratório Kubernetes)
├── .dockerignore
├── modulos/
│   ├── autenticacao.py         # Hash MD5 e token de sessão previsível
│   ├── cartoes.py              # SQL Injection
│   ├── relatorios.py           # Command Injection e Path Traversal
│   └── notificacoes.py         # SSRF, deserialização insegura, eval()
├── regras-banco/                # Regras customizadas do Semgrep (laboratório Semgrep)
│   ├── hash-fraco.yaml
│   ├── eval-perigoso.yaml
│   ├── sql-injection-taint.yaml
│   ├── command-injection.yaml
│   └── deserializacao-insegura.yaml
├── k8s/                          # Manifests do laboratório de Kubernetes (Minikube)
│   ├── 00-namespace.yaml
│   ├── 01-vulneravel.yaml               # Baseline com 9 vulnerabilidades plantadas
│   ├── 02-rbac-corrigido.yaml
│   ├── 03-networkpolicy-default-deny.yaml
│   ├── 04-networkpolicy-allow-dns.yaml
│   ├── 05-networkpolicy-allow-gateway.yaml
│   ├── 06-secret-corrigido.yaml
│   ├── 07-deployment-hardened.yaml
│   └── 08-namespace-pod-security.yaml
├── requirements.txt
└── sonar-project.properties    # Configuração de análise do SonarQube
```

## Vulnerabilidades plantadas (gabarito rápido)

| # | Arquivo | Vulnerabilidade |
|---|---------|------------------|
| 1 | config.py | Segredos hardcoded (SECRET_KEY, DB_PASSWORD, API_KEY_BANDEIRA) |
| 2 | app.py | `debug=True` em execução |
| 3 | modulos/autenticacao.py | Hash de senha com MD5 (algoritmo fraco) |
| 4 | modulos/autenticacao.py | Geração de token com `random` em vez de `secrets` |
| 5 | modulos/cartoes.py | SQL Injection em `consultar_fatura` |
| 6 | modulos/cartoes.py | SQL Injection em `buscar_cartoes_cliente` |
| 7 | modulos/relatorios.py | Command Injection em `gerar_relatorio_pdf` |
| 8 | modulos/relatorios.py | Path Traversal em `baixar_extrato` |
| 9 | modulos/relatorios.py | Command Injection em `executar_diagnostico` |
| 10 | modulos/notificacoes.py | SSRF em `enviar_webhook` |
| 11 | modulos/notificacoes.py | Deserialização insegura (`pickle.loads`) |
| 12 | modulos/notificacoes.py | Uso perigoso de `eval()` |

Consulte o laboratório completo para o passo a passo de instalação do
SonarQube, execução da análise e interpretação de cada um destes
achados na interface web.

## Vulnerabilidades plantadas nos manifests Kubernetes (k8s/01-vulneravel.yaml)

| # | Vulnerabilidade | Corrigida em |
|---|------------------|--------------|
| 1 | ClusterRoleBinding concedendo cluster-admin | 02-rbac-corrigido.yaml |
| 2 | Segredo em ConfigMap (texto claro), não em Secret | 06-secret-corrigido.yaml |
| 3 | `securityContext.privileged: true` | 07-deployment-hardened.yaml |
| 4 | `securityContext.runAsUser: 0` (root explícito) | 07-deployment-hardened.yaml |
| 5 | `securityContext.allowPrivilegeEscalation: true` | 07-deployment-hardened.yaml |
| 6 | Tag de imagem `latest` | 07-deployment-hardened.yaml |
| 7 | Ausência de `resources` (requests/limits) | 07-deployment-hardened.yaml |
| 8 | Ausência de liveness/readiness probes | 07-deployment-hardened.yaml |
| 9 | Nenhuma NetworkPolicy restringindo tráfego | 03, 04 e 05-networkpolicy-*.yaml |

Consulte o Laboratório de Segurança em Kubernetes para o passo a passo
completo de instalação do Minikube, deploy da baseline vulnerável, e
aplicação progressiva de cada correção.
