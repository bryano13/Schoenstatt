with open("out_file.txt", "r") as my_file:
    tienda = my_file.read()
d = {}
for i in range(len(tienda)):
    line_list = tienda.split("\n")
for index, line in enumerate(line_list):
    item_list = line.split("_")
    for index, col in enumerate(item_list):
        if col == item_list[-1]:
            col = item_list[-1][:-4]
            price_list = col.split("-")
            item_list[index] = ".".join(price_list)
        elif "-" in col:
            col_list = col.split("-")
            item_list[index] = " ".join(col_list)
    if len(line) <= 1:
        pass
    else:
        d[line] = item_list
