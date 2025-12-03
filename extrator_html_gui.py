#!/usr/bin/env python3
"""
🌐 Extrator de HTML - Versão GUI
Interface gráfica para extrair HTML de URLs usando BeautifulSoup
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import threading
import os
import sys

class ExtratorHTMLGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🌐 Extrator de HTML - v1.0.0")
        self.root.geometry("1000x750")
        self.root.resizable(True, True)

        # Variável para armazenar HTML
        self.html_atual = ""
        self.url_atual = ""

        # Configurar ícone (opcional)
        try:
            self.root.iconbitmap('icon.ico')  # Se tiver um ícone
        except:
            pass

        self.criar_interface()
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_interface(self):
        """Cria a interface gráfica"""
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')

        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Título
        titulo_frame = ttk.Frame(main_frame)
        titulo_frame.grid(row=0, column=0, columnspan=3, pady=(0, 15), sticky=tk.W)

        titulo = ttk.Label(
            titulo_frame, 
            text="🌐 Extrator de HTML", 
            font=('Arial', 18, 'bold')
        )
        titulo.pack(side=tk.LEFT)

        versao = ttk.Label(
            titulo_frame, 
            text="v1.0.0", 
            font=('Arial', 10), 
            foreground="gray"
        )
        versao.pack(side=tk.RIGHT)

        # Frame de entrada URL
        url_frame = ttk.LabelFrame(main_frame, text="📎 URL", padding="10")
        url_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        url_frame.columnconfigure(1, weight=1)

        ttk.Label(url_frame, text="URL:", font=('Arial', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))

        self.url_entry = ttk.Entry(
            url_frame, 
            width=80, 
            font=('Arial', 10)
        )
        self.url_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        self.url_entry.bind('<Return>', lambda e: self.extrair_thread())

        # Botão extrair
        self.btn_extrair = ttk.Button(
            url_frame, 
            text="🔍 Extrair HTML", 
            command=self.extrair_thread,
            style='Accent.TButton'
        )
        self.btn_extrair.grid(row=0, column=2)

        # Frame de botões de ação
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

        self.btn_salvar = ttk.Button(
            btn_frame, 
            text="💾 Salvar Arquivo", 
            command=self.salvar_arquivo,
            state='disabled'
        )
        self.btn_salvar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_copiar = ttk.Button(
            btn_frame, 
            text="📋 Copiar para Área de Transferência", 
            command=self.copiar_clipboard,
            state='disabled'
        )
        self.btn_copiar.pack(side=tk.LEFT, padx=(0, 10))

        self.btn_limpar = ttk.Button(
            btn_frame, 
            text="🗑️ Limpar Tudo", 
            command=self.limpar_tudo
        )
        self.btn_limpar.pack(side=tk.LEFT)

        # Frame de resultado
        resultado_frame = ttk.LabelFrame(main_frame, text="📄 HTML Extraído", padding="5")
        resultado_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        resultado_frame.columnconfigure(0, weight=1)
        resultado_frame.rowconfigure(0, weight=1)

        # Área de texto com scrollbars
        text_frame = ttk.Frame(resultado_frame)
        text_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.texto_html = scrolledtext.ScrolledText(
            text_frame, 
            width=120, 
            height=30,
            font=('Consolas', 9, 'normal'),
            wrap=tk.NONE,
            bg='#f8f9fa',
            fg='#2d3748',
            insertbackground='black'
        )
        self.texto_html.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.texto_html.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.texto_html.configure(yscrollcommand=v_scrollbar.set)

        h_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL, command=self.texto_html.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        self.texto_html.configure(xscrollcommand=h_scrollbar.set)

        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)

        self.status_label = ttk.Label(
            status_frame, 
            text="✅ Pronto para extrair HTML", 
            foreground="green", 
            font=('Arial', 9)
        )
        self.status_label.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(
            status_frame, 
            mode='indeterminate', 
            length=300
        )
        self.progress.pack(side=tk.RIGHT, padx=(10, 0))

        # Info adicional
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=5, column=0, columnspan=3, pady=(5, 0), sticky=tk.W)

        info_text = (
            "💡 Dicas: "
            "• Cole a URL e pressione ENTER ou clique em 'Extrair HTML' "
            "• Use Ctrl+F para buscar no HTML "
            "• O arquivo é salvo automaticamente com timestamp"
        )
        ttk.Label(info_frame, text=info_text, font=('Arial', 8), foreground="gray").pack(anchor=tk.W)

    def extrair_thread(self):
        """Executa extração em thread separada"""
        if self.url_entry.get().strip():
            thread = threading.Thread(target=self.extrair_html)
            thread.daemon = True
            thread.start()
        else:
            messagebox.showwarning("Aviso", "Por favor, insira uma URL válida!")

    def extrair_html(self):
        """Extrai HTML da URL fornecida"""
        url = self.url_entry.get().strip()

        if not url:
            return

        self.url_atual = url

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            self.url_entry.delete(0, tk.END)
            self.url_entry.insert(0, url)

        # Atualizar interface
        self.status_label.config(text="⏳ Extraindo HTML...", foreground="orange")
        self.btn_extrair.config(state='disabled')
        self.progress.start(10)
        self.root.update()

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            }

            print(f"📡 Fazendo requisição para: {url}")
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()

            print(f"✅ Resposta recebida: {len(response.content):,} bytes")

            # Parse com BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            self.html_atual = soup.prettify()

            # Limpar e inserir no texto
            self.texto_html.delete(1.0, tk.END)
            self.texto_html.insert(1.0, self.html_atual)

            # Ir para o início
            self.texto_html.see(1.0)

            # Estatísticas
            tamanho = len(self.html_atual)
            linhas = self.html_atual.count('\n')
            palavras = len(self.html_atual.split())

            self.status_label.config(
                text=f"✅ Extraído com sucesso! {tamanho:,} caracteres | {linhas:,} linhas | {palavras:,} palavras", 
                foreground="green"
            )

            # Habilitar botões
            self.btn_salvar.config(state='normal')
            self.btn_copiar.config(state='normal')

            # Salvar automaticamente
            self.salvar_automatico()

        except requests.exceptions.Timeout:
            error_msg = "⏰ Timeout: A página demorou muito para carregar"
            self.status_label.config(text=error_msg, foreground="red")
            messagebox.showerror("Timeout", "A requisição demorou muito tempo.\nTente novamente ou verifique a URL.")

        except requests.exceptions.ConnectionError:
            error_msg = "🌐 Erro de conexão: Verifique sua internet"
            self.status_label.config(text=error_msg, foreground="red")
            messagebox.showerror("Erro de Conexão", "Não foi possível conectar à URL.\nVerifique sua conexão com a internet.")

        except requests.exceptions.HTTPError as e:
            error_msg = f"❌ HTTP {e.response.status_code}: {e.response.reason}"
            self.status_label.config(text=error_msg, foreground="red")
            messagebox.showerror("Erro HTTP", f"Erro {e.response.status_code}: {e.response.reason}")

        except Exception as e:
            error_msg = f"❌ Erro inesperado: {str(e)[:100]}"
            self.status_label.config(text=error_msg, foreground="red")
            messagebox.showerror("Erro Inesperado", f"Erro ao processar a página:\n{str(e)}")
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()

        finally:
            self.btn_extrair.config(state='normal')
            self.progress.stop()

    def salvar_automatico(self):
        """Salva automaticamente com timestamp"""
        if not self.html_atual.strip():
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"html_extraido_{timestamp}.html"

        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(f"<!-- HTML extraído de: {self.url_atual} -->\n")
                f.write(f"<!-- Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
                f.write(self.html_atual)

            print(f"💾 Arquivo salvo automaticamente: {nome_arquivo}")

        except Exception as e:
            print(f"⚠️ Erro ao salvar automaticamente: {e}")

    def salvar_arquivo(self):
        """Salva o HTML em arquivo com diálogo"""
        if not self.html_atual.strip():
            messagebox.showwarning("Aviso", "Nenhum conteúdo para salvar!")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_padrao = f"html_extraido_{timestamp}.html"

        arquivo = filedialog.asksaveasfilename(
            title="Salvar HTML como...",
            defaultextension=".html",
            initialfile=nome_padrao,
            filetypes=[
                ("HTML files", "*.html"),
                ("All files", "*.*")
            ]
        )

        if arquivo:
            try:
                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(f"<!-- HTML extraído de: {self.url_atual} -->\n")
                    f.write(f"<!-- Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} -->\n\n")
                    f.write(self.html_atual)

                messagebox.showinfo(
                    "Sucesso", 
                    f"Arquivo salvo com sucesso!\n\n📁 {arquivo}\n📊 {len(self.html_atual):,} caracteres"
                )
                self.status_label.config(text=f"💾 Salvo: {os.path.basename(arquivo)}", foreground="blue")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo:\n{str(e)}")

    def copiar_clipboard(self):
        """Copia HTML para área de transferência"""
        if not self.html_atual.strip():
            messagebox.showwarning("Aviso", "Nenhum conteúdo para copiar!")
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(self.html_atual)
        self.status_label.config(text="📋 HTML copiado para área de transferência", foreground="blue")
        messagebox.showinfo("Copiado", "HTML copiado para área de transferência!")

    def limpar_tudo(self):
        """Limpa todos os campos"""
        self.url_entry.delete(0, tk.END)
        self.texto_html.delete(1.0, tk.END)
        self.html_atual = ""
        self.url_atual = ""
        self.btn_salvar.config(state='disabled')
        self.btn_copiar.config(state='disabled')
        self.status_label.config(text="🗑️ Limpo - Pronto para nova extração", foreground="gray")

    def ao_fechar(self):
        """Ação ao fechar a janela"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.root.destroy()

def main():
    """Função principal"""
    try:
        root = tk.Tk()
        app = ExtratorHTMLGUI(root)

        # Centralizar janela
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")

        print("🌐 Extrator de HTML GUI iniciado!")
        print("💡 Dica: Você pode arrastar este terminal para ver logs")

        root.mainloop()

    except ImportError as e:
        print(f"❌ Erro de importação: {e}")
        print("💡 Instale as dependências com: pip install -r requirements.txt")
        input("Pressione ENTER para sair...")
    except Exception as e:
        print(f"❌ Erro ao iniciar GUI: {e}")
        import traceback
        traceback.print_exc()
        input("Pressione ENTER para sair...")

if __name__ == "__main__":
    main()
