from mitmproxy import http

class Proxy:
    def __init__(self, rules):
        self.rules = rules

    def request(self, flow: http.HTTPFlow) -> None:
        # Check if the request matches any of the rules
        for rule in self.rules:
            if rule.matches_request(flow.request):
                # If the request matches the rule, block it
                flow.response = http.HTTPResponse.make(
                    403, "Forbidden",
                    {"Content-Type": "text/html"},
                    b"Blocked by rule: %s" % rule.rule_name.encode('utf-8')
                )

    def response(self, flow: http.HTTPFlow) -> None:
        # Check if the response matches any of the rules
        for rule in self.rules:
            if rule.matches_response(flow.request, flow.response):
                # If the response matches the rule, block it
                flow.response = http.HTTPResponse.make(
                    403, "Forbidden",
                    {"Content-Type": "text/html"},
                    b"Blocked by rule: %s" % rule.rule_name.encode('utf-8')
                )

class Rule:
    def __init__(self, rule_name, request_headers=None, response_headers=None):
        self.rule_name = rule_name
        self.request_headers = request_headers
        self.response_headers = response_headers

    def matches_request(self, request):
        # Check if the request matches the rule
        if self.request_headers:
            for header, value in self.request_headers.items():
                if header not in request.headers or request.headers[header] != value:
                    return False
        return True

    def matches_response(self, request, response):
        # Check if the response matches the rule
        if self.response_headers:
            for header, value in self.response_headers.items():
                if header not in response.headers or response.headers[header] != value:
                    return False
        return True
