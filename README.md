# Airbyte Opensource - Guia de Instalação

Este guia fornece instruções detalhadas para instalar e configurar o Airbyte na versão opensource usando diferentes métodos.

## Pré-requisitos

- macOS (este guia é otimizado para macOS)
- Docker Desktop instalado e rodando
- Pelo menos 8GB de RAM disponível
- 10GB de espaço livre em disco

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
# Instalar o Airbyte localmente
abctl local install

# O comando acima irá:
# - Baixar as imagens Docker necessárias
# - Configurar o ambiente local
# - Iniciar todos os serviços
```

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
```

### Logs de debug
```bash
# Ver logs detalhados
abctl local logs --follow

# Logs de um serviço específico
abctl local logs webapp
abctl local logs server
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