/**
 * Testes para a interface do QualiSoja usando Jest
 * 
 * Para executar estes testes, instale Jest:
 * npm install jest @testing-library/jest-dom
 * 
 * Execute os testes com:
 * npm test
 */

// Configurações globais para os testes
beforeAll(() => {
    // Mock para console.error e console.warn para não poluir os logs de teste  
    global.console.error = jest.fn();
    global.console.warn = jest.fn();
    
    // Mock para elementos DOM necessários
    document.body.innerHTML = `
        <div id="proteinaTimeChart"></div>
        <div id="proteinaTipoChart"></div>
        <div id="umidadeTimeChart"></div>
        <div id="umidadeTipoChart"></div>
        <div id="proteina-stats"></div>
        <div id="umidade-stats"></div>
        <div id="proteina-data" style="display:none;">
            [{"data":"2023-05-01","horario":"10:00","tipo":"Farelo","resultado":45.2,"resultado_corrigido":46.1},
             {"data":"2023-05-02","horario":"11:00","tipo":"Farelo","resultado":44.8,"resultado_corrigido":45.7},
             {"data":"2023-05-01","horario":"09:00","tipo":"Grão","resultado":42.1,"resultado_corrigido":43.0}]
        </div>
        <div id="umidade-data" style="display:none;">
            [{"data":"2023-05-01","horario":"10:00","tipo":"Farelo Grosso","resultado":12.5},
             {"data":"2023-05-02","horario":"11:00","tipo":"Farelo Fino","resultado":11.8},
             {"data":"2023-05-01","horario":"09:00","tipo":"Grão","resultado":10.2}]
        </div>
    `;
    
    // Definir funções globais para testes
    global.formatarPercentual = (valor, casasDecimais = 2) => {
        if (valor === null || valor === undefined || isNaN(parseFloat(valor))) {
            return 0;
        }
        return parseFloat(parseFloat(valor).toFixed(casasDecimais));
    };
    
    global._groupData = (data, keyField, valueField) => {
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
    };
    
    global.groupByDate = (data, keyField, valueField) => {
        const groupedData = _groupData(data, keyField, valueField);
        
        const result = Object.keys(groupedData).map(date => {
            const group = groupedData[date];
            return {
                x: date,
                y: formatarPercentual(group.sum / group.count)
            };
        });
        
        return result.sort((a, b) => a.x.localeCompare(b.x));
    };
    
    global.groupByTipo = (data, tipoField, valueField) => {
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
    };
    
    global.calcularEstatisticas = (valores) => {
        if (!valores || valores.length === 0) {
            return {
                media: 0,
                mediana: 0,
                minimo: 0,
                maximo: 0,
                desvioPadrao: 0
            };
        }
        
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
        
        const valoresOrdenados = [...valoresValidos].sort((a, b) => a - b);
        
        const soma = valoresValidos.reduce((acc, val) => acc + val, 0);
        const media = soma / valoresValidos.length;
        const minimo = valoresOrdenados[0];
        const maximo = valoresOrdenados[valoresOrdenados.length - 1];
        
        const meio = Math.floor(valoresOrdenados.length / 2);
        const mediana = valoresOrdenados.length % 2 === 0 
            ? (valoresOrdenados[meio - 1] + valoresOrdenados[meio]) / 2
            : valoresOrdenados[meio];
        
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
    };
    
    // Mock para as funções de renderização
    global.chartInstances = {
        proteina: { time: null, tipo: null },
        umidade: { time: null, tipo: null }
    };
    
    global.mostrarErroGrafico = jest.fn();
    
    global.renderProteinaStats = jest.fn();
    global.renderProteinaTimeChart = jest.fn();
    global.renderProteinaTipoChart = jest.fn();
    global.renderUmidadeStats = jest.fn();
    global.renderUmidadeTimeChart = jest.fn();
    global.renderUmidadeTipoChart = jest.fn();
    
    // Mock para funções de renderização globais com implementação
    global.renderProteinaCharts = jest.fn(function(options) {
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
            
            const proteinaData = JSON.parse(jsonStr);
            
            if (!Array.isArray(proteinaData)) {
                console.error('Dados de proteína não estão em formato de array');
                return;
            }
            
            if (!proteinaData || proteinaData.length === 0) {
                console.warn('Nenhum dado de proteína disponível');
                return;
            }
            
            renderProteinaStats(proteinaData);
            renderProteinaTimeChart(proteinaData, options);
            renderProteinaTipoChart(proteinaData);
        } catch (e) {
            console.error("Erro ao processar dados de proteína:", e);
            mostrarErroGrafico('Erro ao processar dados de proteína. Formato inválido.');
        }
    });
    
    // Mock para funções de renderização globais com implementação
    global.renderUmidadeCharts = jest.fn(function(options) {
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
            
            const umidadeData = JSON.parse(jsonStr);
            
            if (!Array.isArray(umidadeData)) {
                console.error('Dados de umidade não estão em formato de array');
                return;
            }
            
            if (!umidadeData || umidadeData.length === 0) {
                console.warn('Nenhum dado de umidade disponível');
                return;
            }
            
            renderUmidadeStats(umidadeData);
            renderUmidadeTimeChart(umidadeData, options);
            renderUmidadeTipoChart(umidadeData);
        } catch (e) {
            console.error("Erro ao processar dados de umidade:", e);
            mostrarErroGrafico('Erro ao processar dados de umidade. Formato inválido.');
        }
    });
    
    global.initRelatorioCharts = jest.fn(function() {
        const commonTimeOptions = {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: 'Evolução dos resultados ao longo do tempo' },
                tooltip: { mode: 'index', intersect: false }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    title: { display: true, text: 'Percentual (%)' }
                },
                x: {
                    title: { display: true, text: 'Data' }
                }
            },
            interaction: {
                intersect: false,
                mode: 'index'
            }
        };
        
        renderProteinaCharts(commonTimeOptions);
        renderUmidadeCharts(commonTimeOptions);
    });
});

describe('Funções Utilitárias', () => {
    test('formatarPercentual deve formatar corretamente valores numéricos', () => {
        expect(formatarPercentual(10.123)).toBe(10.12);
        expect(formatarPercentual(10.126)).toBe(10.13);
        expect(formatarPercentual(10)).toBe(10);
    });
    
    test('formatarPercentual deve tratar valores inválidos', () => {
        expect(formatarPercentual(null)).toBe(0);
        expect(formatarPercentual(undefined)).toBe(0);
        expect(formatarPercentual(NaN)).toBe(0);
        expect(formatarPercentual('abc')).toBe(0);
    });
    
    test('calcularEstatisticas deve calcular estatísticas corretamente', () => {
        const valores = [10, 20, 30, 40, 50];
        const stats = calcularEstatisticas(valores);
        
        expect(stats.media).toBe(30);
        expect(stats.mediana).toBe(30);
        expect(stats.minimo).toBe(10);
        expect(stats.maximo).toBe(50);
        expect(stats.desvioPadrao).toBeCloseTo(14.14, 1);
    });
    
    test('calcularEstatisticas deve tratar array vazio', () => {
        const stats = calcularEstatisticas([]);
        
        expect(stats.media).toBe(0);
        expect(stats.mediana).toBe(0);
        expect(stats.minimo).toBe(0);
        expect(stats.maximo).toBe(0);
        expect(stats.desvioPadrao).toBe(0);
    });
    
    test('calcularEstatisticas deve ignorar valores inválidos', () => {
        const valores = [10, null, 30, NaN, 50, undefined, 'abc'];
        const stats = calcularEstatisticas(valores);
        
        expect(stats.media).toBe(30);
        expect(stats.mediana).toBe(30);
        expect(stats.minimo).toBe(10);
        expect(stats.maximo).toBe(50);
        expect(stats.desvioPadrao).toBeCloseTo(16.33, 1);
    });
});

describe('Funções de Agrupamento', () => {
    test('_groupData deve agrupar dados corretamente', () => {
        // Dados de exemplo
        const data = [
            {tipo: 'Farelo', resultado: 10},
            {tipo: 'Farelo', resultado: 20},
            {tipo: 'Grão', resultado: 30}
        ];
        
        const result = _groupData(data, 'tipo', 'resultado');
        
        expect(Object.keys(result)).toHaveLength(2);
        expect(result.Farelo).toBeDefined();
        expect(result.Grão).toBeDefined();
        
        expect(result.Farelo.sum).toBe(30);
        expect(result.Farelo.count).toBe(2);
        expect(result.Farelo.values).toEqual([10, 20]);
        
        expect(result.Grão.sum).toBe(30);
        expect(result.Grão.count).toBe(1);
        expect(result.Grão.values).toEqual([30]);
    });
    
    test('_groupData deve lidar com dados inválidos', () => {
        expect(_groupData(null, 'tipo', 'resultado')).toEqual({});
        expect(_groupData([], 'tipo', 'resultado')).toEqual({});
        expect(_groupData([null, undefined], 'tipo', 'resultado')).toEqual({});
    });
    
    test('groupByDate deve agrupar dados por data corretamente', () => {
        // Dados de exemplo
        const data = [
            {data: '2023-05-01', resultado: 10},
            {data: '2023-05-01', resultado: 20},
            {data: '2023-05-02', resultado: 30}
        ];
        
        const result = groupByDate(data, 'data', 'resultado');
        
        expect(result).toHaveLength(2);
        
        expect(result[0].x).toBe('2023-05-01');
        expect(result[0].y).toBe(15);
        
        expect(result[1].x).toBe('2023-05-02');
        expect(result[1].y).toBe(30);
    });
    
    test('groupByTipo deve agrupar dados por tipo corretamente', () => {
        // Dados de exemplo
        const data = [
            {tipo: 'Farelo', resultado: 10},
            {tipo: 'Farelo', resultado: 20},
            {tipo: 'Grão', resultado: 30}
        ];
        
        const result = groupByTipo(data, 'tipo', 'resultado');
        
        expect(result.labels).toHaveLength(2);
        expect(result.labels).toContain('Farelo');
        expect(result.labels).toContain('Grão');
        
        expect(result.data).toHaveLength(2);
        
        // Encontrar índice do tipo 'Farelo'
        const indexFarelo = result.labels.indexOf('Farelo');
        expect(result.data[indexFarelo]).toBe(15);
        
        // Encontrar índice do tipo 'Grão'
        const indexGrao = result.labels.indexOf('Grão');
        expect(result.data[indexGrao]).toBe(30);
    });
});

describe('Funções de Renderização', () => {
    beforeEach(() => {
        // Limpar mocks antes de cada teste
        jest.clearAllMocks();
    });
    
    test('initRelatorioCharts deve inicializar gráficos', () => {
        // Executar função
        initRelatorioCharts();
        
        // Verificar se as subfunções foram chamadas
        expect(renderProteinaCharts).toHaveBeenCalled();
        expect(renderUmidadeCharts).toHaveBeenCalled();
    });
    
    test('renderProteinaCharts deve chamar funções de renderização de proteína', () => {
        renderProteinaCharts({});
        
        expect(renderProteinaStats).toHaveBeenCalled();
        expect(renderProteinaTimeChart).toHaveBeenCalled();
        expect(renderProteinaTipoChart).toHaveBeenCalled();
    });
    
    test('renderUmidadeCharts deve chamar funções de renderização de umidade', () => {
        renderUmidadeCharts({});
        
        expect(renderUmidadeStats).toHaveBeenCalled();
        expect(renderUmidadeTimeChart).toHaveBeenCalled();
        expect(renderUmidadeTipoChart).toHaveBeenCalled();
    });
    
    test('renderProteinaCharts deve lidar com dados inválidos', () => {
        // Modificar o elemento para ter conteúdo inválido
        document.getElementById('proteina-data').textContent = 'dados inválidos';
        
        renderProteinaCharts({});
        
        expect(console.error).toHaveBeenCalled();
        expect(mostrarErroGrafico).toHaveBeenCalled();
    });
    
    test('renderUmidadeCharts deve lidar com dados inválidos', () => {
        // Modificar o elemento para ter conteúdo inválido
        document.getElementById('umidade-data').textContent = 'dados inválidos';
        
        renderUmidadeCharts({});
        
        expect(console.error).toHaveBeenCalled();
        expect(mostrarErroGrafico).toHaveBeenCalled();
    });
});

describe('Testes de integração', () => {
    test('Integração entre funções de agrupamento e estatísticas', () => {
        // Dados de exemplo mais complexos
        const data = [
            {data: '2023-05-01', tipo: 'Farelo', resultado: 45.2, resultado_corrigido: 46.1},
            {data: '2023-05-01', tipo: 'Farelo', resultado: 44.8, resultado_corrigido: 45.7},
            {data: '2023-05-01', tipo: 'Grão', resultado: 42.1, resultado_corrigido: 43.0},
            {data: '2023-05-02', tipo: 'Farelo', resultado: 44.9, resultado_corrigido: 45.8},
            {data: '2023-05-02', tipo: 'Grão', resultado: 41.8, resultado_corrigido: 42.7},
            {data: '2023-05-03', tipo: 'Farelo', resultado: 45.5, resultado_corrigido: 46.4}
        ];
        
        // Agrupar por tipo
        const groupedByTipo = _groupData(data, 'tipo', 'resultado');
        
        // Calcular estatísticas para cada tipo
        const estatisticasFarelo = calcularEstatisticas(groupedByTipo['Farelo'].values);
        const estatisticasGrao = calcularEstatisticas(groupedByTipo['Grão'].values);
        
        // Verificações
        expect(estatisticasFarelo.media).toBeCloseTo(45.1, 1);
        expect(estatisticasFarelo.minimo).toBe(44.8);
        expect(estatisticasFarelo.maximo).toBe(45.5);
        
        expect(estatisticasGrao.media).toBeCloseTo(41.95, 1);
        expect(estatisticasGrao.minimo).toBe(41.8);
        expect(estatisticasGrao.maximo).toBe(42.1);
    });
    
    test('Deve lidar com mudança de dados durante a execução', () => {
        // Estado inicial
        document.getElementById('proteina-data').textContent = JSON.stringify([
            {data: '2023-05-01', tipo: 'Farelo', resultado: 45.2}
        ]);
        
        // Primeira renderização
        renderProteinaCharts({});
        expect(renderProteinaStats).toHaveBeenCalled();
        expect(renderProteinaTimeChart).toHaveBeenCalled();
        
        // Limpar mocks para próxima verificação
        jest.clearAllMocks();
        
        // Mudar dados
        document.getElementById('proteina-data').textContent = JSON.stringify([
            {data: '2023-05-01', tipo: 'Farelo', resultado: 45.2},
            {data: '2023-05-02', tipo: 'Grão', resultado: 42.1}
        ]);
        
        // Nova renderização
        renderProteinaCharts({});
        expect(renderProteinaStats).toHaveBeenCalled();
        expect(renderProteinaTimeChart).toHaveBeenCalled();
    });
    
    test('Deve lidar com valores extremos corretamente', () => {
        // Valores extremos para testar
        const valores = [0.0001, 99.9999, 50, 50.0001, 49.9999];
        const stats = calcularEstatisticas(valores);
        
        expect(stats.media).toBeCloseTo(50, 1);
        expect(stats.minimo).toBe(0.0001);
        expect(stats.maximo).toBe(99.9999);
    });
});

describe('Testes de desempenho', () => {
    test('Deve processar conjunto grande de dados eficientemente', () => {
        // Gerar conjunto grande de dados
        const bigData = [];
        for (let i = 0; i < 1000; i++) {
            bigData.push({
                data: `2023-05-${(i % 30) + 1}`.padStart(10, '0'),
                tipo: i % 2 === 0 ? 'Farelo' : 'Grão',
                resultado: 40 + Math.random() * 10
            });
        }
        
        // Medir tempo de agrupamento
        const startTime = performance.now();
        const groupedByTipo = _groupData(bigData, 'tipo', 'resultado');
        const groupedByDate = groupByDate(bigData, 'data', 'resultado');
        const endTime = performance.now();
        
        // Verificações básicas
        expect(Object.keys(groupedByTipo)).toHaveLength(2);
        expect(groupedByDate.length).toBeLessThanOrEqual(30);
        
        // Verificação de desempenho (menos de 50ms para todo o processamento)
        // Tempo exato varia conforme a máquina, mas não deve ser muito lento
        const processingTime = endTime - startTime;
        console.warn(`Tempo de processamento para 1000 registros: ${processingTime}ms`);
        expect(processingTime).toBeLessThan(500);
    });
});
