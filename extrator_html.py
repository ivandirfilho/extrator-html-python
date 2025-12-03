#!/usr/bin/env python3
"""
🌐 Extrator de HTML - Versão CLI
Ferramenta para extrair HTML de qualquer URL usando BeautifulSoup
"""

import requests
from bs4 import BeautifulSoup
import sys
from datetime import datetime
import os
import argparse

def extrair_html(url, salvar_arquivo=True, mostrar_preview=True):
    """
    Extrai o HTML de uma URL usando BeautifulSoup

    Args:
        url (str): URL para extrair HTML
        salvar_arquivo (bool): Se True, salva em arquivo
        mostrar_preview (bool): Se True, mostra preview do HTML

    Returns:
        str: HTML extraído e formatado
    """
    try:
        print(f"🔍 Acessando: {url}")
        print("-" * 50)

        # Headers para simular um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

        # Fazer requisição
        print("📡 Fazendo requisição HTTP...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        print(f"✅ Status: {response.status_code}")
        print(f"📊 Tamanho da resposta: {len(response.content):,} bytes")

        # Parse com BeautifulSoup
        print("🔍 Processando HTML com BeautifulSoup...")
        soup = BeautifulSoup(response.content, 'html.parser')

        # HTML formatado
        html_bonito = soup.prettify()

        if salvar_arquivo:
            # Criar nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nome_arquivo = f"html_extraido_{timestamp}.html"

            # Salvar arquivo
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(html_bonito)

            print(f"\n📄 HTML salvo em: {nome_arquivo}")
            print(f"📊 Tamanho: {len(html_bonito):,} caracteres")
            print(f"📍 Local: {os.path.abspath(nome_arquivo)}")

        if mostrar_preview:
            print("\n" + "=" * 60)
            print("PREVIEW (primeiros 800 caracteres):")
            print("=" * 60)
            print(html_bonito[:800])
            if len(html_bonito) > 800:
                print("\n... (conteúdo cortado para preview)")
            print("=" * 60)

        return html_bonito

    except requests.exceptions.Timeout:
        print(f"❌ Timeout: A requisição demorou muito tempo")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Erro de conexão: Verifique sua internet ou a URL")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erro HTTP {e.response.status_code}: {e.response.reason}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao acessar URL: {e}")
        return None
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Função principal para execução CLI"""
    parser = argparse.ArgumentParser(
        description="🌐 Extrator de HTML - BeautifulSoup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  python extrator_html.py https://exemplo.com
  python extrator_html.py --no-save https://exemplo.com
  python extrator_html.py --no-preview https://exemplo.com
        """
    )

    parser.add_argument('url', nargs='?', help='URL para extrair HTML')
    parser.add_argument('--no-save', action='store_true', help='Não salvar em arquivo')
    parser.add_argument('--no-preview', action='store_true', help='Não mostrar preview')
    parser.add_argument('--version', action='version', version='Extrator HTML v1.0.0')

    args = parser.parse_args()

    print("=" * 60)
    print("🌐 EXTRATOR DE HTML - BeautifulSoup")
    print("Versão 1.0.0 | Criado por Ivandir")
    print("=" * 60)
    print()

    # Verificar se URL foi passada como argumento
    if args.url:
        url = args.url
    else:
        # Solicitar URL ao usuário
        print("📎 Cole a URL aqui:")
        url = input("URL: ").strip()

    if not url:
        print("❌ URL não fornecida!")
        print("\n💡 Dica: Use 'python extrator_html.py --help' para ver opções")
        input("\nPressione ENTER para sair...")
        return

    # Validar URL básica
    if not url.startswith(('http://', 'https://')):
        print("⚠️  Adicionando 'https://' à URL...")
        url = 'https://' + url

    # Extrair HTML
    html_resultado = extrair_html(
        url=url,
        salvar_arquivo=not args.no_save,
        mostrar_preview=not args.no_preview
    )

    if html_resultado:
        print(f"\n✅ Extração concluída com sucesso!")
    else:
        print(f"\n❌ Falha na extração!")

    print("\n" + "=" * 60)
    input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()
