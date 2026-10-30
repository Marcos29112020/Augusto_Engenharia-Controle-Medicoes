# Augusto Engenharia – Controle de Medições

Painel em Streamlit que mostra a aba **Dados_Dashboard** da planilha
**"Controle de Medições e Saldos - Obras"** (Google Sheets).

## Como funciona

```
Aba Medições  ──(soma por obra)──┐
                                 ├──► Aba Dados_Dashboard ──► Dashboard (site)
Aba Obras  ──(valor do contrato)─┘
```

- **Medições**: onde se lança cada medição (data, nº da obra, valor).
- **Obras**: cadastro das obras e valor do contrato.
- **Dados_Dashboard**: 100% fórmulas. Não editar. É a única aba que o site lê.

O site consulta a planilha a cada 1 minuto. O Google pode levar até ~5 minutos para
liberar uma alteração no link publicado. Para forçar, clique em **Atualizar dados**.

## Fontes de dados (em ordem)

1. Link "Publicar na Web" (CSV) da aba Dados_Dashboard.
2. Conta de serviço do Google (opcional, ver `secrets.toml.example`).
3. Última leitura válida, se o Google falhar no momento.
4. Cópia local (22/10/2026), com aviso na tela.

## Lançando medições

Na aba `Medições`, use a primeira linha amarela livre: **uma linha por medição, com o valor daquela medição**
(não o acumulado). Preencha Data, Nº da Obra e Valor. O nome da obra aparece sozinho.

## Nova obra

1. Aba `Obras`: nova linha com Nº, nome e valor do contrato (copie as fórmulas da linha de cima).
2. Aba `Dados_Dashboard`: insira uma linha **acima da linha TOTAL**, com o Nº e o nome, e copie as fórmulas da linha de cima.
