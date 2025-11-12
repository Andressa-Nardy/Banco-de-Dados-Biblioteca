document.addEventListener('DOMContentLoaded', () => {

    const formCadastro = document.getElementById('form-cadastro');
    const mensagemCadastro = document.getElementById('mensagem-cadastro');

    if (formCadastro) {
        formCadastro.addEventListener('submit', (evento) => {
            // 1. Impede que o formulário recarregue a página
            evento.preventDefault(); 
            
            mensagemCadastro.textContent = 'Enviando...';
            mensagemCadastro.style.color = 'var(--cor-texto)';

            // 2. Pega os dados dos campos do formulário
            const dadosFormulario = new FormData(formCadastro);
            
            // 3. Converte os dados do formulário em um objeto JSON
            const dadosUsuario = {
                cpf: dadosFormulario.get('cpf'),
                nome: dadosFormulario.get('nome'),
                email: dadosFormulario.get('email'),
                data_cadastro: dadosFormulario.get('data_cadastro')
            };

            // 4. Envia os dados para o backend usando fetch() com POST
            fetch('http://127.0.0.1:8000/usuario/cadastrar', { // Verifique a porta!
                method: 'POST', // Define o método como POST
                headers: {
                    'Content-Type': 'application/json', // Avisa ao backend que estamos enviando JSON
                },
                body: JSON.stringify(dadosUsuario) // Converte o objeto JS em texto JSON
            })
            .then(response => response.json()) // Converte a resposta do backend (sucesso ou erro) em JSON
            .then(resultado => {
                // 5. Mostra a resposta do backend para o usuário
                if (resultado.erro) {
                    // Se o backend retornou uma mensagem de erro
                    mensagemCadastro.textContent = `Erro: ${resultado.erro}`;
                    mensagemCadastro.style.color = 'red';
                } else {
                    // Se o backend retornou uma mensagem de sucesso
                    mensagemCadastro.textContent = resultado.mensagem;
                    mensagemCadastro.style.color = 'green';
                    formCadastro.reset(); // Limpa o formulário
                }
            })
            .catch(error => {
                // Em caso de erro de rede (ex: backend desligado)
                console.error('Falha ao cadastrar:', error);
                mensagemCadastro.textContent = `Erro de conexão: ${error.message}`;
                mensagemCadastro.style.color = 'red';
            });
        });
    }
});