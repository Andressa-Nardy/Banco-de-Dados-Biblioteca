from flask import Blueprint, jsonify, request
from servicos.analise_servico import top_usuarios_emprestimos, top_usuarios_acessos_digital, usuarios_fisico_e_digital, \
    itens_mais_emprestados, itens_fisicos_e_digitais, locais_mais_reservados, infraestruturas_acima_de_meia_capacidade, \
    eventos_mais_populares, usuarios_que_acessaram_obras_relacionadas, emprestimos_em_atraso, \
    tempo_medio_devolucao_por_usuario, ranking_geral_engajamento, ranking_engajamento_ponderado, \
    media_movel_emprestimos, itens_mais_demorados, correlacao_generos, infraestruturas_sobrecarregadas, \
    analise_temporal_digital_fisico, historico_recursivo_acessos, dashboard_resumo

analise_bp = Blueprint("analise", __name__, url_prefix="/analise")

@analise_bp.route("/top-usuarios", methods=["GET"])
def get_top_usuarios():
    limit = request.args.get("limit", default=10, type=int)
    resultado = top_usuarios_emprestimos(limit)
    return jsonify(resultado), 200

@analise_bp.route("/top-acessos-digitais", methods=["GET"])
def get_top_acessos_digitais():
    limit = request.args.get("limit", default=10, type=int)
    resultado = top_usuarios_acessos_digital(limit)
    return jsonify(resultado), 200

@analise_bp.route("/usuarios-fisico-e-digital", methods=["GET"])
def get_usuarios_fisico_e_digital():
    resultado = usuarios_fisico_e_digital()
    return jsonify(resultado), 200

@analise_bp.route("/itens-mais-emprestados", methods=["GET"])
def get_itens_mais_emprestados():
    limit = request.args.get("limit", default=10, type=int)
    resultado = itens_mais_emprestados(limit)
    return jsonify(resultado), 200

@analise_bp.route("/itens-fisicos-e-digitais", methods=["GET"])
def get_itens_fisicos_e_digitais():
    resultado = itens_fisicos_e_digitais()
    return jsonify(resultado), 200

@analise_bp.route("/locais-mais-reservados", methods=["GET"])
def get_locais_mais_reservados():
    limit = request.args.get("limit", default=10, type=int)
    resultado = locais_mais_reservados(limit)
    return jsonify(resultado), 200

@analise_bp.route("/infraestruturas-acima-meia-capacidade", methods=["GET"])
def get_infraestruturas_acima_meia_capacidade():
    resultado = infraestruturas_acima_de_meia_capacidade()
    return jsonify(resultado), 200

@analise_bp.route("/eventos-mais-populares", methods=["GET"])
def get_eventos_mais_populares():
    limit = request.args.get("limit", default=10, type=int)
    resultado = eventos_mais_populares(limit)
    return jsonify(resultado), 200

@analise_bp.route("/usuarios-obras-relacionadas", methods=["GET"])
def get_usuarios_obras_relacionadas():
    resultado = usuarios_que_acessaram_obras_relacionadas()
    return jsonify(resultado), 200

@analise_bp.route("/emprestimos-atraso", methods=["GET"])
def get_emprestimos_em_atraso():
    resultado = emprestimos_em_atraso()
    return jsonify(resultado), 200

@analise_bp.route("/tempo-medio-devolucao", methods=["GET"])
def get_tempo_medio_devolucao():
    resultado = tempo_medio_devolucao_por_usuario()
    return jsonify(resultado), 200

@analise_bp.route("/ranking-engajamento", methods=["GET"])
def get_ranking_engajamento():
    resultado = ranking_geral_engajamento()
    return jsonify(resultado), 200

@analise_bp.route("/ranking-engajamento-ponderado", methods=["GET"])
def get_ranking_engajamento_ponderado():
    resultado = ranking_engajamento_ponderado()
    return jsonify(resultado), 200

@analise_bp.route("/media-movel-emprestimos", methods=["GET"])
def get_media_movel_emprestimos():
    resultado = media_movel_emprestimos()
    return jsonify(resultado), 200

@analise_bp.route("/itens-mais-demorados", methods=["GET"])
def get_itens_mais_demorados():
    limit = request.args.get("limit", default=15, type=int)
    resultado = itens_mais_demorados(limit)
    return jsonify(resultado), 200

@analise_bp.route("/correlacao-generos", methods=["GET"])
def get_correlacao_generos():
    limit = request.args.get("limit", default=10, type=int)
    resultado = correlacao_generos(limit)
    return jsonify(resultado), 200

@analise_bp.route("/infraestruturas-sobrecarregadas", methods=["GET"])
def get_infraestruturas_sobrecarregadas():
    resultado = infraestruturas_sobrecarregadas()
    return jsonify(resultado), 200

@analise_bp.route("/analise-temporal-digital-fisico", methods=["GET"])
def get_analise_temporal_digital_fisico():
    resultado = analise_temporal_digital_fisico()
    return jsonify(resultado), 200

@analise_bp.route("/historico-recursivo-acessos", methods=["GET"])
def get_historico_recursivo_acessos():
    resultado = historico_recursivo_acessos()
    return jsonify(resultado), 200

