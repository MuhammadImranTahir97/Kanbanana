import { useState } from 'react'

export default function Card({ card, onSave, onMove, onDelete, canMoveLeft, canMoveRight }) {
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(card.title)
  const [description, setDescription] = useState(card.description)
  const [error, setError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  function startEditing() {
    setTitle(card.title)
    setDescription(card.description)
    setError(null)
    setIsEditing(true)
  }

  function cancelEditing() {
    setIsEditing(false)
    setError(null)
  }

  async function handleSave() {
    if (title.trim().length === 0) {
      setError('Title is required.')
      return
    }
    if (title.trim().length > 100) {
      setError('Title must be 100 characters or less.')
      return
    }
    if (description.length > 1000) {
      setError('Description must be 1000 characters or less.')
      return
    }

    setError(null)
    setIsSubmitting(true)
    try {
      await onSave(card.id, { title, description })
      setIsEditing(false)
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  async function handleDelete() {
    if (window.confirm('Delete this card?')) {
      try {
        await onDelete(card.id)
      } catch {
        setError('Something went wrong. Please try again.')
      }
    }
  }

  if (isEditing) {
    return (
      <div className="card card--editing">
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={100}
          aria-label="Title"
          disabled={isSubmitting}
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={1000}
          aria-label="Description"
          disabled={isSubmitting}
        />
        {error && <p className="form-error">{error}</p>}
        <div className="card__actions">
          <button type="button" className="btn btn--primary" onClick={handleSave} disabled={isSubmitting}>
            {isSubmitting ? 'Saving…' : 'Save'}
          </button>
          <button type="button" className="btn" onClick={cancelEditing} disabled={isSubmitting}>
            Cancel
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="card__title">{card.title}</h3>
      {card.description && <p className="card__description">{card.description}</p>}
      {error && <p className="form-error">{error}</p>}
      <div className="card__actions">
        <button
          type="button"
          className="btn btn--icon"
          onClick={() => onMove(card.id, 'left')}
          disabled={!canMoveLeft}
          aria-label="Move left"
          title="Move left"
        >
          ←
        </button>
        <button
          type="button"
          className="btn btn--icon"
          onClick={() => onMove(card.id, 'right')}
          disabled={!canMoveRight}
          aria-label="Move right"
          title="Move right"
        >
          →
        </button>
        <button type="button" className="btn" onClick={startEditing}>
          Edit
        </button>
        <button type="button" className="btn btn--danger" onClick={handleDelete}>
          Delete
        </button>
      </div>
    </div>
  )
}
