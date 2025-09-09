# Airbyte Opensource - Guia de Instalação

Este guia fornece instruções detalhadas para instalar e configurar o Airbyte na versão opensource usando diferentes métodos.

## Pré-requisitos

- macOS (este guia é otimizado para macOS)
- Docker Desktop instalado e rodando
- Pelo menos 4GB de RAM disponível (8GB recomendado)
- 10GB de espaço livre em disco

**Nota**: Para máquinas com recursos limitados, use o modo `--low-resource-mode` durante a instalação.

## Métodos de Instalação

### 1. Instalação via Homebrew (Recomendado)

O Homebrew é a forma mais simples de instalar o Airbyte no macOS.

#### Passo 1: Instalar o Homebrew (se não tiver)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Passo 2: Instalar o Airbyte
```bash
# Adicionar o tap do Airbyte
brew tap airbytehq/tap

# Instalar o abctl (Airbyte Control)
brew install abctl
```

#### Passo 3: Verificar a instalação
```bash
abctl version
```

### 2. Instalação via UV (Python Package Manager)

O UV é um gerenciador de pacotes Python moderno e rápido.

#### Passo 1: Instalar o UV
```bash
# Via Homebrew
brew install uv

# Ou via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Passo 2: Instalar o abctl via UV
```bash
# Instalar globalmente
uv tool install abctl

# Ou usar uvx para execução direta
uvx abctl version
```

#### Passo 3: Verificar a instalação
```bash
abctl version
```

### 3. Instalação Manual (Alternativa)

Se preferir baixar diretamente:

```bash
# Baixar a versão mais recente
curl -LsfS https://get.airbyte.com | bash -

# Ou especificar uma versão
curl -LsfS https://get.airbyte.com | bash -s -- --version=0.50.0
```

## Iniciando o Airbyte

### Instalação Local

Para instalar e iniciar o Airbyte localmente:

```bash
# Instalar o Airbyte localmente (modo padrão)
abctl local install

# Instalar em modo de baixo consumo de recursos
abctl local install --low-resource-mode

# O comando acima irá:
# - Baixar as imagens Docker necessárias
# - Configurar o ambiente local
# - Iniciar todos os serviços
```

**Quando usar o modo de baixo consumo:**
- Máquinas com menos de 8GB de RAM
- Ambientes de desenvolvimento com recursos limitados
- Quando você quer economizar recursos do sistema

### Comandos Úteis

```bash
# Verificar status dos serviços
abctl local status

# Parar os serviços
abctl local stop

# Reiniciar os serviços
abctl local start

# Ver logs
abctl local logs

# Obter credenciais de acesso
abctl local credentials

# Desinstalar completamente
abctl local uninstall
```

## Acessando o Airbyte

Após a instalação bem-sucedida:

1. **Interface Web**: Acesse http://localhost:8000

2. **Descobrir Credenciais**:
   ```bash
   # Obter as credenciais de acesso atuais
   abctl local credentials
   ```
   
   Este comando retornará:
   - URL de acesso (normalmente http://localhost:8000)
   - Email de login
   - Senha atual

3. **Credenciais padrão** (caso não tenha personalizado):
   - Email: `airbyte@example.com`
   - Senha: `password`

## Configuração Inicial

### 1. Primeiro Acesso
- Acesse a interface web
- Faça login com as credenciais padrão
- Altere a senha na primeira utilização

### 2. Configurar Conectores
- Navegue até "Sources" para configurar fontes de dados
- Vá em "Destinations" para configurar destinos
- Crie "Connections" para definir pipelines de dados

## Solução de Problemas

### Docker não está rodando
```bash
# Verificar se o Docker está ativo
docker ps

# Iniciar o Docker Desktop se necessário
open -a Docker
```

### Portas em uso
```bash
# Verificar quais portas estão em uso
lsof -i :8000
lsof -i :8001

# Parar processos se necessário
abctl local stop
```

### Problemas de memória
```bash
# Verificar uso de memória
docker stats

# Limpar containers não utilizados
docker system prune -a

# Se tiver problemas de memória, reinstale em modo de baixo consumo
abctl local uninstall
abctl local install --low-resource-mode
```

### Erro de Cookie/Autenticação (COMUM)
Se você receber o erro: "Your credentials were correct, but the server failed to set a cookie. You appear to have deployed over HTTP. Make sure you have disabled secure cookies."

**Solução Completa (Passo a Passo):**

1. **Desinstalar e reinstalar com modo de baixo consumo:**
```bash
# Desinstalar completamente
abctl local uninstall

# Reinstalar em modo de baixo consumo (mais estável)
abctl local install --low-resource-mode
```

2. **Corrigir configurações de cookies:**
```bash
# Aplicar correção de cookies seguros
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig patch configmap airbyte-abctl-airbyte-env -n airbyte-abctl --type merge -p '{"data":{"AB_COOKIE_SECURE":"false","AB_COOKIE_SAME_SITE":"None"}}'

# Reiniciar o servidor para aplicar mudanças
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig rollout restart deployment/airbyte-abctl-server -n airbyte-abctl
```

3. **Aguardar e testar:**
```bash
# Aguardar 30 segundos para o servidor reiniciar
sleep 30

# Obter novas credenciais
abctl local credentials
```

**Soluções por Navegador:**
- ✅ **Chrome**: Geralmente funciona melhor com as configurações acima
- ⚠️ **Safari**: Pode ter problemas com cookies em localhost - use modo privado
- ⚠️ **Firefox**: Pode precisar desabilitar proteções extras - use modo privado

**Alternativas Adicionais:**
- Limpe completamente o cache e cookies do navegador
- Tente em uma aba anônima/privada (RECOMENDADO)
- Use um navegador diferente (Chrome é mais tolerante)
- Verifique se não há conflitos de porta com `lsof -i :8000`
- Aguarde alguns minutos após a instalação para todos os serviços estabilizarem

**Se ainda não funcionar:**
```bash
# Verificar se todos os pods estão rodando
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig get pods -n airbyte-abctl

# Ver logs do servidor para diagnosticar
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig logs -n airbyte-abctl deployment/airbyte-abctl-server --tail=20
```

### Problemas de Navegador
Se o Airbyte não carregar ou apresentar erros de interface:

**Soluções por Navegador:**
```bash
# Chrome (Recomendado)
# - Geralmente funciona melhor
# - Mais tolerante com cookies localhost
# - Use modo incógnito se houver problemas

# Safari
# - Pode bloquear cookies de localhost
# - Vá em Preferências > Privacidade > Desmarcar "Impedir rastreamento entre sites"
# - Use modo privado

# Firefox
# - Pode ter proteções extras ativas
# - Vá em about:config e defina network.cookie.sameSite.laxByDefault = false
# - Use modo privado
```

**Limpeza de Cache:**
```bash
# Limpar dados do navegador para localhost:8000
# 1. Abra as ferramentas de desenvolvedor (F12)
# 2. Clique com botão direito no ícone de atualizar
# 3. Selecione "Esvaziar cache e recarregar forçadamente"
```

### Logs de debug
```bash
# Ver logs detalhados
abctl local logs --follow

# Logs de um serviço específico
abctl local logs webapp
abctl local logs server

# Logs via kubectl (mais detalhados)
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig logs -n airbyte-abctl deployment/airbyte-abctl-server --tail=50
```

### Verificação de Status Completa
```bash
# Status geral
abctl local status

# Status detalhado dos pods
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig get pods -n airbyte-abctl

# Verificar se o ingress está funcionando
kubectl --kubeconfig=/Users/$USER/.airbyte/abctl/abctl.kubeconfig get ingress -n airbyte-abctl

# Testar conectividade
curl -I http://localhost:8000
```

## Atualizações

### Atualizar via Homebrew
```bash
brew update
brew upgrade abctl
```

### Atualizar via UV
```bash
uv tool upgrade abctl
```

### Atualizar instalação local
```bash
abctl local install --upgrade
```

## Recursos Adicionais

- **Vídeo Tutorial**: [Airbyte Installation Guide](https://www.youtube.com/watch?v=DfWMYccd-Vg) - Tutorial completo de instalação
- **Documentação Oficial**: https://docs.airbyte.com/
- **GitHub**: https://github.com/airbytehq/airbyte
- **Community Slack**: https://slack.airbyte.com/
- **Conectores Disponíveis**: https://docs.airbyte.com/integrations/

## Próximos Passos

1. Configure suas primeiras fontes de dados
2. Defina destinos para seus dados
3. Crie conexões e configure sincronizações
4. Monitore seus pipelines de dados
5. Explore conectores customizados se necessário

---

**Nota**: Este projeto utiliza Python 3.12+ e está configurado para trabalhar com o Airbyte opensource.