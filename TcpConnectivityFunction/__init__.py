import logging
import socket
import azure.functions as func

def get_outbound_ip():
    try:
        # Connect to internal IP to determine outbound IP used
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("192.168.1.4", 80))  # Replace with reachable internal IP and port
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        return f"Error retrieving outbound IP: {e}"

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Connectivity test function triggered.")

    target_ip = "192.168.1.4"
    target_port = 80
    outbound_ip = get_outbound_ip()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((target_ip, target_port))
        sock.close()
        return func.HttpResponse(
            f"✅ Successfully connected to {target_ip}:{target_port}\n"
            f"Outbound IP used: {outbound_ip}",
            status_code=200
        )
    except socket.timeout:
        return func.HttpResponse(
            f"⏱️ Connection to {target_ip}:{target_port} timed out.\n"
            f"Outbound IP used: {outbound_ip}",
            status_code=504
        )
    except socket.error as err:
        return func.HttpResponse(
            f"❌ Connection failed: {err}\n"
            f"Outbound IP used: {outbound_ip}",
            status_code=500
        )
