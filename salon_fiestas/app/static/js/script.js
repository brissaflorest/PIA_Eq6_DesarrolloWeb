/* script.js
 - Poblado simulado de servicios (más tarde Django entregará JSON desde API).
 - Validación de formulario de contacto.
 - Cotizador: calcula total y muestra en alerta.
 - Toggle de tema (claro/oscuro).
*/

function cambiarTamaño(elemento) {
  if (elemento.style.fontSize === '25px') {
    elemento.style.fontSize = '20px';
  } else {
    elemento.style.fontSize = '25px';
  }
}

document.addEventListener('DOMContentLoaded', () => {
  // Año en footer
  document.getElementById('currentYear').textContent = new Date().getFullYear();


  // Simulación de servicios (en Django vendrá desde API)
  const servicios = [
    { id: 1, nombre: "Paquete Básico", descripcion: "Precio por hora, decoración básica, animador.", precio: 400.00, caracteristicas: ["Decoración", "Animador"] },
    { id: 2, nombre: "Paquete Premium", descripcion: "Precio por hora, mesa de dulces, show temático.", precio: 800.00,caracteristicas: ["Mesa de dulces", "Show temático"] },
    { id: 3, nombre: "Show de Magia", descripcion: "Precio por hora, show interactivo con mago profesional.", precio: 1000.00,caracteristicas: ["Show", "Interacción"] },
    { id: 4, nombre: "Pinta Caritas", descripcion: "Precio por hora, pinta caritas para la fiesta.", precio: 500.00,caracteristicas: ["Material incluido", "Buena Calidad"] }
  ];

  // Poblado de la sección de servicios
  const serviciosList = document.getElementById('servicios-list');
  const servicioSelect = document.getElementById('servicioSelect');

  servicios.forEach(s => {
    // opción select
    const opt = document.createElement('option');
    opt.value = s.id;
    opt.textContent = `${s.nombre} — $${s.precio.toFixed(2)}`;
    servicioSelect.appendChild(opt);
  });

  // Handler: botón "Usar en cotización" copia a select
  document.addEventListener('click', (e) => {
    if (e.target.matches('.usarBtn')) {
      const id = e.target.dataset.id;
      servicioSelect.value = id;
      window.scrollTo({ top: document.getElementById('cotizacion').offsetTop - 40, behavior: 'smooth' });
    }
  });

  // Cotizador
  document.getElementById('calcularBtn').addEventListener('click', () => {
    const sel = servicioSelect.value;
    const cantidad = Number(document.getElementById('cantidadInput').value);
    if (!sel) { alert('Por favor selecciona un servicio.'); return; }
    if (!cantidad || cantidad <= 0 || cantidad > 6) { alert('La duración debe estar entre 1 y 6 horas.'); return; }

    const servicio = servicios.find(s => String(s.id) === String(sel));
    if (!servicio) { alert('Servicio no encontrado.'); return; }

    // Cálculo: total = precio * cantidad - descuento
    // Descuento es porcentaje.
    const discountRadios = document.querySelectorAll('input[name="discount"]');
    let discountPercent = 0;
    for (const r of discountRadios) { if (r.checked) { discountPercent = Number(r.value); break; } }

    // Para ser extremadamente explícitos con los pasos de cálculo:
    // 1) subtotal = precio * cantidad
    const subtotal = Number((servicio.precio * cantidad).toFixed(2));
    // 2) descuento = subtotal * (discountPercent / 100)
    const descuento = Number((subtotal * (discountPercent / 100)).toFixed(2));
    // 3) total = subtotal - descuento
    const total = Number((subtotal - descuento).toFixed(2));

    const mensaje = `Cotización:\nServicio: ${servicio.nombre}\nCantidad/duración: ${cantidad}\nPrecio unitario: $${servicio.precio.toFixed(2)}\nSubtotal: $${subtotal.toFixed(2)}\nDescuento (${discountPercent}%): -$${descuento.toFixed(2)}\n\nTotal a pagar: $${total.toFixed(2)}`;
    alert(mensaje);
  });

  // CONTACTO (validaciones básicas)
  const contactForm = document.getElementById('contactForm');
  contactForm.addEventListener('submit', (ev) => {
    ev.preventDefault();
    // validación simple HTML5 + mensajes custom
    const name = document.getElementById('name');
    const email = document.getElementById('email');
    const tel = document.getElementById('telefono');
    const msg = document.getElementById('message');
    const valor = name.value.trim();
   

    if (!valor || valor.length < 3 || /\d/.test(valor)) {alert('Ingrese un nombre válido.'); name.focus(); return;}
    if (!validateEmail(email.value.trim())) { alert('Ingresa un correo válido.'); email.focus(); return; }
    if (!tel.value.trim() || tel.value.trim().length !== 10) { alert('Ingresa un teléfono válido.'); tel.focus(); return; }
    if (!msg.value.trim() || msg.value.trim().length < 6) { alert('Escribe un mensaje más detallado.'); msg.focus(); return; }

    // Simulación de envío
    alert('Mensaje enviado con éxito. ¡Gracias por contactarnos!');
    contactForm.reset();
  });

  // Ejecucucion del boton de toggle de tema
  const themeToggle = document.getElementById('themeToggle');
  themeToggle.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const pressed = document.documentElement.classList.contains('dark');
    themeToggle.setAttribute('aria-pressed', pressed ? 'true' : 'false');
  });

}); // DOMContentLoaded


/* Cambiar gif a claro/oscuro según tema */ 
document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    const heroGif = document.getElementById('heroGif');

    // Detecta preferencia y/o valor guardado
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const saved = localStorage.getItem('theme'); // 'dark' | 'light' | null
    const initialDark = saved ? saved === 'dark' : prefersDark;

    function applyTheme(dark) {
        if (themeToggle) themeToggle.setAttribute('aria-pressed', dark ? 'true' : 'false');

        if (heroGif) {
            const src = dark ? heroGif.dataset.light : heroGif.dataset.dark; /*aca no entendi del todo que hce*/ 
            if (src) heroGif.src = src;
        }

        localStorage.setItem('theme', dark ? 'dark' : 'light');
    }

    applyTheme(initialDark);

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const nowDark = !document.documentElement.classList.contains('dark');
            applyTheme(nowDark);
        });
    }
});

/* Helpers */
function escapeHtml(s){
  return String(s).replace(/[&<>"']/g, (m) => ({ "&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#039;" }[m]));
}
function validateEmail(email){
  // simple RFC-like check
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
