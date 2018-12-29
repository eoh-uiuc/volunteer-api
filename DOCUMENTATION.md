## Authentication

### Registration (POST)

Request Body

```
{
    'uid': string,
    'pass_hash': string,
    'name': string,
    'phone': string,
    'society': string
}
```

Response Body

```
{
    'status': int,
    'message': string,
    'auth_token': string
}
```

#### Login (POST)

Request Body

```
{
    'uid': string,
    'pass_hash': string,
}
```

Response Body

```
{
    'status': int,
    'message': string,
    'auth_token': string
}
```

#### Admin Add/Mod Timeslot (POST)

Request Body

```
{
    'tsid': string,
    'position': string,
    'start': string,
    'duration': int,
    'cap': int,
    'auth_token': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

#### Admin Remove Timeslot (POST)

Request Body

```
{
    'tsid': string,
    'auth_token': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

#### Add/Remove Position (POST)

Removing a position will also remove all time slots associated with that position

Request Body

```
{
    'auth_token': string,
    'position': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

#### Get All Timeslots (GET)

Request Body

```
{
    'auth_token': string
}
```

Response Body

```
{
    'status': int,
    'message': string,
    'data': {
        position: [
            {
                'tsid': string,
                'position': string,
                'start': string,
                'duration': int,
                'cap': int,
                'taken': int
            },
            ...
        ],
        ...
    }
}
```