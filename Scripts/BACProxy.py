import os
import yaml
import requests
from mitmproxy import http
import mitmproxy
from urllib.parse import urlparse
import threading

class AuthHeaderReplacer:
    def __init__(self):
        # Load configuration
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        self.scope = config.get('scope', [])
        self.exclude_endpoints = config.get('exclude_endpoints', [])

        # External variable for user2 header
        self.user2_header_name = os.environ.get('USER2_HEADER_NAME', 'Authorization')
        self.user2_header_value = os.environ.get('USER2_HEADER_VALUE', 'user2_header_value_here')

        # Thread-safe storage for report data
        self.report_data = []
        self.lock = threading.Lock()

    def request(self, flow: http.HTTPFlow):
        # Check if request is within scope
        if not self.is_in_scope(flow.request.url):
            return  # Skip processing

        # Check if endpoint is excluded
        if self.is_excluded(flow.request.url):
            return  # Skip processing

        # Get the original request details
        url = flow.request.url
        method = flow.request.method
        headers = dict(flow.request.headers)
        data = flow.request.get_content()

        # User1 header value
        user1_header_value = headers.get(self.user2_header_name, 'None')

        # Send request with user1 headers
        resp_user1 = self.send_request(url, method, headers, data)

        # Replace the auth header with user2 header
        headers[self.user2_header_name] = self.user2_header_value

        # Send request with user2 headers
        resp_user2 = self.send_request(url, method, headers, data)

        # Compare the responses
        if resp_user1.status_code != resp_user2.status_code:
            match_status = 'NOPE'
        else:
            if resp_user1.text == resp_user2.text:
                match_status = 'MATCH'
            else:
                match_status = 'SIMILAR'

        endpoint = flow.request.url

        # Store the data for report
        with self.lock:
            self.report_data.append({
                'endpoint': endpoint,
                'user1_header': user1_header_value,
                'user2_header': self.user2_header_value,
                'status': match_status,
                'user1_response': resp_user1.text,
                'user2_response': resp_user2.text
            })

        # Let the request proceed as normal
        pass

    def send_request(self, url, method, headers, data):
        # Send the request using requests library
        try:
            resp = requests.request(method, url, headers=headers, data=data, verify=False)
            return resp
        except Exception as e:
            # Return a dummy response with status code 0
            resp = requests.Response()
            resp.status_code = 0
            resp._content = b''
            return resp

    def is_in_scope(self, url):
        for scope_url in self.scope:
            if url.startswith(scope_url):
                return True
        return False

    def is_excluded(self, url):
        for exclude_url in self.exclude_endpoints:
            if url.startswith(exclude_url):
                return True
        return False

    def done(self):
        # Generate the HTML report when mitmproxy is shutting down
        self.generate_report()

    def generate_report(self):
        html_template = '''
        <html>
        <head>
            <title>Auth Header Replacer Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f0f0f0; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                .MATCH {{ background-color: #d4edda; }}
                .SIMILAR {{ background-color: #fff3cd; }}
                .NOPE {{ background-color: #f8d7da; }}
                pre {{ white-space: pre-wrap; word-wrap: break-word; }}
            </style>
        </head>
        <body>
            <h1>Auth Header Replacer Report</h1>
            <table>
                <tr>
                    <th>Endpoint</th>
                    <th>User1 Header</th>
                    <th>User2 Header</th>
                    <th>Status</th>
                    <th>User1 Response</th>
                    <th>User2 Response</th>
                </tr>
                {rows}
            </table>
        </body>
        </html>
        '''

        row_template = '''
        <tr class="{status_class}">
            <td>{endpoint}</td>
            <td><pre>{user1_header}</pre></td>
            <td><pre>{user2_header}</pre></td>
            <td>{status}</td>
            <td><pre>{user1_response}</pre></td>
            <td><pre>{user2_response}</pre></td>
        </tr>
        '''

        rows = ''
        for data in self.report_data:
            status_class = data['status']
            row = row_template.format(
                endpoint=data['endpoint'],
                user1_header=self.escape_html(data['user1_header']),
                user2_header=self.escape_html(data['user2_header']),
                status=data['status'],
                user1_response=self.escape_html(data['user1_response']),
                user2_response=self.escape_html(data['user2_response']),
                status_class=status_class
            )
            rows += row

        html_content = html_template.format(rows=rows)

        with open('report.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

    def escape_html(self, text):
        import html
        return html.escape(text)

addons = [
    AuthHeaderReplacer()
]
