from app import db
from app.models.dados_calculados import (
    Faturamento_total, 
    Lucro_total, 
    Faturamento_produtos, 
    Faturamento_servicos, 
    Lucro_produtos, 
    Lucro_servicos
)
from sqlalchemy.exc import IntegrityError
import logging

logger = logging.getLogger(__name__)


def salvar_ou_atualizar_dados_calculados(user_id, dados_calculados):
    """
    Salva ou atualiza dados calculados no banco de dados para um usuário específico
    
    Args:
        user_id (int): ID do usuário
        dados_calculados (dict): JSON com os dados calculados
        
    Returns:
        bool: True se operação foi bem-sucedida, False caso contrário
    """
    try:
        logger.info(f"Iniciando salvamento de dados calculados para usuário {user_id}")
        logger.debug(f"Dados recebidos: {dados_calculados}")
        
        # Faturamento_total
        if "Faturamento_total" in dados_calculados:
            logger.debug("Processando Faturamento_total")
            faturamento_total = Faturamento_total.query.filter_by(user_id=user_id).first()
            if faturamento_total:
                logger.debug("Atualizando Faturamento_total existente")
                faturamento_total.valor = dados_calculados["Faturamento_total"]["valor"]
                faturamento_total.porcentagem_total_faturamento = dados_calculados["Faturamento_total"]["porcentagem_faturamento_total"]
            else:
                logger.debug("Criando novo Faturamento_total")
                novo_faturamento = Faturamento_total(
                    user_id=user_id,
                    valor=dados_calculados["Faturamento_total"]["valor"],
                    porcentagem_total_faturamento=dados_calculados["Faturamento_total"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento)
        
        # Lucro_total
        if "Lucro_total" in dados_calculados:
            logger.debug("Processando Lucro_total")
            lucro_total = Lucro_total.query.filter_by(user_id=user_id).first()
            if lucro_total:
                logger.debug("Atualizando Lucro_total existente")
                lucro_total.valor = dados_calculados["Lucro_total"]["valor"]
                lucro_total.porcentagem_faturamento_total = dados_calculados["Lucro_total"]["porcentagem_faturamento_total"]
            else:
                logger.debug("Criando novo Lucro_total")
                novo_lucro = Lucro_total(
                    user_id=user_id,
                    valor=dados_calculados["Lucro_total"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Lucro_total"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_lucro)
        
        # Faturamento_produtos
        if "Faturamento_produtos" in dados_calculados:
            faturamento_produtos = Faturamento_produtos.query.filter_by(user_id=user_id).first()
            if faturamento_produtos:
                faturamento_produtos.valor = dados_calculados["Faturamento_produtos"]["valor"]
                faturamento_produtos.porcentagem_faturamento_total = dados_calculados["Faturamento_produtos"]["porcentagem_faturamento_total"]
            else:
                novo_faturamento_produtos = Faturamento_produtos(
                    user_id=user_id,
                    valor=dados_calculados["Faturamento_produtos"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Faturamento_produtos"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento_produtos)
        
        # Faturamento_servicos
        if "Faturamento_servicos" in dados_calculados:
            faturamento_servico = Faturamento_servicos.query.filter_by(user_id=user_id).first()
            if faturamento_servico:
                faturamento_servico.valor = dados_calculados["Faturamento_servicos"]["valor"]
                faturamento_servico.porcentagem_faturamento_total = dados_calculados["Faturamento_servicos"]["porcentagem_faturamento_total"]
            else:
                novo_faturamento_servico = Faturamento_servicos(
                    user_id=user_id,
                    valor=dados_calculados["Faturamento_servicos"]["valor"],
                    porcentagem_faturamento_total=dados_calculados["Faturamento_servicos"]["porcentagem_faturamento_total"]
                )
                db.session.add(novo_faturamento_servico)
        
        # Lucro_produtos
        if "Lucro_produtos" in dados_calculados:
            lucro_produtos = Lucro_produtos.query.filter_by(user_id=user_id).first()
            if lucro_produtos:
                lucro_produtos.valor = dados_calculados["Lucro_produtos"]["valor"]
                lucro_produtos.porcentagem_lucro_total = dados_calculados["Lucro_produtos"]["porcentagem_lucro_total"]
            else:
                novo_lucro_produtos = Lucro_produtos(
                    user_id=user_id,
                    valor=dados_calculados["Lucro_produtos"]["valor"],
                    porcentagem_lucro_total=dados_calculados["Lucro_produtos"]["porcentagem_lucro_total"]
                )
                db.session.add(novo_lucro_produtos)
        
        # Lucro_servicos
        if "Lucro_servicos" in dados_calculados:
            lucro_servico = Lucro_servicos.query.filter_by(user_id=user_id).first()
            if lucro_servico:
                lucro_servico.valor = dados_calculados["Lucro_servicos"]["valor"]
                lucro_servico.porcentagem_lucro_total = dados_calculados["Lucro_servicos"]["porcentagem_lucro_total"]
            else:
                novo_lucro_servico = Lucro_servicos(
                    user_id=user_id,
                    valor=dados_calculados["Lucro_servicos"]["valor"],
                    porcentagem_lucro_total=dados_calculados["Lucro_servicos"]["porcentagem_lucro_total"]
                )
                db.session.add(novo_lucro_servico)
        
        logger.debug("Fazendo commit das alterações no banco de dados")
        db.session.commit()
        logger.info(f"Dados calculados salvos/atualizados com sucesso para usuário {user_id}")
        return True
        
    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Erro de integridade ao salvar dados calculados para usuário {user_id}: {e}")
        return False
    except Exception as e:
        db.session.rollback()
        logger.error(f"Erro ao salvar dados calculados para usuário {user_id}: {e}")
        return False
