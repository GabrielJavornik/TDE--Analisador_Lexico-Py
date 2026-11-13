# Analisador léxico

TDE de Linguagens Formais · Lista 2 · Exercício 2, letra j (página 20 da apostila)

## Execução no Windows

Use uma instalação do Python 3.9 ou mais recente com Tcl/Tk e o inicializador `py`. Abra o terminal na pasta do projeto e execute `py main.py`. A janela usa Tkinter e ttk, da biblioteca padrão do Python.

## Demonstração

Digite uma palavra e pressione **Espaço**. Enquanto você edita o campo, a janela mostra a cadeia, o estado atual e o percurso. A tabela destaca a última transição consultada. Ao encerrar a palavra, a janela registra o resultado e o estado atingido no histórico. O campo fica pronto para a próxima palavra e a análise da anterior permanece visível até você voltar a digitar.

- `c`, `abca` e `ccc` terminam em `qImpar` e são reconhecidas.
- `ab`, `cc` e a cadeia vazia (`ε`) terminam em `qPar` e são rejeitadas. Pressione Espaço com o campo vazio para registrar `ε`.
- `dc` termina em `qErro` e é rejeitada. Digite `cd` e apague `d` para ver o percurso recalculado até `qImpar`.
- Cole `c cc ccc abcx ` para registrar quatro resultados em sequência. Cole `c! ` para ver que apenas `c` é analisado.

Backspace, Delete e a substituição de texto recalculam o percurso. A entrada aceita `a` a `z` e ignora maiúsculas, números, acentos, pontuação e quebras de linha. Tab navega pelos controles. Enter mantém a palavra aberta.

## Modelo formal

A linguagem é `L = { w ∈ {a, b, c}⁺ | w contém um número ímpar de c }`. A apostila usa `⁺` para indicar palavras não vazias.

O AFD mínimo sobre o alfabeto oficial é `M = ({qPar, qImpar}, {a, b, c}, δ, qPar, {qImpar})`. O estado inicial `qPar` representa uma quantidade par de `c`. O único estado final, `qImpar`, representa uma quantidade ímpar. As letras `a` e `b` preservam a paridade, e `c` alterna entre os estados.

A gramática regular equivalente tem símbolo inicial `S`.

```text
S ::= aS | bS | cA
A ::= aA | bA | cS | ε
```

Na janela, o estado `qErro` recebe as letras minúsculas de `d` a `z`. Todas as letras mantêm a máquina em `qErro` até começar outra palavra.

## Tabela de transições e alteração ao vivo

A tabela `TABELA_TRANSICOES` fica em [automato.py](automato.py). A função `analisar` começa em `qPar` e consulta `TABELA_TRANSICOES[estado][simbolo]` para cada letra. O programa encerra a palavra em `main.py` e verifica se o estado atingido é `qImpar`.

Se o professor pedir que `j` preserve a paridade, faça as duas alterações abaixo na tabela. Você pode editar os valores no dicionário ou acrescentar estas linhas logo após a definição dele.

```python
TABELA_TRANSICOES["qPar"]["j"] = "qPar"
TABELA_TRANSICOES["qImpar"]["j"] = "qImpar"
```

Mantenha `"j": "qErro"` na linha de `qErro` e reabra a janela. Com essa alteração, `jcj` seria reconhecida e `jj` seria rejeitada.

Se a mudança passar a valer para o exercício, inclua também `j` no alfabeto do modelo formal e acrescente `jS` e `jA` às produções de `S` e `A`, respectivamente. Os arquivos entregues usam o alfabeto oficial `{a, b, c}`.
