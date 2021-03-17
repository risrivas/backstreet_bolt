
from SingleStockStrategies import SingleStockStrategies


if __name__ == '__main__':
    stock = "F" # Ford
    start = "2012-01-01"
    end = "2021-01-30"
    init_balance = 10000
    SMA = 26 # 26 days
    deviation = 1

    tester = SingleStockStrategies(stock, start, end, init_balance)
    tester.test_boll_strategy(SMA, deviation)


