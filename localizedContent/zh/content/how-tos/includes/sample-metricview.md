本操作指南使用一个示例电商 Metric View 来展示销售数据：三张维度表（产品、客户、日期）与一张事实表（订单）进行联接。

```yaml
version: 0.1
source: sales.fact.orders
joins:
  - name: product
    source: sales.dim.product
    on: source.product_id = product.product_id
  - name: customer
    source: sales.dim.customer
    on: source.customer_id = customer.customer_id
  - name: date
    source: sales.dim.date
    on: source.order_date = date.date_key
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
度量值:
  - name: total_revenue
    expr: SUM(revenue)
  - name: order_count
    expr: COUNT(order_id)
  - name: avg_order_value
    expr: AVG(revenue)
  - name: unique_customers
    expr: COUNT(DISTINCT customer_id)
```
