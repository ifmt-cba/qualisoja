/**
 * QualiSoja - Módulo de Gráficos de Relatórios
 * 
 * Este módulo contém as funções necessárias para criar e gerenciar os gráficos
 * de proteína e umidade no sistema QualiSoja.
 * 
 * @author QualiSoja Team
 * @version 1.2.0
 * @since 2023-01-01
 * @license MIT
 */

// Configurações globais para Chart.js
Chart.defaults.font.family = "'Roboto', 'Helvetica', 'Arial', sans-serif";
Chart.defaults.color = '#555';

// Objeto para armazenar gráficos - facilita referência e atualização
const chartInstances = {
    proteina: {
        time: null,
        tipo: null
    },
    umidade: {
        time: null,
        tipo: null
    },
    oleoDegomado: {
        acidez: null,
        tipo: null
    }
};

// Inicializa os gráficos quando o documento estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    try {
        console.log('Inicializando módulo de gráficos QualiSoja');
        initRelatorioCharts();
    } catch (err) {
        console.error('Erro ao inicializar gráficos:', err);
        mostrarErroGrafico('Ocorreu um erro ao inicializar os gráficos. Por favor, recarregue a página.');
    }
});

/**
 * Inicializa todos os gráficos do relatório
 * @throws {Error} Se ocorrer um erro durante a inicialização
 */
function initRelatorioCharts() {
    // Configurações comuns para gráficos de linha (evolução temporal)
    const commonTimeOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Evolução dos resultados ao longo do tempo'
            },
            tooltip: {
                mode: 'index',
                intersect: false,
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed.y !== null) {
                            label += context.parsed.y.toFixed(2) + '%';
                        }
                        return label;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Percentual (%)'
                }
            },
            x: {
                title: {
                    display: true,
                    text: 'Data'
                }
            }
        },
        interaction: {
            intersect: false,
            mode: 'index'
        }
    };

    // Renderiza gráficos de proteína
    renderProteinaCharts(commonTimeOptions);

    // Renderiza gráficos de umidade
    renderUmidadeCharts(commonTimeOptions);
    
    // Renderiza gráficos de óleo degomado
    renderOleoDegomadoCharts(commonTimeOptions);
}

/**
 * Exibe uma mensagem de erro na interface
 * @param {string} mensagem - Mensagem de erro a ser exibida
 */
function mostrarErroGrafico(mensagem) {
    const containers = document.querySelectorAll('.chart-container');
    
    containers.forEach(container => {
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle"></i> ${mensagem}
            </div>
        `;
    });
}

/**
 * Formata um número como percentual com duas casas decimais
 * @param {number} valor - Valor a ser formatado
 * @param {number} [casasDecimais=2] - Número de casas decimais
 * @returns {number} Valor formatado como número
 */
function formatarPercentual(valor, casasDecimais = 2) {
    if (valor === null || valor === undefined || isNaN(parseFloat(valor))) {
        return 0;
    }
    
    return parseFloat(parseFloat(valor).toFixed(casasDecimais));
}

/**
 * Renderiza os gráficos de proteína
 * @param {Object} commonTimeOptions - Opções comuns para gráficos de linha
 */
function renderProteinaCharts(commonTimeOptions) {
    // Obter e processar dados de proteína
    let proteinaData = [];
    
    try {
        const proteinaJsonElement = document.getElementById('proteina-data');
        if (!proteinaJsonElement) {
            console.warn('Elemento com ID "proteina-data" não encontrado');
            return;
        }
        
        const jsonStr = proteinaJsonElement.textContent.trim();
        if (!jsonStr) {
            console.warn('Dados de proteína vazios');
            return;
        }
        
        proteinaData = JSON.parse(jsonStr);
        
        if (!Array.isArray(proteinaData)) {
            console.error('Dados de proteína não estão em formato de array');
            return;
        }
    } catch (e) {
        console.error("Erro ao processar dados de proteína:", e);
        mostrarErroGrafico('Erro ao processar dados de proteína. Formato inválido.');
        return;
    }

    if (!proteinaData || proteinaData.length === 0) {
        console.warn('Nenhum dado de proteína disponível');
        return;
    }

    // Estatísticas de proteína
    renderProteinaStats(proteinaData);

    // Gráfico de evolução temporal de proteína
    renderProteinaTimeChart(proteinaData, commonTimeOptions);
    
    // Gráfico de tipos de amostra de proteína
    renderProteinaTipoChart(proteinaData);
}

/**
 * Renderiza estatísticas para dados de proteína
 * @param {Array} data - Dados de proteína
 */
function renderProteinaStats(data) {
    const statsDiv = document.getElementById('proteina-stats');
    if (!statsDiv) return;
    
    // Calcular estatísticas
    const valores = data.map(item => parseFloat(item.resultado_corrigido || 0))
                        .filter(val => !isNaN(val));
    
    if (valores.length === 0) {
        statsDiv.innerHTML = '<div class="alert alert-warning">Sem dados para calcular estatísticas</div>';
        return;
    }
    
    const stats = calcularEstatisticas(valores);
    
    statsDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-primary text-white">
                <h5 class="mb-0">Estatísticas de Proteína</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Média:</span>
                            <span class="stat-value">${stats.media.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Mínimo:</span>
                            <span class="stat-value">${stats.minimo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Máximo:</span>
                            <span class="stat-value">${stats.maximo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Desvio Padrão:</span>
                            <span class="stat-value">${stats.desvioPadrao.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Renderiza o gráfico de evolução temporal de proteína
 * @param {Array} data - Dados de proteína
 * @param {Object} options - Opções do gráfico
 */
function renderProteinaTimeChart(data, options) {
    const chartCanvas = document.getElementById('proteinaTimeChart');
    if (!chartCanvas) return;
    
    const proteinaTimeData = groupByDate(data, 'data', 'resultado_corrigido');
    const proteinaTimeLabels = proteinaTimeData.map(item => item.x);
    const proteinaTimeValues = proteinaTimeData.map(item => item.y);
    
    if (proteinaTimeLabels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico temporal</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.proteina.time) {
        chartInstances.proteina.time.destroy();
    }
    
    chartInstances.proteina.time = new Chart(
        chartCanvas,
        {
            type: 'line',
            data: {
                labels: proteinaTimeLabels,
                datasets: [{
                    label: 'Proteína (%)',
                    data: proteinaTimeValues,
                    borderColor: 'rgba(0, 123, 255, 1)',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    fill: true,
                    tension: 0.2
                }]
            },
            options: options
        }
    );
}

/**
 * Renderiza o gráfico de tipos de amostra de proteína
 * @param {Array} data - Dados de proteína
 */
function renderProteinaTipoChart(data) {
    const chartCanvas = document.getElementById('proteinaTipoChart');
    if (!chartCanvas) return;
    
    const proteinaTipoGrouped = groupByTipo(data, 'tipo', 'resultado_corrigido');
    
    if (proteinaTipoGrouped.labels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico de tipos</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.proteina.tipo) {
        chartInstances.proteina.tipo.destroy();
    }
    
    chartInstances.proteina.tipo = new Chart(
        chartCanvas,
        {
            type: 'bar',
            data: {
                labels: proteinaTipoGrouped.labels,
                datasets: [{
                    label: 'Média por tipo (%)',
                    data: proteinaTipoGrouped.data,
                    backgroundColor: [
                        'rgba(0, 123, 255, 0.7)',
                        'rgba(23, 162, 184, 0.7)',
                        'rgba(40, 167, 69, 0.7)',
                        'rgba(255, 193, 7, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Média por tipo de amostra'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y.toFixed(2) + '%';
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentual (%)'
                        }
                    }
                }
            }
        }
    );
}

/**
 * Renderiza os gráficos de umidade
 * @param {Object} commonTimeOptions - Opções comuns para gráficos de linha
 */
function renderUmidadeCharts(commonTimeOptions) {
    // Obter e processar dados de umidade
    let umidadeData = [];
    
    try {
        const umidadeJsonElement = document.getElementById('umidade-data');
        if (!umidadeJsonElement) {
            console.warn('Elemento com ID "umidade-data" não encontrado');
            return;
        }
        
        const jsonStr = umidadeJsonElement.textContent.trim();
        if (!jsonStr) {
            console.warn('Dados de umidade vazios');
            return;
        }
        
        umidadeData = JSON.parse(jsonStr);
        
        if (!Array.isArray(umidadeData)) {
            console.error('Dados de umidade não estão em formato de array');
            return;
        }
    } catch (e) {
        console.error("Erro ao processar dados de umidade:", e);
        mostrarErroGrafico('Erro ao processar dados de umidade. Formato inválido.');
        return;
    }

    if (!umidadeData || umidadeData.length === 0) {
        console.warn('Nenhum dado de umidade disponível');
        return;
    }

    // Estatísticas de umidade
    renderUmidadeStats(umidadeData);

    // Gráfico de evolução temporal de umidade
    renderUmidadeTimeChart(umidadeData, commonTimeOptions);
    
    // Gráfico de tipos de amostra de umidade
    renderUmidadeTipoChart(umidadeData);
}

/**
 * Renderiza estatísticas para dados de umidade
 * @param {Array} data - Dados de umidade
 */
function renderUmidadeStats(data) {
    const statsDiv = document.getElementById('umidade-stats');
    if (!statsDiv) return;
    
    // Calcular estatísticas
    const valores = data.map(item => parseFloat(item.resultado || 0))
                        .filter(val => !isNaN(val));
    
    if (valores.length === 0) {
        statsDiv.innerHTML = '<div class="alert alert-warning">Sem dados para calcular estatísticas</div>';
        return;
    }
    
    const stats = calcularEstatisticas(valores);
    
    statsDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-success text-white">
                <h5 class="mb-0">Estatísticas de Umidade</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Média:</span>
                            <span class="stat-value">${stats.media.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Mínimo:</span>
                            <span class="stat-value">${stats.minimo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Máximo:</span>
                            <span class="stat-value">${stats.maximo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-3">
                        <div class="stat-item">
                            <span class="stat-label">Desvio Padrão:</span>
                            <span class="stat-value">${stats.desvioPadrao.toFixed(2)}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Renderiza o gráfico de evolução temporal de umidade
 * @param {Array} data - Dados de umidade
 * @param {Object} options - Opções do gráfico
 */
function renderUmidadeTimeChart(data, options) {
    const chartCanvas = document.getElementById('umidadeTimeChart');
    if (!chartCanvas) return;
    
    const umidadeTimeData = groupByDate(data, 'data', 'resultado');
    const umidadeTimeLabels = umidadeTimeData.map(item => item.x);
    const umidadeTimeValues = umidadeTimeData.map(item => item.y);
    
    if (umidadeTimeLabels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico temporal</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.umidade.time) {
        chartInstances.umidade.time.destroy();
    }
    
    chartInstances.umidade.time = new Chart(
        chartCanvas,
        {
            type: 'line',
            data: {
                labels: umidadeTimeLabels,
                datasets: [{
                    label: 'Umidade (%)',
                    data: umidadeTimeValues,
                    borderColor: 'rgba(40, 167, 69, 1)',
                    backgroundColor: 'rgba(40, 167, 69, 0.1)',
                    fill: true,
                    tension: 0.2
                }]
            },
            options: options
        }
    );
}

/**
 * Renderiza o gráfico de tipos de amostra de umidade
 * @param {Array} data - Dados de umidade
 */
function renderUmidadeTipoChart(data) {
    const chartCanvas = document.getElementById('umidadeTipoChart');
    if (!chartCanvas) return;
    
    const umidadeTipoGrouped = groupByTipo(data, 'tipo', 'resultado');
    
    if (umidadeTipoGrouped.labels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico de tipos</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.umidade.tipo) {
        chartInstances.umidade.tipo.destroy();
    }
    
    chartInstances.umidade.tipo = new Chart(
        chartCanvas,
        {
            type: 'bar',
            data: {
                labels: umidadeTipoGrouped.labels,
                datasets: [{
                    label: 'Média por tipo (%)',
                    data: umidadeTipoGrouped.data,
                    backgroundColor: [
                        'rgba(40, 167, 69, 0.7)',
                        'rgba(23, 162, 184, 0.7)',
                        'rgba(0, 123, 255, 0.7)',
                        'rgba(255, 193, 7, 0.7)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Média por tipo de amostra'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y.toFixed(2) + '%';
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Percentual (%)'
                        }
                    }
                }
            }
        }
    );
}

/**
 * Renderiza os gráficos de óleo degomado
 * @param {Object} commonTimeOptions - Opções comuns para gráficos de linha
 */
function renderOleoDegomadoCharts(commonTimeOptions) {
    // Obter e processar dados de óleo degomado
    let oleoDegomadoData = [];
    
    try {
        const oleoJsonElement = document.getElementById('oleo-degomado-data');
        if (!oleoJsonElement) {
            console.warn('Elemento com ID "oleo-degomado-data" não encontrado');
            return;
        }
        
        const jsonStr = oleoJsonElement.textContent.trim();
        if (!jsonStr) {
            console.warn('Dados de óleo degomado vazios');
            return;
        }
        
        oleoDegomadoData = JSON.parse(jsonStr);
        
        if (!Array.isArray(oleoDegomadoData)) {
            console.error('Dados de óleo degomado não estão em formato de array');
            return;
        }
    } catch (e) {
        console.error("Erro ao processar dados de óleo degomado:", e);
        mostrarErroGrafico('Erro ao processar dados de óleo degomado. Formato inválido.');
        return;
    }

    if (!oleoDegomadoData || oleoDegomadoData.length === 0) {
        console.warn('Nenhum dado de óleo degomado disponível');
        return;
    }

    // Estatísticas de óleo degomado
    renderOleoDegomadoStats(oleoDegomadoData);

    // Gráfico de evolução da acidez ao longo do tempo
    renderOleoAcidezTimeChart(oleoDegomadoData, commonTimeOptions);
    
    // Gráfico de tipos de amostra de óleo
    renderOleoTipoChart(oleoDegomadoData);
}

/**
 * Renderiza estatísticas para dados de óleo degomado
 * @param {Array} data - Dados de óleo degomado
 */
function renderOleoDegomadoStats(data) {
    const statsDiv = document.getElementById('oleo-degomado-stats');
    if (!statsDiv) return;
    
    // Calcular estatísticas para acidez, umidade e impurezas
    const acidezValues = data.map(item => parseFloat(item.acidez || 0))
                            .filter(val => !isNaN(val));
    const umidadeValues = data.map(item => parseFloat(item.umidade || 0))
                             .filter(val => !isNaN(val));
    const impurezasValues = data.map(item => parseFloat(item.impurezas || 0))
                               .filter(val => !isNaN(val));
    
    if (acidezValues.length === 0 && umidadeValues.length === 0 && impurezasValues.length === 0) {
        statsDiv.innerHTML = '<div class="alert alert-warning">Sem dados para calcular estatísticas</div>';
        return;
    }
    
    const acidezStats = calcularEstatisticas(acidezValues);
    const umidadeStats = calcularEstatisticas(umidadeValues);
    const impurezasStats = calcularEstatisticas(impurezasValues);
    
    statsDiv.innerHTML = `
        <div class="card">
            <div class="card-header bg-warning text-white">
                <h5 class="mb-0">Estatísticas do Óleo Degomado</h5>
            </div>
            <div class="card-body">
                <div class="row mb-3">
                    <div class="col-md-4">
                        <h6 class="text-danger">Acidez (%)</h6>
                        <div class="stat-item">
                            <span class="stat-label">Média:</span>
                            <span class="stat-value">${acidezStats.media.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Mínimo:</span>
                            <span class="stat-value">${acidezStats.minimo.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Máximo:</span>
                            <span class="stat-value">${acidezStats.maximo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <h6 class="text-info">Umidade (%)</h6>
                        <div class="stat-item">
                            <span class="stat-label">Média:</span>
                            <span class="stat-value">${umidadeStats.media.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Mínimo:</span>
                            <span class="stat-value">${umidadeStats.minimo.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Máximo:</span>
                            <span class="stat-value">${umidadeStats.maximo.toFixed(2)}%</span>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <h6 class="text-secondary">Impurezas (%)</h6>
                        <div class="stat-item">
                            <span class="stat-label">Média:</span>
                            <span class="stat-value">${impurezasStats.media.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Mínimo:</span>
                            <span class="stat-value">${impurezasStats.minimo.toFixed(2)}%</span>
                        </div>
                        <div class="stat-item">
                            <span class="stat-label">Máximo:</span>
                            <span class="stat-value">${impurezasStats.maximo.toFixed(2)}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

/**
 * Renderiza o gráfico de evolução da acidez ao longo do tempo
 * @param {Array} data - Dados de óleo degomado
 * @param {Object} options - Opções do gráfico
 */
function renderOleoAcidezTimeChart(data, options) {
    const chartCanvas = document.getElementById('oleoAcidezTimeChart');
    if (!chartCanvas) return;
    
    const acidezTimeData = groupByDate(data, 'data', 'acidez');
    const acidezTimeLabels = acidezTimeData.map(item => item.x);
    const acidezTimeValues = acidezTimeData.map(item => item.y);
    
    if (acidezTimeLabels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico temporal</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.oleoDegomado.acidez) {
        chartInstances.oleoDegomado.acidez.destroy();
    }
    
    chartInstances.oleoDegomado.acidez = new Chart(
        chartCanvas,
        {
            type: 'line',
            data: {
                labels: acidezTimeLabels,
                datasets: [{
                    label: 'Acidez (%)',
                    data: acidezTimeValues,
                    borderColor: 'rgba(220, 53, 69, 1)',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: true,
                    tension: 0.2
                }]
            },
            options: {
                ...options,
                plugins: {
                    ...options.plugins,
                    title: {
                        display: true,
                        text: 'Evolução da Acidez ao Longo do Tempo'
                    }
                }
            }
        }
    );
}

/**
 * Renderiza o gráfico de tipos de amostra de óleo
 * @param {Array} data - Dados de óleo degomado
 */
function renderOleoTipoChart(data) {
    const chartCanvas = document.getElementById('oleoTipoChart');
    if (!chartCanvas) return;
    
    const oleoTipoGrouped = groupByTipo(data, 'tipo_amostra', 'acidez');
    
    if (oleoTipoGrouped.labels.length === 0) {
        chartCanvas.parentNode.innerHTML = '<div class="alert alert-warning">Sem dados suficientes para o gráfico de tipos</div>';
        return;
    }
    
    // Se já existe um gráfico, destrua-o antes de criar um novo
    if (chartInstances.oleoDegomado.tipo) {
        chartInstances.oleoDegomado.tipo.destroy();
    }
    
    chartInstances.oleoDegomado.tipo = new Chart(
        chartCanvas,
        {
            type: 'doughnut',
            data: {
                labels: oleoTipoGrouped.labels,
                datasets: [{
                    label: 'Análises por tipo',
                    data: oleoTipoGrouped.data,
                    backgroundColor: [
                        'rgba(255, 193, 7, 0.8)',  // Amarelo
                        'rgba(220, 53, 69, 0.8)',  // Vermelho
                        'rgba(40, 167, 69, 0.8)',  // Verde
                        'rgba(0, 123, 255, 0.8)'   // Azul
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    title: {
                        display: true,
                        text: 'Distribuição por Tipo de Amostra'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} análises (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        }
    );
}

/**
 * Calcula estatísticas básicas para um conjunto de valores numéricos
 * @param {Array<number>} valores - Array de valores numéricos
 * @returns {Object} Objeto com estatísticas (media, mediana, minimo, maximo, desvioPadrao)
 */
function calcularEstatisticas(valores) {
    if (!valores || valores.length === 0) {
        return {
            media: 0,
            mediana: 0,
            minimo: 0,
            maximo: 0,
            desvioPadrao: 0
        };
    }
    
    // Filtrar valores válidos
    const valoresValidos = valores.filter(v => v !== null && v !== undefined && !isNaN(v));
    
    if (valoresValidos.length === 0) {
        return {
            media: 0,
            mediana: 0,
            minimo: 0,
            maximo: 0,
            desvioPadrao: 0
        };
    }
    
    // Ordenar valores para cálculo da mediana
    const valoresOrdenados = [...valoresValidos].sort((a, b) => a - b);
    
    // Calcular estatísticas
    const soma = valoresValidos.reduce((acc, val) => acc + val, 0);
    const media = soma / valoresValidos.length;
    const minimo = valoresOrdenados[0];
    const maximo = valoresOrdenados[valoresOrdenados.length - 1];
    
    // Calcular mediana
    const meio = Math.floor(valoresOrdenados.length / 2);
    const mediana = valoresOrdenados.length % 2 === 0 
        ? (valoresOrdenados[meio - 1] + valoresOrdenados[meio]) / 2
        : valoresOrdenados[meio];
    
    // Calcular desvio padrão
    const somaDosQuadradosDasDiferencas = valoresValidos.reduce((acc, val) => {
        const diff = val - media;
        return acc + (diff * diff);
    }, 0);
    
    const desvioPadrao = Math.sqrt(somaDosQuadradosDasDiferencas / valoresValidos.length);
    
    return {
        media,
        mediana,
        minimo,
        maximo,
        desvioPadrao
    };
}

/**
 * Função base para agrupar dados por um campo e calcular média de outro campo
 * @param {Array} data - Array de objetos com dados
 * @param {string} keyField - Campo para agrupar
 * @param {string} valueField - Campo para calcular valor médio
 * @returns {Object} - Mapa de chaves para objetos com soma e contagem
 * @private
 */
function _groupData(data, keyField, valueField) {
    if (!Array.isArray(data) || data.length === 0) {
        return {};
    }
    
    const groupedData = {};
    
    data.forEach(item => {
        if (!item || typeof item !== 'object') return;
        
        const key = item[keyField];
        if (key === undefined || key === null) return;
        
        if (!groupedData[key]) {
            groupedData[key] = {
                sum: 0,
                count: 0,
                values: []
            };
        }
        
        const value = parseFloat(item[valueField] || 0);
        if (!isNaN(value)) {
            groupedData[key].sum += value;
            groupedData[key].count += 1;
            groupedData[key].values.push(value);
        }
    });
    
    return groupedData;
}

/**
 * Função para agrupar dados por data e calcular média
 * @param {Array} data - Array de objetos com dados
 * @param {string} keyField - Campo que contém a data
 * @param {string} valueField - Campo que contém o valor a ser calculado
 * @returns {Array} - Array de objetos com x (data) e y (valor médio)
 */
function groupByDate(data, keyField, valueField) {
    const groupedData = _groupData(data, keyField, valueField);
    
    const result = Object.keys(groupedData).map(date => {
        const group = groupedData[date];
        return {
            x: date,
            y: formatarPercentual(group.sum / group.count)
        };
    });
    
    // Ordenar por data
    return result.sort((a, b) => a.x.localeCompare(b.x));
}

/**
 * Função para agrupar dados por tipo e calcular média
 * @param {Array} data - Array de objetos com dados
 * @param {string} tipoField - Campo que contém o tipo
 * @param {string} valueField - Campo que contém o valor a ser calculado
 * @returns {Object} - Objeto com labels (tipos) e data (valores médios)
 */
function groupByTipo(data, tipoField, valueField) {
    const groupedData = _groupData(data, tipoField, valueField);
    
    if (Object.keys(groupedData).length === 0) {
        return { labels: [], data: [] };
    }
    
    return {
        labels: Object.keys(groupedData),
        data: Object.keys(groupedData).map(tipo => {
            const group = groupedData[tipo];
            return formatarPercentual(group.sum / group.count);
        })
    };
}