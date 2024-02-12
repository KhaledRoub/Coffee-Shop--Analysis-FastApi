import json
from fastapi import FastAPI, Request , Form
from starlette import status
from components import *
from db import db_dependency
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Query, Depends



app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/submit_data/", response_class=HTMLResponse)
async def submit_data(
    request: Request,
    db: db_dependency,
    store_id: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    start_hour: int = Form(...),  
    end_hour: int = Form(...),   
):
    # data = date_range(db, store_id, start_date, end_date, start_hour, end_hour)
    data = date_range(db, store_id, start_date, end_date, start_hour, end_hour)
    return templates.TemplateResponse("result_template.html", {"request": request, "data": data})

@app.get("/item/" ) 
async def func (db: db_dependency,sales_outlet_id_param: int = Query(..., title="Sales Outlet ID", description="The ID of the sales outlet"),
    start_date_param: str = Query(..., title="Start Date", description="The start date of the query"),
    end_date_param: str = Query(..., title="End Date", description="The end date of the query"),):
    data = get_total_item_based_day(db, sales_outlet_id_param  , start_date_param, end_date_param  , start_hour = 11, end_hour=13)
    return data
# item/?sales_outlet_id_param=5&start_date_param=2019-04-01&end_date_param=2019-04-03


# 
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Base = declarative_base()

# engine = create_engine("mysql+pymysql://root:@localhost:3306/coffee_shope")
# Base.metadata.create_all(bind=engine)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# db_dependency = Annotated[Session, Depends(get_db)]

# db = SessionLocal()  
# data = get_total_item_based_day(db, "3", "2019-04-01", "2019-04-03", start_hour=11, end_hour=13)
# data2 = date_range(db, "3", "2019-04-01", "2019-04-01"  , start_hour = 7, end_hour=23)
# data3 = get_total_transactions_by_hour(db)
# db.close()

# formatted_result = [
#     {
#         'store_id': row[0],
#         'hour': row[1],
#         'total_sales': row[2],
#     }
#     for row in data3
# ]

# # Print the formatted result
# for entry in formatted_result:
#     print(entry)
# import matplotlib.pyplot as plt


# # Extracting hour and transaction count data
# hours = [item['hour'] for item in data2]
# transaction_counts = [item['transaction_count'] for item in data2]

# # Plotting the continuous plot (line plot)
# plt.plot(hours, transaction_counts, marker='o', linestyle='-', color='b')  # Adjust line style and color as needed
# plt.xlabel("Hour")
# plt.ylabel("Transaction Count")
# plt.title("Transaction Count by Hour")
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
# plt.grid(True)  # Add grid for better visualization
# plt.show()
# products = [item['product'] for item in data]
# total_quantity_sold = [item['total_quantity_sold'] for item in data]

# # Plotting the bar chart with increased width and spacing
# # Example list of colors (replace with your desired colors)
# colors = ['cyan']

# plt.bar(products, total_quantity_sold, width=0.8, color=colors)
# plt.xlabel("Product")
# plt.ylabel("Total Quantity Sold")
# plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability

# # Increase the space between bars
# plt.subplots_adjust(bottom=0.25)  # Adjust bottom margin to create more space

# plt.title("Total Quantity Sold for Each Product")
# plt.show()