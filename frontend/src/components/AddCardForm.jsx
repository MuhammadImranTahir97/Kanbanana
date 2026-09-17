import { useState } from 'react'

export default function AddCardForm({ onAdd }) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

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
      await onAdd({ title, description })
      setTitle('')
      setDescription('')
    } catch {
      setError('Something went wrong. Please try again.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form className="add-card-form" onSubmit={handleSubmit}>
      <div className="add-card-form__fields">
        <input
          type="text"
          placeholder="Card title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          maxLength={100}
          aria-label="Title"
          disabled={isSubmitting}
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          maxLength={1000}
          aria-label="Description"
          disabled={isSubmitting}
        />
        <button type="submit" className="btn btn--primary" disabled={isSubmitting}>
          {isSubmitting ? 'Adding…' : 'Add'}
        </button>
      </div>
      {error && <p className="form-error">{error}</p>}
    </form>
  )
}
