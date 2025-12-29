import random


def roll(rawStr: str, data, type:str ):
    resStr = ''
    if type not in ['外卖','食堂']:
        type = random.choice(['外卖','食堂'])
        resStr = f'{type}，'
    food = random.choice(list(data[type].keys()))
    rawStr = rawStr.replace('吃什么','')
    resStr = f'小助手建议{rawStr}吃{resStr}{data[type][food]}的{food}！'
    return resStr