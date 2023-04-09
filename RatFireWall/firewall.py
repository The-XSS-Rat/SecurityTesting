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

# Block requests with user agent containing "curl"
rule1 = Rule("Block cURL requests", request_headers={"User-Agent": "curl"})

# Block responses with a "Set-Cookie" header
rule2 = Rule("Block Set-Cookie responses", response_headers={"Set-Cookie": "*"})

# Block requests containing <script> tags
rule3 = Rule("Block requests containing <script> tags", block_script_tag=True)

rules = [rule1, rule2, rule3]
proxy = Proxy(rules)
proxy.run()
