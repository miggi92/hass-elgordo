# El Gordo - Spanish Christmas Lottery Winning Conditions

This document outlines the prize tiers and winning conditions for the Spanish Christmas Lottery (Sorteo Extraordinario de Navidad), commonly known as "El Gordo". It serves as a reference for the Home Assistant component logic to evaluate a given 5-digit ticket number against the official drawn results.

## Terminology
*   **Billete**: A full ticket (costs 200 €). Official prize lists usually state the payout per billete.
*   **Décimo**: A tenth of a ticket (costs 20 €). This is the most common format played by individuals. Prizes per décimo are exactly 10% of the billete prize.
*   **Serie**: A series of tickets sharing the same 5-digit number.

## Prize Categories (Payouts per Billete / per Décimo)

### Main Prizes (Premios Mayores)
These are the most significant draws.
1.  **1st Prize (El Gordo)**: 4,000,000 € (400,000 € per décimo) - 1 winning number
2.  **2nd Prize**: 1,250,000 € (125,000 € per décimo) - 1 winning number
3.  **3rd Prize**: 500,000 € (50,000 € per décimo) - 1 winning number
4.  **4th Prize**: 200,000 € (20,000 € per décimo) - 2 winning numbers
5.  **5th Prize**: 60,000 € (6,000 € per décimo) - 8 winning numbers

### The "Pedrea"
The standard minor prizes drawn continuously throughout the event.
*   **La Pedrea**: 1,000 € (100 € per décimo) - 1,794 winning numbers

### Approximations (Aproximaciones)
Numbers immediately preceding (-1) and succeeding (+1) the main prizes.
*   Before/After 1st Prize: 20,000 € (2,000 € per décimo) - 2 winning numbers
*   Before/After 2nd Prize: 12,500 € (1,250 € per décimo) - 2 winning numbers
*   Before/After 3rd Prize: 9,600 € (960 € per décimo) - 2 winning numbers

### Hundreds (Centenas)
Tickets sharing the exact first three digits with the main prizes.
*   First 3 digits of 1st, 2nd, 3rd, and 4th prizes: 1,000 € (100 € per décimo)

### Last Two Digits (Terminaciones)
Tickets sharing the exact last two digits with the main prizes.
*   Last 2 digits of 1st, 2nd, and 3rd prizes: 1,000 € (100 € per décimo)

### Refund (Reintegro)
Tickets where the final digit matches the final digit of the 1st prize (El Gordo).
*   Last digit of 1st prize: 200 € (20 € per décimo) - Basically a refund for the billete/décimo.