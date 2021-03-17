
from SingleStockStrategies import SingleStockStrategies


if __name__ == '__main__':
    stock = "F" # Ford
    start = "2012-01-01"
    end = "2021-01-30"
    init_balance = 10000
    window = 3

    tester = SingleStockStrategies(stock, start, end, init_balance)
    tester.test_con_strategy(window)


