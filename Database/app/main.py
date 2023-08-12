
import datetime
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException
from prisma import Prisma
from pydantic import BaseModel
from typing import List, Optional
from app.dependencies import use_logging
from app.middleware import LoggingMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from app.categoryData import categoryData
app = FastAPI()
app.add_middleware(LoggingMiddleware, fastapi=app)

prisma = Prisma(auto_register=True)

@app.get("/")
async def root(logger=Depends(use_logging)):
    logger.info("Handling your request")
    return {"message": "Your app is working!"}

# @app.post("/collection")
# async def create_user(collection: dict):
#     created_user = await prisma.collection.create(collection)
#     return created_user

@app.post("/collection")
async def create_user(collection: dict):
    existing_user = await prisma.collection.find_first(where={"title": collection["title"]})
    if existing_user:
        pass
    else:
        created_user = await prisma.collection.create(collection)
        return created_user


@app.get("/collection/{id}")
async def get_user(id):
    user = await prisma.collection.find_unique(where={"id": id})
    return user

@app.get("/collection/{id}")
async def get_user(id):
    user = await prisma.collection.find_unique(where={"id": id})
    return user

@app.put("/collection/{id}")
async def update_user(id: str, collection_data: dict):
    updated_user = await prisma.collection.update(
        where={"id": id}, data=collection_data
    )
    return updated_user

class DateUpdate(BaseModel):
    url: str
    DatePublication: str

@app.delete("/collection/{id}")
async def delete_user(id):
    deleted_user = await prisma.collection.delete_many(where={"id": id})
    return deleted_user

@app.get("/collection/path/{language}")
async def get_local_paths(language: str):
    records = await prisma.collection.find_many(where={"Language": language})
    return records

@app.get("/collection")
async def get_local_paths():
    records = await prisma.collection.find_many()
    return records

@app.get("/category/path/{language}")
async def get_category(language):
    category = await prisma.category.find_many(where={"language": language})
    return category

@app.get("/collection/priority/{language}")
async def get_category(language):
    records = await prisma.collection.find_many(where={"Language": language})
    if records:
        max_priority_record = max(records, key=lambda record: record.Priority)
        # Access the record with the maximum Priority value
        
        # You can access the individual fields of the record
        max_priority = max_priority_record.Priority
        # Or you can use the entire record object as needed
        
        return max_priority_record
    return None  # Or any appropriate response if no records found

@app.get("/collection/{id}")
async def get_user(id):
    user = await prisma.collection.find_unique(where={"id": id})
    return user
@app.on_event("startup")
async def startup() -> None:
    await prisma.connect()
    if await prisma.category.find_first() == None:
        await prisma.category.create_many(categoryData)

@app.get("/category/{start_id}")
async def get_category(start_id: int = 1):
    results = await prisma.collection.find_many(take=15, skip=(start_id - 1))
    if len(results) == 0:
        raise HTTPException(status_code=404, detail="Invalid start_id or no more records available.")
    else:
        return results
@app.get("/count_records")
async def count_records():
    record_count = await prisma.collection.count()
    return {"count": record_count}

@app.get("/count_records/{language}")
async def count_records(language: str):
    record_count = await prisma.collection.count(where={'Language':language,},)
    return {"count": record_count}

@app.delete("/category/path/{language}")
async def delete_category(start_id: int, end_id: int):
    # Get the first and last ID for the specified language

    # Perform deletion of IDs within the specified range
    await prisma.category.delete_many(
        where={
            "id": {
                "gte": start_id,
                "lte": end_id,
            }
        }
    )
    return {"message": f"Deleted category IDs from {start_id} to {end_id}"}

@app.get("/language/{language}/ids")
async def get_local_paths(language: str):
    records = await prisma.collection.find_many(where={"Language": language})

    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No records found for language: {language}",
        )

    first_record = records[0]
    last_record = records[-1]
    first_id = first_record.id
    last_id = last_record.id

    return {"first_id": {"id": first_id}, "last_id": {"id": last_id}}


# @app.post("/truncate_table")
# async def truncate_table():
#     table_name = "collection"
#     try:
#         await database.execute(f"TRUNCATE TABLE {table_name};")
#         return {"message": f"Table {table_name} truncated successfully."}
#     except Exception as e:
#         return {"error": str(e)}
class Filter(BaseModel):
    DatePublication: Optional[str] = None
    Language: Optional[str] = None
    Priority: Optional[float] = None
    Actors: Optional[List[str]] = None
    Location: Optional[List[str]] = None
    Organizations: Optional[List[str]] = None
    LocalPath: Optional[str] = None
    KeyWords: Optional[List[str]] = None
    Category: Optional[List[str]] = None

@app.exception_handler(HTTPException)
async def handle_validation_exception(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "field": exc.headers.get("field")}
    )
@app.post("/filter_records")
async def filter_records(filter: Filter, page: int = 1, page_size: int = 10):
    where_clause = {}

    # Check each property and add it to the where_clause if it's not None or an empty list
    if filter.DatePublication is not None:
        where_clause['DatePublication'] = filter.DatePublication
    if filter.Language is not None:
        where_clause['Language'] = filter.Language
    if filter.Priority is not None:
        where_clause['Priority'] = {"gte": filter.Priority}
    if filter.Actors is not None:
        where_clause['Actors'] = {"hasSome": filter.Actors}
    if filter.Location is not None:
        where_clause['Location'] = {"hasSome": filter.Location}
    if filter.Organizations is not None:
        where_clause['Organizations'] = {"hasSome": filter.Organizations}
    if filter.LocalPath:
        where_clause['LocalPath'] = filter.LocalPath
    if filter.KeyWords is not None:
        where_clause['KeyWords'] = {"hasSome": filter.KeyWords}
    if filter.Category is not None:
        where_clause['Category'] = {"hasSome": filter.Category}

    if not where_clause:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filter criteria provided. Please provide at least one filter field.",
            headers={"field": "filter"}
        )
    records = await prisma.collection.find_many(where=where_clause)
    count = len(records)  # Get the count of records
    {"records": records,"count":count}

    # Calculate pagination parameters
    total_pages = (count + page_size - 1) // page_size  # Round up to the nearest integer
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Slice the records based on pagination parameters
    paginated_records = records[start_index:end_index]

    return {"records": paginated_records, "count": count, "page": page, "total_pages": total_pages}

   



@app.on_event("shutdown")
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()
# Apply middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace ["*"] with the appropriate origins
    allow_credentials=True,
    allow_methods=["*"],  # Replace ["*"] with the appropriate HTTP methods
    allow_headers=["*"],  # Replace ["*"] with the appropriate headers
)
