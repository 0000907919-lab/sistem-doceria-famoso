export default function AlertaBadge({ produto, onClose }) {
  const cor = produto.status === 'zerado' ? '#C62828' : '#E8721A'

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      background: `${cor}15`,
      border: `1px solid ${cor}55`,
      borderLeft: `4px solid ${cor}`,
      borderRadius: 8,
      padding: '12px 20px',
    }}>
      <div className="flex items-center gap-3">
        <span style={{ fontSize: 20 }}>⚠️</span>
        <div>
          <p style={{ fontSize: 13, fontWeight: 600, color: '#FFFDF5' }}>
            {produto.status === 'zerado' ? 'Estoque zerado' : 'Estoque crítico'} — {produto.nome}
          </p>
          <p style={{
            fontSize: 11,
            color: 'rgba(255,253,245,0.4)',
            fontFamily: 'DM Mono',
            marginTop: 2,
          }}>
            Atual: {produto.estoque_atual} {produto.unidade} · 
            Mínimo: {produto.estoque_minimo} {produto.unidade}
          </p>
        </div>
      </div>
      <button
        onClick={onClose}
        style={{
          background: 'none',
          border: 'none',
          color: 'rgba(255,253,245,0.3)',
          fontSize: 18,
          cursor: 'pointer',
          padding: '0 4px',
        }}
      >
        ×
      </button>
    </div>
  )
}
