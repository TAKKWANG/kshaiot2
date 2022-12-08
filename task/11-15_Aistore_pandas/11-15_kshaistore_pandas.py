import pandas as pd


class AiStore:

    def __init__(self, name, s_id, locate, products_num, inventory):
        self.name = name
        self.s_id = s_id
        self.locate = locate
        self.products_num = products_num
        self.inventory = inventory

    def set_product(self, p_id, s_id, count, price):
        if p_id in self.inventory.index:
            self.inventory.loc[(p_id, s_id), 'count'] += count
            self.inventory.loc[(p_id, s_id), 'price'] = price
            iv_df.loc[(p_id, s_id)] = self.inventory.loc[(p_id, s_id)]
            return iv_df

        else:
            n_product = pd.DataFrame([[p_id, count, price, s_id]],
                                      columns=['p_id', 'count', 'price', 's_id'])
            n_product = n_product.set_index(['p_id', 's_id'], drop=False)
            #print(n_product)

            self.inventory=pd.concat([self.inventory,n_product])
            s_df.loc[s_id, 'products_num'] = len(self.inventory)

            n_iv_df = pd.concat([iv_df, n_product])
            #print(n_iv_df)

            return n_iv_df

            # n_product = {'p_id': p_id, 'count': count, 'price': price, 's_id': self.s_id}
            # n_product = [ p_id, count, price, self.s_id]
            # print(n_product)

            #iv_df = iv_df.append(n_product)
            #iv_df = pd.concat([iv_df, n_product])
            #iv_df.sort_index()

            # re_n_product = n_product.reset_index(drop=True)
            # re_iv_df = iv_df.reset_index(drop=True)
            # b = pd.concat([re_iv_df, re_n_product])
            # a=b.sort_index()


    def buy_product(self, p_id, s_id, count, amount):
        if p_id not in self.inventory.index:
            print('상품이 존재하지 않습니다.')
            return

        if count > self.inventory.loc[(p_id, s_id), 'count']:
            print('재고가 부족합니다')
            return

        if amount < self.inventory.loc[(p_id, s_id), 'price'] * count:
            print('가격이 부족합니다.')
            return

        changes = amount - self.inventory.loc[(p_id, s_id), 'price'] * count
        print('잔돈은 {}' '입니다'.format(changes))

        self.inventory.loc[(p_id, s_id),'count'] -= count


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

    def show_products(self, ):
        for product in self.inventory.iloc:
            p_id = product['p_id']
            p_name = p_df.loc[p_id,'product']
            price = product['price']
            count = product['count']
            print('상품명 :{} - 가격 :{} - 재고 :{} - 상품id :{}'
                  .format(p_name, int(price), int(count), p_id))

    def get_price(self, p_id, s_id):
        price = self.inventory.loc[(p_id, s_id), 'price']
        return price

def create_store():
    s_name = input('스토어 이름 입력: ')
    s_id = input('스토어 번호 입력: ')
    locate = input('스토어 위치 입력: ')
    store = {'s_id': s_id,
             'name': s_name,
             'locate': locate,
             'products_num': 0,}

    s_df.loc[s_id] = store
    print('{} 스토어가 생성 되었습니다.'.format(store['name']))


def show_list():
    for store in s_df.iloc:
        print('스토어 이름:{} 스토어 번호:{} 스토어 위치:{}'
              .format(store['name'],
                      store['s_id'],
                      store['locate']
                      ))

def search_store(s_id):
    if s_id in s_df.index:
        storeseries = s_df.loc[s_id]
        #inventory = iv_df.loc[(slice(None),s_id), :]
        inventory = iv_df[iv_df['s_id'] == s_id]
        #print(inventory)
        store = AiStore(storeseries['name'],
                       storeseries['s_id'],
                       storeseries['locate'],
                       storeseries['products_num'],
                       inventory)
        return store

    elif s_id not in s_df.index:
        print('스토어를 찾지 못했습니다.')
        return None


def show_store():
    s_id = input('스토어 번호 입력: ')
    store = search_store(s_id)
    if store is None:
        return

    print('{}스토어 위치:{} 등록상품:{}'
          .format(store.get_name(),
                  store.get_locate(),
                  store.get_products_num(),
                  ))

    store.show_products()

def buy():
    s_id = input('스토어 번호 입력: ')
    store = search_store(s_id)
    if store is None:
        return
    print('구매 가능 상품')
    store.show_products()

    p_id = input('상품 아이디 입력:')
    if p_id not in store.inventory['p_id']:
        print('구매 가능한 상품이 아닙니다')
        return
    count = int(input('구매 개수 입력: '))

    # 옵션
    price = store.get_price(p_id, s_id)
    if price is not None:
        print('총 가격은 {} 입니다.'.format(price * count))

    price = int(input('가격 입력: '))

    store.buy_product(p_id, s_id, count, price)
    iv_df.loc[(p_id, s_id)] = store.inventory.loc[(p_id, s_id)]


def manager_product(iv_df):

    s_id = input('스토어 번호 입력: ')
    store = search_store(s_id)
    if store is None:
        return iv_df

    print('등록 가능 상품')
    print(p_df)
    p_id = input('상품 아이디 입력: ')
    if p_id not in p_df['p_id']:
        print('잘못된 입력 입니다')
        return iv_df

    count = int(input('재고 개수 입력: '))
    price = int(input('상품 가격 입력: '))

    iv_df = store.set_product(p_id, s_id, count, price)
    return(iv_df)


def products_counts():
    reiv_df = iv_df.reset_index(drop=True)
    rep_df = p_df.reset_index(drop=True)

    ivp_df = reiv_df.merge(rep_df, on='p_id')
    pc_df = ivp_df[['product','count']].groupby(by = 'product').sum()
    print(pc_df)


if __name__ == '__main__':

    s_df = pd.read_csv('./stores.csv')
    s_df = s_df.set_index('s_id', drop= False)

    iv_df = pd.read_csv('./inventory.csv')
    iv_df = iv_df.set_index(['p_id', 's_id'], drop=False)

    p_df = pd.read_csv('./products.csv')
    p_df = p_df.set_index('p_id', drop=False)


    print('1 - 스토어 생성')
    print('2 - 스토어 리스트 출력')
    print('3 - 스토어 정보 출력')
    print('4 - 상품 구매')
    print('5 - 상품 관리')
    print('6 - csv 파일로 스토어, 재고현황 파일 출력')
    print('7 - 상품명별 전체 재고 개수 출력')
    print('8 - 종료')

    while True:
        print('--'*30)
        input1 = input('옵션을 입력해 주세요: ')
        if input1 == '1':
            create_store()
        elif input1 == '2':
            show_list()
        elif input1 == '3':
            show_store()
        elif input1 == '4':
            buy()
        elif input1 == '5':
            iv_df = manager_product(iv_df)
        elif input1 == '6':
            s_df.to_csv('store_v2.csv', index= False)
            iv_df.to_csv('inventory_v2.csv', index= False)
        elif input1 == '7':
            products_counts()
        elif input1 == '8':
            break
        else:
            print('존재하지 않는 명령어 입니다.')
