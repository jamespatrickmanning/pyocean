def smallest_multpr(x, z):
    '''
    return the smallest y, while x*y>=z
    x, y, z are all positive num.
    '''
    y = 1
    while True:
        z1 = x*y
        if z1>=z: break
        y+=1
    return y
