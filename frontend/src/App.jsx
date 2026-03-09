import { useEffect, useState } from 'react'
import Header from './components/Header'
import CardEstoque from './components/CardEstoque'
import GraficoBarras from './components/GraficoBarras'
import Timeline from './components/Timeline'
import AlertaBadge from './components/AlertaBadge'
import useWebSocket from './hooks/useWebSocket'
import { getProdutos, getMovimentacoes } from './services/api'

export default function App() {
  const [produtos, setProdutos] = useState([])
  const [movimentacoes, setMovimentacoes] = useState([])
  const [alertas, setAlertas] = useState([])

  useEffect(() => {
    getProdutos().then(setProdutos)
    getMovimentacoes().then(setMovimentacoes)
  }, [])

  useWebSocket((msg) => {
    if (msg.tipo === 'estoque_atualizado') {
      setProdutos(prev => prev.map(p => p.id === msg.produto.id ? msg.produto : p))
      if (['critico', 'zerado'].includes(msg.produto.status))
        setAlertas(prev => [msg.produto, ...prev].slice(0, 5))
    }
    if (msg.tipo === 'lote_criado') getMovimentacoes().then(setMovimentacoes)
  })

  return (
    <div className="min-h-screen" style={{ background: '#1A0F00' }}>
      <Header />
      <main className="max-w-6xl mx-auto px-6 py-10 space-y-10">
        {alertas.length > 0 && (
          <div className="space-y-2">
            {alertas.map((a, i) => (
              <AlertaBadge key={i} produto={a} onClose={() =>
                setAlertas(prev => prev.filter((_, idx) => idx !== i))
              } />
            ))}
          </div>
        )}
        <section>
          <p className="text-xs tracking-widest uppercase mb-4"
            style={{ color: '#F4C430', fontFamily: 'DM Mono' }}>
            Estoque em tempo real
          </p>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {produtos.map(p => <CardEstoque key={p.id} produto={p} />)}
          </div>
        </section>
        <section>
          <p className="text-xs tracking-widest uppercase mb-4"
            style={{ color: '#F4C430', fontFamily: 'DM Mono' }}>
            Comparativo de estoque
          </p>
          <GraficoBarras produtos={produtos} />
        </section>
        <section>
          <p className="text-xs tracking-widest uppercase mb-4"
            style={{ color: '#F4C430', fontFamily: 'DM Mono' }}>
            Atividade recente
          </p>
          <Timeline movimentacoes={movimentacoes} />
        </section>
      </main>
    </div>
  )
}
