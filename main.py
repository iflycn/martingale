import ctypes
import matplotlib.pyplot as plt
import random

class MARTINGALE():

    def __init__(self):
        pass

    def print_color_text(self, color, msg = None):
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), color)
        if msg:
            print(msg)
        ctypes.windll.kernel32.SetConsoleTextAttribute(ctypes.windll.kernel32.GetStdHandle(-11), 0x07)

    def shake_dicecup(self):
        rd = random.randint(0, 9)
        if rd % 2 == 0:
            return True
        else:
            return False

    def get_forecast(self, principal = 10000, lend = False):
        i = times = 0
        records = [[times, principal], [times, principal]]
        details = [[times, principal]]
        profit = principal * 2
        while principal > 0 and principal < profit:
            times += 1
            stake = 2 ** i
            interest = 0
            if not lend and stake > principal:
                stake = principal
            if lend and stake > principal:
                interest = int((stake - principal) * 0.1)
            if self.shake_dicecup():
                principal += stake
                i = 0
                if principal > records[0][1]:
                    records[0] = [times, principal]
                records[1] = [times, principal]
            else:
                principal -= stake + interest
                i += 1
            details.append([times, principal])
        records.append([times, principal])
        return records, details

if __name__ == "__main__":
    m = MARTINGALE()
    m.print_color_text(0x07)
    print("-" * 72)
    m.print_color_text(0x0b, "你走进了赌场，尝试使用加倍下注法，规则如下：\n")
    print("1、首次下注 1 元，如果输了，则加倍下注 2 元，再输则下注 4 元，以此类推")
    print("2、如果赢了，则重新从 1 元开始下注")
    print("3、在赌金不足时，你可以选择是否借贷，日利率 10%")
    print("4、盈利目标设置为赌金翻倍，一旦达成即退出")
    print("-" * 72)
    try:
        times = int(input("输入模拟次数 (默认 1 次): "))
    except:
        times = 1
    try:
        principal = int(input("输入你要携带的赌金 (默认 10000 元): "))
    except:
        principal = 10000
    lends = input("赌金不足时是否借贷 (Y/N) ? ")
    plt.figure(figsize = (12, 6)) 
    plt.rc("font", family = "Microsoft Yahei", size = 10)
    plt.suptitle("模拟加倍下注", fontsize = 18, fontweight = "bold")
    plt.xlabel("下注次数")
    plt.ylabel("赌金余额")
    plt.grid(color = "#999999", linestyle = "--", alpha = 0.4)
    winner = 0
    for i in range(times):
        if lends.lower() == "y":
            lend = ""
            records, details = m.get_forecast(principal, True)
        else:
            lend = "不"
            records, details = m.get_forecast(principal)
        print("\n你携带了 {} 元赌金，你选择了{}借贷，第 {} 次下注开始：".format(principal, lend, i + 1))
        print("-" * 72)
        if records[2][1] > 0:
            winner += 1
            m.print_color_text(0x0b, "在第 {} 次下注时，你达到止盈线，剩余赌金 {} 元。".format(records[2][0], records[2][1]))
            m.print_color_text(0x0b, "如果下注一次需要 60 秒，每天赌博 15 个小时，那么你大约花费了 {} 天时间。".format(int(records[2][0] * 60 / 54000) + 1))
        else:            
            m.print_color_text(0x0c, "在第 {} 次下注时，你输光了，剩余赌金 {} 元。".format(records[2][0], records[2][1]))
            m.print_color_text(0x0c, "如果下注一次需要 60 秒，每天赌博 15 个小时，那么你大约浪费了 {} 天生命。".format(int(records[2][0] * 60 / 54000) + 1))
            print("-" * 72)
            if records[0] == records[1]:
                print("第 {} 次是你最后一次，同时也是最好的一次收手机会，剩余赌金 {} 元。".format(records[0][0], records[0][1]))
            else:
                print("第 {} 次是你最好的一次收手机会，剩余赌金 {} 元。".format(records[0][0], records[0][1]))
                print("第 {} 次是你最后一次收手机会，剩余赌金 {} 元。".format(records[1][0], records[1][1]))
        print("-" * 72)
        x = []
        y = []
        for detail in details:
            x.append(detail[0])
            y.append(detail[1])
        plt.plot(x, y)
    print("成功模拟 {} 次，其中止盈 {} 次，破产 {} 次，胜率 {:.2f}%".format(times, winner, times - winner, winner / times * 100))
    plt.title("你走进了赌场，尝试使用加倍下注法，携带赌金 {} 元，模拟 {} 次，胜率 {:.2f}%".format(principal, times, winner / times * 100), fontsize = 8)
    plt.show()
