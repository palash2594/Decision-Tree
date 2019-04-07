import sqlite3
import math


class Node:
    __slots__ = "name", "split_point", "left_node", "right_node"

    def __init__(self, name, split_point):
        self.name = name
        self.split_point = split_point

conn = sqlite3.connect(':memory:')
c = conn.cursor()

def create_conn():

    # create table
    c.execute("""Create table iris_dataset (
        sepal_length float,sepal_width float, petal_length float, petal_width float, iris_type text
        )""")
    conn.commit()


    # file read
    file_data = open("iris.data.txt", "r")


    db_read = []

    line_num = 0
    for line in file_data:
        line_data = line.strip().split(",")
        c.execute("Insert into iris_dataset values ("+ line_data[0] +" ," + line_data[1] +"," + line_data[2] +" , " + line_data[3] + ", '" + line_data[4] +"')")
        line_num += 1
        if line_num % 20 == 0:
            conn.commit()
    conn.commit()
    file_data.close()

    # c.execute("Select distinct iris_type from iris_dataset")
    # rows = c.fetchall()
    #
    # for row in rows:
    #     print(row)

    # conn.close()

def check_count():
    c.execute("""
        select iris_type, count(iris_type) from iris_dataset group by iris_type
        """)

    rows = c.fetchall()

    for row in rows:
        print(row[0], row[1])

def calc_attribute_entropy(rows):
    e1_sl = 0
    sum_sl = 0

    for row in rows:
        sum_sl += row[1]

    for row in rows:
        e1_sl += (row[1] / sum_sl) * math.log(row[1] / sum_sl, 2)

    return (e1_sl * -1)


def calc_attribute_entropy1(name, mean, compare):
    sql = """  
        select iris_type , count(iris_type) from iris_dataset
        where """ + name + compare + str(mean)  + """
        group by iris_type"""

    c.execute(sql)
    rows = c.fetchall()
    e1_sl = 0
    sum_sl = 0

    for row in rows:
        sum_sl += row[1]

    for row in rows:
        e1_sl += (row[1] / sum_sl) * math.log(row[1] / sum_sl, 2)

    return (e1_sl * -1, sum_sl)


##############

def initial_entropy1(attributes):
    gains=[]
    c.execute("""
        select iris_type, count(iris_type) from iris_dataset group by iris_type
        """)
    rows = c.fetchall()

    frequencies = []
    sum = 0

    for row in rows:
        frequencies.append(row[1])
        sum += row[1]

    class_entropy = 0

    for freq in frequencies:
        class_entropy += (freq/sum) * math.log(freq/sum, 2)

    class_entropy *= -1

    print("class entropy:\t\t", class_entropy)

    # entropy for sepal length

    c.execute("""select avg(sepal_length), avg(sepal_width), avg(petal_length), 
    avg(petal_width) from iris_dataset""")

    rows = c.fetchall()

    means = []
    means.append(rows[0][0])
    means.append(rows[0][1])
    means.append(rows[0][2])
    means.append(rows[0][3])

    for i in range(4):
        e1, sum1 = calc_attribute_entropy1(attributes[i], means[i], "<")
        e2, sum2 = calc_attribute_entropy1(attributes[i], means[i], ">=")

        att_entropy = (sum1 / (sum1 + sum2) * e1 + sum2 / (sum1 + sum2) * e2)

        gain = class_entropy - att_entropy

        gains.append(gain)
        print(attributes[i] + " gain:\t", gain)

    print("attribute chosen:\t", attributes[gains.index(max(gains))])

    return attributes[gains.index(max(gains))], means[gains.index(max(gains))]

##############

def initial_entropy(attributes):
    gains=[]
    c.execute("""
        select iris_type, count(iris_type) from iris_dataset group by iris_type
        """)
    rows = c.fetchall()

    frequencies = []
    sum = 0

    for row in rows:
        frequencies.append(row[1])
        sum += row[1]

    class_entropy = 0

    for freq in frequencies:
        class_entropy += (freq/sum) * math.log(freq/sum, 2)

    class_entropy *= -1

    print("class entropy:\t\t", class_entropy)

    # entropy for sepal length

    c.execute("""select avg(sepal_length), avg(sepal_width), avg(petal_length), 
    avg(petal_width) from iris_dataset""")

    rows = c.fetchall()

    sl_mean = rows[0][0]
    sw_mean = rows[0][1]
    pl_mean = rows[0][2]
    pw_mean = rows[0][3]

    e1_sl, sum_sl1 = calc_attribute_entropy1("sepal_length", sl_mean, "<")
    e2_sl, sum_sl2 = calc_attribute_entropy1("sepal_length", sl_mean, ">=")

    sl_entropy = (sum_sl1 / (sum_sl1 + sum_sl2) * e1_sl + sum_sl2 / (sum_sl1 + sum_sl2) * e2_sl)
    # print(sl_entropy)

    gain = class_entropy - sl_entropy
    gains.append(gain)
    print("Sepal length gain:\t", gain)

    e1_sp, sum_sl1 = calc_attribute_entropy1("sepal_width", sw_mean, "<")
    e2_sp, sum_sl2 = calc_attribute_entropy1("sepal_width", sw_mean, ">=")

    sw_entropy = (sum_sl1 / (sum_sl1 + sum_sl2) * e1_sp + sum_sl2 / (sum_sl1 + sum_sl2) * e2_sp)
    # print(sw_entropy)

    gain = class_entropy - sw_entropy
    gains.append(gain)
    print("Sepal width gain:\t", gain)

    e1_pl, sum_sl1 = calc_attribute_entropy1("petal_length", pl_mean, "<")
    e2_pl, sum_sl2 = calc_attribute_entropy1("petal_length", pl_mean, ">=")

    pl_entropy = (sum_sl1 / (sum_sl1 + sum_sl2) * e1_pl + sum_sl2 / (sum_sl1 + sum_sl2) * e2_pl)
    # print(pl_entropy)

    gain = class_entropy - pl_entropy
    gains.append(gain)
    print("Petal Length gain:\t", gain)

    e1_pw, sum_sl1 = calc_attribute_entropy1("petal_width", pw_mean, "<")
    e2_pw, sum_sl2 = calc_attribute_entropy1("petal_width", pw_mean, ">=")

    pw_entropy = (sum_sl1 / (sum_sl1 + sum_sl2) * e1_pw + sum_sl2 / (sum_sl1 + sum_sl2) * e2_pw)
    # print("Entropy: ", pw_entropy)

    gain = class_entropy - pw_entropy
    gains.append(gain)
    print("Petal width gain:\t", gain)

    print("attribute chosen:\t", attributes[gains.index(max(gains))])

    return attributes[gains.index(max(gains))]

def find_entropy(current, cur_split_point, low, high):
    pass

def close_conn():
    conn.close()

if __name__ == '__main__':
    create_conn()

    # check_count()
    attributes = ["sepal_length", "sepal_width", "petal_length", "petal_width"]

    root_node, split_point = initial_entropy1(attributes)
    print(root_node)
    print("Split point: ", split_point)

    root = Node(root_node, split_point)

    close_conn()