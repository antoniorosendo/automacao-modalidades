import pandas as pd
import re

def extrair_modalidades(texto):
    if pd.isna(texto) or str(texto).strip() == '-':
        return []
    
    partes = re.split(r'[\n;]', str(texto))
    return [p.strip() for p in partes if p.strip()]

#Lê a tabela de regras de Treinamentos
df_regras = pd.read_excel('Modalidades-Treinamentos.xlsx')

dict_treinamentos = {}
for index, row in df_regras.iterrows():
    mod_nova = row['Modalidade']
    equivalentes = extrair_modalidades(row['Equivalente'])
    for eq in equivalentes:
        dict_treinamentos[eq] = mod_nova

#Lê a planilha de Treinamentos (header=1 pula o título da primeira linha)
df_treinamentos = pd.read_excel('Treinamentos.xlsx', header=1)

#Formata as datas para dd/mm/aaaa ignorando valores que não são datas
if 'Início da Vigência' in df_treinamentos.columns:
    datas_inicio = pd.to_datetime(df_treinamentos['Início da Vigência'], errors='coerce').dt.strftime('%d/%m/%Y')
    df_treinamentos['Início da Vigência'] = datas_inicio.fillna(df_treinamentos['Início da Vigência'])

if 'Fim da Vigência' in df_treinamentos.columns:
    datas_fim = pd.to_datetime(df_treinamentos['Fim da Vigência'], errors='coerce').dt.strftime('%d/%m/%Y')
    df_treinamentos['Fim da Vigência'] = datas_fim.fillna(df_treinamentos['Fim da Vigência'])

#Remove espaços em branco invisíveis da coluna e aplica a substituição
coluna_limpa = df_treinamentos['Modalidade'].astype(str).str.strip()
df_treinamentos['Modalidade'] = coluna_limpa.map(dict_treinamentos).fillna(df_treinamentos['Modalidade'])

#Salva o arquivo atualizado
df_treinamentos.to_excel('Treinamentos_Atualizados.xlsx', index=False)
print("Planilha de Treinamentos atualizada com sucesso!")
