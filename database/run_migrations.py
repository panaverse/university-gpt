import sys
from dotenv import load_dotenv
from alembic.config import Config
from alembic import command
import os
# Load environment variables from .env
load_dotenv()
postgres_url = os.getenv("POSTGRES_URL")
# Create an Alembic configuration object
alembic_cfg = Config("alembic.ini",config_args={"sqlalchemy.url":postgres_url})

# Check for migration message and optional revision
if len(sys.argv) < 2:
    print("Please provide a migration message.")
    sys.exit(1)

migration_message = sys.argv[1]

revision = sys.argv[2] if len(sys.argv) >= 3 else 'head'

# Run the revision command with a message
command.revision(alembic_cfg, message=migration_message,autogenerate=True)

command.upgrade(alembic_cfg, "head")

