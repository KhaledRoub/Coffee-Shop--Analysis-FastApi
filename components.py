from attr import asdict
from db import db_dependency
from models import Transactions , products
import pandas as pd
from sqlalchemy import func
from datetime import datetime, timedelta

def get_sales_based_hour(
    db: db_dependency,
    sales_outlet_id_param,
    start_date_param,
    end_date_param,
    start_hour,
    end_hour,):
    result = (
        db.query(
            func.count(Transactions.transaction_id).label('transaction_count') ,
            Transactions.hour
        )
        .filter(
            Transactions.sales_outlet_id == sales_outlet_id_param,
            Transactions.transaction_date.between(start_date_param ,end_date_param),
            Transactions.hour.between(start_hour, end_hour)
        )
        .group_by(Transactions.hour)
        .all()
    )
    # formatted_result = [
    #     {'hour': row.hour, 'transaction_count': row.transaction_count}
    #     for row in result
    # ]
    hours_in_range = [str(hour).zfill(2) for hour in range(start_hour, end_hour + 1)]

    # Initialize formatted_result with continuous hours and transaction_count set to 0
    formatted_result = [{'hour': hour, 'transaction_count': 0} for hour in hours_in_range]

    for row in result:
        hour = str(row.hour).zfill(2)
        for entry in formatted_result:
            if entry['hour'] == hour:
                entry['transaction_count'] = row.transaction_count
                break

    return formatted_result

def get_sales_based_day(
    db: db_dependency,
    sales_outlet_id_param,
    start_date_param,
    end_date_param,
    start_hour,
    end_hour,):
    result = (
    db.query(
            func.count(Transactions.transaction_id).label('transaction_count'),
            Transactions.day
        )
        .filter(
            Transactions.sales_outlet_id == sales_outlet_id_param,
            Transactions.transaction_date.between(start_date_param, end_date_param)
        )
        .group_by(Transactions.day)
        .all()
    )

    formatted_result = [
        {
            'day':row.day,
            'transaction_count': row.transaction_count,

        }
        for row in result
    ]
    return formatted_result

def get_sales_based_month(
    db: db_dependency,
    sales_outlet_id_param,
    start_date_param,
    end_date_param,
    start_hour,
    end_hour,):
    result = (
    db.query(
            func.count(Transactions.transaction_id).label('transaction_count'),
            Transactions.sales_outlet_id
        )
        .filter(
            Transactions.sales_outlet_id == sales_outlet_id_param,
        )
    )

    formatted_result = [
        {
            'sales_outlet_id':row.sales_outlet_id,
            'transaction_count': row.transaction_count,

        }
        for row in result
    ]
    return formatted_result




# def get_total_item_based_day(db: db_dependency, sales_outlet_id_param, start_date_param, end_date_param, start_hour , end_hour):
#     result = (
#         db.query(
#             Transactions.sales_outlet_id,products.product,
#             func.sum(Transactions.quantity).label('total_quantity_sold'),
#             Transactions.hour
#         )
#         .join(products, Transactions.product_id == products.product_id)
#         .filter(
#             Transactions.sales_outlet_id == sales_outlet_id_param,
#             Transactions.transaction_date.between(start_date_param, end_date_param)
#         )
#         .group_by(Transactions.sales_outlet_id, products.product, Transactions.hour)
#         .all()
#     )

#     formatted_result = [
#         {
#             'sales_outlet_id': row.sales_outlet_id,
#             'product': row.product,
#             'total_quantity_sold': row.total_quantity_sold,
#             'hour': row.hour
#         }
#         for row in result
#     ]

#     return formatted_result


def get_total_item_based_day(
    db: db_dependency,
    sales_outlet_id_param,
    start_date_param,
    end_date_param,
    start_hour,
    end_hour,
):
    result = (
        db.query(
            products.product,
            func.sum(Transactions.quantity).label('total_quantity_sold'),
        )
        .join(products, Transactions.product_id == products.product_id)
        .filter(
            Transactions.sales_outlet_id == sales_outlet_id_param,
            Transactions.transaction_date.between(start_date_param, end_date_param),
        )
        .group_by(
            products.product,
        )
        .all()
    )

    formatted_result = [
        {
            'product': row.product,
            'total_quantity_sold': row.total_quantity_sold,

        }
        for row in result
    ]

    return formatted_result






from datetime import timedelta


def date_range(db, store_id, start_date, end_date, start_hour, end_hour):
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    duration = end_date - start_date
    if duration <= timedelta(hours=24):
        return get_sales_based_hour(db, store_id, start_date, end_date, start_hour, end_hour)
    elif timedelta(days=1) < duration <= timedelta(days=30):
        return get_sales_based_day(db, store_id, start_date, end_date, start_hour, end_hour)
    elif duration > timedelta(days=30):
        return get_sales_based_month(db, store_id, start_date, end_date, start_hour, end_hour)
    

    
def get_total_transactions_by_hour(
    db: db_dependency,
):
    result = (
        db.query(
            Transactions.sales_outlet_id,
            Transactions.hour,
            func.count(Transactions.transaction_id_comb).label('total_transaction')
        )
        .group_by(Transactions.sales_outlet_id, Transactions.hour)
        .order_by(Transactions.sales_outlet_id)
        .all()
    )
    
    return result

    # formatted_result = [
    #     {
    #         'product': row.product,
    #         'total_quantity_sold': row.total_quantity_sold,

    #     }
    #     for row in result
    # ]

    # return formatted_result
