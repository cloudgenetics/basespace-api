# CORS S3 configuration

```xml
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>HEAD</AllowedMethod>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
```


```json
[
 {
    "AllowedHeaders": [
        "*"
    ],
    "AllowedMethods": [
        "GET",
        "HEAD",
        "PUT",
        "POST"
    ],
    "AllowedOrigins": [
        "*"
    ],
    "ExposeHeaders": []
 }
]
```
