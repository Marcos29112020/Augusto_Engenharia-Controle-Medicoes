# Augusto Engenharia – Controle de Medições

Painel em Streamlit que lê a planilha **"Controle de Medições e Saldos - Obras"** (Google Sheets).

## Abas da planilha usadas

| Aba | Para que serve no painel | Obrigatória? |
|---|---|---|
| `Dados_Dashboard` | Números por obra: contrato, medido, saldo, %, status | Sim |
| `Obras` | Endereço, observações e data da última medição | Não |
| `Medições` | Histórico de lançamentos e gráfico mensal (aba "Medições lançadas") | Não |

## Como o painel lê os dados (nesta ordem)

1. **Conta de serviço do Google** (se configurada em *Settings → Secrets*, ver `secrets.toml.example`): lê as 3 abas e a planilha pode ficar privada.
2. **Publicar na Web (CSV)**: hoje só a aba `Dados_Dashboard` está publicada. Para as abas `Obras` e `Medições` aparecerem por esse caminho, publique o **Documento inteiro** em *Arquivo → Compartilhar → Publicar na Web*.
3. **Última leitura válida**, se o Google falhar momentaneamente.
4. **Cópia local** (22/10/2026), com aviso na tela.

## Recursos

- Indicadores, progresso geral, saldo e % medido por obra
- Tabela com endereço, data da última medição e há quantos dias foi feita
- **Pontos de atenção**: conferência automática da planilha (saldo que não bate, medido acima do contrato,
  status divergente entre abas, obra ativa sem medição há mais de 30 dias, carimbo "Atualizado em" desatualizado)
- Aba **Medições lançadas** com o histórico e o valor medido por mês
- Botão **Baixar Excel** com as obras filtradas e as medições

## Lançando medições

Na aba `Medições`, use as linhas amarelas: **uma linha por medição, com o valor daquela medição** (não o acumulado).
As linhas laranja são o saldo inicial acumulado até outubro/2026 e não devem ser alteradas.
