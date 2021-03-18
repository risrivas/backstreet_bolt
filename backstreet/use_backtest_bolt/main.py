
from SingleStockStrategies import SingleStockStrategies


def single_stock_backtest(stock, start, end, amount, strategy):
    tester = SingleStockStrategies(stock, start, end, amount)
    if strategy == "sma":
        tester.test_sma_strategy(38, 103)
    elif strategy == "con":
        tester.test_con_strategy(3)
    elif strategy == "boll":
        tester.test_boll_strategy(26, 1)


if __name__ == '__main__':
    stocks = ["F"] # Ford ticker
    strategies = ["boll"]
    start = "2012-01-01"
    end = "2021-01-30"
    init_balance = 10000

    for stock in stocks:
        for strategy in strategies:
            single_stock_backtest(stock, start, end, init_balance, strategy)


