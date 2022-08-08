import stock_viewer as sv

tmp = sv.stocks['Symbol']

def get_autofill(word):
    if word == "":
        return []
        
    recommend = tmp[tmp.str[0:len(word)] == word.upper()]
    if recommend.empty:
        return []
    if len(recommend) == 1:
        return [recommend.squeeze()]

    recommend = recommend.squeeze().tolist()
    if len(recommend) <= 5:
        return recommend
    else:
        return recommend[0:5]
