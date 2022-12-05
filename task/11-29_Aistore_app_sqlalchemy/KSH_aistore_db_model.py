from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base, db_session
from sqlalchemy.orm import relationship

class Aistore(Base):
    __tablename__ = 'stores'
    s_id = Column(String(20), primary_key=True) # 문자열(20), 주키 설정 하여 컬럼 생성
    name = Column(String(20))
    locate = Column(String(30))
    products_num = Column(Integer) # 숫자형 컬럼 생성

    def __init__(self, s_id, name, locate):
        self.s_id = s_id
        self.name = name
        self.locate = locate
        self.products_num = 0

    def add_product(self):
        self.products_num += 1

    def __repr__(self):
        return '<{}, {}, {}, {}>'.format(self.s_id, self.name, self.locate, self.products_num,)

class Products(Base):
    __tablename__ = 'products'
    p_id = Column(String(20), primary_key=True)
    name = Column(String(20))
    reco_price = Column(Integer)

    def __repr__(self):
        return '<{}, {}, {}>'.format(self.p_id, self.name, self.reco_price,)

class Inventory(Base):
    __tablename__ = 'inventory'
    p_id = Column(String(20), ForeignKey(Products.p_id), primary_key=True,)
    count = Column(Integer)
    price = Column(Integer)
    s_id = Column(String(20), ForeignKey(Aistore.s_id), )
    # 문자열(20), 외래키(AiStore.s_id), 주키 설정 하여 컬럼 생성
    product = relationship('Products') # products 테이블과 관계 형성되어 자동 조인(products 테이블의 주키가 외래키로 설정되어있어야함)

    def __init__(self, p_id, count, price, s_id):
        self.p_id = p_id
        self.count = count
        self.price = price
        self.s_id = s_id

    def add_count(self, count):
        self.count += count

    def sub_count(self, count):
        self.count -= count

    def __repr__(self):
        return '<{}, {}, {}, {}>'.format(self.p_id, self.count, self.price, self.s_id)

def create_store(s_id, s_name, locate):
    # s_id 가 존재 하지 않는 경우만 AiStore 인스턴스 생성후 데이터베이스에 추가
    # 커밋하여 데이터베이스 적용
    if db_session.get(Aistore, s_id) is None:
        s = Aistore(s_id, s_name, locate)
        db_session.add(s)
        db_session.commit()

def show_list(s_id = None):
    if s_id is None:
        # AiStore 전체 쿼리후 리스트로 반환
        stores = Aistore.query.all()
        return stores

    else:
        # s_id에 해당하는 AiStore를 리스트로 반환
        # 쿼리 사용 또는 get함수 사용 (AiStore가 하나여도 하나만 있는 리스트로 반환)
        store=[]
        store.append(db_session.get(Aistore, s_id))
        return store


def get_menu(s_id):

    # app의 board와 manage 페이지에서 스토어가 가진 상품을 보여주기 위한 menu 리스트 생성 함수
    # Inventory의 s_id가 파라미터의 s_id와 같은 Inventory 쿼리
    # .query.filter 함수 활용할 것
    # Inventory의 product 컬럼은 Products와 관계가 형성 되있으므로 자동조인됨
    # 관계 사용 안할시 다음과 같은 조인방식으로 가능
    # invs = db_session.query(Inventory.p_id, Inventory.price, Inventory.count, Products.product).join(Products, Inventory.p_id == Products.p_id)

    inventory=Inventory.query.filter(Inventory.s_id == s_id).all()
    #print(inventory)

    menu = []
    for i in range(len(inventory)):
        d = {}
        d['p_id'] = inventory[i].p_id
        d['p_name'] = inventory[i].product.name
        d['price'] = inventory[i].price
        d['count'] = inventory[i].count
        menu.append(d)


    # a=db_session.query(Inventory, Products).join(Inventory.p_id == Products.p_id).all()
    # for i in a:
    #     print(i)

    return menu


def set_product(s_id, p_id, price, count):
    a=Inventory.query.filter(Inventory.s_id == s_id, Inventory.p_id == p_id).all()
    # print(type(a[0]))
    # print(a[0])

    if len(a) != 0:
        db_session.query(Inventory).filter(Inventory.s_id == s_id, Inventory.p_id == p_id).update({'price': price})
        db_session.query(Inventory).filter(Inventory.s_id == s_id, Inventory.p_id == p_id).update({'count': count})
        db_session.commit()

    if len(a) == 0:
        inventory = Inventory(p_id, count, price, s_id)
        db_session.add(inventory)
        db_session.commit()

    # 없을때 상품 생성후 스토어의 product_num도 +1 (함수 사용)

def buy_product(p_id, s_id, count):
    # 입력된 재고 이상이 있을때 상품 구매
    # 파라미터로 입력된 s_id, p_id 값을 가지는 Inventory 쿼리 또는 get
    # inventory orm 의 재고가 입력된 재고 보다 클때 입력된 재고만큼 차감(함수 사용)
    # 커밋하여 데이터베이스 적용

    inventory = Inventory.query.filter(Inventory.s_id == s_id, Inventory.p_id == p_id).all()
    inventory[0].count -= count
    # print(inventory[0].count)
    db_session.commit()


    # db_session.query(Inventory).filter(Inventory.s_id == s_id, Inventory.p_id == p_id).update({'count': inventory[0].count})
    # db_session.commit()

    return True