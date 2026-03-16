import json 
import pandas as pd
from sklearn.preprocessing import LabelEncoder
# salvo il file nella variabile data
with open('./data/alerts.json', 'r') as f:
    data = json.load(f)




lista_colonne = ['_source.rule.id','_source.rule.level','_source.rule.groups','_source.rule.description','_source.agent.name','_source.decoder.name']

# creo un dataframe con le colonne desiderate
df = pd.json_normalize(data['hits']['hits'])
for c in df.columns:
    print(c)
df = df[lista_colonne]
df['_source.rule.groups'] = df['_source.rule.groups'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "unknown")
print(df.shape)

print(df.isnull().sum()) # verifico se ci sono valori nulli


# ok zero valori nulli 

# prima nella lista di colonne da includere c'era anche la tecnica mitre, ma era vuota. sicuramente sono liste. 
# verifico


# infatti sono liste
# prendo solo il primo elemento 
# ho modificato direttamente sopra. 
# df['_source.rule.groups'] = df['_source.rule.groups'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else "unknown") 

print(df.dtypes)
# sono tutte stringhe, se devo fare un clustering o comunque passarli su un algoritmo ml vanno encodati. ok

# uso label encoder per trasformare le stringhe in numeri
# importato il pacchetto

'''le = LabelEncoder()
le.fit(["paris", "paris", "tokyo", "amsterdam"])
LabelEncoder()
list(le.classes_)
[np.str_('amsterdam'), np.str_('paris'), np.str_('tokyo')]
le.transform(["tokyo", "tokyo", "paris"])
array([2, 2, 1]...)
list(le.inverse_transform([2, 2, 1]))
[np.str_('tokyo'), np.str_('tokyo'), np.str_('paris')]
'''
# prima di fare encoding copio il df così se devo controllare qualche valore lo tengo con i valori leggibili. 
df_original = df.copy()


# encoding 

le = LabelEncoder()
for c in df.columns.difference(['_source.rule.level']):
    df[c] = le.fit_transform(df[c])

# provo di nuovo a stampare 
print(df.dtypes)
print(df.head())

# in teoria ok 
# salvo in un csv
df.to_csv('./data/alerts.csv', index=False)
print("File 'alerts.csv' creato con successo.")

df_original.to_csv('./data/alerts_readable.csv', index=False)