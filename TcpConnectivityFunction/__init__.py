import logging
import socket
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Connectivity test function triggered.")

    target_ip = "192.168.1.4"
    target_port = 3306

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, target_port))
        sock.close()
        return func.HttpResponse(
            f"✅ Successfully connected to {target_ip}:{target_port}",
            status_code=200
        )
    except socket.timeout:
        return func.HttpResponse(
            f"⏱️ Connection to {target_ip}:{target_port} timed out.",
            status_code=504
        )
    except socket.error as err:
        return func.HttpResponse(
            f"❌ Connection failed: {err}",
            status_code=500
        )
