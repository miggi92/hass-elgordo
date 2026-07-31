DOMAIN = "elgordo"
BASE_API_URL = "https://api.elpais.com/ws/LoteriaNavidadPremiados"
MANUFACTURER = "Loteria de España"
STORAGE_VERSION = 1

TICKET_TYPE_DECIMO = "decimo"
TICKET_TYPE_BILLETE = "billete"
DEFAULT_TICKET_TYPE = TICKET_TYPE_DECIMO


def prize_for_ticket_type(prize, ticket_type):
    """Convert an API prize per billete to the configured ticket type."""
    if prize is None:
        return prize
    if ticket_type == TICKET_TYPE_BILLETE:
        return prize
    if ticket_type == TICKET_TYPE_DECIMO:
        if isinstance(prize, int):
            return prize // 10
        return prize / 10
    raise ValueError(f"Unsupported ticket type: {ticket_type}")

INITIAL_FALLBACK_SUMMARY = {
    "data_source": "stored_results",
    "draw_year": 2025,
    "numero1": "79432",
    "numero2": "70048",
    "numero3": "90693",
    "numero4": "78477",
    "numero5": "25508",
}

INITIAL_FALLBACK_TICKETS = {
    "27133": {"premio": 0},
}
