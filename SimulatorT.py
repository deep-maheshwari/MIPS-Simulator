def parse():
    text = input()

    result = text.split()

    parsed = []

    for st in result:
        
        st = st.split(",")
        for x in st:
            if(x):
                parsed.append(x)

    print(parsed)

parse()