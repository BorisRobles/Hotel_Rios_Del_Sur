PENDIENTE = 'Pendiente'
CONFIRMADA = 'Confirmada'
EN_CURSO = 'En curso'
FINALIZADA = 'Finalizada'
CANCELADA = 'Cancelada'

TODOS_LOS_ESTADOS = [
    PENDIENTE,
    CONFIRMADA,
    EN_CURSO,
    FINALIZADA,
    CANCELADA,
]

# Reservas que todavía no llegan al hotel
ESTADOS_POR_LLEGAR = [PENDIENTE, CONFIRMADA]

# Reservas que bloquean la habitación para esas fechas
ESTADOS_QUE_OCUPAN = [PENDIENTE, CONFIRMADA, EN_CURSO]

# Máximo de noches que se pueden reservar de una vez
MAX_NOCHES = 31