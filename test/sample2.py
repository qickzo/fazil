# numlist = [1,2,3,4,50,4]
# # for i in numlist:
# #     print(i)
# print(numlist[2])
# print(numlist[-1])
# print(numlist[::])
#
# print(1 not in numlist)
# numlist2 = [1,2,3,4,50,4]
# name1 = "abc"
# name2 = "abc"
# print(name1 is name2)
# numlist2.append('esasd')
# numlist2.insert(1,"name")
# print(numlist2)
# numlist2.remove(4)
# print(numlist2)
# numlist2.pop(2)
# print(numlist2)
# # numlist2.clear()
# # print(numlist2)
# del numlist2[1]
# print(numlist2)

# students = {'name': 'fazil', 'class': 'BTECH', 'PLACE': 'ALLOOR'}
# print(students)
# students['name'] = "Dilshad"
# print(students)

# # print()
#
# for i in students:
#     # print(students[i])
#     name = students[i]
#     print("Hello "+ name)
# print(students)
# print(students.items())
# for value in students.values():
#     print("------------------------------")
#     print(value)

# name = "Dilshad"
# age = 20
# print("hello ", name, "age is ",str(age))
# print("Hello %s , age is %d"%(name,age))
# print("hello {1} , age is {0}".format(name, age)

# a = 10
# b = 12
# if a < b: print("b is greater")
# print("b is greater") if a < b else print("a is greater")
# num = [1, 2, 3, 4, 5, 6]
# num1 = []
# for i in num:
#     i =  i + 2
#     num1.append(i)
# print(num1)
# # num = [i+2 for i in num]
# num_even = [n for n in num if n%2==0]
# num_even = [n for n in num if n%2==0]
#
# num_even1 = []
# for i in num:
#     if i % 2 == 0:
#         num_even1.append(i)
# # num_even
# print("num_even1 = ", num_even1)
# print("num_even = ", num_even)

# a = int(input("enter aa number"))
# for i in range(a+1):
#     print(i * '*')
#
# print('\n\n\n')
# a = '*'
# for i in range(11):
#     print(a)
#     a += '*'
# n = ""
# for i in range(1, a):
#     n = n + " " + str(i)
#     print(n)
# a = '*'
# count = int(input())
# c = count
# for i in range(count):
#     contnt = c * '  ' + a
#     print(contnt)
#     a = a + '   *'
#     c -= 1

# while condition:
# #     statements
# a, b, c = 10, 20, 30
# while not(a==b):
#     print('a = ', a)
#     a += 5
#     b += 3
#     c += 2
#
# print(a,b)


# a = lambda x, y: x+y
# print(a(5, 6))


# def function_name(parameeters):
#     statements

# def hello():
#    return "hello"
#
# h = hello()
# print(h)


# def su(a, b):
#     return a + b
#
#
# def avg():
#     return su(1, 2) / 2
# print(avg())
# n = 12
# a = n
# for i in range(n):
#     print('******',n* '*'+' '*(i*2)+n*'*','******',)
#     n -= 1
#
# print('******',(a)*2*'*','******',)
# print('******',(a)*2*'*''******',)
# print('******',(a)*2*'*''******',)

# a = lambda x, y: (x+y)*2
#
# print(a(1,2))

# def hello(sum):
#     return sum/2
#
#
# def sum(a, b):
#     return a + b

# def avg(a, b):
#     def sum(a,b):
#         return a+b
#     return sum(a,b)/2
#
#
# print(avg(10,20))
#
# print(hello(sum(3,4)))

# def fact(n):
#     if n<=1: return 1
#     return n*fact(n-1)
#
# print(fact(5))
