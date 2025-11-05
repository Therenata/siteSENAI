/* JS externo para gerar os gráficos do PIB na página
   - Tenta obter dados do IBGE (Sidra) com endpoint de 'values' para a tabela 5938 (PIB)
   - Se falhar (CORS/estrutura), faz fallback para CSV público
   - Renderiza dois Chart.js: linha (PIB) e barras (crescimento %)
   - Mostra spinner enquanto carrega e formata eixos em bilhões/trilhões
*/

async function fetchSidraValues() {
  // endpoint 'values' retorna uma matriz cujo primeiro elemento costuma ser cabeçalho
  const sidraUrl = 'https://apisidra.ibge.gov.br/values/t/6784/n1/1/v/9808/p/all';
  try {
    const r = await fetch(sidraUrl);
    if (!r.ok) throw new Error('Sidra não respondeu: ' + r.status);
    const data = await r.json();
    if (!Array.isArray(data) || data.length < 2) throw new Error('Resposta Sidra inesperada');

    const headers = data[0];
    const rows = data.slice(1);

    // headers pode ser um array de strings; rows normalmente arrays com mesmos índices
    if (Array.isArray(headers) && Array.isArray(rows[0])) {
      const parsed = rows.map(rw => {
        const obj = {};
        for (let i = 0; i < headers.length; i++) {
          obj[headers[i]] = rw[i];
        }
        return obj;
      });

      // Tentar detectar colunas com ano e valor
      const keys = Object.keys(parsed[0]);
  let yearKey = keys.find(k => /ano|periodo|periodo\.ano|period/i.test(k.toLowerCase())) || keys.find(k => /periodo|V3|D1C/i.test(k));
  let valueKey = keys.find(k => /valor|v|value|dado|valor\.pib/i.test(k)) || keys.find(k => /v3|d1c|v/i.test(k));

      // Se não encontrou, tentar heurística: primeira coluna numérica como ano, última como valor
      if (!yearKey) yearKey = keys.find(k => !isNaN(Number(parsed[0][k])));
      if (!valueKey) valueKey = keys[keys.length - 1];

      const out = parsed.map(p => ({ ano: Number(p[yearKey]), pib: Number(String(p[valueKey]).replace(',','.')) }));
      const clean = out.filter(x => !isNaN(x.ano) && !isNaN(x.pib));
      if (clean.length) return clean;
    }

    // Se a estrutura for diferente (objetos), tentar mapear diretamente
    if (typeof data[1] === 'object' && !Array.isArray(data[1])) {
      const parsed = data.slice(1).map(obj => obj);
      // procurar chaves possíveis
      const keys = Object.keys(parsed[0]);
      const yearKey = keys.find(k => /ano|periodo|year/i.test(k.toLowerCase()));
      const valueKey = keys.find(k => /valor|value|v/i.test(k.toLowerCase()));
      if (yearKey && valueKey) {
        const out = parsed.map(p => ({ ano: Number(p[yearKey]), pib: Number(String(p[valueKey]).replace(',','.')) }));
        return out.filter(x => !isNaN(x.ano) && !isNaN(x.pib));
      }
    }

    throw new Error('Não foi possível mapear resposta Sidra');
  } catch (e) {
    console.warn('Sidra falhou ou retornou formato inesperado:', e.message);
    return null;
  }
}

async function fetchCsvFallback() {
  try {
    const csvUrl = 'https://raw.githubusercontent.com/datasets-brasil/pib/master/pib_ano.csv';
    const r = await fetch(csvUrl);
    if (!r.ok) throw new Error('CSV fallback não respondeu: ' + r.status);
    const text = await r.text();
    const lines = text.trim().split('\n');
    const headers = lines.shift().split(',').map(h => h.trim().toLowerCase());
    const anoIdx = headers.indexOf('ano');
    const pibIdx = headers.indexOf('pib');
    const data = lines.map(l => {
      const cols = l.split(',');
      return { ano: Number(cols[anoIdx]), pib: Number(cols[pibIdx]) };
    }).filter(d => !isNaN(d.ano) && !isNaN(d.pib));
    return data;
  } catch (e) {
    console.error('Erro ao carregar fallback CSV:', e.message);
    return [];
  }
}

function formatLarge(value) {
  // Formata números em escala com sufixo (K, M, B, T) e separador de mil
  const abs = Math.abs(value);
  if (abs >= 1e12) return (value / 1e12).toFixed(2) + ' T';
  if (abs >= 1e9) return (value / 1e9).toFixed(2) + ' B';
  if (abs >= 1e6) return (value / 1e6).toFixed(2) + ' M';
  if (abs >= 1e3) return (value / 1e3).toFixed(2) + ' K';
  return value.toLocaleString();
}

function createChartLine(ctx, labels, data) {
  return new Chart(ctx, {
    type: 'line',
    data: { labels, datasets: [{ label: 'PIB (R$)', data, borderColor: '#2b8cbe', backgroundColor: 'rgba(43,140,190,0.12)', tension: 0.25, pointRadius: 3 }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: ctx => 'R$ ' + formatLarge(ctx.parsed.y) } } },
      scales: { y: { ticks: { callback: val => formatLarge(val) } } }
    }
  });
}

function createChartBar(ctx, labels, data) {
  return new Chart(ctx, {
    type: 'bar',
    data: { labels, datasets: [{ label: 'Crescimento (%)', data, backgroundColor: data.map(v => v >= 0 ? 'rgba(102,194,165,0.9)' : 'rgba(239,138,98,0.9)') }] },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { tooltip: { callbacks: { label: ctx => ctx.dataset.label + ': ' + ctx.parsed.y.toFixed(2) + '%' } } },
      scales: { y: { ticks: { callback: v => v.toFixed(2) + '%' } } }
    }
  });
}

function computeGrowth(sorted) {
  const growth = [];
  for (let i = 1; i < sorted.length; i++) {
    const prev = sorted[i - 1].pib;
    const cur = sorted[i].pib;
    const val = prev !== 0 ? ((cur - prev) / prev) * 100 : 0;
    growth.push({ ano: sorted[i].ano, growth: val });
  }
  return growth;
}

async function renderAll() {
  const spinner = document.getElementById('pib-spinner');
  spinner.style.display = 'block';

  let data = await fetchSidraValues();
  if (!data || data.length === 0) data = await fetchCsvFallback();

  spinner.style.display = 'none';

  if (!data || data.length === 0) {
    const el = document.getElementById('no-data');
    if (el) el.style.display = 'block';
    return;
  }

  const sorted = data.sort((a, b) => a.ano - b.ano);
  const labels = sorted.map(d => String(d.ano));
  const values = sorted.map(d => d.pib);

  const ctx1 = document.getElementById('chart-pib-ano').getContext('2d');
  createChartLine(ctx1, labels, values);

  const growth = computeGrowth(sorted);
  const labelsG = growth.map(g => String(g.ano));
  const valuesG = growth.map(g => Number(g.growth.toFixed(2)));

  const ctx2 = document.getElementById('chart-crescimento').getContext('2d');
  createChartBar(ctx2, labelsG, valuesG);
}

// Executa no carregamento da página
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', renderAll);
} else {
  renderAll();
}
