import pytest
from datetime import datetime, timezone
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.resources.database import Base
from src.models.interconsulta import InterconsultaPedido
from src.helpers.crypto_helper import encrypt_data, decrypt_data

# In-memory SQLite for fast testing
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
    async with SessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_interconsulta_soft_delete(db_session: AsyncSession):
    # Cria pedido mock
    pedido = InterconsultaPedido(
        paciente_cns=encrypt_data("123456789012345"),
        medico_solicitante_crm="12345-PE",
        especialidade_id=1,
        sintomas_json=[{"id": 1, "nome": "Dor Torácica"}],
        gravidade="VERMELHO"
    )
    db_session.add(pedido)
    await db_session.commit()
    await db_session.refresh(pedido)

    assert pedido.id is not None
    assert pedido.deleted_at is None

    # Aplica Soft Delete
    pedido.deleted_at = datetime.now(timezone.utc)
    db_session.add(pedido)
    await db_session.commit()
    await db_session.refresh(pedido)

    assert pedido.deleted_at is not None

@pytest.mark.asyncio
async def test_interconsulta_aes_encryption(db_session: AsyncSession):
    original_cns = "123456789012345"
    encrypted_cns = encrypt_data(original_cns)
    
    # O valor criptografado deve ser diferente do original
    assert encrypted_cns != original_cns
    
    pedido = InterconsultaPedido(
        paciente_cns=encrypted_cns,
        medico_solicitante_crm="12345-PE",
        especialidade_id=1,
        sintomas_json=[{"id": 1, "nome": "Dor Torácica"}],
        gravidade="VERMELHO"
    )
    db_session.add(pedido)
    await db_session.commit()
    await db_session.refresh(pedido)

    # Verifica se ao puxar do banco, a descriptografia funciona
    cns_retornado = decrypt_data(pedido.paciente_cns)
    assert cns_retornado == original_cns
