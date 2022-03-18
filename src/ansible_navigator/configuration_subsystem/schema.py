"""Partial json schema for settings."""
from typing import Dict


PARTIAL_SCHEMA: Dict = {
    "$schema": "http://json-schema.org/draft-07/schema",
    "additionalProperties": False,
    "properties": {
        "ansible-navigator": {
            "properties": {
                "ansible": {
                    "additionalProperties": False,
                    "properties": {
                        "cmdline": {
                            "type": "string",
                        },
                        "config": {
                            "additionalProperties": False,
                            "properties": {
                                "help": {
                                    "type": "boolean",
                                },
                                "path": {
                                    "type": "string",
                                },
                            },
                        },
                        "inventory": {
                            "additionalProperties": False,
                            "properties": {
                                "help": {
                                    "type": "boolean",
                                },
                                "paths": {
                                    "items": {"type": "string"},
                                    "type": "array",
                                },
                            },
                        },
                        "playbook": {
                            "additionalProperties": False,
                            "properties": {
                                "help": {
                                    "type": "boolean",
                                },
                                "path": {
                                    "type": "string",
                                },
                            },
                        },
                    },
                    "type": "object",
                },
                "ansible-builder": {
                    "additionalProperties": False,
                    "type": "object",
                    "properties": {
                        "help": {
                            "type": "boolean",
                        },
                        "workdir": {
                            "type": "string",
                        },
                    },
                },
                "ansible-runner": {
                    "additionalProperties": False,
                    "properties": {
                        "artifact-dir": {
                            "type": "string",
                        },
                        "rotate-artifacts-count": {
                            "type": "integer",
                        },
                        "timeout": {
                            "type": "integer",
                        },
                    },
                    "type": "object",
                },
                "app": {
                    "type": "string",
                },
                "collection-doc-cache-path": {
                    "type": "string",
                },
                "color": {
                    "additionalProperties": False,
                    "properties": {
                        "enable": {
                            "type": "boolean",
                        },
                        "osc4": {
                            "type": "boolean",
                        },
                    },
                    "type": "object",
                },
                "documentation": {
                    "additionalProperties": False,
                    "properties": {
                        "help": {
                            "type": "boolean",
                        },
                        "plugin": {
                            "additionalProperties": False,
                            "properties": {
                                "name": {
                                    "type": "string",
                                },
                                "type": {
                                    "type": "string",
                                },
                            },
                            "type": "object",
                        },
                    },
                    "type": "object",
                },
                "editor": {
                    "additionalProperties": False,
                    "properties": {
                        "command": {
                            "type": "string",
                        },
                        "console": {
                            "type": "boolean",
                        },
                    },
                    "type": "object",
                },
                "exec": {
                    "additionalProperties": False,
                    "properties": {
                        "command": {
                            "type": "string",
                        },
                        "shell": {
                            "type": "boolean",
                        },
                    },
                    "type": "object",
                },
                "execution-environment": {
                    "additionalProperties": False,
                    "properties": {
                        "container-engine": {
                            "type": "string",
                        },
                        "container-options": {
                            "items": {"type": "string"},
                            "type": "array",
                        },
                        "enabled": {
                            "type": "boolean",
                        },
                        "environment-variables": {
                            "additionalProperties": False,
                            "properties": {
                                "pass": {
                                    "items": {"type": "string"},
                                    "type": "array",
                                },
                                "set": {
                                    "type": "object",
                                },
                            },
                            "type": "object",
                        },
                        "image": {
                            "type": "string",
                        },
                        "pull": {
                            "additionalProperties": False,
                            "properties": {
                                "arguments": {
                                    "items": {"type": "string"},
                                    "type": "array",
                                },
                                "policy": {
                                    "type": "string",
                                },
                            },
                        },
                        "volume-mounts": {
                            "additionalProperties": False,
                            "properties": {
                                "dest": {"type": "string"},
                                "label": {"type": "string"},
                                "options": {"type": "string"},
                            },
                            "required": ["src", "dest"],
                            "type": "array",
                        },
                    },
                    "type": "object",
                },
                "inventory-columns": {
                    "items": {"type": "string"},
                    "type": "array",
                },
                "logging": {
                    "additionalProperties": False,
                    "properties": {
                        "append": {
                            "type": "boolean",
                        },
                        "file": {
                            "type": "string",
                        },
                        "level": {
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "mode": {
                    "type": "string",
                },
                "playbook-artifact": {
                    "additionalProperties": False,
                    "properties": {
                        "enable": {
                            "type": "boolean",
                        },
                        "replay": {
                            "type": "string",
                        },
                        "save-as": {
                            "type": "string",
                        },
                    },
                    "type": "object",
                },
                "time-zone": {
                    "type": "string",
                },
                "settings": {
                    "additionalProperties": False,
                    "properties": {"schema": {"type": "string"}},
                },
            },
            "additionalProperties": False,
        },
    },
    "required": ["ansible-navigator"],
    "title": "ansible-navigator settings file schema",
    "type": "object",
}
