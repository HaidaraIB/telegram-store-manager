"""Run Alembic migrations programmatically (e.g. on bot startup)."""
import logging
from pathlib import Path

from alembic import command
from alembic.config import Config as AlembicConfig

from Config import Config

logger = logging.getLogger(__name__)


def run_alembic_upgrade(revision: str = "head") -> None:
    project_root = Path(__file__).resolve().parent.parent
    alembic_cfg = AlembicConfig(str(project_root / "alembic.ini"))
    alembic_cfg.set_main_option("sqlalchemy.url", f"sqlite:///{Config.DB_PATH}")
    # Keep the application's logging config (see alembic/env.py).
    alembic_cfg.attributes["configure_logger"] = False
    logger.info("Running Alembic upgrade to %s", revision)
    command.upgrade(alembic_cfg, revision)
    logger.info("Alembic upgrade complete")
