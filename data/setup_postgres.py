#!/usr/bin/env python3
"""
Script para configurar PostgreSQL com Docker para testes do Airbyte
"""

import subprocess
import time
import os
import sys

def run_command(command, description):
    """Executa comando e mostra resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso")
            return True
        else:
            print(f"❌ {description} - Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {e}")
        return False

def check_docker():
    """Verifica se Docker está instalado e rodando"""
    print("🐳 Verificando Docker...")
    
    # Verificar se Docker está instalado
    if not run_command("docker --version", "Verificando instalação do Docker"):
        print("❌ Docker não está instalado. Instale o Docker Desktop primeiro.")
        return False
    
    # Verificar se Docker está rodando
    if not run_command("docker ps", "Verificando se Docker está rodando"):
        print("❌ Docker não está rodando. Inicie o Docker Desktop.")
        return False
    
    return True

def setup_postgres_container():
    """Configura container PostgreSQL"""
    container_name = "airbyte-postgres-source"
    
    # Verificar se container já existe
    check_cmd = f"docker ps -a --filter name={container_name} --format '{{{{.Names}}}}'"
    result = subprocess.run(check_cmd, shell=True, capture_output=True, text=True)
    
    if container_name in result.stdout:
        print(f"📦 Container {container_name} já existe")
        
        # Verificar se está rodando
        running_cmd = f"docker ps --filter name={container_name} --format '{{{{.Names}}}}'"
        running_result = subprocess.run(running_cmd, shell=True, capture_output=True, text=True)
        
        if container_name not in running_result.stdout:
            print(f"🔄 Iniciando container {container_name}...")
            run_command(f"docker start {container_name}", f"Iniciando {container_name}")
        else:
            print(f"✅ Container {container_name} já está rodando")
    else:
        # Criar novo container
        print(f"🆕 Criando novo container PostgreSQL...")
        docker_cmd = f"""
        docker run -d \
            --name {container_name} \
            -e POSTGRES_DB=airbyte_source \
            -e POSTGRES_USER=postgres \
            -e POSTGRES_PASSWORD=password \
            -p 5432:5432 \
            postgres:13
        """
        
        if run_command(docker_cmd, "Criando container PostgreSQL"):
            print("⏳ Aguardando PostgreSQL inicializar...")
            time.sleep(10)
        else:
            return False
    
    # Testar conexão
    test_cmd = """
    docker exec airbyte-postgres-source psql -U postgres -d airbyte_source -c "SELECT version();"
    """
    
    for attempt in range(5):
        if run_command(test_cmd, f"Testando conexão (tentativa {attempt + 1})"):
            print("✅ PostgreSQL está pronto!")
            return True
        time.sleep(3)
    
    print("❌ Não foi possível conectar ao PostgreSQL")
    return False

def show_connection_info():
    """Mostra informações de conexão"""
    print("\n📋 Informações de Conexão PostgreSQL:")
    print("-" * 50)
    print("Host: localhost")
    print("Port: 5432")
    print("Database: airbyte_source")
    print("User: postgres")
    print("Password: password")
    print("-" * 50)
    
    print("\n🔗 String de Conexão:")
    print("postgresql://postgres:password@localhost:5432/airbyte_source")
    
    print("\n💡 Para usar no Airbyte:")
    print("1. Vá em Sources > New Source")
    print("2. Selecione 'Postgres'")
    print("3. Use as configurações acima")
    print("4. Teste a conexão")

def main():
    """Função principal"""
    print("🚀 Configurando PostgreSQL para Airbyte...")
    
    # Verificar Docker
    if not check_docker():
        sys.exit(1)
    
    # Configurar PostgreSQL
    if not setup_postgres_container():
        sys.exit(1)
    
    # Mostrar informações
    show_connection_info()
    
    print("\n🎯 Próximos passos:")
    print("1. Execute: python insert_postgres_data.py")
    print("2. Configure o Source no Airbyte")
    print("3. Configure um Destination")
    print("4. Crie uma Connection")
    
    print("\n✨ Setup concluído com sucesso!")

if __name__ == "__main__":
    main()