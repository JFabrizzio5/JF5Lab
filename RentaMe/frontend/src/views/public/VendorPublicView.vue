<template>
  <div class="vendor-page" :style="cssVars">
    <!-- Loading -->
    <div v-if="loading" class="loading-screen">
      <div class="spinner"></div>
      <p>Cargando...</p>
    </div>

    <!-- 404 -->
    <div v-else-if="!vendor" class="not-found">
      <h1>404</h1>
      <p>Vendedor no encontrado</p>
      <router-link to="/" class="btn btn-primary">Ir al inicio</router-link>
    </div>

    <template v-else>
      <!-- 1. NAV -->
      <nav class="v-nav" :style="{ background: `${vendor.theme_color}15`, borderBottom: `1px solid ${vendor.theme_color}30` }">
        <div class="v-nav-inner">
          <div class="v-nav-brand">
            <img v-if="vendor.logo_url" :src="vendor.logo_url" :alt="vendor.business_name" class="v-logo" />
            <span class="v-biz-name">{{ vendor.business_name }}</span>
          </div>
          <div class="v-nav-social">
            <a v-if="vendor.facebook_url" :href="vendor.facebook_url" target="_blank" class="social-icon" title="Facebook">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
            </a>
            <a v-if="vendor.instagram_url" :href="vendor.instagram_url" target="_blank" class="social-icon" title="Instagram">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="18" height="18"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
            </a>
            <a v-if="vendor.tiktok_url" :href="vendor.tiktok_url" target="_blank" class="social-icon" title="TikTok">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1V9.01a6.32 6.32 0 0 0-.79-.05 6.34 6.34 0 0 0-6.34 6.34 6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.33-6.34V8.69a8.18 8.18 0 0 0 4.77 1.52V6.76a4.85 4.85 0 0 1-1-.07z"/></svg>
            </a>
            <a v-if="vendor.whatsapp" :href="`https://wa.me/${vendor.whatsapp}`" target="_blank" class="social-icon wa-icon" title="WhatsApp">
              <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
            </a>
          </div>
          <a v-if="vendor.whatsapp" :href="`https://wa.me/${vendor.whatsapp}`" target="_blank" class="cta-nav-btn" :style="{ background: vendor.theme_color }">
            Cotizar por WhatsApp
          </a>
        </div>
      </nav>

      <!-- 2. HERO -->
      <section class="v-hero">
        <div class="v-hero-cover" :style="coverStyle">
          <div class="v-hero-overlay" :style="heroOverlay"></div>
          <div class="v-hero-content">
            <h1 class="v-hero-title">{{ vendor.business_name }}</h1>
            <p v-if="vendor.tagline" class="v-hero-tagline">{{ vendor.tagline }}</p>
            <div v-if="vendor.city" class="v-hero-location">
              <span>📍</span> {{ vendor.city }}
            </div>
            <a class="v-scroll-cta" href="#items" :style="{ background: vendor.accent_color, color: '#07070d' }">
              Ver artículos disponibles ↓
            </a>
          </div>
        </div>
        <div class="hero-scroll-hint">
          <span class="scroll-dot"></span>
        </div>
      </section>

      <!-- 3. ITEMS GRID -->
      <section id="items" class="v-items-section">
        <div class="v-section-inner">
          <h2 class="v-section-title" :style="{ color: vendor.theme_color }">Artículos disponibles</h2>
          <div class="items-filter" v-if="categories.length > 1">
            <button
              v-for="cat in ['all', ...categories]"
              :key="cat"
              class="filter-chip"
              :class="{ active: selectedCategory === cat }"
              :style="selectedCategory === cat ? { background: vendor.theme_color, borderColor: vendor.theme_color } : {}"
              @click="selectedCategory = cat"
            >
              {{ cat === 'all' ? '✨ Todos' : catLabel(cat) }}
            </button>
          </div>
          <div class="items-grid">
            <div
              v-for="item in filteredItems"
              :key="item.id"
              class="item-card"
              @click="openItem(item)"
            >
              <div class="item-card-img">
                <img v-if="item.images[0]" :src="item.images[0]" :alt="item.name" />
                <div v-else class="item-no-img">📦</div>
                <span v-if="item.is_featured" class="featured-badge" :style="{ background: vendor.accent_color }">⭐ Destacado</span>
                <span class="category-chip" :style="{ background: `${vendor.theme_color}20`, color: vendor.theme_color }">
                  {{ catLabel(item.category) }}
                </span>
                <div class="item-qty-badge" v-if="item.quantity > 1">{{ item.quantity }} disponibles</div>
              </div>
              <div class="item-card-body">
                <h3 class="item-name">{{ item.name }}</h3>
                <p v-if="item.description" class="item-desc">{{ item.description.substring(0, 90) }}{{ item.description.length > 90 ? '...' : '' }}</p>
                <div class="item-pricing">
                  <div v-if="item.price_per_hour" class="price-row">
                    <span class="price-val" :style="{ color: vendor.theme_color }">${{ fmt(item.price_per_hour) }}</span>
                    <span class="price-unit">/ hora</span>
                  </div>
                  <div v-if="item.price_per_day" class="price-row">
                    <span class="price-val" :style="{ color: vendor.theme_color }">${{ fmt(item.price_per_day) }}</span>
                    <span class="price-unit">/ día</span>
                  </div>
                  <div v-if="item.price_per_weekend" class="price-row">
                    <span class="price-val" :style="{ color: vendor.theme_color }">${{ fmt(item.price_per_weekend) }}</span>
                    <span class="price-unit">/ fin de semana</span>
                  </div>
                  <div v-if="item.price_per_week" class="price-row">
                    <span class="price-val" :style="{ color: vendor.theme_color }">${{ fmt(item.price_per_week) }}</span>
                    <span class="price-unit">/ semana</span>
                  </div>
                </div>
                <button class="item-cta" :style="{ background: vendor.theme_color }">
                  Ver detalles / Reservar
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. ITEM DETAIL MODAL -->
      <div v-if="selectedItem" class="modal-overlay" @click.self="closeItem">
        <div class="modal modal-lg item-modal">
          <button class="modal-close" @click="closeItem">×</button>
          <div class="item-modal-layout">
            <!-- Left: Gallery + details -->
            <div class="item-modal-left">
              <div class="gallery">
                <img :src="selectedItem.images[activeImg] || selectedItem.images[0]" class="gallery-main" :alt="selectedItem.name" />
                <div v-if="selectedItem.images.length > 1" class="gallery-thumbs">
                  <img
                    v-for="(img, idx) in selectedItem.images"
                    :key="idx"
                    :src="img"
                    class="gallery-thumb"
                    :class="{ active: activeImg === idx }"
                    @click="activeImg = idx"
                    :alt="`Imagen ${idx+1}`"
                  />
                </div>
              </div>
              <h2 class="item-modal-name">{{ selectedItem.name }}</h2>
              <span class="item-cat-chip" :style="{ background: `${vendor.theme_color}20`, color: vendor.theme_color }">
                {{ catLabel(selectedItem.category) }}
              </span>
              <p v-if="selectedItem.description" class="item-modal-desc">{{ selectedItem.description }}</p>

              <!-- Specifications -->
              <div v-if="Object.keys(selectedItem.specifications || {}).length" class="item-specs">
                <h4 class="specs-title">Especificaciones</h4>
                <div class="specs-grid">
                  <div v-for="(val, key) in selectedItem.specifications" :key="key" class="spec-row">
                    <span class="spec-key">{{ key }}</span>
                    <span class="spec-val">{{ val }}</span>
                  </div>
                </div>
              </div>

              <!-- Included / Not included -->
              <div v-if="selectedItem.included?.length || selectedItem.not_included?.length" class="item-lists">
                <div v-if="selectedItem.included?.length" class="list-section">
                  <h4 class="list-title">✅ Incluye</h4>
                  <ul>
                    <li v-for="inc in selectedItem.included" :key="inc">{{ inc }}</li>
                  </ul>
                </div>
                <div v-if="selectedItem.not_included?.length" class="list-section">
                  <h4 class="list-title">❌ No incluye</h4>
                  <ul>
                    <li v-for="ni in selectedItem.not_included" :key="ni">{{ ni }}</li>
                  </ul>
                </div>
              </div>

              <div v-if="selectedItem.requirements" class="item-requirements">
                <h4>⚠️ Requisitos</h4>
                <p>{{ selectedItem.requirements }}</p>
              </div>
            </div>

            <!-- Right: Booking form -->
            <div class="item-modal-right">
              <div v-if="!bookingSuccess" class="booking-form-panel">
                <h3 class="booking-title">Solicitar reserva</h3>

                <!-- Rental unit tabs -->
                <div class="unit-tabs">
                  <button
                    v-for="unit in availableUnits"
                    :key="unit.key"
                    class="unit-tab"
                    :class="{ active: rentalUnit === unit.key }"
                    :style="rentalUnit === unit.key ? { background: vendor.theme_color, borderColor: vendor.theme_color } : {}"
                    @click="setUnit(unit.key)"
                  >
                    {{ unit.label }}
                  </button>
                </div>

                <!-- Pricing display -->
                <div class="price-display" :style="{ borderColor: `${vendor.theme_color}40` }">
                  <div class="price-big" :style="{ color: vendor.theme_color }">${{ fmt(unitPrice) }}</div>
                  <div class="price-period">{{ currentUnitLabel }}</div>
                </div>

                <!-- Dates -->
                <div class="form-group">
                  <label class="label">Fecha y hora de inicio</label>
                  <input type="datetime-local" v-model="startDatetime" class="input" />
                </div>
                <div class="form-group">
                  <label class="label">Fecha y hora de fin</label>
                  <input type="datetime-local" v-model="endDatetime" class="input" />
                </div>

                <!-- Quantity -->
                <div class="form-group">
                  <label class="label">Cantidad (máx: {{ selectedItem.quantity }})</label>
                  <div class="qty-stepper">
                    <button class="qty-btn" @click="quantity = Math.max(1, quantity - 1)">−</button>
                    <span class="qty-val">{{ quantity }}</span>
                    <button class="qty-btn" @click="quantity = Math.min(selectedItem.quantity, quantity + 1)">+</button>
                  </div>
                </div>

                <!-- Live price calc -->
                <div class="price-calc" :style="{ background: `${vendor.theme_color}08`, border: `1px solid ${vendor.theme_color}20` }">
                  <div class="calc-row">
                    <span>Precio unitario</span>
                    <span>${{ fmt(unitPrice) }} × {{ quantity }}</span>
                  </div>
                  <div class="calc-row">
                    <span>Subtotal</span>
                    <span>${{ fmt(subtotal) }}</span>
                  </div>
                  <div class="calc-row" v-if="vendor.deposit_percent > 0">
                    <span>Depósito requerido ({{ vendor.deposit_percent }}%)</span>
                    <span style="color: var(--warning)">${{ fmt(depositAmount) }}</span>
                  </div>
                  <div class="calc-row total-row" :style="{ color: vendor.theme_color }">
                    <span><strong>Total estimado</strong></span>
                    <span><strong>${{ fmt(subtotal) }}</strong></span>
                  </div>
                </div>

                <!-- Customer form -->
                <div class="customer-form">
                  <h4 class="customer-title">Tus datos de contacto</h4>
                  <div class="form-group">
                    <label class="label">Nombre completo</label>
                    <input v-model="customer.name" type="text" class="input" placeholder="Juan García" required />
                  </div>
                  <div class="form-group">
                    <label class="label">Correo electrónico</label>
                    <input v-model="customer.email" type="email" class="input" placeholder="juan@email.com" required />
                  </div>
                  <div class="form-group">
                    <label class="label">Teléfono</label>
                    <input v-model="customer.phone" type="tel" class="input" placeholder="+52 55 1234 5678" />
                  </div>
                  <div class="form-group">
                    <label class="label">Notas adicionales</label>
                    <textarea v-model="customer.notes" class="input" placeholder="¿Tienes alguna pregunta o detalle especial?" rows="2"></textarea>
                  </div>
                </div>

                <div v-if="bookingError" class="error-msg">{{ bookingError }}</div>

                <button
                  class="booking-submit"
                  :style="{ background: vendor.theme_color }"
                  @click="submitBooking"
                  :disabled="bookingLoading || !customer.name || !customer.email || !startDatetime || !endDatetime"
                >
                  {{ bookingLoading ? 'Enviando solicitud...' : '📩 Solicitar reserva' }}
                </button>
              </div>

              <!-- Success -->
              <div v-else class="booking-success">
                <div class="success-icon">🎉</div>
                <h3>¡Solicitud enviada!</h3>
                <p>Tu número de reserva es <strong>#{{ bookingResult.booking_id }}</strong></p>
                <div class="booking-summary">
                  <div class="summary-row">
                    <span>Artículo:</span>
                    <span>{{ selectedItem.name }}</span>
                  </div>
                  <div class="summary-row">
                    <span>Total:</span>
                    <span :style="{ color: vendor.theme_color }">${{ fmt(bookingResult.total) }}</span>
                  </div>
                  <div class="summary-row" v-if="bookingResult.deposit_amount > 0">
                    <span>Depósito:</span>
                    <span>${{ fmt(bookingResult.deposit_amount) }}</span>
                  </div>
                </div>
                <p class="success-note">El vendedor revisará tu solicitud y se pondrá en contacto contigo pronto.</p>
                <a
                  v-if="vendor.whatsapp"
                  :href="waLink"
                  target="_blank"
                  class="wa-confirm-btn"
                  :style="{ background: '#25d366' }"
                >
                  <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
                  Confirmar por WhatsApp
                </a>
                <button class="btn btn-secondary" style="margin-top: 12px; width: 100%; justify-content: center;" @click="resetBooking">
                  Hacer otra reserva
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. SOCIAL / CONTACT -->
      <section class="v-contact-section">
        <div class="v-section-inner">
          <h2 class="v-section-title" :style="{ color: vendor.theme_color }">Contáctanos</h2>
          <div class="contact-grid">
            <a v-if="vendor.whatsapp" :href="`https://wa.me/${vendor.whatsapp}`" target="_blank" class="contact-btn wa-btn">
              <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>
              WhatsApp
            </a>
            <a v-if="vendor.instagram_url" :href="vendor.instagram_url" target="_blank" class="contact-btn ig-btn">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="22" height="22"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
              Instagram
            </a>
            <a v-if="vendor.facebook_url" :href="vendor.facebook_url" target="_blank" class="contact-btn fb-btn">
              <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22"><path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>
              Facebook
            </a>
            <a v-if="vendor.phone" :href="`tel:${vendor.phone}`" class="contact-btn phone-btn">
              📞 {{ vendor.phone }}
            </a>
            <a v-if="vendor.email" :href="`mailto:${vendor.email}`" class="contact-btn email-btn">
              ✉️ {{ vendor.email }}
            </a>
          </div>
        </div>
      </section>

      <!-- 6. POLICIES -->
      <section v-if="vendor.cancellation_policy" class="v-policies-section">
        <div class="v-section-inner">
          <h2 class="v-section-title" :style="{ color: vendor.theme_color }">Políticas</h2>
          <div class="policies-grid">
            <div class="policy-card">
              <h4>📋 Política de cancelación</h4>
              <p>{{ vendor.cancellation_policy }}</p>
            </div>
            <div class="policy-card">
              <h4>💰 Depósito requerido</h4>
              <p>Se solicita un depósito del <strong>{{ vendor.deposit_percent }}%</strong> del total para confirmar la reserva.</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 7. FOOTER -->
      <footer class="v-footer" :style="{ background: `${vendor.theme_color}10`, borderTop: `1px solid ${vendor.theme_color}20` }">
        <div class="v-section-inner">
          <div class="v-footer-inner">
            <div>
              <div class="v-footer-biz">{{ vendor.business_name }}</div>
              <div class="v-footer-city" v-if="vendor.city">📍 {{ vendor.city }}</div>
            </div>
            <div class="v-footer-powered">
              <a href="/" class="powered-badge">
                Powered by <strong>🏷️ RentaMe</strong>
              </a>
            </div>
          </div>
        </div>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { publicAPI } from '../../api/index.js'

const route = useRoute()
const vendor = ref(null)
const loading = ref(true)
const selectedItem = ref(null)
const activeImg = ref(0)
const selectedCategory = ref('all')

// Booking form state
const rentalUnit = ref('day')
const startDatetime = ref('')
const endDatetime = ref('')
const quantity = ref(1)
const customer = ref({ name: '', email: '', phone: '', notes: '' })
const bookingLoading = ref(false)
const bookingError = ref('')
const bookingSuccess = ref(false)
const bookingResult = ref(null)

const CATEGORY_LABELS = {
  boats: '⛵ Barcos',
  vehicles: '🚗 Vehículos',
  furniture: '🪑 Muebles',
  party: '🎉 Fiestas',
  sports: '⚽ Deportes',
  housing: '🏠 Inmuebles',
  equipment: '🔧 Equipo',
  general: '📦 General',
  other: '📦 Otro',
}

function catLabel(cat) {
  return CATEGORY_LABELS[cat] || cat
}

const categories = computed(() => {
  if (!vendor.value?.items) return []
  return [...new Set(vendor.value.items.map(i => i.category))]
})

const filteredItems = computed(() => {
  if (!vendor.value?.items) return []
  if (selectedCategory.value === 'all') return vendor.value.items
  return vendor.value.items.filter(i => i.category === selectedCategory.value)
})

const cssVars = computed(() => ({
  '--vendor-primary': vendor.value?.theme_color || '#6366f1',
  '--vendor-accent': vendor.value?.accent_color || '#f59e0b',
}))

const coverStyle = computed(() => {
  if (vendor.value?.cover_url) {
    return { backgroundImage: `url(${vendor.value.cover_url})`, backgroundSize: 'cover', backgroundPosition: 'center' }
  }
  return { background: `linear-gradient(135deg, ${vendor.value?.theme_color || '#6366f1'}, #07070d)` }
})

const heroOverlay = computed(() => ({
  background: `linear-gradient(to bottom, ${vendor.value?.theme_color || '#6366f1'}60, rgba(7,7,13,0.95))`
}))

const availableUnits = computed(() => {
  if (!selectedItem.value) return []
  const units = []
  if (selectedItem.value.price_per_hour) units.push({ key: 'hour', label: 'Por hora' })
  if (selectedItem.value.price_per_day) units.push({ key: 'day', label: 'Por día' })
  if (selectedItem.value.price_per_weekend) units.push({ key: 'weekend', label: 'Fin de semana' })
  if (selectedItem.value.price_per_week) units.push({ key: 'week', label: 'Por semana' })
  return units
})

const unitPrice = computed(() => {
  if (!selectedItem.value) return 0
  const map = {
    hour: selectedItem.value.price_per_hour,
    day: selectedItem.value.price_per_day,
    weekend: selectedItem.value.price_per_weekend,
    week: selectedItem.value.price_per_week,
  }
  return map[rentalUnit.value] || 0
})

const currentUnitLabel = computed(() => {
  const labels = { hour: '/ hora', day: '/ día', weekend: '/ fin de semana', week: '/ semana' }
  return labels[rentalUnit.value] || ''
})

const subtotal = computed(() => {
  if (!unitPrice.value) return 0
  let multiplier = 1
  if (startDatetime.value && endDatetime.value) {
    const diff = (new Date(endDatetime.value) - new Date(startDatetime.value)) / 1000 / 3600
    if (rentalUnit.value === 'hour') multiplier = Math.max(1, Math.round(diff))
    else if (rentalUnit.value === 'day') multiplier = Math.max(1, Math.ceil(diff / 24))
    else if (rentalUnit.value === 'week') multiplier = Math.max(1, Math.ceil(diff / 168))
  }
  return unitPrice.value * multiplier * quantity.value
})

const depositAmount = computed(() => {
  return Math.round(subtotal.value * (vendor.value?.deposit_percent || 0) / 100)
})

const waLink = computed(() => {
  if (!vendor.value?.whatsapp || !bookingResult.value) return '#'
  const msg = `Hola! Acabo de solicitar la renta de ${bookingResult.value.item_name || selectedItem.value?.name} para las fechas ${bookingResult.value.start_datetime?.slice(0,10)} - ${bookingResult.value.end_datetime?.slice(0,10)}. Mi número de reserva es #${bookingResult.value.booking_id}.`
  return `https://wa.me/${vendor.value.whatsapp}?text=${encodeURIComponent(msg)}`
})

function fmt(n) {
  if (!n && n !== 0) return '0'
  return Number(n).toLocaleString('es-MX')
}

function openItem(item) {
  selectedItem.value = item
  activeImg.value = 0
  rentalUnit.value = availableUnits.value[0]?.key || 'day'
  bookingSuccess.value = false
  bookingError.value = ''
  customer.value = { name: '', email: '', phone: '', notes: '' }
  quantity.value = 1
  startDatetime.value = ''
  endDatetime.value = ''
}

function closeItem() {
  selectedItem.value = null
  bookingSuccess.value = false
  bookingResult.value = null
}

function setUnit(unit) {
  rentalUnit.value = unit
  // Auto-calculate end datetime
  if (startDatetime.value) {
    const start = new Date(startDatetime.value)
    if (unit === 'day') {
      start.setDate(start.getDate() + 1)
    } else if (unit === 'weekend') {
      start.setDate(start.getDate() + 2)
    } else if (unit === 'week') {
      start.setDate(start.getDate() + 7)
    } else if (unit === 'hour') {
      start.setHours(start.getHours() + 1)
    }
    endDatetime.value = start.toISOString().slice(0, 16)
  }
}

watch(startDatetime, (val) => {
  if (val) setUnit(rentalUnit.value)
})

async function submitBooking() {
  if (!customer.value.name || !customer.value.email || !startDatetime.value || !endDatetime.value) {
    bookingError.value = 'Por favor completa todos los campos requeridos'
    return
  }
  bookingLoading.value = true
  bookingError.value = ''
  try {
    const res = await publicAPI.createInquiry(vendor.value.slug, {
      item_id: selectedItem.value.id,
      customer_name: customer.value.name,
      customer_email: customer.value.email,
      customer_phone: customer.value.phone,
      start_datetime: new Date(startDatetime.value).toISOString(),
      end_datetime: new Date(endDatetime.value).toISOString(),
      rental_unit: rentalUnit.value,
      quantity: quantity.value,
      notes: customer.value.notes,
    })
    bookingResult.value = res.data
    bookingSuccess.value = true
  } catch (e) {
    bookingError.value = e.response?.data?.detail || 'Error al enviar solicitud'
  } finally {
    bookingLoading.value = false
  }
}

function resetBooking() {
  bookingSuccess.value = false
  bookingResult.value = null
  customer.value = { name: '', email: '', phone: '', notes: '' }
}

onMounted(async () => {
  try {
    const res = await publicAPI.getVendor(route.params.slug)
    vendor.value = res.data
  } catch {
    vendor.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.vendor-page {
  background: #07070d;
  color: #e2e8f0;
  min-height: 100vh;
}

.loading-screen, .not-found {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(255,255,255,0.1);
  border-top-color: var(--vendor-primary, #6366f1);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* NAV */
.v-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
}
.v-nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.v-nav-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}
.v-logo {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  object-fit: cover;
}
.v-biz-name {
  font-size: 18px;
  font-weight: 700;
  color: #e2e8f0;
}
.v-nav-social {
  display: flex;
  align-items: center;
  gap: 8px;
}
.social-icon {
  color: rgba(255,255,255,0.6);
  display: flex;
  align-items: center;
  padding: 6px;
  border-radius: 6px;
  transition: all 0.2s;
  text-decoration: none;
}
.social-icon:hover { color: white; background: rgba(255,255,255,0.1); }
.cta-nav-btn {
  display: inline-flex;
  align-items: center;
  padding: 8px 16px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 600;
  color: white;
  text-decoration: none;
  transition: opacity 0.2s;
  white-space: nowrap;
}
.cta-nav-btn:hover { opacity: 0.85; }

/* HERO */
.v-hero { position: relative; }
.v-hero-cover {
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.v-hero-overlay {
  position: absolute;
  inset: 0;
}
.v-hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 60px 24px;
}
.v-hero-title {
  font-size: clamp(36px, 6vw, 72px);
  font-weight: 800;
  color: white;
  margin-bottom: 12px;
  text-shadow: 0 2px 20px rgba(0,0,0,0.5);
}
.v-hero-tagline {
  font-size: clamp(16px, 2.5vw, 22px);
  color: rgba(255,255,255,0.8);
  margin-bottom: 16px;
}
.v-hero-location {
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  margin-bottom: 28px;
}
.v-scroll-cta {
  display: inline-block;
  padding: 12px 28px;
  border-radius: 100px;
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.2s, transform 0.2s;
}
.v-scroll-cta:hover { opacity: 0.9; transform: translateY(-2px); }
.hero-scroll-hint {
  display: flex;
  justify-content: center;
  padding: 12px 0;
}
.scroll-dot {
  width: 6px;
  height: 20px;
  background: rgba(255,255,255,0.2);
  border-radius: 3px;
  animation: scrollPulse 1.5s ease-in-out infinite;
}
@keyframes scrollPulse {
  0%, 100% { opacity: 0.2; transform: scaleY(1); }
  50% { opacity: 0.6; transform: scaleY(1.3); }
}

/* ITEMS */
.v-items-section { padding: 60px 0; }
.v-section-inner { max-width: 1200px; margin: 0 auto; padding: 0 24px; }
.v-section-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 24px;
}
.items-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 28px;
}
.filter-chip {
  padding: 6px 14px;
  border-radius: 100px;
  border: 1px solid rgba(255,255,255,0.15);
  background: transparent;
  color: rgba(255,255,255,0.5);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}
.filter-chip:hover { color: rgba(255,255,255,0.8); }
.filter-chip.active { color: white; }

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
}

.item-card {
  background: rgba(15, 15, 26, 0.8);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.25s;
}
.item-card:hover {
  transform: translateY(-4px);
  border-color: rgba(255,255,255,0.15);
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.item-card-img {
  position: relative;
  height: 220px;
  overflow: hidden;
}
.item-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}
.item-card:hover .item-card-img img { transform: scale(1.04); }
.item-no-img {
  width: 100%;
  height: 100%;
  background: rgba(255,255,255,0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}
.featured-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 700;
  color: #07070d;
}
.category-chip {
  position: absolute;
  bottom: 10px;
  left: 10px;
  padding: 4px 10px;
  border-radius: 100px;
  font-size: 11px;
  font-weight: 600;
}
.item-qty-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(0,0,0,0.7);
  color: rgba(255,255,255,0.8);
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 11px;
}
.item-card-body { padding: 18px; }
.item-name { font-size: 17px; font-weight: 700; margin-bottom: 6px; }
.item-desc { font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 14px; line-height: 1.5; }
.item-pricing { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; }
.price-row { display: flex; align-items: baseline; gap: 4px; }
.price-val { font-size: 18px; font-weight: 700; }
.price-unit { font-size: 12px; color: rgba(255,255,255,0.4); }
.item-cta {
  display: block;
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}
.item-cta:hover { opacity: 0.85; }

/* ITEM MODAL */
.item-modal {
  max-height: 92vh;
  overflow-y: auto;
}
.item-modal-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: 28px;
  align-items: start;
}
.gallery-main {
  width: 100%;
  height: 280px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 10px;
}
.gallery-thumbs {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.gallery-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
  cursor: pointer;
  opacity: 0.6;
  border: 2px solid transparent;
  transition: all 0.2s;
}
.gallery-thumb.active, .gallery-thumb:hover { opacity: 1; border-color: var(--vendor-primary, #6366f1); }
.item-modal-name { font-size: 22px; font-weight: 700; margin: 14px 0 8px; }
.item-cat-chip {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 12px;
}
.item-modal-desc { font-size: 14px; color: rgba(255,255,255,0.6); line-height: 1.7; margin-bottom: 20px; }
.item-specs { margin-bottom: 20px; }
.specs-title { font-size: 14px; font-weight: 700; margin-bottom: 10px; color: rgba(255,255,255,0.8); }
.specs-grid { display: flex; flex-direction: column; gap: 6px; }
.spec-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}
.spec-key { color: rgba(255,255,255,0.5); }
.spec-val { font-weight: 600; }
.item-lists { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }
.list-section h4 { font-size: 13px; font-weight: 700; margin-bottom: 8px; }
.list-section ul { padding-left: 16px; }
.list-section li { font-size: 13px; color: rgba(255,255,255,0.6); margin-bottom: 4px; }
.item-requirements { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.2); border-radius: 8px; padding: 12px; }
.item-requirements h4 { font-size: 13px; font-weight: 700; margin-bottom: 6px; }
.item-requirements p { font-size: 13px; color: rgba(255,255,255,0.6); }

/* BOOKING FORM */
.booking-form-panel {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 14px;
  padding: 20px;
  position: sticky;
  top: 20px;
}
.booking-title { font-size: 18px; font-weight: 700; margin-bottom: 16px; }
.unit-tabs { display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 16px; }
.unit-tab {
  padding: 6px 12px;
  border-radius: 6px;
  border: 1px solid rgba(255,255,255,0.15);
  background: transparent;
  color: rgba(255,255,255,0.6);
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.unit-tab.active { color: white; }
.price-display {
  text-align: center;
  padding: 16px;
  border-radius: 10px;
  border: 1px solid;
  margin-bottom: 16px;
}
.price-big { font-size: 32px; font-weight: 800; }
.price-period { font-size: 13px; color: rgba(255,255,255,0.5); }
.qty-stepper {
  display: flex;
  align-items: center;
  gap: 12px;
}
.qty-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid rgba(255,255,255,0.15);
  background: transparent;
  color: rgba(255,255,255,0.8);
  font-size: 18px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.qty-btn:hover { background: rgba(255,255,255,0.08); }
.qty-val { font-size: 18px; font-weight: 700; min-width: 24px; text-align: center; }
.price-calc {
  border-radius: 10px;
  padding: 12px;
  margin-bottom: 16px;
}
.calc-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 4px 0;
  color: rgba(255,255,255,0.7);
}
.total-row { border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; margin-top: 6px; font-size: 15px; }
.customer-form { margin-bottom: 16px; }
.customer-title { font-size: 14px; font-weight: 700; margin-bottom: 12px; color: rgba(255,255,255,0.8); }
.booking-submit {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  color: white;
  cursor: pointer;
  transition: opacity 0.2s;
}
.booking-submit:hover:not(:disabled) { opacity: 0.85; }
.booking-submit:disabled { opacity: 0.5; cursor: not-allowed; }
.error-msg {
  background: rgba(239,68,68,0.1);
  border: 1px solid rgba(239,68,68,0.3);
  color: #f87171;
  padding: 10px;
  border-radius: 8px;
  font-size: 13px;
  margin-bottom: 12px;
}

/* BOOKING SUCCESS */
.booking-success {
  background: rgba(16,185,129,0.05);
  border: 1px solid rgba(16,185,129,0.2);
  border-radius: 14px;
  padding: 24px;
  text-align: center;
}
.success-icon { font-size: 48px; margin-bottom: 12px; }
.booking-success h3 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.booking-success > p { color: rgba(255,255,255,0.7); margin-bottom: 16px; }
.booking-summary {
  background: rgba(255,255,255,0.04);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  text-align: left;
}
.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 4px 0;
  color: rgba(255,255,255,0.7);
}
.success-note { font-size: 13px; color: rgba(255,255,255,0.5); margin-bottom: 16px; }
.wa-confirm-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 700;
  color: white;
  text-decoration: none;
  margin-bottom: 8px;
}

/* CONTACT */
.v-contact-section { padding: 60px 0; }
.contact-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
.contact-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.2s;
  color: white;
}
.contact-btn:hover { transform: translateY(-2px); opacity: 0.9; }
.wa-btn { background: #25d366; }
.ig-btn { background: linear-gradient(135deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
.fb-btn { background: #1877f2; }
.phone-btn { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); }
.email-btn { background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); }

/* POLICIES */
.v-policies-section { padding: 40px 0; }
.policies-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.policy-card {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.07);
  border-radius: 12px;
  padding: 20px;
}
.policy-card h4 { font-size: 15px; font-weight: 700; margin-bottom: 10px; }
.policy-card p { font-size: 14px; color: rgba(255,255,255,0.6); line-height: 1.6; }

/* FOOTER */
.v-footer { padding: 32px 0; }
.v-footer-inner { display: flex; align-items: center; justify-content: space-between; }
.v-footer-biz { font-size: 16px; font-weight: 700; }
.v-footer-city { font-size: 13px; color: rgba(255,255,255,0.4); margin-top: 4px; }
.powered-badge {
  font-size: 13px;
  color: rgba(255,255,255,0.4);
  text-decoration: none;
  transition: color 0.2s;
}
.powered-badge:hover { color: rgba(255,255,255,0.7); }
.powered-badge strong { color: rgba(255,255,255,0.6); }

@media (max-width: 768px) {
  .item-modal-layout { grid-template-columns: 1fr; }
  .item-lists { grid-template-columns: 1fr; }
  .policies-grid { grid-template-columns: 1fr; }
  .v-footer-inner { flex-direction: column; gap: 16px; text-align: center; }
  .cta-nav-btn { display: none; }
  .items-grid { grid-template-columns: 1fr; }
}
</style>
