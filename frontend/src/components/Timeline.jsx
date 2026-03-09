export default function Timeline({ movimentacoes }) {
  if (!movimentacoes.length) return (
    <div style={{
      background: 'rgba(255,253,245,0.03)',
      border: '1px solid rgba(255,253,245,0.06)',
      borderRadius: 8,
      padding: 24,
      textAlign: 'center',
      color: 'rgba(255,253,245,0.3)',
      fontFamily: 'DM Mono',
      fontSize: 13,
    }}>
      Nenhuma movimentação registrada ainda.
    </div>
  )

  return (
    <div style={{
      background: 'rgba(255,253,245,0.03)',
      border: '1px solid rgba(255,253,245,0.06)',
      borderRadius: 8,
      padding: '8px 0',
    }}>
      {movimentacoes.map((m, i) => (
        <div key={m.id} style={{
          display: 'flex',
          alignItems: 'center',
          gap: 16,
          padding: '14px 24px',
          borderBottom: i < movimentacoes.length - 1
            ? '1px solid rgba(255,253,245,0.04)' : 'none',
        }}>
          <div style={{
            width: 10, height: 10,
            borderRadius: '50%',
            background: m.tipo === 'entrada' ? '#66BB6A' : '#E8721A',
            flexShrink: 0,
          }} />
          <span style={{
            fontFamily: 'DM Mono',
            fontSize: 11,
            color: 'rgba(255,253,245,0.3)',
            minWidth: 44,
          }}>
            {new Date(m.created_at).toLocaleTimeString('pt-BR', {
              hour: '2-digit', minute: '2-digit'
            })}
          </span>
          <span style={{ fontSize: 13, color: 'rgba(255,253,245,0.75)', flex: 1 }}>
            {m.tipo === 'entrada' ? '📦' : '🚚'}
            {' '}<strong style={{ color: '#FFFDF5' }}>{m.produto}</strong>
            {' — '}{m.tipo} de{' '}
            <strong style={{ color: m.tipo === 'entrada' ? '#66BB6A' : '#E8721A' }}>
              {m.quantidade} cx
            </strong>
          </span>
          <span style={{
            fontFamily: 'DM Mono',
            fontSize: 10,
            color: m.origem === 'mqtt' ? '#42A5F5' : '#F4C430',
            background: m.origem === 'mqtt' ? '#42A5F518' : '#F4C43018',
            padding: '2px 8px',
            borderRadius: 4,
          }}>
            {m.origem === 'mqtt' ? 'Sensor' : 'Manual'}
          </span>
        </div>
      ))}
    </div>
  )
}
