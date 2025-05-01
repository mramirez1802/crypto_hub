
To scale the solution to multiple cryptocurrencies in real time:
- Real-time processing → Use Kafka for ingestion and Spark Streaming for fast calculations.
- Efficient storage → Iceberg/Delta Lake + Parquet with date and currency partitioning.
- Fast queries → FastAPI with WebSockets and interactive dashboards in Grafana/Plotly.
