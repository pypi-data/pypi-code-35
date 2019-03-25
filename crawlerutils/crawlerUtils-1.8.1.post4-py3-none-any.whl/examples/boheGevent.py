from ..utils import Get


__all__ = ["runBoheGevent"]


url_list = [Get.queue.put_nowait(
    f"http://www.boohee.com/food/group/{str(i)}?page={str(j)}") for i in range(1, 11) for j in range(1, 11)]
url_list2 = [Get.queue.put_nowait(
    f"http://www.boohee.com/food/view_menu?page={str(i)}") for i in range(1, 11)]
url_list += url_list2


def crawler():
    while not Get.queue.empty():
        url = Get.queue.get_nowait()
        res_soup = Get(url).soup
        foods = res_soup.find_all('li', class_='item clearfix')
        for i in range(0, len(foods)):
            food_name = foods[i].find_all('a')[1]['title']
            print(food_name)
            food_url = 'http://www.boohee.com' + foods[i].find_all('a')[1]['href']
            food_calorie = foods[i].find('p').text
            Get.csvWrite(filepath="薄荷.csv", row=[food_name, food_url, food_calorie])


def runBoheGevent():
    Get.csvWrite(filepath="薄荷.csv")
    Get.csvWrite(filepath="薄荷.csv", row=["食物名称", "食物链接", "食物热量"])
    Get.geventRun(crawler, 5)
