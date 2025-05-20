// Configuração global para os testes Jest

// Mock do objeto global para Chart.js
global.Chart = class Chart {
  constructor() {
      this.data = {};
      this.options = {};
      this.type = null;
  }
  
  destroy() {
      // Mock para método destroy
  }
};

// Mock para objeto window necessário para Chart.js
if (typeof window === 'undefined') {
    global.window = {};
}

// Mock para document, caso seja necessário
if (typeof document === 'undefined') {
    global.document = {
        createElement: () => ({
            getContext: () => ({})
        }),
        body: {
            appendChild: () => {}
        }
    };
}

// Mock para console para evitar poluição nos logs de teste
global.console.error = jest.fn();
global.console.warn = jest.fn();
global.console.info = jest.fn();
