# Wayfair Model simulation

To use the app simply run 
```
docker compose up
```

The entire simulation logic is contained within the `src/wayfair` module.

## Service
The service is a flask app supported by nginx and gunicorn. This allows the service
to have multi threads configured simultaneously and can also be configured to auto-restart
in case of unexpected failures.
The service is separated into 3 modules:
1. `data_preprocessing`: Contains the logic to extract the features from the input data
   - `data_dao`: Data access objects
   - `data_models`: Simple dataclass objects for the required data types
   - `feature_extraction`: The bulk of the feature extraction logic
2. `model`: The ML simulation model provided.
3. `serving`:
    - `predictor`: Contains the flask app which exposes the ping and invocations method
    - `wsgi` : A simple wsgi file which points to the above flask app. We can configure it to support other ML models in future.
    - `serve`: Gunicorn configuration to run the process and configure the model timeout and number of workers. We can increase the number of workers to allow more throughput for the model.

## Client
The client is a very lightweight module which simply iterates over orders.csv and invokes the endpoint for inference.
