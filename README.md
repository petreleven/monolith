# monolith
A flask app that is designed to fetch runs from strava.
The fetch occurrs using background celery task queues thar utilize Redis as the message broker;
The implementation is meant to run as a single monolithic architecture
