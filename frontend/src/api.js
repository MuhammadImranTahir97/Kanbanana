// Every backend call lives in this file.

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`)
  }
  if (response.status === 204) {
    return null
  }
  return response.json()
}

export async function getCards() {
  return request('/cards')
}

export async function createCard({ title, description }) {
  return request('/cards', {
    method: 'POST',
    body: JSON.stringify({ title, description }),
  })
}

export async function updateCard(id, { title, description, status }) {
  const body = {}
  if (title !== undefined) body.title = title
  if (description !== undefined) body.description = description
  if (status !== undefined) body.status = status
  return request(`/cards/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  })
}

export async function deleteCard(id) {
  await request(`/cards/${id}`, { method: 'DELETE' })
}
