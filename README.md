# Máquina de inferência

## A linguagem

### Fatos
Fatos são variáveis únicas com valor Verdadeiro, sempre. Exemplo:

    A: True
    B: True

Pode ser uma base de fatos.

#### Arquivo csv
O arquivo 'facts.csv' deve ser organizado da seguite forma:

- Header 'variavel', abaixo do qual ficam listadas as variáveis:


        variavel
        A
        B
        C
        ...

### Regras
Regras são do tipo P -> Q, em que P é uma expressão conjutiva e Q é uma variável. Todos os valores de P são verdadeiros. Exemplo:

    A ^ B -> C
    A -> D
    A ^ B ^ C ^ D -> E

É uma base de regras. Já os seguintes exemplos:

    A v B -> C
    A -> C ^ D
    A -> C v B

não são regras aceitas pelo programa.

O programa não espera que mais de um antecedente gere o mesmo consequente. Exemplo:

    A ^ B -> C
    B ^ D -> C

#### Arquivo csv
O arquivo 'rules.csv' deve ser organizado da seguite forma:

- Headers 'antecedente' e 'consequente'
- Sob 'antecedente' ficam as expressões antecedentes. Caso haja conjução, o operador '^' será escrito 'and'.
- O consequente é separado do antecedente por vírgula (como se fosse o operador ->) e é uma variável simples. 

Exemplo:

    antecedente,consequente
    A and B,C
    A,D
    C and D,E
    B and E and F,G
    A and E,H
    D and E and G,I


## Execução da questão 1

    cd src/quest1

Aqui é possível executar o programa. Ele aceita como argumentos de linha de comando a pasta com os exemplos, a qual devem conter um arquivo 'facts.csv' e um arquivo 'facts.csv', a serem lidos. Assim:

    python3 quest1.py ex1 # usa os arquivos de exemplo da pasta ex1

