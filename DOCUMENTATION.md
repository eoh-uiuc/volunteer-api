## Authentication

### Registration

Request

```
{
    'uid': string,
    'pass_hash': string,
    'name': string,
    'phone': string,
    'society': string
}
```

Response

```
{
    'status': int,
    'message': string,
    'auth_token': string
}
```

#### Login

Request

```
{
    'uid': string,
    'pass_hash': string,
}
```

Response

```
{
    'status': int,
    'message': string,
    'auth_token': string
}
```