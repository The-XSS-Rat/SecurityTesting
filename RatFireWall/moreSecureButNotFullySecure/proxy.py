from mitmproxy import http
from rules import rules

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

proxy = Proxy(rules)
proxy.run
