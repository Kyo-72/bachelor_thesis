def read_file(str):
    with open(str) as f:
        for line in f:
           print line

read_file("test.txt")
