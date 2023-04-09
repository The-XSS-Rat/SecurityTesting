class Rule:
    def __init__(self, rule_name, request_headers=None, response_headers=None, block_script_tag=False):
        self.rule_name = rule_name
        self.request_headers = request_headers
        self.response_headers = response_headers
        self.block_script_tag = block_script_tag

    def matches_request(self, request):
        if self.request_headers:
            for header, value in self.request_headers.items():
                if header not in request.headers or request.headers[header] != value:
                    return False
        
        if self.block_script_tag and "<script>" in request.get_text():
            return True
        
        return False

    def matches_response(self, request, response):
        if self.response_headers:
            for header, value in self.response_headers.items():
                if header not in response.headers or response.headers[header] != value:
                    return False
        
        return False

rules = [
    Rule("Block cURL requests", request_headers={"User-Agent": "curl"}),
    Rule("Block Set-Cookie responses", response_headers={"Set-Cookie": "*"}),
    Rule("Block requests containing <script> tags", block_script_tag=True),
    Rule("Block SQL injection attacks"),
    Rule("Block XML external entity (XXE) attacks"),
    Rule("Block remote file inclusion (RFI) attacks"),
    Rule("Block command injection attacks"),
    Rule("Block cross-site scripting (XSS) attacks"),
    Rule("Block path traversal attacks"),
    Rule("Require API key in request headers", request_headers={"api_key": "my-api-key"}),
    Rule("Require JWT token in request headers", request_headers={"Authorization": "Bearer my-jwt-token"}),
    Rule("Require HTTPS encryption"),
    Rule("Block requests with invalid characters in URL"),
    Rule("Block requests with too many parameters in URL"),
    Rule("Block requests with too large request body", max_request_size=2048),
    Rule("Block requests from known malicious IP addresses"),
    Rule("Block requests to known malicious domains"),
    Rule("Block requests to known malicious URLs"),
    Rule("Block requests from blacklisted user agents", request_headers={"User-Agent": ["BadBot", "EvilBot"]}),
    Rule("Block requests without a valid referer header", request_headers={"Referer": "localhost"}),
    Rule("Block requests to suspicious paths", request_headers={"User-Agent": ["Mozilla", "Chrome"]})
]
