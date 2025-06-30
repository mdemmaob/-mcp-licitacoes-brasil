from prometheus_client import start_http_server, Counter, Summary
import threading

REQUESTS = Counter('mcp_requests_total', 'Total de requisições MCP')
EXCEPTIONS = Counter('mcp_exceptions_total', 'Total de exceções MCP')
REQUEST_TIME = Summary('mcp_request_processing_seconds', 'Tempo de processamento de requisição MCP')

def start_metrics_server(port=8080):
    thread = threading.Thread(target=start_http_server, args=(port,), daemon=True)
    thread.start() 