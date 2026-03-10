# conecta db com a interface

import tkinter as tk
from tkinter import messagebox

from config import COLORS, WINDOW_TITLE, WINDOW_SIZE

from database import CandidaturaRepository
from views import aplicar_estilos, FormularioCadastro, ListagemCandidaturas

# Controller
class CandidaturaApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.configure(bg=COLORS['bg'])
        
        self.repo = CandidaturaRepository()# dados
        
        aplicar_estilos()
        self._montar_interface() # componentes visuais
        self._atualizar_lista()  # dados iniciais

        # fecha db
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    # interface
    def _montar_interface(self):
        self.formulario = FormularioCadastro(
            self.root,
            on_adicionar_callback=self._adicionar,
        )
        self.formulario.pack(fill="x", padx=10, pady=5)

        self.listagem = ListagemCandidaturas(self.root)
        self.listagem.pack(fill="both", expand=True, padx=10, pady=5)

    def _adicionar(self):
        dados = self.formulario.obter_valores()

        if not dados['empresa'] or not dados['cargo']:
            messagebox.showwarning("Campos obrigatórios",
                                   "Empresa e cargo são obrigatórios.")
            return

        try:
            self.repo.inserir(
                empresa=dados['empresa'],
                cargo=dados['cargo'],
                link=dados['link'],
                data=dados['data'],
                status=dados['status'],
                obs=dados['obs'],
            )
            messagebox.showinfo("Sucesso", "Candidatura adicionada!")
            self.formulario.limpar()
            self._atualizar_lista()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível adicionar: {e}")

    def _atualizar_lista(self):
        try:
            candidaturas = self.repo.listar_todas()
            self.listagem.popular(candidaturas)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")

    def _ao_fechar(self):
        self.repo.fechar()
        self.root.destroy()
