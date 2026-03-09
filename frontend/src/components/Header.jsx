export default function Header() {
  return (
    <header style={{ background: '#2D1A00', borderBottom: '1px solid rgba(244,196,48,0.15)' }}>
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span style={{ fontSize: 28 }}>🍌</span>
          <div>
            <h1 style={{
              fontFamily: 'DM Mono',
              fontSize: 14,
              color: '#F4C430',
              letterSpacing: 3,
              textTransform: 'uppercase'
            }}>
              Doceria Famoso
            </h1>
            <p style={{ fontSize: 11, color: 'rgba(255,253,245,0.4)', letterSpacing: 2 }}>
              SISTEMA DE ESTOQUE
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span style={{
            width: 8, height: 8,
            borderRadius: '50%',
            background: '#66BB6A',
            display: 'inline-block',
            boxShadow: '0 0 6px #66BB6A'
          }} />
          <span style={{
            fontSize: 12,
            color: 'rgba(255,253,245,0.4)',
            fontFamily: 'DM Mono'
          }}>
            ao vivo
          </span>
        </div>
      </div>
    </header>
  )
}
