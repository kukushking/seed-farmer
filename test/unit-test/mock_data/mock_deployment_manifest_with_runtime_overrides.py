deployment_manifest = {
    "name": "mlops",
    "toolchain_region": "us-east-1",
    "groups": [
        {
            "name": "optionals",
            "path": "manifests/mlops/optional-modules.yaml",
            "modules": [
                {
                    "name": "networking",
                    "path": "modules/optionals/networking/",
                    "runtime_overrides": {"java": "corretto21"},
                    "parameters": [{"name": "internet-accessible", "value": True}],
                    "target_account": "primary",
                    "target_region": "us-east-1",
                },
            ],
        },
    ],
    "target_account_mappings": [
        {
            "alias": "primary",
            "account_id": "123456789012",
            "default": True,
            "runtime_overrides": {"python": "3.13"},
            "parameters_global": {
                "dockerCredentialsSecret": "aws-addf-docker-credentials",
                "permissionsBoundaryName": "boundary",
            },
            "region_mappings": [
                {
                    "region": "us-east-1",
                    "default": True,
                    "parameters_regional": {},
                    "runtime_overrides": {"nodejs": "22"},
                }
            ],
        }
    ],
}
