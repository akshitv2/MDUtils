# Installation Guide

Follow these steps to set up the environment locally.

## Prerequisites

- Node.js >= 18.0.0
- npm >= 9.0.0

## Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/example/project.git](https://github.com/example/project.git)
   cd project

```

2. **Install dependencies:**
```bash
npm install

```


3. **Start the development server:**
```bash
npm run dev

```

---

### `api.md`

```markdown
# API Reference

## Endpoints

### `GET /api/v1/users`

Retrieves a list of all users.

| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `page` | `integer` | No | Page number (default: `1`) |
| `limit` | `integer` | No | Items per page (default: `20`) |

#### Response Example

```json
{
  "status": 200,
  "data": [
    {
      "id": 101,
      "username": "alex99",
      "role": "admin"
    }
  ]
}
```