from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker                # rysiams tarp lennteliu
from sqlalchemy import Column, Integer, String , Numeric, DateTime, ForeignKey
import datetime
Base = declarative_base()

engine = create_engine("sqlite:///:memory:", echo=False) # echo=True will allow you to see all SQL commands

class Shop(Base):
    __tablename__ = "shops"
    # Strukuros aprasas
    id = Column(Integer, primary_key=True)
    name = Column(String(length=40), nullable=False)
    address = Column(String(length=100))
    items = relationship("Item", backref="shops")

    # Naudojama informacijos spausdinimui
    def __repr__(self):
        return "<User('{id}','{name}','{address}')>".format(id=self.id, name=self.name, address=self.address)

class Item(Base):
    __tablename__ = "items"
    # Strukuros aprasas
    id = Column(Integer, primary_key=True)
    barcode = Column(String(length=32))
    name = Column(String(length=40), nullable=False)
    description = Column(String(length=200), default="Empty")
    unit_price = Column(Numeric(10, 2), default=1.00)
    created_at = Column(DateTime, default=datetime.datetime.now())
    shop_id = Column(Integer, ForeignKey('shops.id'))
    components = relationship("Component", backref="items")

    #Naudojama informacijos spausdinimui
    def __repr__(self):
        return "  <Item('{id}','{barcode}','{name}','{description}','{unit_price}','{created_at}','{shop_id}')>".format(id=self.id, barcode=self.barcode, name=self.name,description=self.description,unit_price=self.unit_price,created_at=self.created_at,shop_id=self.shop_id)

class Component(Base):
    # Strukuros aprasas
    __tablename__ = "components"
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    quantity = Column(Numeric(10, 2), default=1.00)
    item_id = Column(Integer, ForeignKey("items.id"))

    def __repr__(self):
        return "     <Component('{id}','{name}','{quantity}','{item_id}')>".format(id=self.id, name=self.name, quantity=self.quantity, item_id=self.item_id)

def outAll(shop,title):
    print("--------------{}-----------------".format(title))
    #parduotuves duomenys
    print(shop.__repr__())
    for el in shop.items:
        # item duomenys
        print(el.__repr__())
        for comp in el.components:
            #komponento duomenys
            print(comp)

def start():

    # Use a breakpoint in the code line below to debug your script.
    Base.metadata.create_all(engine)    #build table
    # naudojama darbui su DB
    Session = sessionmaker(bind=engine)
    session = Session()

    print("-------------Uzduotis 2--------------")
    # pildom duomenimis
    iki = Shop(name="IKI", address="Kaunas, Iki gatve 1")
    maxima = Shop(name="MAXIMA", address="Kaunas, Maksima gatve 2")
    iki.items = [
        Item(barcode="112233112233", name="Zemaiciu duona", unit_price=1.55),
        Item(barcode="33333222111", description="Pienas is Zemaitijos", name="Pienas is Zemaitijos", unit_price=2.69)
    ]
    maxima.items = [
        Item(barcode="99898989898", name="Aukstaiciu duona", unit_price=1.65),
        Item(barcode="99919191991", description="Pienas is Aukstaitijos", name="Aukstaiciu pienas", unit_price=2.99)
    ]

    iki.items[0].components = [Component(name="Miltai", quantity=1.50), Component(name="Vanduo", quantity=1.00)]
    iki.items[1].components = [Component(name="Pienas", quantity=1.00)]

    maxima.items[0].components = [Component(name="Miltai", quantity=1.60), Component(name="Vanduo", quantity=1.10)]
    maxima.items[1].components = [Component(name="Pienas", quantity=1.10)]
    #saugom DB
    session.add_all([iki, maxima])
    session.commit()
    # spaudinam
    outAll(iki,"IKI")
    outAll(maxima, "Maxima")

    #Uzduotis 3
    #Pakeisti 'IKI' parduotuvės, 'Žemaičių duonos' komponento 'Vandens' kiekį (quantity) iš 1.00 į 1.45.
    #Ištrinti 'MAXIMA' parduotuvės, 'Aukštaičių pieno' komponentą 'Pienas'.
    print("-------------Uzduotis 3--------------")
    iki.items[0].components[1].quantity = 1.45
    #salinamas elementas
    session.delete(maxima.items[1].components[0])
    session.commit()
    print ("Pakeitimai atlikti")

    # spaudinam rezultatus
    # 4 uzduotis
    print("-------------Uzduotis 4--------------")
    outAll(iki, "IKI")
    outAll(maxima, "Maxima")
    print("-------------Uzduotis 5--------------")
    """
    Sukurti užklausas:

    Atrinkti prekes, kurios turi susietų komponentų
    Atrinkti prekes, kurių pavadinime yra tekstas 'ien'
    Suskaičiuoti iš kiek komponentų sudaryta kiekviena prekė
    Suskaičiuoti kiekvienos prekės komponentų kiekį (quantity)
    Savo nuožiūra suformuoti pasirinktų duomenų užklausą, bei ją aprašyti.
    """
    print("Atrinkti prekes, kurios turi susietų komponentų")
    # imame Item elementus ir išfiltruojame kurie neturi komponentų
    for item in session.query(Item).filter( Item.components != None ):
        print(item)
    print("Suskaičiuoti iš kiek komponentų sudaryta kiekviena prekė")
    #imami Item elementai
    for item in session.query(Item):
        print(item)
        #skaiciuojamas komponentu skaicius
        print("komponentu kiekis: {}".format(len(item.components)))
    print("Suskaičiuoti kiekvienos prekės komponentų kiekį (quantity)")
    for item in session.query(Item):
        print(item)
        sum = 0
        # skaiciuojama komponentu quantity suma
        for comp in item.components:
            print(comp)
            sum = sum + comp.quantity
        print("bendras komponentų kiekis: {}".format(sum))
    print("Savo nuožiūra suformuoti pasirinktų duomenų užklausą, bei ją aprašyti.")
    print("mano uzklauoje ieskoma prekiu su zodzio fragmentu zemait prekes aprasyme")
    for item in session.query(Item).filter(Item.description.like("%zemait%")):
        print(item)


if __name__ == '__main__':
    start()