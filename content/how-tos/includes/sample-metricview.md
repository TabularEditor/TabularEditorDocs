This how-to uses a sample e-commerce Metric View representing sales data with three dimension tables (product, customer, date) joined to a fact table (orders).

```yaml
version: 0.1
source: sales.fact.orders
joins:
  - name: product
    source: sales.dim.product
    on: product_id = product.product_id
  - name: customer
    source: sales.dim.customer
    on: customer_id = customer.customer_id
  - name: date
    source: sales.dim.date
    on: order_date = date.date_key
dimensions:
  - name: product_name
    expr: product.product_name
  - name: product_category
    expr: product.category
  - name: customer_segment
    expr: customer.segment
  - name: order_date
    expr: date.full_date
  - name: order_year
    expr: date.year
  - name: order_month
    expr: date.month_name
measures:
  - name: total_revenue
    expr: SUM(revenue)
  - name: order_count
    expr: COUNT(order_id)
  - name: avg_order_value
    expr: AVG(revenue)
  - name: unique_customers
    expr: COUNT(DISTINCT customer_id)
```
