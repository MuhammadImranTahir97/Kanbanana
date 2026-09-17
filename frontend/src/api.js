// Every backend call lives in this file. Right now it's backed by in-memory
// mock data so the app works without a server. When the real backend exists,
// swap the bodies of these functions for `fetch` calls to API_URL and the
// rest of the app won't need to change.

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const MOCK_DELAY_MS = 300

const STATUSES = ['todo', 'in_progress', 'done']

let nextId = 4
let cards = [
  {
    id: 1,
    title: 'Set up the project',
    description: 'Scaffold the frontend and backend folders.',
    status: 'done',
    created_at: '2026-09-14T09:00:00.000Z',
  },
  {
    id: 2,
    title: 'Design the board layout',
    description: 'Three columns: To Do, In Progress, Done.',
    status: 'in_progress',
    created_at: '2026-09-15T10:30:00.000Z',
  },
  {
    id: 3,
    title: 'Write the product spec',
    description: '',
    status: 'todo',
    created_at: '2026-09-16T12:00:00.000Z',
  },
]

function delay() {
  return new Promise((resolve) => setTimeout(resolve, MOCK_DELAY_MS))
}

function clone(card) {
  return { ...card }
}

function validateCardInput({ title, description }) {
  const trimmedTitle = (title ?? '').trim()
  if (trimmedTitle.length === 0) {
    return 'Title is required.'
  }
  if (trimmedTitle.length > 100) {
    return 'Title must be 100 characters or less.'
  }
  if (description && description.length > 1000) {
    return 'Description must be 1000 characters or less.'
  }
  return null
}

export async function getCards() {
  await delay()
  return cards
    .map(clone)
    .sort((a, b) => new Date(a.created_at) - new Date(b.created_at))
}

export async function createCard({ title, description }) {
  await delay()
  const error = validateCardInput({ title, description })
  if (error) {
    throw new Error(error)
  }
  const card = {
    id: nextId++,
    title: title.trim(),
    description: (description ?? '').trim(),
    status: 'todo',
    created_at: new Date().toISOString(),
  }
  cards.push(card)
  return clone(card)
}

export async function updateCard(id, { title, description, status }) {
  await delay()
  const card = cards.find((c) => c.id === id)
  if (!card) {
    throw new Error('Card not found.')
  }
  if (title !== undefined || description !== undefined) {
    const error = validateCardInput({
      title: title ?? card.title,
      description: description ?? card.description,
    })
    if (error) {
      throw new Error(error)
    }
  }
  if (status !== undefined && !STATUSES.includes(status)) {
    throw new Error('Invalid status.')
  }
  if (title !== undefined) card.title = title.trim()
  if (description !== undefined) card.description = description.trim()
  if (status !== undefined) card.status = status
  return clone(card)
}

export async function deleteCard(id) {
  await delay()
  const index = cards.findIndex((c) => c.id === id)
  if (index === -1) {
    throw new Error('Card not found.')
  }
  cards.splice(index, 1)
}
