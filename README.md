
# Basic Airline, Aircraft API

In this project there are 2 different "app" such that "Airline" and "Aircraft"
these apps include 2 different model respectively.

These models has one-to-many relations. 
    Airline can have many aircraft, but aircraft has only one airline


## API properties
    
- Pagination -> 5 objects per page
- Rate limiting -> anon's has '100/day', user's has '1000/day'

### Note that you can change in /Narts/settings.py 
```
'PAGE_SIZE': 5, 

'DEFAULT_THROTTLE_RATES': {
    'anon': '100/day',  
    'user': '1000/day' 
}
```




> [!NOTE]
> Delete requests method changed to "DELETE" from "POST"
> DELETE methods use soft delete!


## API Kullanımı
 
### Auth
#### Create a JWT token

```http
  POST /api/api-token-auth
```


### Airline
#### Get all objects

```http
  GET /api/airline/?page=${page_number}
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `page` | `int` |  Page number |

##### GET /api/airline/ only list page 1

#### Get one airline object

```http
  GET /api/airline/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` |  Key value of the element to be called |

#### Update an airline object

```http
  PATCH /api/airline/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | Key value of the element to be called |


#### Delete an airline object
```http
  DELETE /api/airline/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | Key value of the element to be called |


#### Create an airline object
```http
  POST /api/airline/
```




### Aircraft
#### Get all Aircraft objects

```http
  GET /api/aircraft/?page=${page_number}
```

| Parametre | Tip     | Açıklama                |
| :-------- | :------- | :------------------------- |
| `page` | `int` |  Page number |

##### GET /api/airline/ only list page 1

#### Get one Aircraft object

```http
  GET /api/aircraft/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` |  Key value of the element to be called |

#### Update an Aircraft object

```http
  PATCH /api/aircraft/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | Key value of the element to be called |


#### Delete an Aircraft object
```http
  DELETE /api/aircraft/${id}
```

| Parametre | Tip     | Açıklama                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `int` | Key value of the element to be called |


#### Create an Aircraft object
```http
  POST /api/aircraft/
```
