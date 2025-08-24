import logging
from typing import Optional


def configure_logger(
    name: str = "scrapping-app",
    level: int = logging.INFO,
    log_format: Optional[str] = None,
    propagate: bool = False,
    handler: Optional[logging.Handler] = None
) -> logging.Logger:
    """
    Configura y devuelve un logger personalizado para la aplicación.
    Puedes ajustar el nivel, formato y handler desde fuera (por ejemplo, en FastAPI/main.py).
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate  # Evita logs duplicados

    if not log_format:
        log_format = "%(asctime)s [%(levelname)s] %(name)s %(module)s:%(lineno)d | %(message)s"
    formatter = logging.Formatter(log_format)

    # Si no hay handlers configurados aún, agrega uno
    if not logger.handlers:
        handler = handler or logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
