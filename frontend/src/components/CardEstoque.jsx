const STATUS_COLOR = {
  ok:      '#66BB6A',
  baixo:   '#F4C430',
  critico: '#E8721A',
  zerado:  '#C62828',
}

const STATUS_LABEL = {
  ok:      'Normal',
  baixo:   'Baixo',
  critico: 'Crítico',
  zerado:  'Zerado',
}

export default function CardEstoque({ produto }) {
  const cor = STATUS_COLOR[produto.status] || '#fff'
  const pct = Math.min(
    Math.round((produto.estoque_atual / (produto.estoque_minimo * 2)) * 100),
    100
  )

  return (
    <div style={{
      background: 'rgba(255,253,245,0.04)',
      border: `1px solid ${cor}33`,
      borderTop: `3px solid ${cor}`,
      borderRadius: 8,
      padding: '20px 16px',
      transition: 'all 0.3s ease',
    }}>
      <div className="flex items-center justify-between mb-3">
        <p style={{ fontSize: 12, color: 'rgba(255,253,245,0.5)', fontFamily: 'DM Mono' }}>
          {produto.nome}
        </p>
        <span style={{
          fontSize: 10,
          fontFamily: 'DM Mono',
          color: cor,
          background: `${cor}18`,
          padding: '2px 8px',
          borderRadius: 4,
        }}>
          {STATUS_LABEL[produto.status]}
        </span>
      </div>
      <p style={{
        fontFamily: 'DM Mono',
        fontSize: 36,
        fontWeight: 700,
        color: cor,
        lineHeight: 1,
        marginBottom: 4,
      }}>
        {produto.estoque_atual.toLocaleString('pt-BR')}
      </p>
      <p style={{ fontSize: 11, color: 'rgba(255,253,245,0.3)' }}>
        {produto.unidade} · mín. {produto.estoque_minimo}
      </p>
      <div style={{
        marginTop: 14,
        height: 4,
        background: 'rgba(255,253,245,0.08)',
        borderRadius: 2,
        overflow: 'hidden',
      }}>
        <div style={{
          width: `${pct}%`,
          height: '100%',
          background: cor,
          borderRadius: 2,
          transition: 'w
