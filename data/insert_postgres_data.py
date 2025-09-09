#!/usr/bin/env python3
"""
Script para inserir dados de exemplo em PostgreSQL
Útil para testar conectores do Airbyte
"""

import psycopg2
import json
from datetime import datetime, timedelta
import random
import os
from typing import List, Dict, Any

# Configurações de conexão PostgreSQL
DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'port': os.getenv('POSTGRES_PORT', '5432'),
    'database': os.getenv('POSTGRES_DB', 'airbyte_source'),
    'user': os.getenv('POSTGRES_USER', 'postgres'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password')
}

def create_connection():
    """Cria conexão com PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print(f"✅ Conectado ao PostgreSQL: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
        return conn
    except psycopg2.Error as e:
        print(f"❌ Erro ao conectar ao PostgreSQL: {e}")
        return None

def create_tables(conn):
    """Cria tabelas de exemplo"""
    cursor = conn.cursor()
    
    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(150) UNIQUE NOT NULL,
            age INTEGER,
            city VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            category VARCHAR(100),
            price DECIMAL(10,2),
            stock INTEGER DEFAULT 0,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            product_id INTEGER REFERENCES products(id),
            quantity INTEGER NOT NULL,
            total_amount DECIMAL(10,2),
            status VARCHAR(50) DEFAULT 'pending',
            order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabela de eventos (para streaming)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(100),
            user_id INTEGER,
            event_data JSONB,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    print("✅ Tabelas criadas com sucesso")

def generate_users_data(count: int = 100) -> List[Dict[str, Any]]:
    """Gera dados de usuários"""
    names = [
        "Ana Silva", "João Santos", "Maria Oliveira", "Pedro Costa", "Carla Souza",
        "Lucas Pereira", "Fernanda Lima", "Rafael Alves", "Juliana Rocha", "Bruno Martins",
        "Camila Ferreira", "Diego Ribeiro", "Larissa Cardoso", "Thiago Nascimento", "Priscila Gomes"
    ]
    
    cities = [
        "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador", "Brasília",
        "Fortaleza", "Curitiba", "Recife", "Porto Alegre", "Manaus"
    ]
    
    users = []
    for i in range(count):
        name = random.choice(names)
        email = f"{name.lower().replace(' ', '.')}.{i}@email.com"
        users.append({
            'name': name,
            'email': email,
            'age': random.randint(18, 80),
            'city': random.choice(cities)
        })
    
    return users

def generate_products_data(count: int = 50) -> List[Dict[str, Any]]:
    """Gera dados de produtos"""
    products = [
        {"name": "Smartphone Samsung Galaxy", "category": "Eletrônicos", "price": 1299.99},
        {"name": "Notebook Dell Inspiron", "category": "Informática", "price": 2499.90},
        {"name": "Tênis Nike Air Max", "category": "Esportes", "price": 399.99},
        {"name": "Livro Python para Iniciantes", "category": "Livros", "price": 59.90},
        {"name": "Cafeteira Elétrica", "category": "Casa", "price": 189.90},
        {"name": "Fone de Ouvido Bluetooth", "category": "Eletrônicos", "price": 149.99},
        {"name": "Camiseta Básica", "category": "Roupas", "price": 29.90},
        {"name": "Mouse Gamer", "category": "Informática", "price": 89.90},
        {"name": "Perfume Importado", "category": "Beleza", "price": 199.90},
        {"name": "Mochila Escolar", "category": "Acessórios", "price": 79.90}
    ]
    
    result = []
    for i in range(count):
        base_product = random.choice(products)
        result.append({
            'name': f"{base_product['name']} - Modelo {i+1}",
            'category': base_product['category'],
            'price': round(base_product['price'] * random.uniform(0.8, 1.5), 2),
            'stock': random.randint(0, 100),
            'description': f"Descrição detalhada do produto {base_product['name']}"
        })
    
    return result

def insert_users(conn, users_data: List[Dict[str, Any]]):
    """Insere usuários no banco"""
    cursor = conn.cursor()
    
    for user in users_data:
        cursor.execute("""
            INSERT INTO users (name, email, age, city)
            VALUES (%(name)s, %(email)s, %(age)s, %(city)s)
            ON CONFLICT (email) DO NOTHING
        """, user)
    
    conn.commit()
    print(f"✅ {len(users_data)} usuários inseridos")

def insert_products(conn, products_data: List[Dict[str, Any]]):
    """Insere produtos no banco"""
    cursor = conn.cursor()
    
    for product in products_data:
        cursor.execute("""
            INSERT INTO products (name, category, price, stock, description)
            VALUES (%(name)s, %(category)s, %(price)s, %(stock)s, %(description)s)
        """, product)
    
    conn.commit()
    print(f"✅ {len(products_data)} produtos inseridos")

def generate_orders(conn, count: int = 200):
    """Gera pedidos aleatórios"""
    cursor = conn.cursor()
    
    # Buscar IDs de usuários e produtos
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id, price FROM products")
    products = cursor.fetchall()
    
    orders = []
    for _ in range(count):
        user_id = random.choice(user_ids)
        product_id, price = random.choice(products)
        quantity = random.randint(1, 5)
        total_amount = round(float(price) * quantity, 2)
        status = random.choice(['pending', 'processing', 'shipped', 'delivered', 'cancelled'])
        
        # Data aleatória nos últimos 30 dias
        order_date = datetime.now() - timedelta(days=random.randint(0, 30))
        
        orders.append((user_id, product_id, quantity, total_amount, status, order_date))
    
    cursor.executemany("""
        INSERT INTO orders (user_id, product_id, quantity, total_amount, status, order_date)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, orders)
    
    conn.commit()
    print(f"✅ {len(orders)} pedidos inseridos")

def generate_events(conn, count: int = 500):
    """Gera eventos para simular streaming de dados"""
    cursor = conn.cursor()
    
    # Buscar IDs de usuários
    cursor.execute("SELECT id FROM users")
    user_ids = [row[0] for row in cursor.fetchall()]
    
    event_types = [
        'page_view', 'click', 'purchase', 'login', 'logout', 
        'search', 'add_to_cart', 'remove_from_cart', 'checkout'
    ]
    
    events = []
    for _ in range(count):
        user_id = random.choice(user_ids)
        event_type = random.choice(event_types)
        
        # Dados específicos por tipo de evento
        event_data = {
            'user_agent': 'Mozilla/5.0 (compatible; AirbyteBot/1.0)',
            'ip_address': f"192.168.1.{random.randint(1, 255)}",
            'session_id': f"sess_{random.randint(1000, 9999)}"
        }
        
        if event_type == 'page_view':
            event_data['page'] = random.choice(['/home', '/products', '/about', '/contact'])
        elif event_type == 'search':
            event_data['query'] = random.choice(['smartphone', 'notebook', 'tênis', 'livro'])
        elif event_type == 'purchase':
            event_data['amount'] = round(random.uniform(10, 1000), 2)
        
        # Timestamp aleatório nas últimas 24 horas
        timestamp = datetime.now() - timedelta(hours=random.randint(0, 24))
        
        events.append((event_type, user_id, json.dumps(event_data), timestamp))
    
    cursor.executemany("""
        INSERT INTO events (event_type, user_id, event_data, timestamp)
        VALUES (%s, %s, %s, %s)
    """, events)
    
    conn.commit()
    print(f"✅ {len(events)} eventos inseridos")

def show_summary(conn):
    """Mostra resumo dos dados inseridos"""
    cursor = conn.cursor()
    
    tables = ['users', 'products', 'orders', 'events']
    
    print("\n📊 Resumo dos dados inseridos:")
    print("-" * 40)
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"{table.capitalize()}: {count} registros")
    
    print("-" * 40)

def main():
    """Função principal"""
    print("🚀 Iniciando inserção de dados no PostgreSQL...")
    print(f"📍 Conectando em: {DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}")
    
    # Conectar ao banco
    conn = create_connection()
    if not conn:
        return
    
    try:
        # Criar tabelas
        create_tables(conn)
        
        # Gerar e inserir dados
        print("\n📝 Inserindo dados de exemplo...")
        
        # Usuários
        users_data = generate_users_data(100)
        insert_users(conn, users_data)
        
        # Produtos
        products_data = generate_products_data(50)
        insert_products(conn, products_data)
        
        # Pedidos
        generate_orders(conn, 200)
        
        # Eventos
        generate_events(conn, 500)
        
        # Mostrar resumo
        show_summary(conn)
        
        print("\n🎉 Dados inseridos com sucesso!")
        print("\n💡 Dicas para usar com Airbyte:")
        print("1. Configure um Source PostgreSQL apontando para este banco")
        print("2. Use as tabelas: users, products, orders, events")
        print("3. Configure um Destination (BigQuery, Snowflake, etc.)")
        print("4. Crie conexões para sincronizar os dados")
        
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        conn.rollback()
    
    finally:
        conn.close()
        print("\n🔌 Conexão fechada")

if __name__ == "__main__":
    main()