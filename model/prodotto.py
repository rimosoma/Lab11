from dataclasses import dataclass
@dataclass()
class Prodotto:
        Product_number:int
        Product_line:str
        Product_type:str
        Product:str
        Product_brand:str
        Product_color:str
        Unit_cost:float
        Unit_price:float


        def __hash__(self):
                return hash(self.Product_number)