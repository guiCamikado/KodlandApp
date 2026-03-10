#formulario, listagem e janela de edição
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from config import COLORS, STATUS_OPTIONS, EDIT_WINDOW_SIZE

def aplicar_estilos():
    style = ttk.Style()

    style.theme_use('clam')

    style.configure(
        'TCombobox',
        fieldbackground=COLORS['entry_bg'],
        background=COLORS['entry_bg'],
        foreground=COLORS['entry_fg'],
        arrowcolor=COLORS['fg']
    )

    style.theme_use('clam')
    style.configure('TCombobox',
                    fieldbackground=COLORS['entry_bg'],
                    background=COLORS['entry_bg'],
                    foreground=COLORS['entry_fg'],
                    arrowcolor=COLORS['fg'])

    style.configure('Vertical.TScrollbar',
                    background=COLORS['entry_bg'],
                    troughcolor=COLORS['bg'],
                    arrowcolor=COLORS['fg'])

    style.configure("Treeview",
                    background=COLORS['tree_bg'],
                    foreground=COLORS['tree_fg'],
                    fieldbackground=COLORS['tree_bg'],
                    rowheight=25)
    style.map('Treeview', background=[('selected', COLORS['selected_bg'])])

    style.configure("Treeview.Heading",
                    background=COLORS['tree_heading_bg'],
                    foreground=COLORS['tree_heading_fg'],
                    relief="flat")
    style.map("Treeview.Heading", background=[('active', '#4a4a4a')])
    #fix combobox
    style.map(
        'TCombobox',
        fieldbackground=[('readonly', COLORS['entry_bg'])],
        foreground=[('readonly', COLORS['entry_fg'])])

# formulario de cadastro
class FormularioCadastro(tk.Frame):
    def __init__(self, parent, on_adicionar_callback, **kwargs):
        super().__init__(parent, bg=COLORS['bg'], **kwargs)
        self._on_adicionar = on_adicionar_callback
        self._construir()

    def _construir(self):
        campos = [
            ("Empresa:",              "entry_empresa", 40),
            ("Cargo:",                "entry_cargo",   40),
            ("Link:",                 "entry_link",    60),
            ("Data (AAAA-MM-DD):",    "entry_data",    20),
            ("Observações:",          "entry_obs",     60),
        ]

        for row, (label, attr, width) in enumerate(campos):
            tk.Label(self, text=label, bg=COLORS['bg'],
                     fg=COLORS['fg']).grid(row=row, column=0, sticky="w", pady=2)

            entry = tk.Entry(self, width=width,
                             bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                             insertbackground=COLORS['fg'],
                             relief=tk.FLAT, bd=2)
            entry.grid(row=row, column=1, padx=5, pady=2,
                       sticky="w" if width <= 20 else "")
            setattr(self, attr, entry)

        # data de hj por padrão
        self.entry_data.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # combobox de status
        status_row = 4
        # Recria o layout com status na posição correta
        self._reposicionar_com_status()

        tk.Button(self, text="Adicionar", command=self._on_adicionar,
                  bg=COLORS['button_bg'], fg=COLORS['button_fg'],
                  relief=tk.FLAT, padx=20, pady=5,
                  cursor="hand2").grid(row=6, column=1, pady=10, sticky="w")

    def _reposicionar_com_status(self):
        # Destrói todos os widgets filhos e reconstrói em ordem correta
        for widget in self.winfo_children():
            widget.destroy()

        linhas = [
            ("Empresa:",           "entry_empresa", 40),
            ("Cargo:",             "entry_cargo",   40),
            ("Link:",              "entry_link",    60),
            ("Data (AAAA-MM-DD):", "entry_data",    20),
        ]

        for row, (label, attr, width) in enumerate(linhas):
            tk.Label(self, text=label, bg=COLORS['bg'],
                     fg=COLORS['fg']).grid(row=row, column=0, sticky="w", pady=2)
            entry = tk.Entry(self, width=width,
                             bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                             insertbackground=COLORS['fg'],
                             relief=tk.FLAT, bd=2)
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="w")
            setattr(self, attr, entry)

        self.entry_data.insert(0, datetime.today().strftime('%Y-%m-%d'))

        # status
        tk.Label(self, text="Status:", bg=COLORS['bg'],
                 fg=COLORS['fg']).grid(row=4, column=0, sticky="w", pady=2)
        self.combo_status = ttk.Combobox(self, values=STATUS_OPTIONS,
                                         state="readonly", width=18)
        self.combo_status.set("Pendente")
        self.combo_status.grid(row=4, column=1, padx=5, pady=2, sticky="w")

        # observações
        tk.Label(self, text="Observações:", bg=COLORS['bg'],
                 fg=COLORS['fg']).grid(row=5, column=0, sticky="w", pady=2)
        self.entry_obs = tk.Entry(self, width=60,
                                  bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                                  insertbackground=COLORS['fg'],
                                  relief=tk.FLAT, bd=2)
        self.entry_obs.grid(row=5, column=1, padx=5, pady=2)

        # botão
        tk.Button(self, text="Adicionar", command=self._on_adicionar,
                  bg=COLORS['button_bg'], fg=COLORS['button_fg'],
                  relief=tk.FLAT, padx=20, pady=5,
                  cursor="hand2").grid(row=6, column=1, pady=10, sticky="w")

    # API ppub
    def obter_valores(self) -> dict:
        return {
            'empresa': self.entry_empresa.get().strip(),
            'cargo':   self.entry_cargo.get().strip(),
            'link':    self.entry_link.get().strip(),
            'data':    self.entry_data.get().strip(),
            'status':  self.combo_status.get(),
            'obs':     self.entry_obs.get().strip(),
        }

    #reseta Campos
    def limpar(self):
        self.entry_empresa.delete(0, tk.END)
        self.entry_cargo.delete(0, tk.END)
        self.entry_link.delete(0, tk.END)
        self.entry_data.delete(0, tk.END)
        self.entry_data.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.combo_status.set("Pendente")
        self.entry_obs.delete(0, tk.END)


# Listagem
class ListagemCandidaturas(tk.Frame):
    COLUNAS = ('id', 'empresa', 'cargo', 'data_cadastro', 'status', 'link', 'observacoes')
    LARGURAS = (40, 150, 150, 90, 100, 150, 200)
    CABECALHOS = ('ID', 'Empresa', 'Cargo', 'Data', 'Status', 'Link', 'Observações')

    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=COLORS['bg'], **kwargs)
        self._construir()

    def _construir(self):
        self.tree = ttk.Treeview(self, columns=self.COLUNAS,
                                 show='headings', height=12)

        for col, cabecalho, largura in zip(self.COLUNAS, self.CABECALHOS, self.LARGURAS):
            self.tree.heading(col, text=cabecalho)
            self.tree.column(col, width=largura)

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL,
                                  command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def popular(self, candidaturas: list[tuple]):
        """Substitui o conteúdo da Treeview pelos registros fornecidos."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for c in candidaturas:
            link_display = c[3][:30] + '...' if c[3] and len(c[3]) > 30 else (c[3] or '')
            obs_display  = c[6][:30] + '...' if c[6] and len(c[6]) > 30 else (c[6] or '')

            self.tree.insert('', tk.END, iid=c[0], values=(
                c[0],          # id
                c[1],          # empresa
                c[2],          # cargo
                c[4],          # data_cadastro
                c[5],          # status
                link_display,
                obs_display,
            ))

    def item_selecionado_id(self) -> int | None:
        foco = self.tree.focus()
        if not foco:
            return None
        return int(self.tree.item(foco, 'iid'))

    def valores_selecionados(self) -> tuple | None:
        foco = self.tree.focus()
        if not foco:
            return None
        return self.tree.item(foco, 'values')