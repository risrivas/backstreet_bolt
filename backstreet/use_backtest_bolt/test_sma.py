
from SingleStockStrategies import SingleStockStrategies


if __name__ == '__main__':
    stock = "F" # Ford
    start = "2012-01-01"
    end = "2021-01-30"
    init_balance = 10000

    tester = SingleStockStrategies(stock, start, end, init_balance)
    tester.test_sma_strategy(38, 103)


