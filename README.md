# kuac
kuac ("KUbernetes configuration As Code") is a Python library for writing maintainable Kubernetes configuration files,
fostering reuse, or establishing recommended practices typically in an organization.

Instead of struggling with YAML files or YAML linting tools, of doing heroic efforts
to reuse YAML fragments or instantiate YAML templates, use kuac to write Kubernetes
configuration with Python code, and let it generate files ready to be applied with
`kubectl`.
