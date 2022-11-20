class AiStore:

    def __init__(self, s_name, s_id, s_locate):
        self.name = s_name
        self.s_id = s_id
        self.locate = s_locate
        self.products_EA = {'커피':10}
        self.products_Price = {'커피':1000}

    def set_product(self, product, count, price):
        if product in self.products_EA:
            self.products_EA[product] += count
            self.products_Price[product] = price
        elif product not in self.products_EA:
            self.products_EA[product] = count
            self.products_Price[product] = price

    def buy_product(self, product, count, amount):
        needmoney = self.products_Price[product] * count
        if self.products_EA[product] < count:
            print('재고가 부족합니다.')
        elif needmoney > amount:
            print('금액이 부족합니다.')
        else:
            print('잔돈은', amount-needmoney, '입니다')
            self.products_EA[product]-=count
            print('남은재고는', self.products_EA[product], '입니다')

    def get_name(self):
        return self.name
    def get_id(self):
        return self.s_id
    def get_locate(self):
        return self.locate
    def get_products(self):
        return self.products_EA
    def get_prices(self):
        return self.products_Price


def create_store():
    print('새로운 스토어를 생성합니다.')
    s_name = input('스토어 이름 입력: ')
    s_id = input('스토어 아이디 입력: ')
    s_locate = input('스토어 위치 입력: ')

    store=AiStore(s_name, s_id, s_locate)
    print('{} 스토어가 생성 되었습니다.'.format(store.get_name()))
    return store
    # 아이디 중복 확인 할 수 있는 코드 짜볼 것

def show_list():
    print('생성된 스토어 리스트 입니다.')
    for store in store_list:
        print('스토어 이름:{} 스토어 아이디:{} 스토어 위치:{}'
              .format(store.get_name(),
                      store.get_id(),
                      store.get_locate()
                      ))

def search_store(s_id):
    for store in store_list:
        if store.get_id() == s_id:
            return store
    print('스토어 아이디를 찾지 못했습니다.')
    return None


def show_store():
    print('스토어 아이디를 입력하면 해당 스토어 상품 재고와 가격 현황이 나옵니다')
    s_id = input('스토어 아이디 입력: ')
    store=search_store(s_id)
    # if store is none:
    #     return

    if store in store_list:
     print('{} 스토어 재고 현황: {}'
           .format(store.get_name(),
                   store.get_products()
                   ))
     print('{} 스토어 가격 현황: {}'
           .format(store.get_name(),
                   store.get_prices()
                   ))

def buy():
    print('스토어 아이디를 입력하면 해당 스토어 상품을 구매할 수 있습니다')
    s_id = input('스토어 아이디 입력: ')
    store=search_store(s_id)

    if store in store_list:
        product = input('상품 입력:')
        if product in store.get_products(): #구매시 상품 존재 여부 조건을 추가하였습니다.
            # store.products_EA =  store.products_Price  = store.get_products() = store.get_prices()
            count = int(input('구매 개수 입력: '))
            print('총 가격은', store.products_Price[product]*count, '입니다. 가격을 입력해 주세요')
            price = int(input('가격 입력: '))
            store.buy_product(product, count, price)
        else:
            print('{} 스토어에 해당 상품이 없습니다.'.format(store.get_name()))

def manager_product():
    print('아이디를 입력하면 상품 추가와 가격 변경을 할 수 있습니다.')
    s_id = input('스토어 아이디 입력: ')
    store = search_store(s_id)

    if store in store_list:
        product = input('상품 입력: ')
        count = int(input('추가 개수 입력: '))
        price = int(input('상품 가격 입력: '))

        store.set_product(product, count, price)

def txt_to_store():
    file = open('./stores.txt', 'r', encoding='UTF8')
    data = file.readlines()
    file.close()

    store_flist = []
    print('다음 스토어가 추가 되었습니다.')

    for store in data:
        store_flist.append(store.strip())
    for nameidlocate in store_flist:
        name_id_locate = nameidlocate.split(' ')
        print(name_id_locate)
        store = AiStore(name_id_locate[0], name_id_locate[1],name_id_locate[2])
        store_list.append(store)


import json
def store_to_json():
    file = open('./stores.json', 'w')
    json_data = []
    for store in store_list:
        store_dict = {
            'name': store.get_name(),
            's_id': store.get_id(),
            'locate': store.get_locate(),
            'products': store.get_products(),
            'prices': store.get_prices()
        }
        json_data.append(store_dict)

    json.dump(json_data, file)
    file.close()

    print('다음 json 파일이 생성 되었습니다')
    for i in range(len(json_data)):
        print(json_data[i])

if __name__ == '__main__':
    store_list = []

    print('1 - 스토어 생성')
    print('2 - 스토어 리스트 출력')
    print('3 - 스토어 정보 출력')
    print('4 - 상품 구매')
    print('5 - 상품 관리')
    print('6 - txt파일로 스토어 리스트 추가')
    print('7 - 스토어 정보 json파일로 내보내기')
    print('8 - 종료')

    while True:
        print('--'*30)
        input1 = input('옵션을 입력해 주세요: ')
        if input1 == '1':
            store=create_store()
            store_list.append(store)
        elif input1 == '2':
            show_list()
        elif input1 == '3':
            show_store()
        elif input1 == '4':
            buy()
        elif input1 == '5':
            manager_product()
        elif input1 == '6':
            txt_to_store()
        elif input1 == '7':
            store_to_json()
        elif input1 == '8':
            break
        else:
            print('존재하지 않는 명령어 입니다.')