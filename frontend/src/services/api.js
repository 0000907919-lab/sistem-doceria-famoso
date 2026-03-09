import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api'
})

export const getProdutos = async () => (await api.get('/produtos')).data
export const getProduto = async (id) => (await api.get(`/produtos/${id}`)).data
export const criarProduto = async (payload) => (await api.post('/produtos', payload)).data
export const atualizarEstoqueMinimo = async (id, estoque_minimo) =>
  (await api.patch(`/produtos/${id}/estoque-minimo`, { estoque_minimo })).data

export const getMovimentacoes = async (produto_id, limit = 20) =>
  (await api.get('/movimentacoes', { params: { produto_id, limit } })).data
export const registrarMovimentacao = async (payload) =>
  (await api.post('/movimentacoes', payload)).data

export const getLotes = async (produto_id) =>
  (await api.get('/lotes', { params: produto_id ? { produto_id } : {} })).data
export const getLote = async (codigo) => (await api.get(`/lotes/${codigo}`)).data
export const criarLote = async (payload) => (await api.post('/lotes', payload)).data
