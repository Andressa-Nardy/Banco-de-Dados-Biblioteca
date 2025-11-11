from servicos.database.conector import DatabaseManager

db = DatabaseManager()

def top_usuarios_emprestimos(limit: int = 10):
    query = f"""
        SELECT 
            u.cpf,
            u.nome,
            COUNT(e.id_item) AS total_emprestimos
        FROM emprestimo e
        INNER JOIN usuario u ON u.cpf = e.cpf_usuario
        GROUP BY u.cpf, u.nome
        ORDER BY total_emprestimos DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def top_usuarios_acessos_digital(limit: int = 10):
    query = f"""
        SELECT 
            u.cpf,
            u.nome,
            COUNT(a.id_item_digital) AS total_acessos
        FROM acesso_digital a
        INNER JOIN usuario u ON u.cpf = a.cpf_usuario
        GROUP BY u.cpf, u.nome
        ORDER BY total_acessos DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def usuarios_fisico_e_digital():
    query = """
        SELECT DISTINCT 
            u.cpf,
            u.nome
        FROM usuario u
        INNER JOIN emprestimo e ON e.cpf_usuario = u.cpf
        INNER JOIN acesso_digital a ON a.cpf_usuario = u.cpf
        ORDER BY u.nome;
    """
    return db.execute_select_all(query)

def itens_mais_emprestados(limit: int = 10):
    query = f"""
        SELECT 
            i.id_item,
            i.titulo,
            i.autor,
            i.ano_publicacao,
            COUNT(e.id_item) AS total_emprestimos
        FROM emprestimo e
        INNER JOIN item_acervo i ON i.id_item = e.id_item
        GROUP BY i.id_item, i.titulo, i.autor, i.ano_publicacao
        ORDER BY total_emprestimos DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def itens_fisicos_e_digitais():
    query = """
        SELECT DISTINCT 
            a.id_item,
            a.titulo
        FROM item_acervo a
        JOIN item_digital d ON d.id_item = a.id_item
        JOIN exemplar e ON e.id_item = a.id_item
        ORDER BY a.titulo;
    """
    return db.execute_select_all(query)

def locais_mais_reservados(limit: int = 10):
    query = f"""
        SELECT 
            i.id_infra,
            i.local,
            COUNT(r.id_infra) AS total_reservas
        FROM reserva_infra r
        JOIN infraestrutura i ON i.id_infra = r.id_infra
        GROUP BY i.id_infra, i.local
        ORDER BY total_reservas DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def infraestruturas_acima_de_meia_capacidade():
    query = """
        SELECT 
            i.id_infra,
            i.local,
            i.capacidade,
            COUNT(r.cpf_usuario) AS reservas,
            ROUND((COUNT(r.cpf_usuario)::decimal / NULLIF(i.capacidade, 0)) * 100, 2) AS percentual_ocupacao
        FROM infraestrutura i
        LEFT JOIN reserva_infra r ON i.id_infra = r.id_infra
        GROUP BY i.id_infra, i.local, i.capacidade
        HAVING COUNT(r.cpf_usuario) > (i.capacidade / 2)
        ORDER BY percentual_ocupacao DESC;
    """
    return db.execute_select_all(query)

def eventos_mais_populares(limit: int = 10):
    query = f"""
        SELECT 
            e.id_evento,
            e.nome_evento,
            e.tipo,
            e.data_inicio,
            e.data_fim,
            COUNT(a.cpf_usuario) AS total_acessos
        FROM acesso_evento a
        JOIN eventos e ON e.id_evento = a.id_evento
        GROUP BY e.id_evento, e.nome_evento, e.tipo, e.data_inicio, e.data_fim
        ORDER BY total_acessos DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def usuarios_que_acessaram_obras_relacionadas():
    query = """
        SELECT DISTINCT 
            u.cpf,
            u.nome
        FROM acesso_evento ae
        JOIN eventos ev ON ae.id_evento = ev.id_evento
        JOIN item_acervo ia 
            ON ia.titulo = ANY(string_to_array(ev.obras_relacionadas, ','))
        JOIN item_digital idg 
            ON idg.id_item = ia.id_item
        JOIN acesso_digital ad 
            ON ad.id_item_digital = idg.id_item 
           AND ad.cpf_usuario = ae.cpf_usuario
        JOIN usuario u ON u.cpf = ae.cpf_usuario;
    """
    return db.execute_select_all(query)

def emprestimos_em_atraso():
    query = """
        SELECT 
            u.cpf,
            u.nome,
            i.titulo,
            e.data_emprestimo,
            e.data_devolucao_prevista
        FROM emprestimo e
        JOIN usuario u ON u.cpf = e.cpf_usuario
        JOIN item_acervo i ON i.id_item = e.id_item
        WHERE e.data_devolucao_real IS NULL 
          AND e.data_devolucao_prevista < CURRENT_DATE;
    """
    return db.execute_select_all(query)

def tempo_medio_devolucao_por_usuario():
    query = """
        SELECT 
            u.cpf,
            u.nome,
            ROUND(AVG(e.data_devolucao_real - e.data_emprestimo), 2) AS media_dias
        FROM emprestimo e
        JOIN usuario u ON u.cpf = e.cpf_usuario
        WHERE e.data_devolucao_real IS NOT NULL
        GROUP BY u.cpf, u.nome
        ORDER BY media_dias DESC;
    """
    return db.execute_select_all(query)

def ranking_geral_engajamento():
    query = """
        WITH emprestimos AS (
            SELECT cpf_usuario, COUNT(*) AS qtd 
            FROM emprestimo 
            GROUP BY cpf_usuario
        ),
        acessos AS (
            SELECT cpf_usuario, COUNT(*) AS qtd 
            FROM acesso_digital 
            GROUP BY cpf_usuario
        ),
        eventos AS (
            SELECT cpf_usuario, COUNT(*) AS qtd 
            FROM acesso_evento 
            GROUP BY cpf_usuario
        )
        SELECT 
            u.cpf,
            u.nome,
            COALESCE(e.qtd, 0) AS emprestimos,
            COALESCE(a.qtd, 0) AS acessos_digitais,
            COALESCE(ev.qtd, 0) AS eventos,
            (COALESCE(e.qtd,0) + COALESCE(a.qtd,0) + COALESCE(ev.qtd,0)) AS total_interacoes
        FROM usuario u
        LEFT JOIN emprestimos e ON e.cpf_usuario = u.cpf
        LEFT JOIN acessos a ON a.cpf_usuario = u.cpf
        LEFT JOIN eventos ev ON ev.cpf_usuario = u.cpf
        ORDER BY total_interacoes DESC;
    """
    return db.execute_select_all(query)

def media_movel_emprestimos():
    query = """
        WITH emprestimos_por_semana AS (
            SELECT
                DATE_TRUNC('week', data_emprestimo) AS semana,
                COUNT(*) AS total_emprestimos
            FROM emprestimo
            GROUP BY 1
        )
        SELECT 
            semana,
            total_emprestimos,
            ROUND(
                AVG(total_emprestimos) OVER (
                    ORDER BY semana 
                    ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                ), 2
            ) AS media_movel_3_sem
        FROM emprestimos_por_semana
        ORDER BY semana;
    """
    return db.execute_select_all(query)


def ranking_engajamento_ponderado():
    query = """
        WITH metricas AS (
            SELECT 
                u.cpf,
                u.nome,
                COUNT(DISTINCT e.id_item) AS emprestimos,
                COUNT(DISTINCT ad.id_item_digital) AS acessos_digitais,
                COUNT(DISTINCT r.id_infra) AS reservas_infra,
                COUNT(DISTINCT ae.id_evento) AS acessos_eventos
            FROM usuario u
            LEFT JOIN emprestimo e ON e.cpf_usuario = u.cpf
            LEFT JOIN acesso_digital ad ON ad.cpf_usuario = u.cpf
            LEFT JOIN reserva_infra r ON r.cpf_usuario = u.cpf
            LEFT JOIN acesso_evento ae ON ae.cpf_usuario = u.cpf
            GROUP BY u.cpf, u.nome
        )
        SELECT 
            nome,
            emprestimos,
            acessos_digitais,
            reservas_infra,
            acessos_eventos,
            ROUND((emprestimos*2 + acessos_digitais*1.5 + reservas_infra + acessos_eventos*0.5), 2) AS score_engajamento,
            RANK() OVER (
                ORDER BY (emprestimos*2 + acessos_digitais*1.5 + reservas_infra + acessos_eventos*0.5) DESC
            ) AS posicao
        FROM metricas
        ORDER BY score_engajamento DESC;
    """
    return db.execute_select_all(query)

def itens_mais_demorados(limit: int = 15):
    query = f"""
        SELECT 
            u.nome,
            i.titulo,
            e.data_emprestimo,
            e.data_devolucao_real,
            (e.data_devolucao_real - e.data_emprestimo) AS dias_emprestado,
            RANK() OVER (ORDER BY (e.data_devolucao_real - e.data_emprestimo) DESC) AS posicao
        FROM emprestimo e
        JOIN item_acervo i ON i.id_item = e.id_item
        JOIN usuario u ON u.cpf = e.cpf_usuario
        WHERE e.data_devolucao_real IS NOT NULL
        ORDER BY dias_emprestado DESC
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def correlacao_generos(limit: int = 10):
    query = f"""
        WITH fisico AS (
            SELECT 
                a.genero,
                COUNT(*) AS emprestimos
            FROM emprestimo e
            JOIN item_acervo a ON a.id_item = e.id_item
            GROUP BY a.genero
        ),
        digital AS (
            SELECT 
                a.genero,
                COUNT(*) AS acessos
            FROM acesso_digital ad
            JOIN item_digital d ON d.id_item = ad.id_item_digital
            JOIN item_acervo a ON a.id_item = d.id_item
            GROUP BY a.genero
        )
        SELECT 
            COALESCE(f.genero, d.genero) AS genero,
            COALESCE(f.emprestimos, 0) AS emprestimos,
            COALESCE(d.acessos, 0) AS acessos_digitais,
            (COALESCE(d.acessos,0)::FLOAT / NULLIF(f.emprestimos,0)) AS taxa_digitalizacao
        FROM fisico f
        FULL OUTER JOIN digital d ON f.genero = d.genero
        ORDER BY taxa_digitalizacao DESC NULLS LAST
        LIMIT {limit};
    """
    return db.execute_select_all(query)

def infraestruturas_sobrecarregadas():
    query = """
        WITH reservas AS (
            SELECT 
                r.id_infra,
                COUNT(*) AS total_reservas,
                AVG(i.capacidade) AS capacidade_media
            FROM reserva_infra r
            JOIN infraestrutura i ON i.id_infra = r.id_infra
            GROUP BY r.id_infra
        ),
        eventos_locais AS (
            SELECT 
                e.id_infra,
                COUNT(*) AS eventos_no_local
            FROM eventos e
            GROUP BY e.id_infra
        )
        SELECT 
            i.local,
            COALESCE(r.total_reservas,0) AS reservas,
            COALESCE(e.eventos_no_local,0) AS eventos,
            ROUND(
                (COALESCE(r.total_reservas,0)::decimal / NULLIF(i.capacidade,0)) * 100, 2
            ) AS ocupacao_pct,
            CASE 
                WHEN (COALESCE(r.total_reservas,0)::decimal / NULLIF(i.capacidade,0)) > 0.8 
                    THEN 'SOBRECARGA'
                ELSE 'NORMAL'
            END AS status
        FROM infraestrutura i
        LEFT JOIN reservas r ON r.id_infra = i.id_infra
        LEFT JOIN eventos_locais e ON e.id_infra = i.id_infra
        ORDER BY ocupacao_pct DESC;
    """
    return db.execute_select_all(query)

def analise_temporal_digital_fisico():
    query = """
        SELECT DISTINCT 
            u.nome,
            a.titulo,
            ad.data_acesso,
            e.data_emprestimo
        FROM acesso_digital ad
        JOIN item_digital d ON d.id_item = ad.id_item_digital
        JOIN item_acervo a ON a.id_item = d.id_item
        JOIN emprestimo e ON e.id_item = a.id_item AND e.cpf_usuario = ad.cpf_usuario
        JOIN usuario u ON u.cpf = ad.cpf_usuario
        WHERE ad.data_acesso < e.data_emprestimo
        ORDER BY a.titulo, u.nome;
    """
    return db.execute_select_all(query)

def historico_recursivo_acessos():
    query = """
        WITH RECURSIVE acessos_ordenados AS (
            SELECT 
                cpf_usuario,
                data_acesso,
                ROW_NUMBER() OVER (PARTITION BY cpf_usuario ORDER BY data_acesso) AS ordem
            FROM acesso_digital
        ),
        sequencia AS (
            SELECT 
                cpf_usuario,
                ordem,
                1 AS consecutivos
            FROM acessos_ordenados
            WHERE ordem = 1
            UNION ALL
            SELECT 
                a.cpf_usuario,
                a.ordem,
                s.consecutivos + 1
            FROM acessos_ordenados a
            JOIN sequencia s 
                ON a.cpf_usuario = s.cpf_usuario
               AND a.ordem = s.ordem + 1
        )
        SELECT cpf_usuario, MAX(consecutivos) AS maior_sequencia_acessos
        FROM sequencia
        GROUP BY cpf_usuario;
    """
    return db.execute_select_all(query)
