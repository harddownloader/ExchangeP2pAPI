import traceback

def p2p_order_mapper(order_data):
    try:
        trade_methods_list = [method["identifier"] for method in order_data["tradeMethods"]]
        trade_methods = ", ".join(trade_methods_list)

        desired_keys = [
            "advNo",
            "tradeType",
            "asset",
            "fiatUnit",
            "price",
            "surplusAmount",
            "maxSingleTransAmount",
            "minSingleTransAmount",
            "tradeMethods"
        ]

        # mapping
        updated_order = {k: order_data[k] for k in desired_keys}
        updated_order["tradeMethods"] = trade_methods

        return updated_order
    except Exception as e:
        print(traceback.format_exc())