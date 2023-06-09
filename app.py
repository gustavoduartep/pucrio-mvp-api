from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect

from sqlalchemy.exc import IntegrityError

from model import Session, Item
from schemas import *
from flask_cors import CORS

info = Info(title="SushiPuc API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags

#home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
item_tag = Tag(name="Item", description="Inclusão de itens na lista, consulta e exclusão de itens")

@app.get('/')
def home():
    return redirect('/openapi/swagger')

@app.post('/item', tags=[item_tag], responses={"200": ItemViewSchema, "409" : ErrorSchema, "400" : ErrorSchema, "500" : ErrorSchema})
def cadastrar_item(form: ItemSchema):
    """Adiciona um item na lista de compra do cliente
    Adiciona o item disponível do catálogo na lista de compra.
    """

    item = Item(
        nome = form.nome,
        quantidade = form.quantidade,
        valor = form.valor)
    try:
        sessao = Session()
        sessao.add(item)
        sessao.commit()
        return apresenta_item(item), 200
      
    except IntegrityError as e:
        mensagem_erro = "Item com o mesmo nome já cadastrado"
        return{"message" : mensagem_erro}, 409
    
    except Exception as e:
        mensagem_erro = "Não foi possível cadastrar um novo item"
        return {"message" : mensagem_erro}, 400
    
    except TypeError as e:
        mensagem_erro = "Problema interno no servidor da aplicação"
        return {"message" : mensagem_erro}, 500

    
@app.get('/itens', tags=[item_tag], responses={"200" : ListagemItemSchema, "404": ErrorSchema})

def get_itens():
    """Lista todos os itens cadastrados
    Retorna a lista de todos os itens disponíveis na lista de compra.
    """

    sessao = Session()
    itens = sessao.query(Item).all()

    if not itens:
        return {"itens": []}, 200
    else:
        print(itens)
        return apresenta_itens(itens),200
    
@app.get('/item', tags=[item_tag], responses={"200" : ItemViewSchema, "404": ErrorSchema})
def lista_item(query: BuscaItemSchema):
    """Faz a busca de um item específico
    Realiza a consulta do item e retorna uma resposta em JSON. Em caso de sucesso retorna o objeto, em caso de falha retorna um feedback negativo.
    """

    item_id = query.id
    print(item_id)
    sessao = Session()

    item = sessao.query(Item).filter(Item.id == item_id).first()

    if not item:
        mensagem_erro = "Item não encontrado"
        return {"message": mensagem_erro}, 404
    else:
        return apresenta_item(item), 200

@app.delete('/item', tags=[item_tag],
            responses={"200": ItemDelSchema, "404": ErrorSchema})
def del_produto(query: BuscaItemSchema):
    """Deleta um Item a partir do id informado

    Remove o item da base de dados. Em caso de sucesso retorna uma mensagem de confirmação da remoção, em caso de falha retorna um feedback negativo.
    """
    item_id = query.id
    print(item_id)
    # criando conexão com a base
    sessao = Session()
    # fazendo a remoção
    count = sessao.query(Item).filter(Item.id == item_id).delete()
    sessao.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"message": "Item removido do seu pedido", "id": item_id}
    else:
        # se o item não foi encontrado
        mensagem_erro = "Item não encontrado"
        return {"message": mensagem_erro}, 404
    



