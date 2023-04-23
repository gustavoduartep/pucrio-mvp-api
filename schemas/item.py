from pydantic import BaseModel, Field, conint
from typing import Optional, List
from model.item import Item

class ItemSchema(BaseModel):
    """
    """
    nome: str = Field("Uramaki Salmão", description="Nome do item")
    quantidade: conint(gt=0) = Field(1, description="A quantidade de itens para adicionar na lista")
    valor: float = Field(4.99, description="O valor do item em formato de moeda internacional (i.e casas decimais com divisão em .)")

class BuscaItemSchema(BaseModel):
    """Define como deve retorna a estrutura do objeto consultado através do ID.
    """

    id: int = Field(..., title="ID do item", description="O ID do item alvo do evento.")

class ListagemItemSchema(BaseModel):
    itens:List[ItemSchema]

def apresenta_itens(itens: List[Item]):
    """Lista todos os Itens cadastrados
    """

    resultado = []
    for item in itens:
        resultado.append({
            "id" : item.id,
            "nome" : item.nome,
            "quantidade" : item.quantidade,
            "valor" : item.valor
        })
    return {'itens' : resultado}

class ItemViewSchema(BaseModel):
    """Define como um Item será apresentado
    """

    id: int = 1
    nome: str = "Uramaki Salmão"
    quantidade: Optional[int] = 10
    valor: float = 4.99

class ItemDelSchema(BaseModel):
    """Descrição da exclusão
    """

    message : str
    id: int = Field(..., title="ID do item", description="O ID do item que deve ser excluído.")

def apresenta_item(item: Item):
    """ Retorna a exibição de um item
    """

    return {
        "id" : item.id,
        "nome" : item.nome,
        "quantidade" : item.quantidade,
        "valor" : item.valor
    }