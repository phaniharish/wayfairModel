# Wayfair Model simulation

To use the app simply run 
```
docker-compose up
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

### Configuration

The nginx configuration for the service can be found at `conf/nginx.conf`

The following environment variables are currently supported for other service configuration:
   - `MODEL_SERVER_TIMEOUT`: Configure the service timeout, default 60 seconds
   - `MODEL_SERVER_WORKERS`: Configure number of gunicorn threads that can be invoked.

## Client
The client is a very lightweight module which simply iterates over orders.csv and invokes the endpoint for inference.


# Alternative design choices
These are some design choices I would have preferred to use but couldn't scope well for the current assignment:

1. In a production scenario I would have preferred to design the feature extraction and 
ml model as sklearn transformers. This will allow for a much more modular development and better extensibility
for future. With the correct implementation these can also be serialized and transferred from a training job
 and then loaded directly to a bare-bones inference endpoint.
2. Allow processing hooks, this is much easier to add in a `pipeline` style approach and
woul be a very valuable addition for a lot of ML endpoints. Hooks can be used to sample and store
data, validate latencies, check data thresholds and a lot of other useful use cases.
3. Feature to sample and store input requests, intermediate features and outputs. This will 
allow us to monitor the distribution of data and check for any deviation form the training data. It
is also a useful feature to allow for historical data analysis and model performance checks.
