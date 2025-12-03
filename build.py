#!/usr/bin/env python3
"""
🔨 Build Script - Extrator de HTML
Cria executável (.exe) do projeto usando PyInstaller
"""

import os
import subprocess
import sys
import shutil

def verificar_pyinstaller():
    """Verifica se PyInstaller está instalado"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller encontrado: v{PyInstaller.__version__}")
        return True
    except ImportError:
        print("⚠️ PyInstaller não encontrado. Instalando...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("✅ PyInstaller instalado com sucesso!")
        return True

def limpar_builds_anteriores():
    """Remove builds anteriores"""
    pastas = ['build', 'dist', '__pycache__']
    arquivos = ['ExtratorHTML.spec', 'ExtratorHTML_GUI.spec']
    
    for pasta in pastas:
        if os.path.exists(pasta):
            print(f"🗑️ Removendo pasta: {pasta}")
            shutil.rmtree(pasta)
    
    for arquivo in arquivos:
        if os.path.exists(arquivo):
            print(f"🗑️ Removendo arquivo: {arquivo}")
            os.remove(arquivo)

def criar_executavel_cli():
    """Cria executável da versão CLI"""
    print("\n" + "=" * 60)
    print("🔨 Criando executável CLI...")
    print("=" * 60)
    
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'ExtratorHTML',
        '--clean',
        '--noconfirm',
        '--console',
        'extrator_html.py'
    ]
    
    try:
        subprocess.run(comando, check=True)
        print("\n✅ Executável CLI criado: dist/ExtratorHTML.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao criar executável CLI: {e}")
        return False

def criar_executavel_gui():
    """Cria executável da versão GUI"""
    print("\n" + "=" * 60)
    print("🔨 Criando executável GUI...")
    print("=" * 60)
    
    comando = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--name', 'ExtratorHTML_GUI',
        '--clean',
        '--noconfirm',
        '--windowed',  # Sem console para GUI
        '--add-data', '.;.',  # Incluir arquivos do diretório
        'extrator_html_gui.py'
    ]
    
    try:
        subprocess.run(comando, check=True)
        print("\n✅ Executável GUI criado: dist/ExtratorHTML_GUI.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao criar executável GUI: {e}")
        return False

def mostrar_resultado():
    """Mostra resultado final"""
    print("\n" + "=" * 60)
    print("🎉 BUILD CONCLUÍDO!")
    print("=" * 60)
    
    dist_path = os.path.join(os.getcwd(), 'dist')
    
    if os.path.exists(dist_path):
        print(f"\n📁 Executáveis criados em: {dist_path}")
        print("\nArquivos gerados:")
        for arquivo in os.listdir(dist_path):
            caminho = os.path.join(dist_path, arquivo)
            tamanho = os.path.getsize(caminho) / (1024 * 1024)  # MB
            print(f"  📦 {arquivo} ({tamanho:.1f} MB)")
    
    print("\n💡 Como usar:")
    print("  1. Navegue até a pasta 'dist'")
    print("  2. Execute 'ExtratorHTML.exe' (CLI) ou 'ExtratorHTML_GUI.exe' (Interface)")
    print("  3. Cole a URL e extraia o HTML!")

def main():
    """Função principal"""
    print("=" * 60)
    print("🔨 BUILD SCRIPT - Extrator de HTML")
    print("Versão 1.0.0 | Criado por Ivandir")
    print("=" * 60)
    
    # Verificar PyInstaller
    if not verificar_pyinstaller():
        print("❌ Não foi possível instalar PyInstaller")
        input("\nPressione ENTER para sair...")
        return
    
    # Limpar builds anteriores
    print("\n🧹 Limpando builds anteriores...")
    limpar_builds_anteriores()
    
    # Perguntar qual versão criar
    print("\n📋 Qual versão deseja criar?")
    print("  1. Apenas CLI (linha de comando)")
    print("  2. Apenas GUI (interface gráfica)")
    print("  3. Ambas as versões")
    
    escolha = input("\nEscolha (1/2/3) [3]: ").strip() or "3"
    
    sucesso_cli = True
    sucesso_gui = True
    
    if escolha in ["1", "3"]:
        sucesso_cli = criar_executavel_cli()
    
    if escolha in ["2", "3"]:
        sucesso_gui = criar_executavel_gui()
    
    # Mostrar resultado
    if sucesso_cli or sucesso_gui:
        mostrar_resultado()
    else:
        print("\n❌ Falha ao criar executáveis!")
    
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()

