import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.base import Base
from app.models.promo_code import PromoCode
from app.services.promo_service import PromoService


# -----------------------------
# Тестовая база данных (in-memory SQLite)
# -----------------------------

@pytest.fixture()
def db():
    engine = create_engine("sqlite:///:memory:", future=True)
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True
    )

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


# -----------------------------
# Тесты PromoService
# -----------------------------

def test_generate_unique_promo_code(db):
    service = PromoService()

    promo1 = service.create_promo_code(db=db, user_id=123)
    promo2 = service.create_promo_code(db=db, user_id=123)

    assert promo1.code != promo2.code
    assert len(promo1.code) == 5
    assert promo1.code.isdigit()


def test_promo_code_saved_in_db(db):
    service = PromoService()

    promo = service.create_promo_code(db=db, user_id=555)

    saved = db.query(PromoCode).filter_by(code=promo.code).first()

    assert saved is not None
    assert saved.user_id == 555
