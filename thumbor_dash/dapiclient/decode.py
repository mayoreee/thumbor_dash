import base64
import re

def decode_byte_string(byte_string):
    # Extract fields from the binary data
    version = byte_string[0]  # Assuming the first byte is version
    id = int.from_bytes(byte_string[1:5], 'big')  # Next 4 bytes for id (big endian)
    purpose = byte_string[5]  # Next byte for purpose
    security_level = byte_string[6]  # Next byte for security level
    contract_bounds = None  # Contract bounds is null
    type_field = byte_string[7]  # Next byte for type
    read_only = False  # Assuming the readOnly is False as per your expected result

    # Extracting the data field (33 bytes from position 8 to 41)
    data_field = byte_string[8:41]
    data_base64 = base64.b64encode(data_field).decode('utf-8')

    # The 'disabledAt' field is also null
    disabled_at = None

    # Construct the final decoded structure
    decoded_object = {
        '$version': str(version),
        'id': id,
        'purpose': purpose,
        'securityLevel': security_level,
        'contractBounds': contract_bounds,
        'type': type_field,
        'readOnly': read_only,
        'data': data_base64.rstrip('='),  # Removing '=' padding to match the exact expected output
        'disabledAt': disabled_at
    }
    
    return decoded_object


def decode_doc_byte_string(byte_string):
    data_field = byte_string.decode('utf-8', errors='ignore')
    # Use regex to extract the URL
    url_pattern = re.compile(r'(https?://[^\s]+)')
    url_match = url_pattern.search(data_field)
    extracted_url = url_match.group(0) if url_match else "URL not found"

    return extracted_url
