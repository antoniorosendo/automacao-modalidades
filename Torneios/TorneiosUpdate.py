import pandas as pd
import re

def extrair_modalidades(texto):
    if pd.isna(texto) or str(texto).strip() == '-':
        return []
    
    partes = re.split(r'[\n;]', str(texto))
    return [p.strip() for p in partes if p.strip()]

#Lê a tabela de regras de Torneios
df_regras = pd.read_excel('Modalidades-Torneios.xlsx')

dict_torneios = {}
for index, row in df_regras.iterrows():
    mod_nova = row['Modalidade']
    equivalentes = extrair_modalidades(row['Equivalente'])
    for eq in equivalentes:
        dict_torneios[eq] = mod_nova

#Lê a planilha de Torneios (header=1 pula o título da primeira linha)
df_torneios = pd.read_excel('Torneios.xlsx', header=1)

#Formata as datas para dd/mm/aaaa ignorando valores que não são datas
if 'Início da Vigência' in df_torneios.columns:
    datas_inicio = pd.to_datetime(df_torneios['Início da Vigência'], errors='coerce').dt.strftime('%d/%m/%Y')
    df_torneios['Início da Vigência'] = datas_inicio.fillna(df_torneios['Início da Vigência'])

if 'Fim da Vigência' in df_torneios.columns:
    datas_fim = pd.to_datetime(df_torneios['Fim da Vigência'], errors='coerce').dt.strftime('%d/%m/%Y')
    df_torneios['Fim da Vigência'] = datas_fim.fillna(df_torneios['Fim da Vigência'])

#Remove espaços em branco invisíveis da coluna e aplica a substituição
coluna_limpa = df_torneios['Modalidade'].astype(str).str.strip()
df_torneios['Modalidade'] = coluna_limpa.map(dict_torneios).fillna(df_torneios['Modalidade'])

#Salva o arquivo atualizado
df_torneios.to_excel('Torneios_Atualizados.xlsx', index=False)
print("Planilha de Torneios atualizada com sucesso!")
