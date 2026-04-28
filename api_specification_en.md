# Project Specification: Camera Management & Vector Search System (API)

## 1. Project Overview
This project is an API system developed using **Python (Flask)** designed to manage a list of surveillance cameras. The key feature of this system is the integration of **AI Vector Search**, which enables semantic (text-based) and visual (image-based) camera searches using deep learning models (CLIP).

The system combines a traditional relational database for storing structured information with a vector database to handle advanced AI-powered queries.

## 2. Technology Stack & Architecture
- **Web Framework:** Flask (Python)
- **Primary Database (Relational DB):** MySQL (Handles camera CRUD operations)
- **Vector Database (Vector Store):** ChromaDB (Stores embeddings and performs similarity searches)
- **AI Models (Embeddings):**
  - Text: `sentence-transformers/clip-ViT-B-32-multilingual-v1` (Multilingual support)
  - Image: `clip-ViT-B-32` (Image feature extraction)
- **Image Processing:** Pillow (PIL)
- **CORS:** Flask-CORS

**Embedding Workflow:**
When a camera is created or updated with an image:
1. The system generates an embedding for the text information (Name, Location, Status, Resolution).
2. An embedding is generated for the camera's image.
3. The two vectors are combined (Text is weighted at 70%, Image at 30%).
4. The combined vector is stored in ChromaDB.

## 3. Core Features
1. **Camera Management (CRUD):** Add, edit, delete, list, and retrieve detailed camera information.
2. **Image Management:** Supports uploading and storing camera images.
3. **Traditional Search:** Search cameras by name, location, or filter by status (active/inactive).
4. **Vector Search (AI Search):**
   - **Semantic Text Search:** Search for cameras using natural language text descriptions.
   - **Image Similarity Search:** Find cameras with similar images by uploading a file, providing a URL, or using a Base64 string.
5. **Dashboard Statistics:** Provides an overview of the total number of cameras, active cameras, and inactive cameras.

## 4. API Specification

### 4.1. Core Management Endpoints (CRUD & Stats)
| Method | Endpoint | Description | Parameters/Body |
|---|---|---|---|
| GET | `/` | Returns the user interface (index.html) | None |
| GET | `/api/cameras` | Retrieve a list of cameras | Query: `limit`, `offset` |
| GET | `/api/cameras/<id>` | Retrieve details of a specific camera | Path: `id` |
| GET | `/api/cameras/search/<term>` | Traditional keyword search | Path: `term` |
| GET | `/api/cameras/status/<status>` | Filter cameras by status | Path: `status` (active/inactive) |
| GET | `/api/stats` | Retrieve overall statistics | None |
| POST | `/api/cameras` | Create a new camera | Form-data: `name`, `location`, `ip_address`, `status`, `resolution`, `image` (file) |
| PUT | `/api/cameras/<id>` | Update camera information | Form-data: Fields to update |
| DELETE | `/api/cameras/<id>` | Delete camera from MySQL and ChromaDB | Path: `id` |

### 4.2. Vector Search Endpoints
| Method | Endpoint | Description | Parameters/Body |
|---|---|---|---|
| GET | `/api/vector/status` | View current ChromaDB index information | None |
| POST | `/api/vector/search/text` | Semantic search using text | JSON: `{ "query": "...", "limit": 10 }` |
| POST | `/api/vector/search/image` | Search using an image | JSON: `{ "url": "..." }` OR `{ "b64": "..." }` OR Form-data: `image` (file) |
| POST | `/api/vector/index/all` | Re-embed and synchronize (re-index) all cameras from MySQL to ChromaDB | None |

## 5. Expected Directory Structure
```text
/
├── app.py              # Application entry point, defines Flask Routes
├── config.py           # System configuration (Database, Port, Debug, etc.)
├── database.py         # MySQL connection and operations
├── crud.py             # Data manipulation logic (Create, Read, Update, Delete) for MySQL
├── embeddings.py       # SentenceTransformers model integration to generate vectors for Text/Image
├── vector_store.py     # ChromaDB integration (Store vectors, perform searches)
├── ui/
│   ├── routes.py       # API logic handlers for specific endpoints
│   └── static/         # Frontend UI (index.html) and uploaded images
└── data/chroma/        # Local storage directory for ChromaDB
```

## 6. Error Handling
The system uses a standard JSON response structure for all APIs:
- **Success (200/201):** `{ "success": true, ...data }`
- **Error (400/404/500):** `{ "success": false, "message": "Error message", "error": "Detailed error (if available)" }`
