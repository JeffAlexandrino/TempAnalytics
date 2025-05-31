import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import sys

# ---------------------------------------------------------------
# Dicionário com opções de gráficos para cada script
# As chaves são nomes dos arquivos Python (scripts auxiliares),
# e os valores são as opções de rótulo que o usuário verá.
# ---------------------------------------------------------------
opcoes_graficos = {
    "tempGlobal.py": [
        "Todos",
        "Sazonal com Incerteza",
        "Média Móvel 10 Anos",
        "Terra vs Terra+Oceano",
        "Décadas"
    ],
    "tempPaises.py": [
        "Todos",
        "Evolução por País",
        "Temperatura por Década",
        "Amplitude Térmica",
        "Distribuição Países",
        "Mapa de Calor Brasil"
    ]
}


def executar_script():
    script = script_var.get()
    grafico = grafico_var.get()

    # Verifica se o usuário escolheu um script
    if not script:
        messagebox.showerror("Atenção", "Você precisa selecionar um script.")
        return
    # Verifica se o usuário escolheu um tipo de gráfico
    if not grafico:
        messagebox.showerror("Atenção", "Você precisa selecionar um tipo de gráfico.")
        return

    # ---------------------------------------------------------------
    # Mapeamento de rótulos amigáveis para os argumentos 
    # esperados pelos scripts auxiliares (os mesmos definidos em choices).
    # ---------------------------------------------------------------
    mapeamento_argumentos = {
        "Sazonal com Incerteza": "sazonal",
        "Média Móvel 10 Anos": "media_movel",
        "Terra vs Terra+Oceano": "comparacao",
        "Décadas": "decadas",
        "Evolução por País": "evolucao",
        "Temperatura por Década": "decada",
        "Amplitude Térmica": "amplitude",
        "Distribuição Países": "distribuicao",
        "Mapa de Calor Brasil": "mapa",
        "Todos": "Todos"
    }

    argumento = mapeamento_argumentos.get(grafico, "Todos")

    # ---------------------------------------------------------------
    # Usa sys.executable para garantir que o mesmo Python que
    # executa o menu seja utilizado nos scripts auxiliares.
    # ---------------------------------------------------------------
    try:
        subprocess.run([sys.executable, f"scripts/{script}", "--grafico", argumento], check=True)
        # Opcional: você pode descomentar a linha abaixo para exibir
        # uma mensagem de sucesso após o script terminar:
        # messagebox.showinfo("Sucesso", f"'{script}' executado com sucesso.")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao executar '{script}':\n{e}")


def atualizar_graficos(event):
    script = script_var.get()
    # Atualiza as opções do combobox de gráficos conforme o script escolhido
    menu_grafico['values'] = opcoes_graficos.get(script, [])
    # Seleciona automaticamente a primeira opção ("Todos")
    if opcoes_graficos.get(script):
        menu_grafico.current(0)


# ---------------------------------------------------------------
# Construção da interface Tkinter
# ---------------------------------------------------------------
janela = tk.Tk()
janela.title("Menu de Visualização de Temperaturas")

# Label e Combobox para selecionar o script
ttk.Label(janela, text="Selecione o script:").grid(row=0, column=0, padx=10, pady=10)
script_var = tk.StringVar()
menu_script = ttk.Combobox(
    janela,
    textvariable=script_var,
    values=list(opcoes_graficos.keys()),
    state="readonly"
)
menu_script.grid(row=0, column=1, padx=10, pady=10)
menu_script.bind("<<ComboboxSelected>>", atualizar_graficos)

# Label e Combobox para selecionar o tipo de gráfico
ttk.Label(janela, text="Selecione o gráfico:").grid(row=1, column=0, padx=10, pady=10)
grafico_var = tk.StringVar()
menu_grafico = ttk.Combobox(
    janela,
    textvariable=grafico_var,
    state="readonly"
)
menu_grafico.grid(row=1, column=1, padx=10, pady=10)

# Botão para executar o script com o argumento selecionado
btn_executar = ttk.Button(janela, text="Executar", command=executar_script)
btn_executar.grid(row=2, column=0, columnspan=2, pady=20)

# ---------------------------------------------------------------
# Pré-seleciona o primeiro script ao abrir a janela, para já
# popular o combobox de gráficos imediatamente.
# ---------------------------------------------------------------
menu_script.current(0)
atualizar_graficos(None)

janela.mainloop()
