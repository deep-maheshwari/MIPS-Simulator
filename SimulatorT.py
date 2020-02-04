def parse():
    text = "add $s1, $s2, $s3"

    result = [x.split() for x in text.split(",")]
    for st in result:
        print(st)

    

    if(result[0][0] == "add"):
        r1 = add(r2, r3)

parse()

def add(r2, r3):
    return r2 + r3