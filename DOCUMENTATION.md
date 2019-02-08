## Authentication

### Registration (/register/ POST)

Request Body

```
{
    'uid': string,
    'pwd': string,
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

### Login (/login/ POST)

Request Body

```
{
    'uid': string,
    'pwd': string,
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

## Admin

### Admin Add/Mod Timeslot (/admin_add_timeslot/ /admin_mod_timeslot/ POST)

Headers

```
Authorization: auth_token
```

Request Body

```
{
    'tsid': string,
    'position': string,
    'start': string,
    'duration': int,
    'cap': int
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

### Admin Remove Timeslot (/admin_del_timeslot/ POST)

Headers

```
Authorization: auth_token
```

Request Body

```
{
    'tsid': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

### Add/Remove Position (/admin_add_position/ /admin_del_position/ POST)

Removing a position will also remove all time slots associated with that position

Headers

```
Authorization: auth_token
```

Request Body

```
{
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

## Timeslots

### Get All Timeslots (/get_all_timeslots/ GET)

Headers

```
Authorization: auth_token
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

### Add/remove timeslot (/add_timeslot/ /del_timeslot/ POST)

Headers

```
Authorization: auth_token
```

Request Body

```
{
    'tsid': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

### Get registered timeslots (/get_timeslots/ GET)

Headers

```
Authorization: auth_token
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

## Checking in and out

### Check in (/check_in/ POST)

Request Body

```
{
    'uid': string,
    'time': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

### Check out (/check_out/ POST)

Request Body

```
{
    'uid': string,
    'time': string
}
```

Response Body

```
{
    'status': int,
    'message': string
}
```

### Get user hours (/get_logged_hours/ GET)

Request Arguments

```
{
    'uid': string
}
```

Response Body

```
{
    'status': int,
    'message': string,
    'logged_hours': [
        [time, time], // [login, logout]
        ...
    ]
}
```