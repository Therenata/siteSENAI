# Ambiente de Testes - Site SENAI

## 📋 Visão Geral
Este é o ambiente de testes do projeto Site SENAI, onde desenvolvemos e testamos novas funcionalidades antes de integrá-las ao ambiente principal.

## 🗂️ Estrutura do Projeto
- **📁 Html/**
  - `ok_test.html` - Galeria responsiva de raças de cachorros
  - `pib_graficos.html` - Visualização interativa de dados do PIB brasileiro
  - Outros arquivos HTML para diferentes raças de cachorros

- **🎨 css/**
  - `test.css` - Estilos responsivos mobile-first para a galeria e gráficos

- **📊 js/**
  - `pib-charts.js` - Geração dinâmica de gráficos usando Chart.js
  - Integração com API IBGE (Sidra) e fallback para CSV

- **🖼️ img/**
  - Imagens das raças de cachorros
  - Placeholders SVG para gráficos
  - Recursos visuais do site

## 🔧 Tecnologias Utilizadas
- HTML5 com design responsivo
- CSS3 com abordagem mobile-first
- JavaScript para interatividade
- Chart.js para visualização de dados
- Integração com API IBGE (Sidra)

## 📈 Funcionalidades
1. **Galeria Responsiva**
   - Layout adaptativo com CSS Grid
   - Lightbox para visualização de imagens
   - Navegação intuitiva

2. **Visualização de Dados**
   - Gráficos interativos do PIB brasileiro
   - Atualização dinâmica via API IBGE
   - Formatação automática de valores em K/M/B/T

## 🚀 Como Executar
1. Abra `Html/ok_test.html` para a galeria
2. Abra `Html/pib_graficos.html` para os gráficos do PIB
3. Para dados locais do PIB (opcional):
   ```bash
   pip install -r ../../requirements.txt
   python ../../Python/PIB_brasil.py
   ```

## 📝 Observações
- Ambiente dedicado a testes e desenvolvimento
- Implementa features antes da integração com produção
- Mantém compatibilidade com o projeto principal
- Serve como playground para novas tecnologias e abordagens

## 🔄 Status do Projeto
- [x] Layout responsivo implementado
- [x] Integração com API IBGE
- [x] Visualização dinâmica de dados
- [x] Sistema de fallback para dados
- [ ] Testes completos de UI/UX
- [ ] Otimização de performance
