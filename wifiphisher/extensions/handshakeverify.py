# pylint: skip-file
"""Extension that verifies WPA key by precaptured handshake using cowpatty."""

import logging
import os
import subprocess
from collections import defaultdict
from pathlib import Path

import wifiphisher.common.extensions as extensions

logger = logging.getLogger(__name__)


def get_process_result(command):
    """
    Execute a command and return its output securely.
    
    :param command: Command as a list of arguments
    :type command: list
    :return: Command output
    :rtype: str
    """
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=30,
            check=False
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        logger.error("Command timed out: %s", " ".join(command))
        return ""
    except Exception as e:
        logger.error("Error executing command: %s", e)
        return ""


def is_valid_handshake_capture(filename):
    """
    Check if capture file contains valid handshake data.
    
    :param filename: Path to capture file
    :type filename: str
    :return: True if valid handshake found
    :rtype: bool
    """
    if not os.path.isfile(filename):
        logger.error("Capture file not found: %s", filename)
        return False
    
    command = ['/bin/cowpatty', '-c', '-r', filename]
    output = get_process_result(command)
    return "Collected all necessary data" in output


class Handshakeverify:
    """Extension to verify WPA keys against captured handshakes."""

    def __init__(self, data):
        """Initialize handshake verification extension."""
        self.capt_file = data.args.handshake_capture
        self.essid = data.target_ap_essid
        self.key_file_path = "/tmp/keyfile.tmp"
        self.key = ""
        self.found = False

    def send_channels(self):
        """Return empty channel list."""
        return []

    def get_packet(self, packet):
        """Return empty packet dictionary."""
        return defaultdict(list)

    def send_output(self):
        """
        Send verification status to UI.
        
        :return: Status message
        :rtype: list
        """
        if self.key and self.found:
            return [f"VALID KEY: {self.key}"]
        elif self.key and not self.found:
            return [f"INVALID KEY ({self.key})"]
        return [f"WAITING FOR WPA KEY POST (ESSID: {self.essid})"]

    def on_exit(self):
        """Clean up temporary files on exit."""
        if os.path.isfile(self.key_file_path):
            try:
                os.remove(self.key_file_path)
            except OSError as e:
                logger.error("Failed to remove key file: %s", e)

    @extensions.register_backend_funcs
    def psk_verify(self, *list_data):
        """
        Verify PSK against captured handshake.
        
        :param list_data: Contains the PSK to verify
        :return: Verification result
        :rtype: str
        """
        if not list_data:
            return 'unknown'
        
        self.key = str(list_data[0])
        
        # Validate inputs
        if not os.path.isfile(self.capt_file):
            logger.error("Capture file not found: %s", self.capt_file)
            return 'fail'
        
        # Write key to temporary file securely
        try:
            with open(self.key_file_path, "w", encoding="utf-8") as keyfile:
                keyfile.write(f"{self.key}\n")
        except IOError as e:
            logger.error("Failed to write key file: %s", e)
            return 'fail'
        
        # Build command securely with list (no shell injection)
        command = [
            '/bin/cowpatty',
            '-f', self.key_file_path,
            '-r', self.capt_file,
            '-s', self.essid
        ]
        
        self.found = False
        output = get_process_result(command)
        
        if "The PSK is" in output:
            self.found = True
            logger.info("Valid PSK found for ESSID: %s", self.essid)
        
        # Clean up key file after use
        try:
            os.remove(self.key_file_path)
        except OSError:
            pass
        
        if self.key and self.found:
            return 'success'
        elif self.key and not self.found:
            return 'fail'
        return 'unknown'
