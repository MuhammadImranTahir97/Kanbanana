from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.models import Card, CardCreate, CardUpdate
from app.storage import store

app = FastAPI(title="Kanbanana API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api")


@router.get("/cards", response_model=list[Card])
def list_cards() -> list[dict]:
    return store.list_cards()


@router.post("/cards", response_model=Card, status_code=201)
def create_card(payload: CardCreate) -> dict:
    return store.create_card(title=payload.title, description=payload.description)


@router.patch("/cards/{card_id}", response_model=Card)
def update_card(card_id: int, payload: CardUpdate) -> dict:
    updates = {
        key: value
        for key, value in payload.model_dump(exclude_unset=True).items()
        if value is not None
    }
    card = store.update_card(card_id, **updates)
    if card is None:
        raise HTTPException(status_code=404, detail="Card not found.")
    return card


@router.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int) -> None:
    if not store.delete_card(card_id):
        raise HTTPException(status_code=404, detail="Card not found.")


app.include_router(router)
