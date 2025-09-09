# Scripts de Dados para Airbyte

Esta pasta contém scripts para configurar e popular um banco PostgreSQL com dados de exemplo para testar o Airbyte.

## Arquivos

- `setup_postgres.py` - Configura container PostgreSQL com Docker
- `insert_postgres_data.py` - Insere dados de exemplo no PostgreSQL
- `.env.example` - Exemplo de configurações de ambiente

## Uso Rápido

### 1. Configurar PostgreSQL

```bash
# Executar setup do PostgreSQL (cria container Docker)
python setup_postgres.py
```

### 2. Inserir Dados de Exemplo

```bash
# Inserir dados de teste
python insert_postgres_data.py
```

## Configuração Manual

### Variáveis de Ambiente

Copie `.env.example` para `.env` e ajuste as configurações:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=airbyte_source
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
```

### PostgreSQL Existente

Se você já tem um PostgreSQL rodando, apenas execute:

```bash
# Definir variáveis de ambiente
export POSTGRES_HOST=seu_host
export POSTGRES_PORT=5432
export POSTGRES_DB=sua_database
export POSTGRES_USER=seu_usuario
export POSTGRES_PASSWORD=sua_senha

# Inserir dados
python insert_postgres_data.py
```

## Dados Gerados

O script cria as seguintes tabelas com dados de exemplo:

### 📊 Tabelas

1. **users** (100 registros)
   - id, name, email, age, city, created_at, updated_at

2. **products** (50 registros)
   - id, name, category, price, stock, description, created_at

3. **orders** (200 registros)
   - id, user_id, product_id, quantity, total_amount, status, order_date

4. **events** (500 registros)
   - id, event_type, user_id, event_data (JSON), timestamp

### 📈 Casos de Uso

- **Batch Sync**: Tabelas users, products, orders
- **Incremental Sync**: Tabela events (por timestamp)
- **CDC (Change Data Capture)**: Todas as tabelas
- **JSON Data**: Campo event_data na tabela events

## Configuração no Airbyte

### 1. Source PostgreSQL

1. Vá em **Sources** > **New Source**
2. Selecione **Postgres**
3. Configure:
   - **Host**: `localhost`
   - **Port**: `5432`
   - **Database**: `airbyte_source`
   - **Username**: `postgres`
   - **Password**: `password`
   - **SSL Mode**: `disable` (para desenvolvimento local)

### 2. Schemas e Tabelas

Selecione o schema `public` e as tabelas:
- ✅ users
- ✅ products  
- ✅ orders
- ✅ events

### 3. Sync Modes Recomendados

- **users**: Full Refresh - Overwrite
- **products**: Full Refresh - Overwrite
- **orders**: Incremental - Append (cursor: order_date)
- **events**: Incremental - Append (cursor: timestamp)

## Comandos Úteis

### Docker PostgreSQL

```bash
# Ver logs do container
docker logs airbyte-postgres-source

# Conectar ao PostgreSQL
docker exec -it airbyte-postgres-source psql -U postgres -d airbyte_source

# Parar container
docker stop airbyte-postgres-source

# Remover container
docker rm airbyte-postgres-source
```

### Consultas SQL

```sql
-- Ver resumo dos dados
SELECT 'users' as table_name, COUNT(*) as records FROM users
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'events', COUNT(*) FROM events;

-- Ver eventos recentes
SELECT event_type, COUNT(*) 
FROM events 
WHERE timestamp > NOW() - INTERVAL '1 hour'
GROUP BY event_type;

-- Ver pedidos por status
SELECT status, COUNT(*), SUM(total_amount) as total_revenue
FROM orders 
GROUP BY status;
```

## Dependências

```bash
# Instalar dependências Python
pip install psycopg2-binary

# Ou se estiver usando o projeto principal
cd ..
uv sync
```

## Troubleshooting

### Erro de Conexão

```bash
# Verificar se PostgreSQL está rodando
docker ps | grep postgres

# Verificar logs
docker logs airbyte-postgres-source

# Testar conexão
telnet localhost 5432
```

### Erro de Permissão

```bash
# Dar permissão de execução aos scripts
chmod +x setup_postgres.py
chmod +x insert_postgres_data.py
```

### Limpar e Recriar

```bash
# Remover container e dados
docker stop airbyte-postgres-source
docker rm airbyte-postgres-source

# Executar setup novamente
python setup_postgres.py
python insert_postgres_data.py
```

## Próximos Passos

1. ✅ Configure o Source PostgreSQL no Airbyte
2. ✅ Configure um Destination (BigQuery, Snowflake, etc.)
3. ✅ Crie Connections para sincronizar os dados
4. ✅ Monitore as sincronizações
5. ✅ Explore os dados no seu data warehouse