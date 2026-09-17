"""Storage for cards, backed by SQLite through SQLAlchemy.

All access goes through the `CardStore` class so the database can be
swapped for something else later without changing the rest of the app.
"""

from datetime import datetime, timezone
from typing import Any

from app.database import SessionLocal
from app.db_models import CardModel


def _to_dict(card: CardModel) -> dict[str, Any]:
    return {
        "id": card.id,
        "title": card.title,
        "description": card.description,
        "status": card.status,
        "created_at": card.created_at,
    }


class CardStore:
    def list_cards(self) -> list[dict[str, Any]]:
        with SessionLocal() as session:
            cards = (
                session.query(CardModel)
                .order_by(CardModel.created_at, CardModel.id)
                .all()
            )
            return [_to_dict(card) for card in cards]

    def create_card(self, title: str, description: str) -> dict[str, Any]:
        with SessionLocal() as session:
            card = CardModel(
                title=title,
                description=description,
                status="todo",
                created_at=datetime.now(timezone.utc),
            )
            session.add(card)
            session.commit()
            session.refresh(card)
            return _to_dict(card)

    def get_card(self, card_id: int) -> dict[str, Any] | None:
        with SessionLocal() as session:
            card = session.get(CardModel, card_id)
            return _to_dict(card) if card else None

    def update_card(self, card_id: int, **fields: Any) -> dict[str, Any] | None:
        with SessionLocal() as session:
            card = session.get(CardModel, card_id)
            if card is None:
                return None
            for key, value in fields.items():
                setattr(card, key, value)
            session.commit()
            session.refresh(card)
            return _to_dict(card)

    def delete_card(self, card_id: int) -> bool:
        with SessionLocal() as session:
            card = session.get(CardModel, card_id)
            if card is None:
                return False
            session.delete(card)
            session.commit()
            return True

    def reset(self) -> None:
        with SessionLocal() as session:
            session.query(CardModel).delete()
            session.commit()


store = CardStore()
