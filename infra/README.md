
```
pulumi package add terraform-provider planetscale/planetscale
```

```python
# Planetscale MySQL Database
db = planetscale.Database(
    resource_name="mydb", 
    organization="lukehoban", 
    cluster_size="PS-10"
)
```
