Simple service to queue up entity objects (e.g. posts, comments) and push/update/delete
them in batch. How the processing is orchestrated, e.g. sequentially or concurrently,
is left up to separate classes that selected through dependency injection or
environment variables.
