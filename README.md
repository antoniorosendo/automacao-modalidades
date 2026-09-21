# Automação Atualizadora de Modalidades em Planilhas Excel

Automação em Python para padronização em massa de modalidades em planilhas Excel, desenvolvida para uso real na **Secretaria de Pesquisa da FT Unicamp**.

---

## Contexto

A Secretaria de Pesquisa da FT Unicamp mantém planilhas de controle de bolsas e projetos de pesquisa com **mais de 1000 linhas cada**, exportadas de um sistema interno (SIP). Com o tempo, o sistema acumulou inconsistências nos nomes das modalidades: a mesma modalidade aparecia grafada de formas diferentes dependendo da época do cadastro ou da agência de fomento — por exemplo, `PIBIC`, `BOLSA NO PAIS - REGULAR - INICIACAO CIENTIFICA` e `IC` representavam a mesma categoria, mas estavam registradas de formas distintas ao longo dos anos.

Corrigir isso manualmente linha a linha seria inviável. Esta automação resolve o problema em segundos, independentemente do tamanho das planilhas.

> **Nota sobre os dados:** por se tratarem de dados institucionais, as planilhas originais não estão neste repositório. Em seu lugar, foi criado um exemplo fictício com tema de um clube de xadrez, que preserva exatamente a mesma estrutura e lógica da aplicação real.

---

## O que a automação faz

Cada script lê duas planilhas:

1. **Planilha de dados** — contém os registros com a coluna `Modalidade` a ser padronizada.
2. **Planilha de regras** — define o mapeamento: qual é o nome oficial de cada modalidade (`Modalidade`) e quais são todas as variações antigas que devem ser substituídas por ele (`Equivalente`).

Com base nesse mapeamento, o script percorre cada linha da planilha de dados, identifica a qual modalidade oficial aquele valor pertence e faz a substituição. Além disso, formata as colunas de data para o padrão `dd/mm/aaaa`, ignorando células que não sejam datas sem interromper a execução.

O resultado é salvo em um novo arquivo Excel, preservando o original.

---

## Estrutura do projeto

```
├── Treinamentos/
│   ├── Treinamentos.xlsx           # Planilha de dados (entradas)
│   ├── Modalidades-Treinamentos.xlsx  # Planilha de regras de mapeamento
│   └── TreinamentosUpdate.py       # Script de atualização
│
└── Projetos/
    ├── Torneios.xlsx               # Planilha de dados (entradas)
    ├── Modalidades-Torneios.xlsx   # Planilha de regras de mapeamento
    └── TorneiosUpdate.py          # Script de atualização
```

Cada pasta é independente — os scripts lêem e gravam apenas dentro de seu próprio diretório.

---

## Como usar

**Pré-requisitos**

```bash
pip install pandas openpyxl
```

**Execução**

Entre na pasta desejada e rode o script correspondente:

```bash
cd Treinamentos
python TreinamentosUpdate.py
```

```bash
cd Projetos
python TorneiosUpdate.py
```

Os arquivos de saída (`Treinamentos_Atualizados.xlsx` e `Torneios_Atualizados.xlsx`) serão gerados na mesma pasta.

---

## Como funciona o mapeamento

A planilha de regras tem a seguinte estrutura:

| Ordem | Modalidade | Equivalente | Agência | Tipo |
|-------|------------|-------------|---------|------|
| 1 | INI - INICIACAO AO XADREZ | BOLSA TREINAMENTO - REGULAR - INICIACAO<br>TREINO BASICO<br>INICIACAO | Todas | Bolsa |

A coluna `Equivalente` pode conter múltiplos valores separados por quebra de linha (`\n`) ou ponto e vírgula (`;`). O script constrói um dicionário com cada um desses valores apontando para a modalidade oficial e aplica a substituição em toda a planilha de uma vez.

Se um valor não tiver correspondência no dicionário, ele é mantido como está — nenhum dado é perdido.

---

## Tecnologias

- **Python 3**
- **pandas** — leitura, manipulação e escrita das planilhas
- **openpyxl** — engine de suporte ao formato `.xlsx`
- **re** — expressões regulares para separar os equivalentes de cada regra
