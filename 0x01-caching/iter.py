# إنشاء قائمة
my_list = [1, 2, 3]

# إنشاء مكرر من القائمة
my_iterator = iter(my_list)
print(my_iterator)
# الحصول على العناصر واحدة بواحدة
first_element = next(my_iterator)  # كيرجع 1
second_element = next(my_iterator)  # كيرجع 2
third_element = next(my_iterator)   # كيرجع 3

print(first_element)  # غادي يطبع: 1
print(second_element)  # غادي يطبع: 2
print(third_element)  # غادي يطبع: 3
