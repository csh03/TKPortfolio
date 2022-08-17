
def format_num(n):
    if n < 1e6:
        return n
    suffix = [" M"," B"," T"]
    vals = [1e6,1e9,1e12]
    for i in range(len(vals) - 1):
        if vals[i + 1] > n:
            return str(round(n/vals[i],2)) + suffix[i]
        elif n > vals[-1]:
            return str(round(n/vals[-1],2)) + suffix[-1]

print(format_num(1234))

