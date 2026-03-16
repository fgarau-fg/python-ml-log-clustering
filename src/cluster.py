import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np


file = pd.read_csv('./data/alerts.csv')
file_readable =  pd.read_csv('./data/alerts_readable.csv')
print(file.head())
print(file.shape)


#  formula: z=x−μσz=σx−μ


# standardizzazione dei dati: 

'''

logica: 
partendo da molto indietro: 
cosa sto cercando di fare: clusterizzare i dati, quindi trovare dei gruppi di eventi simili tra loro.
potrei utilizzare anche altri algoritmi, ma parto da kmenasperché per me è il piu facile da capire, 
in futuro proverò con DBSCAN, che è più lento ma più libero,
e anche Agglomerative Clustering, che però costruisce una gerarchia di cluster. 

Riguardo KMEANS: 
è molto veloce,
restituisce un risultato che posso interpretare, poiché ogni punto appartiene ad un cluster con un centro. 
sono tuttavia forzato a decidere un numero k di cluster a priori e come si puo vedere nell'immagine in ../notebooks/cluster.png, 
devo anche in un certo senso adattarmi all'aspetto che kmeans vorrebbe su un cluster, ossia sferico.

Il problema: 
i log hanno dati, attributi che sono su scale completamente diverse. Basti pensare per esempio alla porta, che va da 1 fino a 65535...
non ha nulla in comune con l'id dell evento o della rule, tantomeno del gruppo, tantomeno ancora con l'agent name vettorizzato. 
In altre, parole, i dati sono su scale e range diversi, e ciò non mi consente di avere cluster sferici. 
quindi faccio in modo che lo siano; 

La soluzione: 
standardizzando i dati, posso far si che abbiano tutti una media comune (0) e una stdev 1. 

'''

ss = StandardScaler()
x = ss.fit_transform(file)
print(x[:5]) # perfetto, adesso la media è 0 e la stdev 1


# elbow method per trovare il k ottimale
# NB diverse k vengono testate, fin quando non si trova il gomito: rif. file ../notebooks/elbow_method.png 

inertia_ = [] # creo lista vuota 

for k in range(2,12):
    # print(k)
    km = KMeans(n_clusters=k, random_state=42)
    km.fit(x) # Sto dicendo a K-Means "prendi questi dati e trovami k gruppi". Lui li analizza, calcola i centroidi e assegna ogni riga a un cluster.
    inertia_.append(km.inertia_) # attributo calcolato dall'algoritmo, non lo sto passando io

# plotto il grafico

x_axis = range(2,12)
y_axis = inertia_ 
plt.plot(x_axis, y_axis, marker='o') 
plt.show() # forse 8 ??????
# provo a fare la derivata
# su internet usano np.gradient ma ha bisogno di un array numpy
derivata_y = np.gradient(np.array(inertia_))
plt.plot(x_axis, derivata_y, marker='o')
plt.show()
# vado con 8

km_finale = KMeans(n_clusters=8, random_state=42)
labels = km_finale.fit_predict(x)
print(labels, len(labels))


# quindi ricapitolando ho allenato KMEANS con 8 clusters perfetto, e ogni numero mi indica il cluster di appartenenza. 
# ora dovrei aggiungere questo array come colonna al csv, così mi indicherebbe ogni alert in che cluster appare. 

file['cluster'] = labels
file_readable['cluster'] = file['cluster']
file_readable.to_csv('./data/alerts_readable_clustered.csv', index=False) # salvo colonna cluster anche nel csv leggibile 
# sono sicuro che siano gli stessi eventi nello stesso ordine? 
print(file.index.equals(file_readable.index)) # verifico, se stampa true ok
print(file.head())
print(file.groupby('cluster').size())
print(file.groupby('cluster')['_source.rule.level'].mean())
print(file[file['cluster'] == 7])

print(file_readable.iloc[[709, 994]])