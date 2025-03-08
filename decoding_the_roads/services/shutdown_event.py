from ..utils.logger import setup_logger

logger = setup_logger(__name__)  

async def shutdown_event():

    logger.info("Shutting down...")

    logger.info("Shutdown complete.")