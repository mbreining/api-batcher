Simple service to queue up entity objects (e.g. posts, comments) and create/update/delete
them in batch in an API endpoint. How the processing is orchestrated, e.g. sequentially or
 concurrently, is left up to separate classes that are loaded through dependency injection or
environment variables.
