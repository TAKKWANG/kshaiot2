import pandas as pd

s_df = pd.read_csv('./static/stores.csv')
s_df = s_df.set_index('s_id', drop=False)
p_df = pd.read_csv('./static/products.csv')
iv_df = pd.read_csv('./static/inventory.csv')

class AiStore:

    def __init__(self, name, s_id, locate, products_num, inventory):
        self.name = name
        self.s_id = s_id
        self.locate = locate
        self.products_num = products_num
        self.inventory = inventory

    def add_product(self, p_id, count, price, idx):
        n_product = {'p_id': p_id, 'count': count, 'price': price, 's_id': self.s_id}
        self.inventory.loc[idx] = n_product
        self.products_num = len(self.inventory)
        return n_product

    def set_product(self, p_id, count, price):
        product =  self.inventory[self.inventory['p_id'] == p_id]
        product['count'] += count
        product['price'] = price
        self.inventory.update(product)

    def is_product(self, p_id):
        product = self.inventory[self.inventory['p_id'] == p_id]
        if len(product) == 0:
            return False
        else:
            return True
    def buy_product(self, p_id, count):

        product =  self.inventory[self.inventory['p_id'] == p_id]
        product = product[product['count'] > count]
        if len(product) == 0:
            return

        product['count'] -= count
        self.inventory.update(product)

    def get_name(self):
        return self.name

    def get_id(self):
        return self.s_id

    def get_locate(self):
        return self.locate

    def get_products_num(self):
        return self.products_num

    def get_inventory(self):
        return self.inventory

    def get_menu(self):
        #a = {'p_name': p_name, 'price': int(price), 'count': int(count), 'p_id':p_id}
        # 형태로 인벤토리의 상품들을 메뉴리스트에 추가
        #print(self.inventory)

        common = []
        for p1 in self.inventory.iloc:
            for p2 in p_df.iloc:
                if p1['p_id'] == p2['p_id']:
                    common.append(p2['product'])
        #print(common)

        self.inventory=self.inventory.reset_index()

        menu = []
        for i in range(len(self.inventory)):
            d={}
            d['p_id'] = self.inventory.loc[i, 'p_id']
            d['p_name'] = common[i]
            d['price'] = self.inventory.loc[i, 'price']
            d['count'] = self.inventory.loc[i, 'count']
            menu.append(d)

        #print(menu)
        return menu

    def get_product(self, p_id):
        # p_id 해당하는 상품 반환 인벤토리에서 쿼리 후 .iloc[0] 을 통해 상품 가져올것
        p = p_df[p_df['p_id'] == p_id]
        #print(p)

        for product in self.inventory.iloc:
            if product['p_id'] == p_id:
                d={}
                d['p_id'] = product['p_id']
                d['p_name'] = p['product'].values[0]
                d['price'] = product['price']
                d['count'] = product['count']

        return d
#{'p_name': p_name, 'price': int(price), 'count': int(count), 'p_id':p_id}


def create_store(s_id, s_name, locate):

    store = {'s_id': s_id, 'name': s_name,
             'locate': locate,
             'products_num': 0,}

    s_df.loc[s_id] = store
    print('{} 스토어가 생성 되었습니다.'.format(store['name']))


def show_list(s_id = None):
    if s_id is None:
        print(s_df.to_dict('records'))
        return s_df.to_dict('records')
    else:
        print(s_df[s_df['s_id'] == s_id].to_dict('records'))
        return s_df[s_df['s_id'] == s_id].to_dict('records')

def search_store(s_id):
    print(s_id)
    if s_id in s_df.index:
        store = s_df.loc[s_id]
        # 인벤토리에서 s_id에 해당하는 상품 쿼리 후 p_df 와 p_id를 기준으로 머지 (인벤토리가 왼쪽이 되야함)
        inventory = iv_df[iv_df['s_id'] == s_id]

        return AiStore(store['name'],
                       store['s_id'],
                       store['locate'],
                       store['products_num'],
                       inventory)
    else:
        print('스토어를 찾지 못했습니다.')
        return None

def get_products():
    return p_df.to_dict('records')

def set_product(store, p_id, price, count):

    if store.is_product(p_id):
        store.set_product(p_id, int(count), int(price))
    else:
        idx = len(iv_df)
        n_product = store.add_product(p_id, int(count), int(price), idx)
        iv_df.loc[idx] = n_product

def update(store: AiStore):
    s_df[store.get_id()] = {'s_id': store.get_id(),
                       'name': store.get_name(),
                       'locate': store.get_locate(),
                       'products_num': store.get_products_num(), }
    iv_df.update(store.get_inventory())

