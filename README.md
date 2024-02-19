# 1. problema dei sottoeventi
## (risolto divinamente e implementato)
possono essere creati dei sottoeventi da pushare in un unico evento 
ma questo potrebbe comportare problemi di incompatibilita' tra la seguenza di sottoeventi e quindi calcolare tutta la correttezza della sequenza di sottoeventi e fare revert nel caso ci sia un errore
per carita' e' implementable facilmente perche tanto se si crea un errore si cancellano facilmente tutte le operazioni di tutti i sottoeventi prima 
questa potrebbe essere a mio parere la soluzione migliore. ovvero tutte le create, modify, delete possono essere singoli eventi o sottoeventi di un evento piu' grande che contiene tutti i sottoeventi
cosi risulta tutto flessibile e componibile
il problema e' che si genera una profondita' di eventi che potrebbe essere problematica per la gestione di un evento

# 2. problema dell'ordine e dello storico dei qualifier nello stesso evento
## (al momento gestito archiviando l'intero storico dei qualifier dell'evento eseguendoli tutti e mantenendo l'ordine, permettendo qualsiasi composizione valida di qualifiers)
con la soluzione implementata nel caso di un create object 1, delete object 1 e create object 1, avremo che object 1 e' coinvolto nell'evento 3 volte distinte due create e una delete nell'ordine sopracitato riuscendo a capire a posteriori l'effettivo ordine degli eventi  

# 3. object_attribute_values 
## (al momento non ho coinvolto name come parte della chiave)
key: object_attribute_value_id, object_id # maybe also name
perche' altrimenti si potrebbe avere due attributi con value_id diversi ma con lo stesso nome e valore
permettendo si comunque di distinguerli ma risulta difficile per l'umano discriminare tra i due

# 4. type of attribute values
## (questo va sistemato, vanno consentiti i seguenti valori [str, int, float, bool, None] e non solo str)
i value di object e event volendo potrebbero essere di tipo str, int, float, bool, None e non solo e unicamente str.
qui si pone il problema che la colonna type non ha un tipo unico e il qualifier modify potrebbe cambiare il valore di un attributo da un tipo ad un altro. forse in realta' e' meglio archiviare tutto sottoforma di stringhe, ovvero obbligare l'utente a passare solo stringhe.
non sollo, diventa piu' articoltato fare dump e load. al momento ho gestito facilmente tutti i valori come stringhe tranne gli existency come bool e event_id e qualifier_index come int. ovvero tutte e sole le variabili che non inserisce lutente.

# 5. current state or history
## (implementato il current state)
dubbio relativo ad archiviare nella parte destra solo lo stato corrente del sistema o tutto lo storico.
meglio la prima opzione siccome tutto lo storico e' archiviato implicitamente nella parte sinistra.
ma in realta' non e' vero perche' nella parte sinistra ad esempio non posso vedere come variano i valori degli attibuti della parte destra. si potremme storare anche questa informazione sulla parte sinistra ma non diventa flessibile e modulare e si appesantisce inutilmente la parte sinistra delegando a lei una funzione non pianificata cosi'.
meglio implementare la history sulla parte destra.
occorre quindi per ogni object, object_attribute_value, object_relation mantenere in memoria una variabile alive booleana.
il problema pero' e' che cosi' vengono meno i vincoli dell'esistenza di nomi di attributi che persistono nel database anche se gli oggetti vengono eliminati

# 6. implementare il qualifier add che porta in vita un oggetto eliminato con il qualifier delete
siccome ho assunto che non si puo' fare create su un oggetto precedentemente creato e poi eliminato per farlo tornare in vita

# 7 non permettere la modifica a vuoto usando inutilmente i modify qualifiers
implementato da un qualifier al suo successivo non da un evento all'altro e non da un qualifier ad index x ad un qualifier ad index x+y con y>1
nota che solo per modify e' possibile avere due righe uguali nelle tabelle event_x_* quando faccio ad esempio modifica in 2 modifica in 1 modifica in 2
si potrebbe aggiungere il vincolo che da pre e post evento il valore deve essere modificato per davvero non solo a singoli step 

# 8. permetto di modificare solo se gli id hanno existency == True
implementato cosi'

# 9. permettere di fare get degli attributi di tutti gli oggetti e non potermi modificare in nessun modo eccetto con la reflection
implementato cosi' e quindi ad ogni get ho messo .deepcopy

# 10. posso avere eventi che non hanno nessun qualifier? eventi non correlati a nessun object, object_relation, object_attribute_value
al momento questa cosa e; consentita percvhe' la lista qualifiers dentro event non ha il vincolo di essere diversa da lista vuota
e' giusto cosi perche' un eveto potrebbe anche non voler coinvolgere nessun evento con nessun qualifier 

# 11. from object id e to object id devono essere differenti 
implementato cosi'



# TODO
- gestire l'eliminazione di un oggetto secondo le regole della call for application
ad esempio se elimino un oggetto elimino anche i suoi attributi e tutte le sue relazioni (forse... ricontrolla l'articolo) 
elimino pero' anche tutti i suoi oggetti figli 



- permettere la creazione di relationship anche quando uno dei due oggetti non esiste se questo oggetto in questione e' il figlio di quelo che esiste, 
cosi' facendo l'ogetto figlio viene creato al volo senza il qualifier opportuno e il type dell'oggetto e' 'CHILD_OF_{type dell'oggetto padre}'