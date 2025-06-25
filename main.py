import re
from splinter.browser import Browser
from time import sleep
import sys
from selenium.webdriver.common.by import By


class BrushTicket(object):
    """买票类及实现方法"""

    def __init__(self, user_name, password, passengers, from_time, from_station, to_station,seat_type):
        """定义实例属性，初始化"""
        # 1206账号密码
        self.user_name = user_name
        self.password = password
        # 乘客姓名
        self.passengers = passengers
        # 起始站和终点站
        self.from_station = from_station
        self.to_station = to_station
        # 乘车日期
        self.from_time = from_time

        # 座位类型所在td位置
        if seat_type == '商务座特等座':
            seat_type_index = 1
        elif seat_type == '一等座':
            seat_type_index = 2
        elif seat_type == '二等座':
            seat_type_index = 3
        elif seat_type == '高级软卧':
            seat_type_index = 4
        elif seat_type == '软卧':
            seat_type_index = 5
        elif seat_type == '动卧':
            seat_type_index = 6
        elif seat_type == '硬卧':
            seat_type_index = 7
        elif seat_type == '软座':
            seat_type_index = 8
        elif seat_type == '硬座':
            seat_type_index = 9
        elif seat_type == '无座':
            seat_type_index = 10
        elif seat_type == '其他':
            seat_type_index = 11
        else:
            seat_type_index = 7
        self.seat_type_index = seat_type_index

        # 主要页面网址
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.init_my_url = 'https://kyfw.12306.cn/otn/view/index.html'
        self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
        self.driver_name = 'chrome'
        self.executable_path = r'.\D:\\python\chromedriver.exe'
    def do_login(self):
        """登录功能实现，手动识别验证码进行登录"""
        self.driver.visit(self.login_url)
        sleep(1)
        element1=self.driver._find_elements(By.ID, "J-userName")
        element1[0].send_keys(self.user_name)
        element2=self.driver._find_elements(By.ID, "J-password")
        element2[0].send_keys(self.password)
        element3=self.driver._find_elements(By.ID, "J-login")
        element3[0].click()

        print('请输入验证码……')

        while True:
            if self.driver.url != self.init_my_url:

                sleep(1)
            else:
                break

    def start_brush(self):
        """买票功能实现"""
        self.driver = Browser(driver_name=self.driver_name)
        # 浏览器窗口的大小
        self.driver.driver.set_window_size(900, 700)
        self.do_login()
        self.driver.visit(self.ticket_url)
        try:
            print('开始刷票……')
            # 加载车票查询信息
            self.driver.cookies.add({"_jc_save_fromStation": self.from_station})
            self.driver.cookies.add({"_jc_save_toStation": self.to_station})
            self.driver.cookies.add({"_jc_save_fromDate": self.from_time})
            self.driver.reload()
            count = 0
            while self.driver.url.split('?')[0] == self.ticket_url:
                self.driver.find_by_text('查询').click()
                sleep(1)
                count += 1
                print('第%d次点击查询……' % count)
                try:
                    car_no_location = self.driver.find_by_id("queryLeftTable")[0]
                    current_tr = car_no_location.find_by_xpath("./../../../../..")
                    if current_tr.find_by_tag('td')[self.seat_type_index].text == '--':
                        print('无此座位类型出售，已结束当前刷票，请重新开启！')
                        sys.exit(1)
                    elif current_tr.find_by_tag('td')[self.seat_type_index].text == '无':
                        print('无票，继续尝试……')
                    else:
                        # 有票，尝试预订
                        print('刷到票了，开始尝试预订……')
                        current_tr.find_by_css('td.no-br>a')[0].click()
                        sleep(0.2)

                        for p in self.passengers:
                            # 选择用户
                            print('开始选择用户……')
                            sleep(2)
                            element1=self.driver._find_elements(by=By.XPATH, value='//*[@id="normalPassenger_0"]')
                            element1[0].click()
                            element2=self.driver._find_elements(by=By.XPATH, value='//*[@id="dialog_xsertcj_close"]')
                            element2[0].click()
                            # 选择座位类型
                            print('开始选择席别……')
                            sleep(0.5)

                        print('正在提交订单……')

                        sleep(8)
                        self.driver.find_by_id('submitOrder_id').click()
                        print('正在确认订单……')
                        sleep(800)
                        self.driver.find_by_id('qr_submit_id').click()
                        print('预订成功，请在两分钟内及时前往支付……')


                except Exception as error_info:
                    print(error_info)
        except Exception as error_info:
            print(error_info)



if __name__ == '__main__':

    # 12306用户名
    user_name = input('请输入12306用户名：')
    while user_name == '':
        user_name = input('12306用户名不能为空，请重新输入：')
    # 12306登陆密码
    password = input('请输入12306登陆密码：')
    while password == '':
        password = input('12306登陆密码不能为空，请重新输入：')
    # 乘客姓名
    passengers_input = input('请输入乘车人姓名：')
    passengers = passengers_input.split(",")
    while passengers_input == '' :
        print('乘车人最少1位！')
        passengers_input = input('请重新输入乘车人姓名：')
        passengers = passengers_input.split(",")
    # 乘车日期
    from_time = input('请输入乘车日期（例如“2025-01-20”）：')
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    while from_time == '' or re.findall(date_pattern, from_time) == []:
        from_time = input('乘车日期不能为空或者时间格式不正确，请重新输入：')
    # 城市cookie字典
    city_list = {
        'bj': '%u5317%u4EAC%2CBJP',  # 北京
        'nn': '%u5357%u5B81%2CNNZ',  # 南宁
        'wh': '%u6B66%u6C49%2CWHN',  # 武汉
        'cs': '%u957F%u6C99%2CCSQ',  # 长沙
        'qj': '%u6F5C%u6C5F%2CQJN',  #潜江
        'njn':'%u5357%u4EAC%u5357%2CNKH',  #南京南
        'shhq':'%u4E0A%u6D77%u8679%u6865%2CAOH', #上海虹桥
        'gzn': '%u5E7F%u5DDE%u5357%2CIZQ',  # 广州南
        'wzn': '%u68A7%u5DDE%u5357%2CWBZ',  # 梧州南

    }
    # 出发站
    from_input = input('请输入出发站，只需要输入首字母就行（例如上海虹桥“shhq”）：')
    while from_input not in city_list.keys():
        from_input = input('出发站不能为空或不支持当前出发站，请重新输入：')
    from_station = city_list[from_input]
    # 终点站
    to_input = input('请输入终点站，只需要输入首字母就行（例如上海虹桥“shhq”）：')
    while to_input not in city_list.keys():
        to_input = input('终点站不能为空或不支持当前终点站，请重新输入：')
    to_station = city_list[to_input]
    # 座位类型
    seat_type = input('请输入座位类型（例如“软卧”）：')
    while seat_type == '':
        seat_type = input('座位类型不能为空，请重新输入：')

    # 开始购票
    ticket = BrushTicket(user_name, password, passengers, from_time, from_station, to_station,  seat_type)
    ticket.start_brush()

