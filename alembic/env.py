# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
# Importe o create_async_engine do SQLAlchemy
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context

# Adicione estas duas linhas para importar sua Base de modelos
import sys, os
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from app.database import Base
from app.settings import settings # Importe suas configurações

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adicione seu model's MetaData object aqui
# para suporte ao 'autogenerate'
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    (Esta função geralmente não precisa de alterações)
    """
    url = settings.DATABASE_URL # Usando a URL dos settings
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Função auxiliar que executa as migrações dentro de um contexto.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    Neste cenário, nós criamos um Engine
    e associamos uma conexão com o contexto.
    """
    # Cria um engine assíncrono a partir da nossa URL de settings
    connectable = create_async_engine(
        settings.DATABASE_URL,
        poolclass=pool.NullPool,
    )

    # Conecta-se de forma assíncrona
    async with connectable.connect() as connection:
        # Usa o metodo run_sync para executar a função de migração síncrona
        await connection.run_sync(do_run_migrations)

    # Descarta o engine
    await connectable.dispose()


# O ponto de entrada principal: verifica se está offline ou online
# e então usa asyncio.run para executar a função async run_migrations_online
if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())