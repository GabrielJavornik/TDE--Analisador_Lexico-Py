import tkinter as tk
from itertools import groupby
from tkinter import ttk

from automato import (
    ALFABETO,
    ESTADO_ERRO,
    ESTADO_FINAL,
    ESTADO_INICIAL,
    TABELA_TRANSICOES,
    analisar,
    eh_letra_minuscula,
)


FUNDO = "#eef3f8"
PAINEL = "#ffffff"
FAIXA = "#e4edf7"
AZUL = "#173354"
TEXTO = "#253850"
SUAVE = "#4d6076"
BORDA = "#d4deea"
VERDE = "#236548"
VERMELHO = "#9e3c45"


def configurar_estilos(janela):
    janela.configure(background=FUNDO)
    estilo = ttk.Style(janela)
    estilo.theme_use("clam")
    estilo.configure(".", font=("Segoe UI", 10), foreground=TEXTO)
    estilo.configure("TFrame", background=FUNDO)
    estilo.configure("TLabel", background=FUNDO)
    estilo.configure("Faixa.TFrame", background=FAIXA)
    estilo.configure("Faixa.TLabel", background=FAIXA)
    estilo.configure(
        "Titulo.TLabel", background=FAIXA, foreground=AZUL,
        font=("Segoe UI", 22, "bold"),
    )
    estilo.configure("Subtitulo.TLabel", background=FAIXA, foreground=SUAVE)
    estilo.configure(
        "TituloModelo.TLabel", background=FAIXA, foreground=AZUL,
        font=("Segoe UI", 12, "bold"),
    )
    estilo.configure(
        "RotuloModelo.TLabel", background=FAIXA, foreground=SUAVE,
        font=("Segoe UI", 10, "bold"),
    )
    estilo.configure("Modelo.TLabel", background=FAIXA, font=("Consolas", 10))
    estilo.configure("TSeparator", background=BORDA)
    estilo.configure(
        "Painel.TFrame", background=PAINEL, bordercolor=BORDA,
        borderwidth=1, relief="solid",
    )
    estilo.configure("Painel.TLabel", background=PAINEL)
    estilo.configure(
        "Secao.TLabel", background=PAINEL, foreground=AZUL,
        font=("Segoe UI", 12, "bold"),
    )
    estilo.configure("Nota.TLabel", background=PAINEL, foreground=SUAVE)
    estilo.configure(
        "Estado.TLabel", background=PAINEL, foreground=AZUL,
        font=("Consolas", 13, "bold"),
    )
    estilo.configure("Transicao.TFrame", background=FUNDO)
    estilo.configure("Transicao.TLabel", background=FUNDO, foreground=AZUL, font=("Consolas", 10))

    for nome, cor in (("Resultado", SUAVE), ("Aceita", VERDE), ("Rejeitada", VERMELHO)):
        estilo.configure(
            f"{nome}.TLabel", background=PAINEL, foreground=cor,
            font=("Segoe UI", 15, "bold"),
        )

    estilo.configure(
        "Celula.TLabel", background="#f3f6fa", padding=(6, 1), anchor="center",
    )
    estilo.configure(
        "Cabecalho.TLabel", background="#e5edf6", foreground=AZUL,
        font=("Segoe UI", 10, "bold"), padding=(6, 1), anchor="center",
    )
    estilo.configure(
        "Destaque.TLabel", background=AZUL, foreground=PAINEL,
        font=("Segoe UI", 10, "bold"), padding=(6, 1), anchor="center",
    )
    estilo.configure("TEntry", fieldbackground=PAINEL, bordercolor=BORDA, padding=6)
    estilo.map("TEntry", bordercolor=[("focus", "#497bb4")])
    estilo.configure("TButton", padding=(9, 5), background="#e9f0f8", bordercolor=BORDA)
    estilo.map("TButton", background=[("active", "#dce8f5")])
    estilo.configure(
        "Treeview", background=PAINEL, fieldbackground=PAINEL,
        bordercolor=BORDA, rowheight=25,
    )
    estilo.configure(
        "Treeview.Heading", background="#e5edf6", foreground=AZUL,
        font=("Segoe UI", 10, "bold"), padding=(6, 4),
    )
    estilo.map(
        "Treeview", background=[("selected", AZUL)], foreground=[("selected", PAINEL)],
    )


def vai_para_erro(simbolo):
    return simbolo not in ALFABETO and all(
        linha[simbolo] == ESTADO_ERRO for linha in TABELA_TRANSICOES.values()
    )


class JanelaAnalisador:
    def __init__(self, janela):
        self.janela = janela
        janela.title("Analisador léxico | Linguagens Formais")
        configurar_estilos(janela)

        self.palavra = tk.StringVar()
        self.cadeia = tk.StringVar()
        self.estado_atual = tk.StringVar()
        self.ultima_transicao = tk.StringVar()
        self.celulas = {}
        self.celula_destacada = None

        self.montar_cabecalho(janela)
        pagina = ttk.Frame(janela, padding=(20, 12))
        pagina.pack(fill="both", expand=True)
        pagina.columnconfigure(0, weight=3)
        pagina.columnconfigure(1, weight=2)
        pagina.rowconfigure(1, weight=3)
        pagina.rowconfigure(2, weight=2)
        self.montar_entrada(pagina)
        self.montar_analise(pagina)
        self.montar_tabela(pagina)
        self.montar_historico(pagina)

        self.palavra.trace_add("write", self.atualizar_analise)
        self.atualizar_analise()
        janela.update_idletasks()
        largura_minima = max(820, janela.winfo_reqwidth())
        altura_minima = janela.winfo_reqheight()
        janela.minsize(largura_minima, altura_minima)
        janela.geometry(f"{max(1040, largura_minima)}x{max(675, altura_minima)}")
        self.entrada.focus_set()

    def montar_cabecalho(self, pai):
        faixa = ttk.Frame(pai, padding=(20, 12), style="Faixa.TFrame")
        faixa.pack(fill="x")
        faixa.columnconfigure(2, weight=1)

        identificacao = ttk.Frame(faixa, style="Faixa.TFrame")
        identificacao.grid(row=0, column=0, sticky="w")
        ttk.Label(identificacao, text="Analisador léxico", style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(
            identificacao, text="Linguagens Formais\nLista 2 · Exercício 2, letra j",
            style="Subtitulo.TLabel", justify="left",
        ).pack(anchor="w", pady=(3, 0))
        ttk.Separator(faixa, orient="vertical").grid(row=0, column=1, sticky="ns", padx=20)

        modelo = ttk.Frame(faixa, style="Faixa.TFrame")
        modelo.grid(row=0, column=2, sticky="ew")
        ttk.Label(modelo, text="Modelo formal", style="TituloModelo.TLabel").grid(
            row=0, column=0, columnspan=3, sticky="w", pady=(0, 5),
        )
        secoes = (
            (
                "Linguagem", "Palavras sobre {a, b, c} com um número ímpar de c.",
                "Faixa.TLabel", 190,
            ),
            (
                "AFD mínimo", "M = ({qPar, qImpar}, {a, b, c},\n     δ, qPar, {qImpar})",
                "Modelo.TLabel", 0,
            ),
            (
                "Gramática regular · S inicial", "S ::= aS | bS | cA\nA ::= aA | bA | cS | ε",
                "Modelo.TLabel", 0,
            ),
        )
        for coluna, (titulo, texto, estilo, largura) in enumerate(secoes):
            modelo.columnconfigure(coluna, weight=1)
            margem = (0, 16) if coluna < len(secoes) - 1 else (0, 0)
            ttk.Label(modelo, text=titulo, style="RotuloModelo.TLabel").grid(
                row=1, column=coluna, sticky="w", padx=margem, pady=(0, 3),
            )
            ttk.Label(
                modelo, text=texto, style=estilo, justify="left", wraplength=largura,
            ).grid(row=2, column=coluna, sticky="nw", padx=margem)
        ttk.Separator(pai, orient="horizontal").pack(fill="x")

    def montar_entrada(self, pai):
        painel = ttk.Frame(pai, padding=12, style="Painel.TFrame")
        painel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        painel.columnconfigure(0, weight=1)
        painel.columnconfigure(1, minsize=200)
        ttk.Label(
            painel, text="Digite uma palavra e pressione Espaço", style="Secao.TLabel",
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))
        validar = self.janela.register(self.validar_entrada)
        self.entrada = ttk.Entry(
            painel, textvariable=self.palavra, font=("Consolas", 17),
            validate="key", validatecommand=(validar, "%P"),
        )
        self.entrada.grid(row=1, column=0, sticky="ew")
        self.entrada.bind("<KeyPress>", self.filtrar_tecla)
        self.entrada.bind("<space>", self.encerrar_palavra)
        self.entrada.bind("<<Paste>>", self.colar)

        ttk.Label(painel, text="Último resultado", style="Nota.TLabel").grid(
            row=0, column=1, sticky="w", padx=(22, 0),
        )
        self.resultado = ttk.Label(painel, text="—", style="Resultado.TLabel")
        self.resultado.grid(row=1, column=1, sticky="w", padx=(22, 0))

    def montar_analise(self, pai):
        painel = ttk.Frame(pai, padding=(12, 7), style="Painel.TFrame")
        painel.grid(row=1, column=0, sticky="nsew", padx=(0, 6), pady=(0, 12))
        painel.columnconfigure(0, weight=1)
        painel.rowconfigure(4, weight=1)
        ttk.Label(painel, text="Análise da palavra", style="Secao.TLabel").grid(
            row=0, column=0, sticky="w",
        )
        ttk.Button(painel, text="Limpar análise", command=self.limpar_analise).grid(
            row=0, column=1, sticky="e", padx=(10, 0),
        )
        ttk.Label(painel, text="Cadeia analisada", style="Nota.TLabel").grid(
            row=1, column=0, sticky="w", pady=(4, 2),
        )
        self.rotulo_estado = ttk.Label(painel, text="Estado atual", style="Nota.TLabel")
        self.rotulo_estado.grid(
            row=1, column=1, sticky="w", padx=(10, 0), pady=(4, 2),
        )
        campo_cadeia = ttk.Entry(
            painel, textvariable=self.cadeia, state="readonly",
            font=("Consolas", 12), width=12,
        )
        campo_cadeia.grid(row=2, column=0, sticky="ew")
        ttk.Label(painel, textvariable=self.estado_atual, style="Estado.TLabel").grid(
            row=2, column=1, sticky="w", padx=(10, 0),
        )
        ttk.Label(painel, text="Percurso das transições", style="Nota.TLabel").grid(
            row=3, column=0, columnspan=2, sticky="w", pady=(5, 3),
        )
        self.percurso = self.criar_lista(
            painel, 4, (("Passo", 52), ("Origem", 86), ("Letra", 60), ("Destino", 88)),
            altura=3,
        )

    def montar_historico(self, pai):
        painel = ttk.Frame(pai, padding=12, style="Painel.TFrame")
        painel.grid(row=2, column=0, columnspan=2, sticky="nsew")
        painel.columnconfigure(0, weight=1)
        painel.rowconfigure(1, weight=1)
        ttk.Label(painel, text="Histórico", style="Secao.TLabel").grid(
            row=0, column=0, sticky="w", pady=(0, 7),
        )
        ttk.Button(painel, text="Limpar histórico", command=self.limpar_historico).grid(
            row=0, column=1, sticky="e", padx=(10, 0), pady=(0, 7),
        )
        self.historico = self.criar_lista(
            painel, 1, (("Palavra", 90), ("Resultado", 105), ("Estado atingido", 110)),
            altura=3,
        )
        self.historico.tag_configure("aceita", foreground=VERDE)
        self.historico.tag_configure("rejeitada", foreground=VERMELHO)

    def criar_lista(self, pai, linha, colunas, altura):
        moldura = ttk.Frame(pai, style="Painel.TFrame")
        moldura.grid(row=linha, column=0, columnspan=2, sticky="nsew")
        moldura.columnconfigure(0, weight=1)
        moldura.rowconfigure(0, weight=1)
        lista = ttk.Treeview(
            moldura, columns=[nome for nome, _ in colunas], show="headings",
            height=altura, selectmode="browse",
        )
        for nome, largura in colunas:
            lista.heading(nome, text=nome)
            lista.column(nome, width=largura, minwidth=largura, anchor="center")
        rolagem = ttk.Scrollbar(moldura, orient="vertical", command=lista.yview)
        lista.configure(yscrollcommand=rolagem.set)
        lista.grid(row=0, column=0, sticky="nsew")
        rolagem.grid(row=0, column=1, sticky="ns")
        return lista

    def montar_tabela(self, pai):
        painel = ttk.Frame(pai, padding=(12, 7), style="Painel.TFrame")
        painel.grid(row=1, column=1, sticky="nsew", padx=(6, 0), pady=(0, 12))
        ttk.Label(painel, text="Tabela de transições", style="Secao.TLabel").pack(anchor="w")
        matriz = ttk.Frame(painel, style="Painel.TFrame")
        matriz.pack(fill="x", pady=(4, 5))
        estados = list(TABELA_TRANSICOES)
        for coluna, texto in enumerate(("Símbolo", *estados)):
            matriz.columnconfigure(coluna, weight=1, uniform="transicoes")
            self.criar_celula(matriz, 0, coluna, texto, "Cabecalho.TLabel")

        simbolos = TABELA_TRANSICOES[ESTADO_INICIAL]
        grupos = groupby(simbolos, key=lambda letra: "" if vai_para_erro(letra) else letra)
        for linha, (_, grupo) in enumerate(grupos, start=1):
            letras = list(grupo)
            rotulo = letras[0] if len(letras) == 1 else f"{letras[0]}–{letras[-1]}"
            self.criar_celula(matriz, linha, 0, rotulo, "Cabecalho.TLabel")
            for coluna, estado in enumerate(estados, start=1):
                destino = TABELA_TRANSICOES[estado][letras[0]]
                celula = self.criar_celula(matriz, linha, coluna, destino, "Celula.TLabel")
                for letra in letras:
                    self.celulas[estado, letra] = celula

        ultima = ttk.Frame(painel, padding=(8, 4), style="Transicao.TFrame")
        ultima.pack(fill="x", pady=(1, 4))
        ttk.Label(ultima, text="Última transição").pack(side="left", padx=(0, 10))
        ttk.Label(ultima, textvariable=self.ultima_transicao, style="Transicao.TLabel").pack(side="left")
        ttk.Label(
            painel, text="Letras de d a z levam a qErro até a próxima palavra.",
            style="Nota.TLabel", wraplength=340, justify="left",
        ).pack(anchor="w")

    def criar_celula(self, matriz, linha, coluna, texto, estilo):
        celula = ttk.Label(matriz, text=texto, style=estilo)
        celula.grid(row=linha, column=coluna, sticky="ew", padx=1, pady=1)
        return celula

    def validar_entrada(self, texto):
        return all(eh_letra_minuscula(letra) for letra in texto)

    def filtrar_tecla(self, evento):
        if evento.char and evento.char.isprintable() and not eh_letra_minuscula(evento.char):
            return "break"
        return None

    def colar(self, _evento):
        try:
            texto = self.entrada.clipboard_get()
        except tk.TclError:
            return "break"
        texto = "".join(letra for letra in texto if letra == " " or eh_letra_minuscula(letra))
        for indice, trecho in enumerate(texto.split(" ")):
            if indice:
                self.encerrar_palavra()
            if trecho:
                if self.entrada.selection_present():
                    self.entrada.icursor("sel.first")
                    self.entrada.delete("sel.first", "sel.last")
                self.entrada.insert("insert", trecho)
        return "break"

    def atualizar_analise(self, *_):
        palavra = self.palavra.get()
        self.rotulo_estado.configure(text="Estado atual")
        self.mostrar_analise(palavra, *analisar(palavra))

    def mostrar_analise(self, palavra, estado, percurso):
        self.cadeia.set(palavra or "ε")
        self.estado_atual.set(estado)
        self.percurso.delete(*self.percurso.get_children())
        for passo, transicao in enumerate(percurso, start=1):
            item = self.percurso.insert("", "end", values=(passo, *transicao))
        if percurso:
            self.percurso.see(item)
        self.destacar_transicao(percurso[-1] if percurso else None)

    def destacar_transicao(self, transicao):
        if self.celula_destacada is not None:
            self.celula_destacada.configure(style="Celula.TLabel")
            self.celula_destacada = None
        self.ultima_transicao.set("—")
        if transicao is not None:
            origem, letra, destino = transicao
            self.celula_destacada = self.celulas[origem, letra]
            self.celula_destacada.configure(style="Destaque.TLabel")
            self.ultima_transicao.set(f"δ({origem}, {letra}) = {destino}")

    def encerrar_palavra(self, _evento=None):
        palavra = self.palavra.get()
        estado, percurso = analisar(palavra)
        if estado == ESTADO_FINAL:
            texto, estilo, tag = "Reconhecida", "Aceita.TLabel", "aceita"
        else:
            texto, estilo, tag = "Rejeitada", "Rejeitada.TLabel", "rejeitada"
        self.resultado.configure(text=texto, style=estilo)
        item = self.historico.insert("", "end", values=(palavra or "ε", texto, estado), tags=(tag,))
        self.historico.see(item)
        self.palavra.set("")
        self.mostrar_analise(palavra, estado, percurso)
        self.rotulo_estado.configure(text="Estado atingido")
        return "break"

    def limpar_analise(self):
        self.palavra.set("")
        self.resultado.configure(text="—", style="Resultado.TLabel")
        self.entrada.focus_set()

    def limpar_historico(self):
        self.historico.delete(*self.historico.get_children())


def main():
    janela = tk.Tk()
    JanelaAnalisador(janela)
    janela.mainloop()


if __name__ == "__main__":
    main()
