<script setup>
import { onMounted, ref } from 'vue'
import AppLayout from '../components/AppLayout.vue'
import { apiStaff, apiCreateStaff, apiRules, apiCreateRule } from '../api/endpoints'

const items = ref([])
const rules = ref([])
const loading = ref(true)
const showForm = ref(false)
const form = ref({ name: '', email: '', phone: '', role: 'professional', color: '#0c1933', bio: '' })
const showRuleForm = ref(null) // staff id si se abre
const ruleForm = ref({ weekday: 1, start_time: '10:00', end_time: '20:00' })
const colors = ['#0c1933', '#1e40af', '#b6892b', '#0891b2', '#059669', '#7c3aed', '#ef4444', '#f59e0b']
const weekdays = ['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']

async function load() {
  loading.value = true
  const [s, r] = await Promise.all([apiStaff(), apiRules()])
  items.value = s; rules.value = r
  loading.value = false
}
onMounted(load)

async function submit() {
  try {
    await apiCreateStaff(form.value)
    showForm.value = false
    form.value = { name: '', email: '', phone: '', role: 'professional', color: '#0c1933', bio: '' }
    await load()
  } catch (e) { alert(e?.response?.data?.detail || e.message) }
}

function rulesFor(sid) { return rules.value.filter(r => r.staff_id === sid) }

async function addRule(sid) {
  try {
    await apiCreateRule({ staff_id: sid, weekday: ruleForm.value.weekday, start_time: ruleForm.value.start_time, end_time: ruleForm.value.end_time })
    showRuleForm.value = null
    await load()
  } catch (e) { alert(e?.response?.data?.detail || e.message) }
}
</script>

<template>
  <AppLayout>
    <div class="page-head">
      <div>
        <h1 class="page-title">Staff</h1>
        <p class="page-subtitle">Quién atiende, con su color y horarios recurrentes.</p>
      </div>
      <button class="btn btn-primary" @click="showForm = true">
        <i class="mdi mdi-plus"></i> Nuevo staff
      </button>
    </div>

    <div v-if="loading" class="muted">Cargando...</div>
    <div v-else class="grid-2">
      <div v-for="s in items" :key="s.id" class="staff-card" :style="{ '--sc': s.color }">
        <div class="staff-row">
          <div class="avatar" :style="{ background: s.color }">{{ s.name.split(' ').map(n=>n[0]).slice(0,2).join('') }}</div>
          <div class="staff-body">
            <div class="staff-name">{{ s.name }}</div>
            <div class="muted" style="font-size:12px;">{{ s.role }} · {{ s.email }}</div>
            <div class="muted" style="font-size:13px;margin-top:6px;" v-if="s.bio">{{ s.bio }}</div>
          </div>
        </div>
        <div class="schedule">
          <div class="schedule-head">
            <span>Horarios</span>
            <button class="btn btn-ghost btn-sm" @click="showRuleForm = s.id">
              <i class="mdi mdi-plus"></i> Agregar
            </button>
          </div>
          <div v-if="!rulesFor(s.id).length" class="muted" style="font-size:12px;">Sin horarios definidos.</div>
          <div v-else class="rules-list">
            <div v-for="r in rulesFor(s.id)" :key="r.id" class="rule-row">
              <span class="wd-chip">{{ weekdays[r.weekday] }}</span>
              <span class="rule-time">{{ r.start_time.slice(0,5) }} – {{ r.end_time.slice(0,5) }}</span>
            </div>
          </div>
          <div v-if="showRuleForm === s.id" class="rule-form">
            <select v-model.number="ruleForm.weekday">
              <option v-for="(wd, i) in weekdays" :value="i" :key="i">{{ wd }}</option>
            </select>
            <input type="time" v-model="ruleForm.start_time">
            <input type="time" v-model="ruleForm.end_time">
            <button class="btn btn-primary btn-sm" @click="addRule(s.id)">Agregar</button>
          </div>
        </div>
      </div>
      <div v-if="!items.length" class="muted" style="grid-column: 1/-1; text-align:center; padding:48px 0;">
        Aún no hay staff.
      </div>
    </div>

    <div v-if="showForm" class="modal-bg" @click.self="showForm = false">
      <div class="modal">
        <div class="modal-head">
          <h3 class="serif" style="font-weight:600;margin:0;color:var(--navy);">Nuevo staff</h3>
          <button class="btn btn-ghost btn-sm" @click="showForm = false"><i class="mdi mdi-close"></i></button>
        </div>
        <form @submit.prevent="submit" class="modal-body">
          <label>Nombre</label><input v-model="form.name" required>
          <div class="grid-2">
            <div><label>Email</label><input v-model="form.email" type="email"></div>
            <div><label>Teléfono</label><input v-model="form.phone"></div>
          </div>
          <label>Rol</label>
          <select v-model="form.role">
            <option value="owner">Dueño</option>
            <option value="manager">Manager</option>
            <option value="professional">Profesional</option>
            <option value="assistant">Asistente</option>
          </select>
          <label>Bio</label>
          <textarea v-model="form.bio" rows="2"></textarea>
          <label>Color</label>
          <div class="color-picker">
            <button v-for="c in colors" :key="c" type="button"
                    :class="['color-swatch', { selected: form.color === c }]"
                    :style="{ background: c }" @click="form.color = c"></button>
          </div>
          <div style="display:flex;gap:10px;margin-top:12px;">
            <button type="submit" class="btn btn-primary">Crear</button>
            <button type="button" class="btn btn-ghost" @click="showForm = false">Cancelar</button>
          </div>
        </form>
      </div>
    </div>
  </AppLayout>
</template>

<style scoped>
.staff-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 22px;
  border-top: 4px solid var(--sc);
}
.staff-row { display: flex; gap: 14px; margin-bottom: 16px; }
.avatar {
  width: 54px; height: 54px; border-radius: 50%;
  display: grid; place-items: center;
  color: var(--cream); font-family: var(--serif);
  font-weight: 700; font-size: 20px; flex-shrink: 0;
}
.staff-name { font-family: var(--serif); font-size: 20px; color: var(--navy); margin-bottom: 2px; font-weight: 600; }
.schedule { border-top: 1px solid var(--line-soft); padding-top: 14px; }
.schedule-head {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 11px; text-transform: uppercase; color: var(--muted);
  letter-spacing: 0.08em; margin-bottom: 10px; font-weight: 600;
}
.rules-list { display: flex; flex-direction: column; gap: 6px; }
.rule-row {
  display: flex; gap: 10px; align-items: center;
  font-size: 13px; color: var(--ink-2);
}
.wd-chip {
  background: var(--navy); color: var(--cream); padding: 3px 9px;
  border-radius: 6px; font-size: 11px; font-weight: 700;
}
.rule-time { font-family: 'SF Mono', ui-monospace, monospace; color: var(--text); }
.rule-form {
  display: grid; grid-template-columns: 1fr 1fr 1fr auto; gap: 6px;
  margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--line-soft);
}
.rule-form input, .rule-form select { padding: 7px 10px; font-size: 13px; }

.modal-bg {
  position: fixed; inset: 0; background: rgba(12,25,51,0.55);
  display: grid; place-items: center; z-index: 95; padding: 20px;
}
.modal {
  background: var(--surface); border-radius: var(--radius);
  padding: 0; max-width: 520px; width: 100%;
  box-shadow: var(--shadow-lg); max-height: 90vh; overflow-y: auto;
}
.modal-head {
  padding: 20px 24px; border-bottom: 1px solid var(--line-soft);
  display: flex; justify-content: space-between; align-items: center;
}
.modal-body { padding: 20px 24px; display: flex; flex-direction: column; gap: 10px; }
label { font-size: 12px; font-weight: 600; color: var(--muted); text-transform: uppercase; letter-spacing: 0.06em; }

.color-picker { display: flex; gap: 8px; flex-wrap: wrap; }
.color-swatch {
  width: 34px; height: 34px; border-radius: 50%;
  border: 2px solid var(--border); cursor: pointer; transition: all .15s;
}
.color-swatch.selected { border-color: var(--navy); transform: scale(1.15); }
</style>
