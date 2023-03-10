# CRUDFileStorage

File storage with `key` or `Authentication Token` based access.

- `Authentication Token` - user authentication token. Available by `/api/token` after registration.
- `key` - `FILE-ACCESS-KEY` field in request form-data.

`File owner` can access all the file, that he uploaded.
Any file uploaded with `key` might be accesses (inc. `deleted`) by request with `key`.

- `File owner` - user, that used `Authentication Token` to upload file.

`Anonymous user` can upload and access their files by the `key`. 
- `Anonymous user` - user, that didn't used `Authentication Token` to upload file.
## Requirements:
- docker
- docker compose

## How to start:
```bash
docker compose -f docker-compose.yml up
```
## API:
```python
{
    '/storage': {
        'GET': 'List files',
        'POST': 'Upload file',
    },
    '/storage/*': {
        'DELETE': 'Delete file by id',
        'LINK': 'Download file by id',
    },
    '/profiles': {
        'GET': 'List profiles'
    },
    '/token': {
        'POST': 'Get token',
    },
    '/register': {
        'Register using base auth'
    },
    '/': {
        'GET': 'List available API routines'
    }
}
```
