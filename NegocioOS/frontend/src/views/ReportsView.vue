<template>
  <div>
    <div class="page-header">
      <h1>Reportes</h1>
      <p>Análisis de ventas e inventario — últimos 30 días</p>
    </div>

    <div class="page-body">
      <!-- KPI Cards -->
      <div class="kpi-grid" v-if="summary">
        <div class="kpi-card">
          <div class="kpi-icon">💰</div>
          <div class="kpi-value">${{ formatNum(summary.total_sales_today) }}</div>
          <div class="kpi-label">Ventas hoy</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">📈</div>
          <div class="kpi-value">${{ formatNum(summary.total_sales_30_days) }}</div>
          <div class="kpi-label">Ventas 30 días</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">🛍️</div>
          <div class="kpi-value">{{ summary.sales_count_30_days }}</div>
          <div class="kpi-label">Transacciones (30 días)</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">📦</div>
          <div class="kpi-value">{{ summary.total_products }}</div>
          <div class="kpi-label">Productos activos</div>
        </div>
        <div class="kpi-card" :class="{ 'kpi-alert': summary.low_stock_count > 0 }">
          <div class="kpi-icon">⚠️</div>
          <div class="kpi-value">{{ summary.low_stock_count }}</div>
          <div class="kpi-label">Stock bajo</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-icon">👥</div>
          <div class="kpi-value">{{ summary.total_customers }}</div>
          <div class="kpi-label">Clientes registrados</div>
        </div>
      </div>

      <div class="charts-grid">
        <!-- Revenue chart -->
        <div class="card chart-card">
          <h3 class="chart-title">💵 Ingresos diarios (últimos 30 días)</h3>
          <div v-if="revenueData.length === 0" class="no-data">Sin datos</div>
          <div v-else class="bar-chart">
            <div
              v-for="day in revenueData"
              :key="day.date"
              class="bar-col"
              :title="`${day.date}: $${day.total}`"
            >
              <div
                class="bar"
                :style="{ height: barHeight(day.total) + '%', minHeight: day.total > 0 ? '4px' : '0' }"
              ></div>
              <div class="bar-label">{{ shortDate(day.date) }}</div>
            </div>
          </div>
        </div>

        <!-- Top products -->
        <div class="card">
          <h3 class="chart-title">🏆 Top 5 Productos</h3>
          <div v-if="topProducts.length === 0" class="no-data">Sin ventas registradas</div>
          <div v-else class="top-list">
            <div v-for="(p, i) in topProducts" :key="p.name" class="top-item">
              <div class="top-rank">#{{ i + 1 }}</div>
              <div class="top-info">
                <div class="top-name">{{ p.name }}</div>
                <div class="top-bar-wrap">
                  <div class="top-bar" :style="{ width: topPct(p.total_qty) + '%' }"></div>
                </div>
              </div>
              <div class="top-stats">
                <div class="top-qty">{{ p.total_qty }} uds</div>
                <div class="top-rev">${{ formatNum(p.total_revenue) }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Payment methods -->
        <div class="card">
          <h3 class="chart-title">💳 Métodos de Pago</h3>
          <div v-if="paymentData.length === 0" class="no-data">Sin ventas</div>
          <div v-else class="payment-list">
            <div v-for="p in paymentData" :key="p.method" class="payment-item">
              <div class="payment-icon">{{ methodIcon(p.method) }}</div>
              <div class="payment-info">
                <div class="payment-label">{{ methodLabel(p.method) }}</div>
                <div class="payment-bar-wrap">
                  <div class="payment-bar" :style="{ width: payPct(p.revenue) + '%', background: methodColor(p.method) }"></div>
                </div>
              </div>
              <div class="payment-stats">
                <div class="payment-count">{{ p.count }} ventas</div>
                <div class="payment-rev">${{ formatNum(p.revenue) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api/index.js'

const summary = ref(null)
const revenueData = ref([])
const topProducts = ref([])
const paymentData = ref([])

const maxRevenue = computed(() => Math.max(...revenueData.value.map(d => d.total), 1))
const maxTopQty = computed(() => Math.max(...topProducts.value.map(p => p.total_qty), 1))
const maxPayRev = computed(() => Math.max(...paymentData.value.map(p => p.revenue), 1))

function barHeight(v) { return Math.max((v / maxRevenue.value) * 100, 0) }
function topPct(v) { return (v / maxTopQty.value) * 100 }
function payPct(v) { return (v / maxPayRev.value) * 100 }

function shortDate(d) {
  const parts = d.split('-')
  return `${parts[2]}/${parts[1]}`
}

function formatNum(n) {
  return Number(n).toLocaleString('es-MX', { minimumFractionDigits: 0, maximumFractionDigits: 0 })
}

function methodLabel(m) {
  return { cash: 'Efectivo', card: 'Tarjeta', transfer: 'Transferencia' }[m] || m
}
function methodIcon(m) {
  return { cash: '💵', card: '💳', transfer: '📲' }[m] || '💰'
}
function methodColor(m) {
  return { cash: '#22c55e', card: '#6366f1', transfer: '#f97316' }[m] || '#f97316'
}

onMounted(async () => {
  const [sumRes, revRes, topRes, payRes] = await Promise.all([
    api.get('/reports/summary'),
    api.get('/reports/revenue'),
    api.get('/reports/top-products'),
    api.get('/reports/payment-methods'),
  ])
  summary.value = sumRes.data
  revenueData.value = revRes.data
  topProducts.value = topRes.data
  paymentData.value = payRes.data
})
</script>

<style scoped>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 14px;
  margin-bottom: 24px;
}

.kpi-card {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 18px;
  text-align: center;
}

.kpi-card.kpi-alert { border-color: var(--warning); background: rgba(245,158,11,0.07); }

.kpi-icon { font-size: 24px; margin-bottom: 8px; }
.kpi-value { font-size: 22px; font-weight: 800; color: var(--primary); }
.kpi-label { font-size: 12px; color: var(--text-muted); margin-top: 4px; }

.charts-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  grid-template-rows: auto auto;
  gap: 20px;
}

.chart-card { grid-column: span 2; }
.chart-title { font-size: 15px; font-weight: 700; margin-bottom: 16px; }
.no-data { text-align: center; padding: 32px; color: var(--text-muted); }

/* Bar chart */
.bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 3px;
  height: 140px;
  padding-bottom: 24px;
  position: relative;
}

.bar-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  position: relative;
}

.bar {
  width: 100%;
  background: linear-gradient(to top, var(--primary), var(--accent));
  border-radius: 3px 3px 0 0;
  transition: height 0.3s;
  cursor: pointer;
}

.bar:hover { opacity: 0.8; }

.bar-label {
  position: absolute;
  bottom: -20px;
  font-size: 9px;
  color: var(--text-muted);
  white-space: nowrap;
  transform: rotate(-45deg);
}

/* Top products */
.top-list { display: flex; flex-direction: column; gap: 14px; }
.top-item { display: flex; align-items: center; gap: 12px; }
.top-rank { font-size: 18px; font-weight: 800; color: var(--primary); min-width: 28px; }
.top-info { flex: 1; }
.top-name { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.top-bar-wrap { background: var(--bg3); border-radius: 4px; height: 6px; overflow: hidden; }
.top-bar { height: 100%; background: linear-gradient(90deg, var(--primary), var(--accent)); border-radius: 4px; transition: width 0.4s; }
.top-stats { text-align: right; }
.top-qty { font-size: 13px; font-weight: 700; }
.top-rev { font-size: 11px; color: var(--success); }

/* Payment methods */
.payment-list { display: flex; flex-direction: column; gap: 16px; }
.payment-item { display: flex; align-items: center; gap: 12px; }
.payment-icon { font-size: 20px; }
.payment-info { flex: 1; }
.payment-label { font-size: 13px; font-weight: 600; margin-bottom: 4px; }
.payment-bar-wrap { background: var(--bg3); border-radius: 4px; height: 6px; overflow: hidden; }
.payment-bar { height: 100%; border-radius: 4px; transition: width 0.4s; }
.payment-stats { text-align: right; }
.payment-count { font-size: 12px; color: var(--text-muted); }
.payment-rev { font-size: 13px; font-weight: 700; color: var(--text); }

@media (max-width: 1000px) {
  .kpi-grid { grid-template-columns: repeat(3, 1fr); }
  .charts-grid { grid-template-columns: 1fr; }
  .chart-card { grid-column: span 1; }
}
</style>
