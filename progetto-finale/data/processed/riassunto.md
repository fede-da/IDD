Una volta ottenuta la tabella principale genero un nuovo file contenente il risultato della strategia di blocking applicata ("bigrams"" o "trigrams" ad esempio).

Ad esempio "bigrams_temp.csv" contiene per ogni riga, bigramma e identificatore (riga del file aziende a cui quel bigramma fa riferimento).

Successivamente vengono creati i "block" ovvero tutti gli n-gram identici (stessa stringa) vengono inseriti all'interno dello stesso blocco (se l'n-gram è troppo frequente allora viene scartato). Quindi si costruisce un indice inverso che contiene per ogni riga l'id del blocco e le righe (del file aziende) in cui questo compare.

Quindi viene eseguito il "pairwise matching" ovvero vengono confontati nel seguente modo:

```python
# Quando si confrontano nomi di aziende, ad esempio, è comune trovare piccole variazioni o errori di battitura. La distanza di Levenshtein aiuta a quantificare quanto sono simili due stringhe, fornendo una base per decidere se due voci rappresentano lo stesso elemento nonostante lievi differenze.
compare.string('CompanyName', 'CompanyName', method='levenshtein', label='CompanyName')
# Per confronti numerici è utile sapere quanto due numeri sono vicini. La funzione gaussiana fornisce una misura di similarità che considera la distanza tra numeri in modo continuo e “moroso”.
compare.numeric('MarketCap', 'MarketCap', method='gauss', scale=1, label='MarketCap')
# Il numero di dipendenti è un intero, quindi cerchiamo l'esatto numero
compare.exact('EmployeesTotalAmount', 'EmployeesTotalAmount', label='EmployeesTotalAmount')
```

Due per volta, tutti gli id all'interno dello stesso blocco recuperando il loro record dal file originale delle aziende ed avviene il confronto tramite un certo parametro. Se il risultato del confronto è maggiore di una certa soglia allora quella coppia viene indicata come match, altrimenti no.