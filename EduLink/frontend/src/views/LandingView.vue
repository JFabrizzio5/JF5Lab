<template>
  <div class="landing">
    <!-- Navbar -->
    <nav class="land-nav">
      <div class="nav-brand">🎓 EduLink</div>
      <div class="nav-links">
        <RouterLink to="/login" class="btn btn-ghost">Iniciar Sesión</RouterLink>
        <RouterLink to="/register" class="btn btn-primary">Registrarse</RouterLink>
      </div>
    </nav>

    <!-- Hero -->
    <section class="hero">
      <div class="hero-content">
        <div class="hero-badge">🏫 Para Universidades Mexicanas</div>
        <h1 class="hero-title">
          El <span class="highlight">YouTube</span> de
          <br />Cursos Universitarios
        </h1>
        <p class="hero-subtitle">
          Aprende con tutores de tu universidad. Clases grabadas, sesiones en vivo
          y tutorías personalizadas para UAM, UNAM, POLI, IPN, ITESM y más.
        </p>

        <!-- Category chips -->
        <div class="category-chips">
          <span v-for="cat in categories" :key="cat.name" class="chip">
            {{ cat.emoji }} {{ cat.name }}
          </span>
        </div>

        <!-- Demo buttons -->
        <div class="demo-section">
          <p class="demo-label">Acceso demo rápido (contraseña: demo123)</p>
          <div class="demo-btns">
            <button @click="demoLogin('alumno@edulink.mx')" class="demo-btn student" :disabled="loading">
              <span>👩‍🎓</span>
              <div>
                <div class="demo-role">Estudiante</div>
                <div class="demo-email">alumno@edulink.mx</div>
              </div>
            </button>
            <button @click="demoLogin('tutor@edulink.mx')" class="demo-btn tutor" :disabled="loading">
              <span>👨‍🏫</span>
              <div>
                <div class="demo-role">Tutor</div>
                <div class="demo-email">tutor@edulink.mx</div>
              </div>
            </button>
            <button @click="demoLogin('admin@edulink.mx')" class="demo-btn admin" :disabled="loading">
              <span>⚙️</span>
              <div>
                <div class="demo-role">Administrador</div>
                <div class="demo-email">admin@edulink.mx</div>
              </div>
            </button>
          </div>
          <p v-if="error" class="alert alert-error">{{ error }}</p>
        </div>
      </div>

      <div class="hero-visual">
        <div class="video-mockup">
          <div class="video-player">
            <div class="play-circle">▶</div>
          </div>
          <div class="course-info-mock">
            <div class="mock-title">Cálculo Diferencial</div>
            <div class="mock-meta">Prof. Carlos Mendoza · UNAM</div>
            <div class="mock-progress">
              <div class="prog-bar"><div class="prog-fill" style="width:65%"></div></div>
              <span>65% completado</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features -->
    <section class="features">
      <h2>Todo lo que necesitas para aprender</h2>
      <div class="features-grid">
        <div class="feature-card" v-for="f in features" :key="f.title">
          <div class="feature-icon">{{ f.icon }}</div>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- Schools -->
    <section class="schools">
      <h2>Universidades afiliadas</h2>
      <div class="schools-grid">
        <div v-for="s in schools" :key="s" class="school-badge">{{ s }}</div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="land-footer">
      <p>🎓 EduLink &copy; 2024 — El YouTube de cursos universitarios</p>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth.js'

const auth = useAuthStore()
const router = useRouter()
const loading = ref(false)
const error = ref('')

const categories = [
  { name: 'Matemáticas', emoji: '📐' },
  { name: 'Física', emoji: '⚡' },
  { name: 'Química', emoji: '🧪' },
  { name: 'Programación', emoji: '💻' },
  { name: 'Historia', emoji: '📜' },
  { name: 'Inglés', emoji: '🌎' },
  { name: 'Biología', emoji: '🔬' },
  { name: 'Economía', emoji: '📈' },
]

const features = [
  { icon: '🎬', title: 'Video Lecciones', desc: 'Aprende con videos explicativos de YouTube integrados directamente en la plataforma.' },
  { icon: '🏫', title: 'Por Escuela', desc: 'Cursos exclusivos para tu universidad. Conecta con compañeros y tutores de tu plantel.' },
  { icon: '📅', title: 'Tutorías 1:1', desc: 'Reserva sesiones personalizadas con tutores de tu escuela en los horarios que prefieras.' },
  { icon: '⭐', title: 'Reseñas', desc: 'Lee opiniones de otros estudiantes y elige los mejores cursos para tu carrera.' },
  { icon: '📊', title: 'Progreso', desc: 'Sigue tu avance en cada curso y mantén el ritmo de aprendizaje que necesitas.' },
  { icon: '🆓', title: 'Gratis y Premium', desc: 'Accede a cursos gratuitos o paga por contenido premium de alta calidad.' },
]

const schools = ['UAM', 'UNAM', 'POLI', 'IPN', 'ITESM', 'OTHER']

async function demoLogin(email) {
  loading.value = true
  error.value = ''
  try {
    const data = await auth.login(email, 'demo123')
    const role = data.user.role
    if (role === 'admin') router.push('/admin')
    else if (role === 'tutor') router.push('/tutor/dashboard')
    else router.push('/courses')
  } catch (e) {
    error.value = 'Error al iniciar sesión. Verifica que el backend esté corriendo.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.landing { min-height: 100vh; background: var(--bg); }

.land-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 40px;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  z-index: 10;
}
.nav-brand { font-size: 22px; font-weight: 800; color: var(--primary); }
.nav-links { display: flex; gap: 12px; }

.hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  padding: 80px 40px;
  max-width: 1200px;
  margin: 0 auto;
  align-items: center;
}

.hero-badge {
  display: inline-block;
  background: rgba(245,158,11,0.15);
  color: var(--primary);
  border: 1px solid rgba(245,158,11,0.3);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 20px;
}

.hero-title {
  font-size: 52px;
  font-weight: 900;
  line-height: 1.1;
  margin-bottom: 20px;
}
.highlight {
  background: linear-gradient(135deg, var(--primary), #ef4444);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-subtitle {
  font-size: 17px;
  color: var(--text2);
  line-height: 1.7;
  margin-bottom: 28px;
}

.category-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 36px;
}
.chip {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px 14px;
  font-size: 13px;
  color: var(--text2);
}

.demo-section { background: var(--bg2); border: 1px solid var(--border); border-radius: 16px; padding: 24px; }
.demo-label { font-size: 13px; color: var(--text2); margin-bottom: 14px; text-align: center; }
.demo-btns { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.demo-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px;
  border-radius: 10px;
  border: 1px solid var(--border);
  background: var(--bg3);
  color: var(--text);
  font-size: 12px;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s;
}
.demo-btn:hover:not(:disabled) { border-color: var(--primary); background: rgba(245,158,11,0.1); }
.demo-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.demo-btn span { font-size: 24px; }
.demo-role { font-weight: 700; font-size: 13px; }
.demo-email { font-size: 11px; color: var(--text2); }
.demo-btn.student { border-color: rgba(99,102,241,0.4); }
.demo-btn.tutor { border-color: rgba(16,185,129,0.4); }
.demo-btn.admin { border-color: rgba(245,158,11,0.4); }

/* Hero visual */
.hero-visual { display: flex; justify-content: center; }
.video-mockup {
  background: var(--bg2);
  border: 1px solid var(--border);
  border-radius: 16px;
  overflow: hidden;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.video-player {
  background: linear-gradient(135deg, #1e1b4b, #312e81);
  aspect-ratio: 16/9;
  display: flex;
  align-items: center;
  justify-content: center;
}
.play-circle {
  width: 60px;
  height: 60px;
  background: rgba(245,158,11,0.9);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  color: #0f172a;
  padding-left: 4px;
}
.course-info-mock { padding: 16px; }
.mock-title { font-weight: 700; font-size: 15px; margin-bottom: 4px; }
.mock-meta { font-size: 12px; color: var(--text2); margin-bottom: 12px; }
.mock-progress { display: flex; align-items: center; gap: 10px; }
.prog-bar { flex: 1; height: 6px; background: var(--bg3); border-radius: 3px; }
.prog-fill { height: 100%; background: var(--primary); border-radius: 3px; }
.mock-progress span { font-size: 12px; color: var(--text2); white-space: nowrap; }

/* Features */
.features { padding: 80px 40px; background: var(--bg2); }
.features h2 { text-align: center; font-size: 32px; font-weight: 800; margin-bottom: 48px; }
.features-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; max-width: 1100px; margin: 0 auto; }
.feature-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  transition: border-color 0.2s;
}
.feature-card:hover { border-color: var(--primary); }
.feature-icon { font-size: 32px; margin-bottom: 12px; }
.feature-card h3 { font-size: 16px; font-weight: 700; margin-bottom: 8px; }
.feature-card p { font-size: 13px; color: var(--text2); line-height: 1.6; }

/* Schools */
.schools { padding: 60px 40px; text-align: center; }
.schools h2 { font-size: 28px; font-weight: 800; margin-bottom: 32px; }
.schools-grid { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }
.school-badge {
  padding: 12px 28px;
  background: var(--bg2);
  border: 2px solid var(--border);
  border-radius: 12px;
  font-size: 16px;
  font-weight: 800;
  color: var(--primary);
  letter-spacing: 1px;
}

.land-footer { text-align: center; padding: 24px; border-top: 1px solid var(--border); color: var(--text2); font-size: 14px; }

@media (max-width: 900px) {
  .hero { grid-template-columns: 1fr; gap: 40px; padding: 40px 20px; }
  .hero-title { font-size: 36px; }
  .hero-visual { display: none; }
  .demo-btns { grid-template-columns: 1fr; }
}
</style>
