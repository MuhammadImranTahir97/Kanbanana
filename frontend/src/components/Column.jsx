import Card from './Card.jsx'

export default function Column({ status, label, cards, onSave, onMove, onDelete }) {
  return (
    <div className="column">
      <div className="column__header">
        <h2>{label}</h2>
        <span className="column__count">{cards.length}</span>
      </div>
      <div className="column__cards">
        {cards.length === 0 && <p className="column__empty">No cards yet</p>}
        {cards.map((card) => (
          <Card
            key={card.id}
            card={card}
            onSave={onSave}
            onMove={onMove}
            onDelete={onDelete}
            canMoveLeft={status !== 'todo'}
            canMoveRight={status !== 'done'}
          />
        ))}
      </div>
    </div>
  )
}
