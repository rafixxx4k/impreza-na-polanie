# impreza-na-polanie
Algorytm programowania rozproszonego do umawiania się zwierząt na imprezę

każdy proces wie o Z zajączków o N niedźwiedi i liście P polan o pojemniości S gdzie niedźwiedź to 4 zajączki

założenia P * (S - 1) < Z

każda polana ma:
sekcję krytyczną z S miejscami
sekca krytyczna 1 miejscowa (kto przynosi alkohol dla niedzwiedzi)


## Struktury i zmienne:
1. **liczba zajączków** - Z
2. **liczba niedźwiedzi** - N
3. **liczba polan** - P
4. **pojemność każdej polany** - S
5. każdy proces lista Px[]- na itej polanie są te indexy


## Wiadomości
Wszystkie wiadomości są podbite znacznikiem czasowym
(timestampem), modyfikowanym zgodnie z zasadami skalarnego
zegara logicznego Lamporta.

1. REQ [nr] [id] żądanie dostępu do n-tej polany
2. ACK [id] - potwierdzenie dostępu do sekcji krytycznej z polaną
3. ENTER [nr] [id] wejście na polanę
4. ALK [nr] [id] żądanie pmożliwoości przyniesienia więcej alkoholu (dla niedźwiedzi)
5. OK [id] - potwierdzenie możliwości przyniesienia więcej alkoholu (dla niedźwiedzi)

## Stany
 Stanem początkowym procesu jest REST
 
REST
WAIT
CRIT
ALCO
