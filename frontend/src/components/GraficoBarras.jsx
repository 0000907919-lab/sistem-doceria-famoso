import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts'

const CORES = ['#F4C430', '#E8721A', '#8BC34A', '#42A5F5']

const TooltipCustom = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: '#2D1A00',
      border: '1px solid rgba(244,196,48,0.2)',
      borderRadius: 6,
      padding: '10px 14px',
      fontFamily: 'DM Mono',
      fontSize: 12,
    }}>
      <p style={{ color: '#F4C430', marginBottom: 4 }}>{label}</p>
      <p style={{ color: '#FFFDF5' }}>
        Estoque: <strong>{payload[0].value}</strong> cx
      </p>
      <p style={{ color: 'rgba(255,253,245,0.4)' }}>
        Mínimo: {payload[0].payload.estoque_minimo} cx
      </p>
    </div>
  )
}

export default function GraficoBarras({ produtos }) {
  if (!produtos.length) return null
  return (
    <div style={{
      background: 'rgba(255,253,245,0.03)',
      border: '1px solid rgba(255,253,245,0.06)',
      borderRadius: 8,
      padding: '24px 16px',
    }}>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={produtos} barCategoryGap="30%">
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,253,245,0.05)"
            vertical={false}
          />
          <XAxis
            dataKey="nome"
            tick={{ fill: 'rgba(255,253,245,0.4)', fontSize: 11, fontFamily: 'DM Mono' }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: 'rgba(255,253,245,0.4)', fontSize: 11, fontFamily: 'DM Mono' }}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip content={<TooltipCustom />} cursor={{ fill: 'rgba(255,253,245,0.03)' }} />
          <Bar dataKey="estoque_atual" radius={[4, 4, 0, 0]}>
            {produtos.map((p, i) => (
              <Cell key={p.id} fill={CORES[i % CORES.length]} />
            ))}
          </Bar>
