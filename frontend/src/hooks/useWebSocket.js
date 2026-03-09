import { useEffect, useRef } from 'react'

const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000'

export default function useWebSocket(onMessage) {
  const ws = useRef(null)
  const reconnectTimer = useRef(null)

  useEffect(() => {
    function conectar() {
      ws.current = new WebSocket(WS_URL)
      ws.current.onopen = () => {
        console.log('🔌 WebSocket conectado')
        clearTimeout(reconnectTimer.current)
      }
      ws.current.onmessage = (e) => {
        try { onMessage(JSON.parse(e.data)) } catch {}
      }
      ws.current.onclose = () => {
        reconnectTimer.current = setTimeout(conectar, 3000)
      }
      ws.current.onerror = () => ws.current.close()
    }
    conectar()
    return () => {
      clearTimeout(reconnectTimer.current)
      ws.current?.close()
    }
  }, [])
}
