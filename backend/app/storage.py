"""In-memory storage for cards.

This is a mock database. All access goes through the `CardStore` class so
the storage can later be swapped for a real database (e.g. SQLite via
SQLAlchemy) without changing the rest of the app.
"""

from datetime import datetime, timezone
from typing import Any


class CardStore:
    def __init__(self) -> None:
        self._cards: dict[int, dict[str, Any]] = {}
        self._next_id = 1

    def list_cards(self) -> list[dict[str, Any]]:
        return sorted(self._cards.values(), key=lambda card: card["created_at"])

    def create_card(self, title: str, description: str) -> dict[str, Any]:
        card = {
            "id": self._next_id,
            "title": title,
            "description": description,
            "status": "todo",
            "created_at": datetime.now(timezone.utc),
        }
        self._cards[card["id"]] = card
        self._next_id += 1
        return card

    def get_card(self, card_id: int) -> dict[str, Any] | None:
        return self._cards.get(card_id)

    def update_card(self, card_id: int, **fields: Any) -> dict[str, Any] | None:
        card = self._cards.get(card_id)
        if card is None:
            return None
        card.update(fields)
        return card

    def delete_card(self, card_id: int) -> bool:
        return self._cards.pop(card_id, None) is not None

    def reset(self) -> None:
        self._cards.clear()
        self._next_id = 1


store = CardStore()
