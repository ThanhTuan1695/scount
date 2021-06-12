import asyncio
from pyppeteer import launch
import time
import regex

async def get_new_browser(url, headless:bool=True):
    browser = await launch({
        "headless" : headless,
        "ignoreHTTPSErrors": True,
        'autoClose': False,
        "args": [
            '--disable-infobars',  
            '--log-level=30',
            '--user-agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"',
            '--no-sandbox',
            '--start-maximized',
        ],
    })
    page = await browser.pages()
    current_page = page[0]
    await current_page.setJavaScriptEnabled(enabled=True)
    await page[0].goto(url)
    return browser

async def get_element_by_xpath(page, xpath):
    try:
        await page.waitForXPath(xpath, {
            "timeout" : 5000,
            "visible" : True
        })
        element = await page.xpath(xpath)
        return element[0]
    except Exception as exc:
        print("Not found element")
    return None
async def click_element(page, xpath):
    try:
        btn_button = await get_element_by_xpath(page, xpath)
        await btn_button.click()
        await page.evaluate('(btn_button) => { return btn_button;}', btn_button)
        return True
    except Exception as exc:
        print(str(exc))
        print("Click error")
    return False
async def login(user, passwd):
    browser = await get_new_browser('https://shopee.vn/buyer/login', False)
    pages = await browser.pages()
    current_page = pages[0]
    input_user = await get_element_by_xpath(current_page, '/html/body/div[1]/div/div[2]/div/div/form/div/div[2]/div[2]/div[1]/input')
    input_passwd = await get_element_by_xpath(current_page, '/html/body/div[1]/div/div[2]/div/div/form/div/div[2]/div[3]/div[1]/input')
    await input_user.type(user)
    await input_passwd.type(passwd)
    await current_page.keyboard.press("Enter")
    time.sleep(2)
    return browser

async def change_address(browser, tinh, quan, phuong, duong, sdt):
    pages = await browser.pages()
    page = pages[0]
    await page.goto("https://shopee.vn/user/account/address")
    await click_element(page, '//*[@id="main"]/div/div[2]/div[2]/div[2]/div/div/div[3]/div[2]/div/div[3]/div[1]/button[1]')
    xpath_sdt = '//*[@id="modal"]/div[2]/div[1]/div/div/div[2]/div/div[3]/div/div[1]/input'
    xpath_duong = '//*[@id="modal"]/div[2]/div[1]/div/div/div[2]/div/div[7]/div/div[1]/input'
    xpath_select_tinh = '/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[4]/div/div/div/div[2]'                    
    xpath_select_quan = '/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]/div/div/div/div[2]'
    xpath_select_phuong = '/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[6]/div/div/div/div[2]'
    xpath_button_submit = '/html/body/div[2]/div[2]/div[1]/div/div/div[3]/button[2]'

    # Change so dien thoai
    input_sdt = await get_element_by_xpath(page, xpath_sdt)
    await input_sdt.click({"clickCount" : 3})
    await input_sdt.type(sdt)

    # Change ten duong
    input_duong = await get_element_by_xpath(page, xpath_duong)
    await input_duong.click({"clickCount" : 3})
    await input_duong.type(duong)
    # Change tinh
    await click_element(page, xpath_select_tinh)
    try:
        for i in range(1, 64):
            xpath_value_tinh = "/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[4]/div/div/div/div[3]/div/div[%s]" % str(i)
            value_tinh_element = await get_element_by_xpath(page, xpath_value_tinh)
            value = await page.evaluate("(value_tinh_element) => {return value_tinh_element.innerText}", value_tinh_element)
            if value.lower() == tinh.lower():
                await value_tinh_element.click()
                break
    except Exception as exc:
        print("Not found ten tinh")
    # Change quan
    await click_element(page, xpath_select_quan)
    try:
        for i in range(1, 100):
            xpath_value_quan = "/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[5]/div/div/div/div[3]/div/div[%s]" % str(i)
            value_quan_element = await get_element_by_xpath(page, xpath_value_quan)
            value = await page.evaluate("(value_quan_element) => {return value_quan_element.innerText}", value_quan_element)
            if value.lower() == quan.lower():
                await value_quan_element.click()
                break
    except Exception as exc:
        print("Not found ten quan")

    # Change phuong
    await click_element(page, xpath_select_phuong)
    try:
        for i in range(1, 100):
            xpath_value_phuong = "/html/body/div[2]/div[2]/div[1]/div/div/div[2]/div/div[6]/div/div/div/div[3]/div/div[%s]" % str(i)
            value_phuong_element = await get_element_by_xpath(page, xpath_value_phuong)
            value = await page.evaluate("(value_phuong_element) => {return value_phuong_element.innerText}", value_phuong_element)
            if value.lower() == phuong.lower():
                await value_phuong_element.click()
                break
    except Exception as exc:
        print("Not found ten phuong")
    # Click button
    await click_element(page, xpath_button_submit)

async def get_status_don_hang(browser, url):
    page =await browser.newPage()
    id_don_hang = "Error"
    status_don_hang = "Error"
    try:
        await page.goto(url)
        element_id = await get_element_by_xpath(page, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/span[1]")
        element_status = await get_element_by_xpath(page, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/span[3]")
        id_don_hang = await page.evaluate('(element_id) => {return element_id.innerText}', element_id)
        status_don_hang = await page.evaluate('(element_status) => {return element_status.innerText}', element_status)
    except Exception as exc:
        raise("Error in get_status_don_hang")
    await page.close()
    return (id_don_hang, status_don_hang)

async def check_status_don_hang(browser):
    list_res = []
    pages = await browser.pages()
    page = pages[0]
    await page.goto("https://shopee.vn/user/purchase/")
    idx = 1
    while True:
        try:
            xpath_don_hang = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div[5]/div[%s]/div[1]/div/a" % str(idx)
            element_don_hang = await get_element_by_xpath(page, xpath_don_hang)
            url_don_hang = await page.evaluate('(element_don_hang) => {return element_don_hang.href}', element_don_hang)
            url_don_hang = "https://shopee.vn/" + url_don_hang if "https://shopee.vn/" not in url_don_hang else url_don_hang
            tuple_res = await get_status_don_hang(browser, url_don_hang)
            list_res.append(tuple_res)
            idx+=1
        except Exception as exc:
            break
    return list_res

async def order_shopee(browser, dict_san_pham: dict)-> bool:
    page = browser.newPage()
    await page.goto(dict_san_pham["url"])

    # So luong
    element_input = await get_element_by_xpath(page, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[3]/div/div[2]/div[2]/div[1]/div/input")
    await element_input.click({"clickCount" : 3})
    await element_input.type(dict_san_pham["so_luong"])

    # Phan loai
    idx = 1
    for idx_label in range(1, 10):
        try:
            xpath_label = "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[%s]/div/div[1]/label" % str(idx_label)
            element_phan_loai = await get_element_by_xpath(page, xpath_label)
            value_phan_loai = await page.evaluate('(element_phan_loai)=> {return element_phan_loai.innerText}', element_phan_loai)
            if value_phan_loai.lower() in dict_san_pham["phan_loai"]:
                for idx in range(1,100):            
                    xpath_choose =  '/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[4]/div/div[%s]/div/div[1]/div/button[%s]' % (str(idx_label), str(idx))
                    element_choose = await get_element_by_xpath(page, xpath_choose)
                    value_element = await page.evaluate('(element_choose)=> {return element_choose.innerText}', element_choose)
                    if value_element.lower() == dict_san_pham["phan_loai"][value_phan_loai].lower():
                        await element_choose.click()
                        break
        except Exception as exc:
            pass

    # Click mua hang
    await click_element(page, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[3]/div/div[5]/div/div/button[2]")

    if await page.title.lower() == "Giỏ Hàng".lower():
        # Su dung xu
        if dict_san_pham["su_dung_xu"] == True:
            await click_element(page, "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[3]/label/div")
        if dict_san_pham["shop_voucher"] is not None:
            await click_element(page, "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[1]/span")

            # Nhap shoppe voucher
            input_voucher = await get_element_by_xpath(page, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/div/input")
            await input_voucher.type(dict_san_pham["shop_voucher"])
            await click_element(page, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/button")
            # To do: voucher de check

            # Click xem them neu co
            try:
                await click_element(page, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[4]/div[1]")
            except:
                pass

            for i in range(1, 10):  # Check voucher freeship
                try:
                    xpath_voucher_freeship = "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div[%s]/div/div[2]/div[2]/div[1]/div" % str(i)
                    element_voucher_freeship = await get_element_by_xpath(page, xpath_voucher_freeship)
                    await element_voucher_freeship.click()
                    break
                except Exception as exc:
                    pass
            
            for i in range(1, 10):  # Check voucher discount
                try:
                    xpath_voucher_discount = "/html/body/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div[7]/div[%s]/div/div[2]/div[2]/div[1]/div" % str(i)
                    element_voucher_discount = await get_element_by_xpath(page, xpath_voucher_discount)
                    await element_voucher_discount.click()
                    break
                except Exception as exc:
                    pass
            
            # Click ok
            await click_element(page, "/html/body/div[2]/div[2]/div/div[2]/div/div/div[3]/button[2]")
        
        # Click mua hang
        await click_element(page, "/html/body/div[1]/div/div[2]/div[2]/div/div[3]/div[2]/div[7]/div[5]/button")

        # Click phuong thuc thanh toan
        await click_element(page, "/html/body/div[1]/div/div[3]/div[2]/div[4]/div[1]/div/div[3]")
        # Click vi_shopee_pay
        await click_element(page, "/html/body/div[1]/div/div[3]/div[2]/div[4]/div[1]/div/div[1]/div[2]/span[1]/button")

        # get price
        element_price = get_element_by_xpath(page, "/html/body/div[1]/div/div[3]/div[2]/div[4]/div[2]/div[9]")
        value_price = page.evaluate('(element_price) => {return element_price.innerText}', element_price)
        if int(regex.sub('[^0-9]','', value_price)) > MAX_PRICE:
            raise "Price too high"
        else:
            # Click dat hang
            await click_element(page, "/html/body/div[1]/div/div[3]/div[2]/div[4]/div[2]/div[10]/button")
            return True
    else:
        raise "Order error"