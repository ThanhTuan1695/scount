from core import get_new_browser, change_address, login, check_status_don_hang, order_shopee 
import asyncio
from concurrent.futures import ThreadPoolExecutor
from data_access import get_data_from_address_excel_file, get_data_from_goods_excel_file
async def main():
    browser = await login("84937503940", "hQQcAtrwjwS")
    dict_san_pham = {
        "url" : "https://shopee.vn/%C3%81o-kho%C3%A1c-Jean-Nam-Strange-cao-c%E1%BA%A5p-%C3%A1o-kho%C3%A1c-b%C3%B2-Nam-c%C3%A1-t%C3%ADnh-standbyshop888-i.420989394.11104718416",
        "so_luong" : 2,
        "voucher" : None,
        "shop_voucher" : None,
        "phan_loai" : {     # Doc du lieu o dang text -> PHAI chuyen ve dict
            "size" : "L (<1m65, <62kg)"
        },
        "don_vi_van_chuyen" : None,
        "mua_kem" : None,
        "su_dung_xu" : None,
        "free_ship" : None,
        "max_price" : 720000
    }

asyncio.get_event_loop().run_until_complete(main())