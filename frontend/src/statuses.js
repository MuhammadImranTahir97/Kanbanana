export const STATUSES = [
  { key: 'todo', label: 'To Do' },
  { key: 'in_progress', label: 'In Progress' },
  { key: 'done', label: 'Done' },
]

export function nextStatus(status) {
  const index = STATUSES.findIndex((s) => s.key === status)
  return index < STATUSES.length - 1 ? STATUSES[index + 1].key : null
}

export function previousStatus(status) {
  const index = STATUSES.findIndex((s) => s.key === status)
  return index > 0 ? STATUSES[index - 1].key : null
}
