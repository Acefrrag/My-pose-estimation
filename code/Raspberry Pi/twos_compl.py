#Questo modulo contiene la funzione twos_comp che associa alla rappresentazione
#di un numero intero in complemento a 2, il numero intero.
#Per informazioni consulta la tesi.

#Funzione efficente utilizzata nei moduli dei sensori. Usa solo i bit della
#rappresentazione e non la funzione potenza
def twos_comp(rappresentation, N):
    if(rappresentation&(1<<(N-1)) != 0):
        number = rappresentation - (1<<N) # You know that 2^N is 1000....0 where 1 is the N+1 bit of the sequence
    else:
        number = rappresentation
    return number

#Questa coppia di funzioni e stata sviluppata all inizio sulla base della
#definizione di  #complemento a due di un numero. NON viene utilizzata ne
#modulo dei sensori
def twos_comp_ineff(rappresentation, N):
    if(rappresentation <= (potenza(2,N-1)-1)):
        number = rappresentation
    else:
        number = -(potenza(2,N) - rappresentation)
        #Questo e perche |number| = 2^(N) - rappresentation
    return number
def potenza(natural, M):
    potenza = 1
    for i in range(M):
        potenza = potenza * natural
    return potenza
