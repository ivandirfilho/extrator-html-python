# 🌐 Extrator de HTML - Python

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-ivandirfilho-black.svg)](https://github.com/ivandirfilho)

Ferramenta poderosa para extrair HTML de qualquer URL usando BeautifulSoup.

## ✨ Funcionalidades

- 🔍 **Extração de HTML** completo de qualquer URL
- 💾 **Salvamento automático** com timestamp
- 🖥️ **Versão CLI** (linha de comando)
- 🎨 **Versão GUI** (interface gráfica com Tkinter)
- 📦 **Geração de executável** (.exe) com PyInstaller
- 🚀 **Preview do HTML** extraído
- 📋 **Copiar para clipboard** com um clique
- 🌐 **Landing Page** moderna incluída

## 🛠️ Instalação

### Opção 1: Usar o Executável (Windows)

1. Baixe o executável na seção [Releases](../../releases)
2. Execute `ExtratorHTML.exe` (CLI) ou `ExtratorHTML_GUI.exe` (Interface)
3. Cole a URL e pronto!

### Opção 2: Executar com Python

```bash
# Clone o repositório
git clone https://github.com/ivandirfilho/extrator-html-python.git
cd extrator-html-python

# Instale as dependências
pip install -r requirements.txt

# Execute a versão CLI
python extrator_html.py

# Ou execute a versão GUI
python extrator_html_gui.py
```

## 🚀 Como Usar

### Versão CLI (Linha de Comando)

```bash
# Com URL como argumento
python extrator_html.py https://exemplo.com

# Ou digite a URL quando solicitado
python extrator_html.py

# Opções disponíveis
python extrator_html.py --help
python extrator_html.py --no-save https://exemplo.com    # Não salvar arquivo
python extrator_html.py --no-preview https://exemplo.com # Sem preview
```

### Versão GUI (Interface Gráfica)

```bash
python extrator_html_gui.py
```

1. Cole a URL no campo
2. Clique em "🔍 Extrair HTML"
3. Visualize o resultado
4. Clique em "💾 Salvar Arquivo" ou "📋 Copiar"

## 🔨 Criar Executável (.exe)

```bash
# Instalar PyInstaller (se necessário)
pip install pyinstaller

# Executar script de build
python build.py

# O executável estará em: dist/ExtratorHTML.exe
```

## 📦 Estrutura do Projeto

```
extrator-html-python/
├── extrator_html.py      # Versão CLI
├── extrator_html_gui.py  # Versão GUI
├── build.py              # Script para criar .exe
├── requirements.txt      # Dependências
├── index.html            # Landing Page do projeto
├── README.md             # Este arquivo
└── .gitignore            # Arquivos ignorados pelo Git
```

## 📋 Dependências

- `requests` - Requisições HTTP
- `beautifulsoup4` - Parse do HTML
- `lxml` - Parser XML/HTML
- `tkinter` - Interface gráfica (incluído no Python)
- `pyinstaller` - Geração de executável (opcional)

## 🧪 Exemplo de Uso

```python
from extrator_html import extrair_html

url = "https://exemplo.com"
html = extrair_html(url)
print(html[:500])  # Primeiros 500 caracteres
```

## 🌐 Landing Page

O projeto inclui uma landing page moderna (`index.html`) que pode ser visualizada:

1. Abra o arquivo `index.html` no navegador
2. Ou acesse via GitHub Pages (se configurado)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abrir um Pull Request

## 📄 Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👤 Autor

**Ivandir**

- GitHub: [@ivandirfilho](https://github.com/ivandirfilho)

## 🙏 Agradecimentos

- Criado com assistência de IA (Inner AI Fusion, Cursor)
- BeautifulSoup pela excelente biblioteca
- Comunidade Python

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**
