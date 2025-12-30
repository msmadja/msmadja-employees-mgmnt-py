from .http_correlation_id_middleware import correlation_id_middleware

method_middlewares = [
    correlation_id_middleware
]