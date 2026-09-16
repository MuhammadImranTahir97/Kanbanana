# Kanbanana 🍌 — Product Spec

## 1. Overview

Kanbanana is a simple Kanban board for tracking tasks. You add cards and move them from **To Do** → **In Progress** → **Done**.

**Who it's for:** anyone who wants a quick, no-fuss way to track tasks, such as a student tracking homework.

- One shared board
- No login
- Cards are saved in a database, so they stay after a page refresh and look the same in every browser

## 2. The board

- The board always has exactly 3 columns, from left to right:
  1. To Do
  2. In Progress
  3. Done
- Columns can't be added, renamed or deleted.
- Each column header shows the column name and how many cards are in it.
- An empty column shows the text "No cards yet".
- Inside a column, cards are sorted by creation time, oldest at the top.

## 3. Cards

| Field       | Required | Rules                                  |
|-------------|----------|----------------------------------------|
| Title       | Yes      | 1–100 characters, can't be only spaces |
| Description | No       | Up to 1000 characters                  |

The app also stores these fields (the user never types them):

- `id`: unique number
- `status`: the card's column, one of `todo`, `in_progress`, `done`
- `created_at`: when the card was created

## 4. Features

### 4.1 Add a card

- An "Add card" form sits above the board: Title, Description, and an **Add** button.
- New cards always go into **To Do**.
- If the title is empty or only spaces, show an error and don't create the card.
- After a card is added, the form clears.

### 4.2 Edit a card

- Each card has an **Edit** button.
- Editing lets the user change the title and description, then **Save** or **Cancel**.
- The same rules as "Add a card" apply.

### 4.3 Move a card

- Each card has two arrow buttons:
  - **←** moves the card one column to the left
  - **→** moves the card one column to the right
- In **To Do** the ← button is disabled. In **Done** the → button is disabled.

### 4.4 Delete a card

- Each card has a **Delete** button.
- The app first asks "Delete this card?". The card is removed only if the user confirms.

### 4.5 Loading and errors

- While cards are loading, show "Loading…".
- If the server can't be reached or an action fails, show a short message: "Something went wrong. Please try again."

## 5. API (draft)

All endpoints start with `/api`.

| Method | Path              | What it does                                                   |
|--------|-------------------|----------------------------------------------------------------|
| GET    | `/api/cards`      | List all cards                                                 |
| POST   | `/api/cards`      | Create a card from `title` and `description`; status is `todo` |
| PATCH  | `/api/cards/{id}` | Change `title`, `description` and/or `status`                  |
| DELETE | `/api/cards/{id}` | Delete a card                                                  |

- Invalid data returns `422`.
- A card that doesn't exist returns `404`.

## 6. Tech stack

| Part     | Technology                          | Folder           |
|----------|-------------------------------------|------------------|
| Frontend | React + Vite (JavaScript)           | `frontend/`      |
| Backend  | Python + FastAPI, managed with `uv` | `backend/`       |
| Database | SQLite, accessed through SQLAlchemy | `backend/`       |
| Tests    | pytest                              | `backend/tests/` |

## 7. Not in this version

- Login or user accounts
- More than one board
- Adding, renaming or deleting columns
- Drag and drop
- Reordering cards inside a column
- Due dates, labels, colors or attachments
- Live updates between browsers (other browsers see changes after a refresh)

## 8. Done when

- [ ] I can add a card with a title and an optional description
- [ ] An empty title shows an error
- [ ] I can edit a card's title and description
- [ ] I can move a card left and right with the arrow buttons
- [ ] I can delete a card after confirming
- [ ] Cards are still there after I refresh the page
- [ ] Two browser windows show the same cards (after a refresh)
- [ ] Backend tests pass
