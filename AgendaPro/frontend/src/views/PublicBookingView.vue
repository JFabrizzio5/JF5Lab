<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { pubTenant, pubAvailability, pubBook } from '../api/endpoints'

const route = useRoute()
const slug = computed(() => route.params.slug)

const tenant = ref(null)
const loading = ref(true)
const error = ref('')

// Flow state
const step = ref(1) // 1=service 2=date 3=slot 4=customer 5=review
const selectedService = ref(null)
const selectedStaff = ref(null)
const selectedDate = ref(null)
const selectedSlot = ref(null)
const slots = ref([])
const slotsLoading = ref(false)
const customer = ref({ name: '', phone: '', email: '' })
const booking = ref(null)
const bookError = ref('')
const bookLoading = ref(false)

function fmtMoney(n) { return '$' + Number(n||0).toLocaleString('es-MX') }
function fmtTime(iso) { return new Date(iso).toLocaleTimeString('es-MX', { hour: '2-digit', minute: '2-digit', hour12: false }) }

onMounted(async () => {
  try {
    tenant.value = await pubTenant(slug.value)
    // set brand color as CSS var dynamic
    document.documentElement.style.setProperty('--brand', tenant.value.brand_color || '#0c1933')
  } catch (e) {
    error.value = e?.response?.status === 404 ? 'Negocio no encontrado' : (e?.message || 'Error')
  } finally { loading.value = false }
})

const weekDays = computed(() => {
  const out = []
  const base = new Date(); base.setHours(0,0,0,0)
  for (let i = 0; i < 14; i++) {
    const d = new Date(base); d.setDate(d.getDate() + i)
    out.push(d)
  }
  return out
})

function pickService(svc) {
  selectedService.value = svc
  selectedStaff.value = null
  selectedDate.value = null
  selectedSlot.value = null
  step.value = 2
}

async function pickDate(d) {
  selectedDate.value = d
  selectedSlot.value = null
  step.value = 3
  slotsLoading.value = true
  try {
    const r = await pubAvailability(slug.value, {
      service_id: selectedService.value.id,
      date: d.toISOString().split('T')[0],
      staff_id: selectedStaff.value || undefined,
    })
    slots.value = (r[0]?.slots || [])
  } finally { slotsLoading.value = false }
}

function pickSlot(s) {
  selectedSlot.value = s
  step.value = 4
}

async function submit() {
  bookError.value = ''; bookLoading.value = true
  try {
    const r = await pubBook(slug.value, {
      service_id: selectedService.value.id,
      staff_id: selectedSlot.value.staff_id,
      starts_at: selectedSlot.value.starts_at,
      customer: customer.value,
    })
    booking.value = r
    if (r.checkout_url) {
      // redirigir a checkout
      setTimeout(() => { window.location.href = r.checkout_url }, 800)
    } else {
      step.value = 5
    }
  } catch (e) {
    bookError.value = e?.response?.data?.detail || e.message
  } finally { bookLoading.value = false }
}

function reset() {
  step.value = 1
  selectedService.value = selectedDate.value = selectedSlot.value = null
  selectedStaff.value = null
  booking.value = null
  customer.value = { name: '', phone: '', email: '' }
}
</script>

<template>
  <div class="pub-shell" v-if="tenant">
    <div class="pub-header" :style="{ background: tenant.brand_color }">
      <h1>{{ tenant.name }}</h1>
      <div class="tagline" v-if="tenant.tagline">{{ tenant.tagline }}</div>
      <div class="pub-meta">
        <span v-if="tenant.city"><i class="mdi mdi-map-marker-outline"></i> {{ tenant.city }}</span>
        <span v-if="tenant.instagram"><i class="mdi mdi-instagram"></i> {{ tenant.instagram }}</span>
      </div>
    </div>

    <div class="pub-body">
      <div class="pub-card">
        <div class="steps">
          <div :class="['step', { active: step >= 1, done: step > 1 }]">1 · Servicio</div>
          <div :class="['step', { active: step >= 2, done: step > 2 }]">2 · Fecha</div>
          <div :class="['step', { active: step >= 3, done: step > 3 }]">3 · Hora</div>
          <div :class="['step', { active: step >= 4, done: step > 4 }]">4 · Tus datos</div>
        </div>

        <!-- Step 1: Service -->
        <div v-if="step === 1">
          <h2 class="step-title">Elige el servicio</h2>
          <div class="svc-list">
            <button v-for="s in tenant.services" :key="s.id" class="svc-opt" @click="pickService(s)"
                    :style="{ '--c': s.color }">
              <div>
                <div class="svc-opt-name">{{ s.name }}</div>
                <div class="svc-opt-meta">{{ s.duration_minutes }} min{{ s.requires_prepay ? ' · depósito requerido' : '' }}</div>
                <div class="muted" style="font-size:12px;margin-top:4px;" v-if="s.description">{{ s.description }}</div>
              </div>
              <div class="svc-opt-price">{{ fmtMoney(s.price_mxn) }}</div>
            </button>
          </div>
        </div>

        <!-- Step 2: Date + staff -->
        <div v-if="step === 2">
          <button class="back-btn" @click="step = 1"><i class="mdi mdi-arrow-left"></i> Cambiar servicio</button>
          <h2 class="step-title">¿Con quién quieres?</h2>
          <div class="staff-pick">
            <button :class="['staff-opt', { sel: !selectedStaff }]" @click="selectedStaff = null">
              <i class="mdi mdi-account-multiple-outline"></i> Cualquiera
            </button>
            <button v-for="st in tenant.staff" :key="st.id"
                    :class="['staff-opt', { sel: selectedStaff === st.id }]"
                    @click="selectedStaff = st.id"
                    :style="{ '--c': st.color }">
              <span class="dot" :style="{ background: st.color }"></span>
              {{ st.name }}
            </button>
          </div>

          <h2 class="step-title" style="margin-top:28px;">¿Qué día?</h2>
          <div class="days">
            <button v-for="d in weekDays" :key="d.toISOString()" class="day-btn" @click="pickDate(d)">
              <div class="day-wd">{{ d.toLocaleDateString('es-MX', { weekday: 'short' }) }}</div>
              <div class="day-n">{{ d.getDate() }}</div>
              <div class="day-m">{{ d.toLocaleDateString('es-MX', { month: 'short' }) }}</div>
            </button>
          </div>
        </div>

        <!-- Step 3: slot -->
        <div v-if="step === 3">
          <button class="back-btn" @click="step = 2"><i class="mdi mdi-arrow-left"></i> Cambiar fecha</button>
          <h2 class="step-title">{{ selectedDate.toLocaleDateString('es-MX', { weekday:'long', day:'numeric', month:'long' }) }}</h2>
          <div v-if="slotsLoading" class="muted" style="padding:20px 0;">Buscando horarios...</div>
          <div v-else-if="!slots.length" class="muted" style="padding:20px 0;">Sin horarios disponibles este día.</div>
          <div v-else class="slots-grid">
            <button v-for="s in slots" :key="s.starts_at + s.staff_id"
                    class="slot-btn" @click="pickSlot(s)">
              <div class="slot-time">{{ fmtTime(s.starts_at) }}</div>
              <div class="slot-staff">con {{ s.staff_name.split(' ')[0] }}</div>
            </button>
          </div>
        </div>

        <!-- Step 4: customer form -->
        <div v-if="step === 4">
          <button class="back-btn" @click="step = 3"><i class="mdi mdi-arrow-left"></i> Cambiar hora</button>
          <h2 class="step-title">Tus datos</h2>
          <div class="summary">
            <div><strong>{{ selectedService.name }}</strong> · {{ fmtMoney(selectedService.price_mxn) }}</div>
            <div class="muted">{{ selectedDate.toLocaleDateString('es-MX', { weekday:'long', day:'numeric', month:'long' }) }} · {{ fmtTime(selectedSlot.starts_at) }} · con {{ selectedSlot.staff_name }}</div>
          </div>

          <form @submit.prevent="submit" class="form">
            <div>
              <label>Tu nombre completo</label>
              <input v-model="customer.name" required placeholder="Ej. Ana Ramírez">
            </div>
            <div>
              <label>WhatsApp (con lada)</label>
              <input v-model="customer.phone" required placeholder="+525555123456">
            </div>
            <div>
              <label>Email (opcional)</label>
              <input v-model="customer.email" type="email" placeholder="ana@ejemplo.com">
            </div>
            <div v-if="selectedService.requires_prepay" class="deposit-box">
              <i class="mdi mdi-credit-card-outline"></i>
              <div>
                <strong>Depósito: {{ fmtMoney(selectedService.deposit_mxn || selectedService.price_mxn) }}</strong>
                <div class="muted" style="font-size:12px;">Te redirigimos a la pasarela de pago.</div>
              </div>
            </div>
            <button class="btn btn-primary btn-big" :disabled="bookLoading">
              <i class="mdi mdi-check"></i>
              <span v-if="bookLoading">Reservando...</span>
              <span v-else>
                {{ selectedService.requires_prepay ? 'Pagar y reservar' : 'Confirmar reserva' }}
              </span>
            </button>
            <div v-if="bookError" class="err">{{ bookError }}</div>
          </form>
        </div>

        <!-- Step 5: success (without prepay) -->
        <div v-if="step === 5" class="success-step">
          <div class="success-icon"><i class="mdi mdi-check-circle-outline"></i></div>
          <h2 class="serif" style="font-weight:600;color:var(--navy);font-size:28px;">¡Listo, {{ customer.name.split(' ')[0] }}!</h2>
          <p class="muted">Tu cita está confirmada. Te enviaremos un WhatsApp con el recordatorio.</p>
          <div class="summary" style="margin-top:18px;">
            <div><strong>{{ selectedService.name }}</strong></div>
            <div class="muted">{{ selectedDate.toLocaleDateString('es-MX', { weekday:'long', day:'numeric', month:'long' }) }} · {{ fmtTime(selectedSlot.starts_at) }}</div>
          </div>
          <button class="btn btn-ghost" @click="reset" style="margin-top:24px;">
            <i class="mdi mdi-calendar-plus"></i> Hacer otra reserva
          </button>
        </div>
      </div>

      <div v-if="tenant.about" class="about">
        <h3 class="serif" style="font-weight:600;color:var(--navy);">Sobre {{ tenant.name }}</h3>
        <p>{{ tenant.about }}</p>
      </div>

      <div class="foot">
        Powered by <strong class="serif italic">AgendaPro</strong>
      </div>
    </div>
  </div>

  <div v-else-if="loading" class="loader">
    <i class="mdi mdi-loading mdi-spin"></i> Cargando...
  </div>
  <div v-else-if="error" class="loader">
    <i class="mdi mdi-alert-circle-outline"></i> {{ error }}
  </div>
</template>

<style scoped>
.pub-header {
  background: #0c1933;
}
.pub-meta {
  display: flex; gap: 16px; justify-content: center; margin-top: 14px;
  color: rgba(253,251,245,0.7); font-size: 13px;
}
.pub-meta .mdi { margin-right: 4px; }

.steps {
  display: flex; gap: 8px; margin-bottom: 28px;
  padding-bottom: 18px; border-bottom: 1px solid var(--line-soft);
  flex-wrap: wrap;
}
.step {
  font-size: 12px; color: var(--muted); font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.06em;
  padding: 4px 10px; border-radius: 6px;
}
.step.active { color: var(--navy); background: var(--cream-2); }
.step.done { color: var(--success); }

.step-title {
  font-family: var(--serif); font-size: 26px;
  color: var(--navy); margin: 0 0 20px; font-weight: 600;
  letter-spacing: -0.01em;
}

.svc-list { display: flex; flex-direction: column; gap: 10px; }
.svc-opt {
  display: flex; justify-content: space-between; align-items: center; gap: 18px;
  background: var(--surface); border: 1.5px solid var(--border);
  border-left: 4px solid var(--c, var(--navy));
  border-radius: var(--radius); padding: 18px 22px;
  text-align: left; cursor: pointer; transition: all .18s;
  font-family: inherit; width: 100%;
}
.svc-opt:hover { border-color: var(--navy); transform: translateY(-2px); box-shadow: var(--shadow-md); }
.svc-opt-name { font-family: var(--serif); font-size: 19px; color: var(--navy); font-weight: 600; }
.svc-opt-meta { font-size: 12px; color: var(--muted); margin-top: 2px; }
.svc-opt-price { font-family: var(--serif); font-size: 24px; color: var(--navy); font-weight: 600; letter-spacing: -0.02em; flex-shrink: 0; }

.staff-pick { display: flex; flex-wrap: wrap; gap: 8px; }
.staff-opt {
  display: inline-flex; align-items: center; gap: 8px;
  padding: 10px 16px; border-radius: 999px;
  border: 1.5px solid var(--border); background: var(--surface);
  color: var(--ink-2); font-size: 14px; font-weight: 500; cursor: pointer;
  font-family: inherit; transition: all .15s;
}
.staff-opt:hover { border-color: var(--navy); }
.staff-opt.sel { background: var(--navy); color: var(--cream); border-color: var(--navy); }
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--navy); }

.days {
  display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px;
}
.day-btn {
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--radius-sm); padding: 12px 8px; text-align: center;
  cursor: pointer; transition: all .15s; font-family: inherit;
}
.day-btn:hover { border-color: var(--navy); background: var(--cream-2); }
.day-wd { font-size: 10px; text-transform: uppercase; color: var(--muted); letter-spacing: 0.08em; font-weight: 700; }
.day-n { font-family: var(--serif); font-size: 22px; color: var(--navy); font-weight: 600; }
.day-m { font-size: 10px; color: var(--muted); text-transform: uppercase; }

.slots-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 8px; }
.slot-btn {
  background: var(--surface); border: 1.5px solid var(--border);
  border-radius: var(--radius-sm); padding: 12px; text-align: center;
  cursor: pointer; transition: all .15s; font-family: inherit;
}
.slot-btn:hover { border-color: var(--gold); background: rgba(182,137,43,.06); transform: translateY(-2px); }
.slot-time { font-family: var(--serif); font-size: 20px; color: var(--navy); font-weight: 600; }
.slot-staff { font-size: 11px; color: var(--muted); }

.back-btn {
  background: transparent; border: none; color: var(--muted);
  font-size: 13px; cursor: pointer; margin-bottom: 14px; padding: 4px 0;
  font-family: inherit;
}
.back-btn:hover { color: var(--navy); }

.summary {
  background: var(--cream-2); padding: 14px 16px;
  border-radius: var(--radius-sm); margin-bottom: 20px;
  border-left: 4px solid var(--gold);
}

.form { display: flex; flex-direction: column; gap: 14px; }
.form label { font-size: 12px; color: var(--muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; display: block; margin-bottom: 5px; }
.deposit-box {
  display: flex; gap: 12px; align-items: center;
  background: var(--cream-2); padding: 14px 16px;
  border-radius: var(--radius-sm); border: 1px solid var(--line-soft);
}
.deposit-box .mdi { font-size: 32px; color: var(--gold); }
.btn-big { padding: 14px 24px; font-size: 15px; justify-content: center; }
.err { color: var(--danger); font-size: 13px; }

.success-step { text-align: center; padding: 12px 0; }
.success-icon {
  width: 72px; height: 72px; border-radius: 50%;
  background: var(--success); color: var(--cream);
  display: grid; place-items: center; font-size: 44px; margin: 0 auto 20px;
}

.about {
  margin-top: 28px; padding: 28px;
  background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius);
}
.about h3 { margin: 0 0 10px; font-size: 20px; }
.about p { margin: 0; color: var(--ink-2); line-height: 1.7; }

.foot { text-align: center; color: var(--muted); font-size: 12px; margin-top: 32px; }
.foot strong { color: var(--navy); }

.loader {
  min-height: 100vh; display: grid; place-items: center;
  color: var(--muted); font-size: 16px; background: var(--cream);
}
.mdi-spin { animation: spin 1s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

@media (max-width: 600px) {
  .days { grid-template-columns: repeat(4, 1fr); }
  .step-title { font-size: 22px; }
}
</style>
