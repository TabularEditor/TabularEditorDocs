## 对这些代码示例的 Metric View 进行反序列化

本操作指南使用一个示例电商 Metric View 来表示销售数据，其中三个维度表（product、customer、date）连接到一个事实表（orders）。
如果你想在阅读本操作指南其余部分时跟着代码一起操作，请先运行下面的代码片段

```csharp
SemanticBridge.MetricView.Deserialize("""
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
    measures:
      - name: total_revenue
        expr: SUM(revenue)
      - name: order_count
        expr: COUNT(order_id)
      - name: avg_order_value
        expr: AVG(revenue)
      - name: unique_customers
        expr: COUNT(DISTINCT customer_id)
    """);
```
