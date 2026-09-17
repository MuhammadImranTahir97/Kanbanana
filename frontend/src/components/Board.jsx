import Column from './Column.jsx'
import { STATUSES } from '../statuses.js'

export default function Board({ cards, onSave, onMove, onDelete }) {
  return (
    <div className="board">
      {STATUSES.map(({ key, label }) => (
        <Column
          key={key}
          status={key}
          label={label}
          cards={cards.filter((c) => c.status === key)}
          onSave={onSave}
          onMove={onMove}
          onDelete={onDelete}
        />
      ))}
    </div>
  )
}
