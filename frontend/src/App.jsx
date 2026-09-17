import { useEffect, useState } from 'react'
import { getCards, createCard, updateCard, deleteCard } from './api.js'
import { nextStatus, previousStatus } from './statuses.js'
import AddCardForm from './components/AddCardForm.jsx'
import Board from './components/Board.jsx'
import './App.css'

const GENERIC_ERROR = 'Something went wrong. Please try again.'

function App() {
  const [cards, setCards] = useState([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    setIsLoading(true)
    getCards()
      .then((data) => {
        if (!cancelled) setCards(data)
      })
      .catch(() => {
        if (!cancelled) setError(GENERIC_ERROR)
      })
      .finally(() => {
        if (!cancelled) setIsLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [])

  async function handleAdd({ title, description }) {
    const card = await createCard({ title, description })
    setError(null)
    setCards((prev) => [...prev, card])
  }

  async function handleSave(id, { title, description }) {
    const updated = await updateCard(id, { title, description })
    setError(null)
    setCards((prev) => prev.map((c) => (c.id === id ? updated : c)))
  }

  async function handleMove(id, direction) {
    const card = cards.find((c) => c.id === id)
    if (!card) return
    const newStatus = direction === 'left' ? previousStatus(card.status) : nextStatus(card.status)
    if (!newStatus) return
    try {
      const updated = await updateCard(id, { status: newStatus })
      setError(null)
      setCards((prev) => prev.map((c) => (c.id === id ? updated : c)))
    } catch {
      setError(GENERIC_ERROR)
    }
  }

  async function handleDelete(id) {
    await deleteCard(id)
    setError(null)
    setCards((prev) => prev.filter((c) => c.id !== id))
  }

  return (
    <div className="app">
      <header className="app__header">
        <h1>Kanbanana 🍌</h1>
        <p className="app__subtitle">Add a card, then move it across the board as you work.</p>
      </header>

      <AddCardForm onAdd={handleAdd} />

      {error && <p className="banner banner--error">{error}</p>}

      {isLoading ? (
        <p className="banner">Loading…</p>
      ) : (
        <Board cards={cards} onSave={handleSave} onMove={handleMove} onDelete={handleDelete} />
      )}
    </div>
  )
}

export default App
