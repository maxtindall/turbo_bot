positions = {}

def update(market, side):
    positions[market] = side

def get_position(market):
    return positions.get(market)
