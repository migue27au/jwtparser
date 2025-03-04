import sys
import base64
import json
from datetime import datetime, timezone

COLOR_HEADER = '\033[94m'		# Azul
COLOR_PAYLOAD = '\033[92m'		# Verde
COLOR_SIGNATURE = '\033[91m'	# Rojo
COLOR_KEY = '\033[93m'			# Amarillo
COLOR_COMMENT = '\033[90m'		# Gris
COLOR_RESET = '\033[0m'			# END

def unix_to_datetime(unixtime):
	return datetime.fromtimestamp(unixtime, timezone.utc).strftime('%Y/%m/%d %H:%M:%S')

def base64_url_decode(input_str):
	# Base64 URL-safe decoding (con padding añadido si es necesario)
	rem = len(input_str) % 4
	if rem > 0:
		input_str += '=' * (4 - rem)
	return base64.urlsafe_b64decode(input_str).decode('utf-8')

def format_jwt(jwt):
	header_b64, payload_b64, signature_b64 = jwt.split('.')
	
	header = json.loads(base64_url_decode(header_b64))
	payload = json.loads(base64_url_decode(payload_b64))

	# RAW
	print(f"{COLOR_COMMENT}# JWT RAW: {jwt}{COLOR_RESET}\n")
	
	# Header
	print(f"{COLOR_HEADER}Header:{COLOR_RESET}")
	for key, value in header.items():
		print(f'	{COLOR_KEY}"{key}":{COLOR_RESET} {json.dumps(value)}')
	
	# Payload
	print(f"{COLOR_PAYLOAD}Payload:{COLOR_RESET}")
	for key, value in payload.items():
		if key in ['iat', 'exp']:  # Si es un campo de timestamp
			formatted_time = unix_to_datetime(value)
			print(f'	{COLOR_KEY}"{key}":{COLOR_RESET} {value}, {COLOR_COMMENT}# ({formatted_time}){COLOR_RESET}')
		else:
			print(f'	{COLOR_KEY}"{key}":{COLOR_RESET} {json.dumps(value)}')
	
	# Signature
	print(f"{COLOR_SIGNATURE}Signature:{COLOR_RESET}")
	print(f"	{signature_b64}")

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print("Uso: python decode_jwt.py <JWT>")
		sys.exit(1)
	
	jwt_input = sys.argv[1]
	format_jwt(jwt_input)
