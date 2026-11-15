document.getElementById('fecha').valueAsDate = new Date();

const getBaseUrl = () => document.getElementById('apiUrl').value.replace(/\/$/, "");
const getHeaders = () => ({
  'Content-Type': 'application/json',
  'X-API-Key': document.getElementById('apiKey').value.trim()
});

// --- MANEJO FORMULARIO RIESGO ---
document.getElementById('formRiesgo').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = document.getElementById('btnRiesgo');
  const resDiv = document.getElementById('resRiesgo');
  btn.disabled = true;
  btn.textContent = "Calculando...";

  const gVictima = document.getElementById('generoVictima').value;
  const gAgresor = document.getElementById('generoAgresor').value;
  const vinculo = document.getElementById('vinculo').value;

  const payload = {
    edad_persona_en_situacion_de_violencia: parseFloat(document.getElementById('edad').value),
    log_pobl_prov: parseFloat(document.getElementById('provincia').value),
    is_weekend: parseInt(document.getElementById('isWeekend').value),
    tipo_de_violencia_psicologica_si: document.getElementById('v_psicologica').checked ? 1 : 0,
    tipo_de_violencia_simbolica_si: document.getElementById('v_simbolica').checked ? 1 : 0,
    tipo_de_violencia_economica_y_patrimonial_si: document.getElementById('v_economica').checked ? 1 : 0,
    tipo_de_violencia_domestica_si: document.getElementById('v_domestica').checked ? 1 : 0,
    modalidad_de_violencia_institucional_si: document.getElementById('m_institucional').checked ? 1 : 0,
    modalidad_de_violencia_laboral_si: document.getElementById('m_laboral').checked ? 1 : 0,
    modalidad_de_violencia_otras_si: document.getElementById('m_otras').checked ? 1 : 0,
    vinculo_con_la_persona_agresora_pareja: vinculo === 'pareja' ? 1 : 0,
    "vinculo_con_la_persona_agresora_ex pareja": vinculo === 'ex pareja' ? 1 : 0,
    vinculo_con_la_persona_agresora_otro: vinculo === 'otro' ? 1 : 0,
    "vinculo_con_la_persona_agresora_otro familiar": vinculo === 'otro familiar' ? 1 : 0,
    genero_persona_en_situacion_de_violencia_mujer: gVictima === 'mujer' ? 1 : 0,
    genero_persona_en_situacion_de_violencia_varon: gVictima === 'varon' ? 1 : 0,
    genero_de_la_persona_agresora_varon: gAgresor === 'varon' ? 1 : 0,
    genero_de_la_persona_agresora_mujer: gAgresor === 'mujer' ? 1 : 0
  };

  try {
    const response = await fetch(`${getBaseUrl()}/predecir/riesgo`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Error en la API");

    const esAlto = data.nivel_riesgo_codigo === 2;
    resDiv.className = "resultado";
    resDiv.style.display = "block";
    resDiv.innerHTML = `
      <p style="margin:0 0 8px 0;"><strong>Resultado:</strong> 
        <span class="badge ${esAlto ? 'badge-alto' : 'badge-medio'}">
          Riesgo ${data.nivel_riesgo_etiqueta}
        </span>
      </p>
      <p style="margin:0; font-size:0.9rem;">
        Probabilidad Riesgo Alto: <strong>${(data.probabilidades.Alto * 100).toFixed(1)}%</strong> | 
        Riesgo Medio: <strong>${(data.probabilidades.Medio * 100).toFixed(1)}%</strong>
      </p>
    `;
  } catch (err) {
    resDiv.className = "resultado error";
    resDiv.style.display = "block";
    resDiv.textContent = `Error: ${err.message}. Verifica la URL, la API Key y que el servidor esté activo.`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Evaluar Riesgo";
  }
});

// --- MANEJO FORMULARIO VOLUMEN ---
document.getElementById('formVolumen').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = document.getElementById('btnVolumen');
  const resDiv = document.getElementById('resVolumen');
  btn.disabled = true;
  btn.textContent = "Calculando...";

  const payload = {
    fecha: document.getElementById('fecha').value,
    lag_1: parseFloat(document.getElementById('lag1').value),
    lag_7: parseFloat(document.getElementById('lag7').value)
  };

  try {
    const response = await fetch(`${getBaseUrl()}/predecir/volumen`, {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Error en la API");

    resDiv.className = "resultado";
    resDiv.style.display = "block";
    resDiv.innerHTML = `
      <p style="margin:0 0 6px 0;"><strong>Fecha:</strong> ${data.fecha}</p>
      <p style="margin:0; font-size:1.1rem;">
        Demanda estimada: <strong>${data.llamadas_estimadas_entero} llamadas</strong> 
        <span style="font-size:0.85rem; color:#64748b;">(${data.llamadas_estimadas})</span>
      </p>
    `;
  } catch (err) {
    resDiv.className = "resultado error";
    resDiv.style.display = "block";
    resDiv.textContent = `Error: ${err.message}. Verifica la URL, la API Key y que el servidor esté activo.`;
  } finally {
    btn.disabled = false;
    btn.textContent = "Predecir Volumen";
  }
});
