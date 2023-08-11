from stocksymbol import StockSymbol
import yaml


def load_stock_symbols(save_to_file: bool) -> (bool, int):
    """
    Load all available stock symbols with description as a list of dicts
    :param save_to_file: bool key - if it's True then result will be written to the file 'data/raw/stocksymbols.yaml'
    :return: if save_to_file=True then return True and number of items that have been added to file
    if save_to_file=False then return False and number of stock symbols
    """
    key = ''
    with open('../../Private_keys/stocksymbol.key', 'r') as keyfile:
        for line in keyfile:
            key = line
    api_key = key
    ss = StockSymbol(api_key)
    symbol_list_us = ss.get_symbol_list(market="US")

    if save_to_file:
        _, res = add_symbols_to_file(symbol_list_us, '../../data/raw/stocksymbols.yaml')
        return True, res
    else:
        return False, len(symbol_list_us)


def add_symbols_to_file(simbols_list: list, symbol_file_name: str) -> (int, int):
    """
    Compares the contents of the list with the contents of the file
    and adds the missing values to the file
    :param simbols_list: list of dictionaries that describe each symbol
    :param symbol_file_name: name of yaml file
    :return: tuple:
    first number 0 if OK, -1 if errors,
    second number - number of dicts that have been added
    """
    add_in = []
    try:
        old_symbol_list = yaml.load(open(symbol_file_name), Loader=yaml.SafeLoader)
        for item in simbols_list:
            if item not in old_symbol_list:
                add_in.append(item)

        with open(symbol_file_name, 'a') as file:
            yaml.dump(add_in, file)

        return 0, len(add_in)
    except IOError:
        return -1, 0


def main():
    _, number_of_stocks = load_stock_symbols(save_to_file=False)
    print(number_of_stocks)


if __name__ == '__main__':
    main()
