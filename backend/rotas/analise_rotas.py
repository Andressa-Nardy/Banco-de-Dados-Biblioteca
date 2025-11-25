from flask import Blueprint, jsonify, request
from servicos.analise_servico import (
    usuarios_top_emprestimos, infra_mais_reservada, itens_nunca_emprestados,
    taxa_pontualidade_usuarios, ranking_itens_mais_emprestados,
    infra_sem_uso, itens_por_titulo_autor, infra_capacidade_acima_tipo
)

analise_bp = Blueprint("analise", __name__, url_prefix="/analise")

@analise_bp.route("/usuarios-top-emprestimos", methods=["GET"])
def get_usuarios_top_emprestimos():
    resultado = usuarios_top_emprestimos()
    return jsonify(resultado), 200


@analise_bp.route("/infra-mais-reservada", methods=["GET"])
def get_infra_mais_reservada():
    resultado = infra_mais_reservada()
    return jsonify(resultado), 200


@analise_bp.route("/itens-nunca-emprestados", methods=["GET"])
def get_itens_nunca_emprestados():
    resultado = itens_nunca_emprestados()
    return jsonify(resultado), 200


@analise_bp.route("/itens-por-titulo-autor", methods=["GET"])
def get_itens_por_titulo_autor():
    titulo = request.args.get("titulo", "")
    autor = request.args.get("autor", "")

    if not titulo and not autor:
        return jsonify({"erro": "Você deve informar ao menos 'titulo' ou 'autor'."}), 400

    try:
        resultados = itens_por_titulo_autor(titulo, autor)
        return jsonify(resultados), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@analise_bp.route("/infra-acima-tipo", methods=["GET"])
def get_infra_acima_tipo():
    tipo = request.args.get("tipo")

    if not tipo:
        return jsonify({"erro": "Você deve informar o parâmetro 'tipo'."}), 400

    resultado = infra_capacidade_acima_tipo(tipo)
    return jsonify(resultado), 200



@analise_bp.route("/taxa-pontualidade", methods=["GET"])
def get_taxa_pontualidade():
    resultado = taxa_pontualidade_usuarios()
    return jsonify(resultado), 200


@analise_bp.route("/ranking-itens-emprestados", methods=["GET"])
def get_ranking_itens_emprestados():
    resultado = ranking_itens_mais_emprestados()
    return jsonify(resultado), 200


@analise_bp.route("/infra-sem-uso", methods=["GET"])
def get_infra_sem_uso():
    resultado = infra_sem_uso()
    return jsonify(resultado), 200


