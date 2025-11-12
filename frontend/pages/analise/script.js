document.addEventListener('DOMContentLoaded', () => {

    // --- SEÇÃO DE ANÁLISE (LISTAR ITENS) ---
    const botaoAnalisar = document.getElementById('btnCarregarDados');
    const listaResultadosEl = document.getElementById('lista-resultados');
    const selectAnalise = document.getElementById('select-analise');

    /**
     * Função auxiliar para formatar as chaves do JSON
     * Ex: "ano_publicacao" -> "Ano publicacao: "
     */
    function formatarLabel(key) {
        // ================== MUDANÇA AQUI ==================
        // Exceção específica para "cpf"
        if (key.toLowerCase() === 'cpf') {
            return 'CPF: ';
        }
        // ================== FIM DA MUDANÇA ==================

        let label = key.replace(/_/g, ' '); // Troca _ por espaço
        // Capitaliza a primeira letra
        label = label.charAt(0).toUpperCase() + label.slice(1);
        return `${label}: `;
    }

    /**
     * Função auxiliar para criar e exibir os resultados formatados
     */
    function exibirResultadosFormatados(dados) {
        listaResultadosEl.innerHTML = ''; // Limpa a lista

        if (dados === null || dados === undefined) {
            listaResultadosEl.innerHTML = '<li>Nenhum dado retornado.</li>';
            return;
        }

        // Função interna para processar um *único* item (objeto)
        const processarItem = (item) => {
            const li = document.createElement('li');
            
            // Itera sobre todas as chaves do objeto (ex: "titulo", "autor")
            for (const key in item) {
                if (Object.hasOwnProperty.call(item, key)) {
                    const value = item[key];
                    
                    // Cria um parágrafo para a linha
                    const p = document.createElement('p');

                    // Cria um <span> para o label (ex: "Autor: ")
                    const labelSpan = document.createElement('span');
                    labelSpan.className = 'item-label';
                    labelSpan.textContent = formatarLabel(key);
                    
                    // Cria um <span> para o valor (ex: "Carla Martins")
                    const valueSpan = document.createElement('span');
                    valueSpan.className = 'item-value';
                    valueSpan.textContent = value;

                    p.appendChild(labelSpan);
                    p.appendChild(valueSpan);
                    li.appendChild(p);
                }
            }
            return li;
        };

        // Verifica se 'dados' é um array ou um objeto único
        if (Array.isArray(dados)) {
            if (dados.length === 0) {
                listaResultadosEl.innerHTML = '<li>Nenhum item encontrado.</li>';
                return;
            }
            // Processa cada item do array
            dados.forEach(item => {
                listaResultadosEl.appendChild(processarItem(item));
            });
        } else if (typeof dados === 'object') {
            // Processa o objeto único
            listaResultadosEl.appendChild(processarItem(dados));
        } else {
            // Caso seja um valor simples (string, número)
            listaResultadosEl.innerHTML = `<li>${dados}</li>`;
        }
    }

    // Verifica se os elementos existem
    if (botaoAnalisar && listaResultadosEl && selectAnalise) { 
        botaoAnalisar.addEventListener('click', () => {
            listaResultadosEl.innerHTML = '<li>Carregando...</li>';
            
            const endpointSelecionado = selectAnalise.value;
            const url = `http://127.0.0.1:8000/analise/${endpointSelecionado}`;

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Erro na requisição: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(dados => {
                    // Chama a nova função de exibição
                    exibirResultadosFormatados(dados);
                })
                .catch(error => {
                    console.error('Falha ao buscar dados:', error);
                    listaResultadosEl.innerHTML = `<li>Erro ao carregar dados: ${error.message}</li>`;
                });
        });
    }
});