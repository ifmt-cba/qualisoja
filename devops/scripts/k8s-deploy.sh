#!/bin/bash

# QualiSoja Kubernetes Deploy Script
# Este script facilita o deploy da aplicação no Kubernetes

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurações
NAMESPACE="qualisoja"
RELEASE_NAME="qualisoja"
HELM_CHART="./devops/kubernetes/helm"

# Funções auxiliares
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Verificar dependências
check_dependencies() {
    log_info "Verificando dependências..."
    
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl não encontrado. Instale kubectl primeiro."
        exit 1
    fi
    
    if ! command -v helm &> /dev/null; then
        log_error "helm não encontrado. Instale helm primeiro."
        exit 1
    fi
    
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Não é possível conectar ao cluster Kubernetes."
        exit 1
    fi
    
    log_success "Dependências verificadas com sucesso"
}

# Criar namespace se não existir
create_namespace() {
    log_info "Verificando namespace $NAMESPACE..."
    
    if ! kubectl get namespace $NAMESPACE &> /dev/null; then
        log_info "Criando namespace $NAMESPACE..."
        kubectl create namespace $NAMESPACE
        log_success "Namespace $NAMESPACE criado"
    else
        log_info "Namespace $NAMESPACE já existe"
    fi
}

# Deploy com manifests brutos
deploy_manifests() {
    log_info "Aplicando manifests Kubernetes..."
    
    if [ -d "./devops/kubernetes/manifests" ]; then
        kubectl apply -f ./devops/kubernetes/manifests/ -n $NAMESPACE
        log_success "Manifests aplicados com sucesso"
    else
        log_error "Diretório de manifests não encontrado"
        exit 1
    fi
}

# Deploy com Helm
deploy_helm() {
    log_info "Fazendo deploy com Helm..."
    
    # Verificar se o chart existe
    if [ ! -f "$HELM_CHART/Chart.yaml" ]; then
        log_error "Helm chart não encontrado em $HELM_CHART"
        exit 1
    fi
    
    # Adicionar repositórios necessários
    log_info "Adicionando repositórios Helm..."
    helm repo add bitnami https://charts.bitnami.com/bitnami
    helm repo update
    
    # Fazer deploy ou upgrade
    if helm list -n $NAMESPACE | grep -q $RELEASE_NAME; then
        log_info "Atualizando release existente..."
        helm upgrade $RELEASE_NAME $HELM_CHART \
            --namespace $NAMESPACE \
            --timeout 10m \
            --wait
    else
        log_info "Instalando nova release..."
        helm install $RELEASE_NAME $HELM_CHART \
            --namespace $NAMESPACE \
            --create-namespace \
            --timeout 10m \
            --wait
    fi
    
    log_success "Deploy com Helm concluído"
}

# Verificar status do deployment
check_status() {
    log_info "Verificando status do deployment..."
    
    echo -e "\n📊 Status dos Pods:"
    kubectl get pods -n $NAMESPACE
    
    echo -e "\n🔗 Services:"
    kubectl get services -n $NAMESPACE
    
    echo -e "\n🌐 Ingress:"
    kubectl get ingress -n $NAMESPACE
    
    # Verificar se todos os pods estão rodando
    local ready_pods=$(kubectl get pods -n $NAMESPACE --no-headers | grep "Running" | wc -l)
    local total_pods=$(kubectl get pods -n $NAMESPACE --no-headers | wc -l)
    
    if [ "$ready_pods" -eq "$total_pods" ] && [ "$total_pods" -gt 0 ]; then
        log_success "Todos os pods estão rodando ($ready_pods/$total_pods)"
    else
        log_warning "Nem todos os pods estão rodando ($ready_pods/$total_pods)"
    fi
}

# Função para limpar recursos
cleanup() {
    log_warning "Removendo recursos do QualiSoja..."
    
    if helm list -n $NAMESPACE | grep -q $RELEASE_NAME; then
        helm uninstall $RELEASE_NAME -n $NAMESPACE
        log_success "Helm release removido"
    fi
    
    kubectl delete namespace $NAMESPACE --ignore-not-found=true
    log_success "Namespace removido"
}

# Logs da aplicação
show_logs() {
    log_info "Mostrando logs da aplicação..."
    kubectl logs -n $NAMESPACE -l app=qualisoja --tail=100 -f
}

# Port forward para acesso local
port_forward() {
    local port=${1:-8000}
    log_info "Iniciando port-forward na porta $port..."
    kubectl port-forward -n $NAMESPACE svc/qualisoja-service $port:8000
}

# Menu principal
show_help() {
    echo "🚀 QualiSoja Kubernetes Deploy Script"
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponíveis:"
    echo "  deploy-manifests  Deploy usando manifests Kubernetes"
    echo "  deploy-helm      Deploy usando Helm Chart"
    echo "  status           Verificar status do deployment"
    echo "  logs             Mostrar logs da aplicação"
    echo "  port-forward     Port forward para acesso local"
    echo "  cleanup          Remover todos os recursos"
    echo "  help             Mostrar esta ajuda"
    echo ""
    echo "Exemplos:"
    echo "  $0 deploy-helm"
    echo "  $0 status"
    echo "  $0 port-forward 8080"
}

# Script principal
main() {
    case "${1:-help}" in
        "deploy-manifests")
            check_dependencies
            create_namespace
            deploy_manifests
            check_status
            ;;
        "deploy-helm")
            check_dependencies
            deploy_helm
            check_status
            ;;
        "status")
            check_status
            ;;
        "logs")
            show_logs
            ;;
        "port-forward")
            port_forward $2
            ;;
        "cleanup")
            cleanup
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

main "$@"
