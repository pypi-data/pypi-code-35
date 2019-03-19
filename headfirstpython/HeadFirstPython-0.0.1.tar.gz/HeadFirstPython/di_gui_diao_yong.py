print("案例1：斐波那契数列，第一个数是1，第二个数是1，第三个数是2（前两数和）")
def fb(n):
    if n == 1:
        return 1
    if n == 2:
        return 1
    return fb(n - 1) + fb(n - 2)

shulie = 5
print("斐波那契数列第{}个数是：{}".format(shulie, fb(shulie)))

print("案例2：青蛙跳台阶，每次可以随机跳1级或2级")
def frog(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return frog(n - 1) + frog(n - 2)

fg = 4
print("青蛙跳{}级台阶能有{}种方法".format(fg, frog(fg)))

print("案例3：反转单链表")
def frog(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return frog(n - 1) + frog(n - 2)

fg = 4
print("青蛙跳{}级台阶能有{}种方法".format(fg, frog(fg)))