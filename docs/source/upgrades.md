# Upgrades

This page give indications related to supporting upgrading `seed-farmer` from previous version where changes must be enacted in order to properly use new feature.

This is not an exhaustive list but merely a guide.


## Upgrading to 3.5.0

`seed-farmer` 3.5.0 introduces the use of `pypiMirrorSecret` to support configuring a pypi mirror with credentials (see [Manifests - Mirrors](./manifests.md#mirroroverride)).

If you are currently using an older version of `seed-farmer`, to upgrade you must install the 3.5.0 version from Pypi and then update your current deployments by updating the seedkit in each target account/region mapping via the CLI using the `--update-seedkit` flag.  This is needed only once
```code
seedfarmer apply <manifest-path> --update-seedkit
```

Please see the [CLI references](./cli_commands.rst) for more details


## Upgrading to 4.0.0  
This is a **BREAKING CHANGE !!!**

`seed-farmer` 4.0.0 introduces the support of S3 to persist bundles of successfully deployed modules.  This is meant to help when destroying modules that may have changed code over time.  For example, if a developer has deployed a module from a local path, then moves that module, `seed-farmer` will still be able to destroy that module as the bundle used to deploy is stored in S3.  The change is backward-compatible, but the permissions ARE BREAKING from an older version, so you MUST perform the following steps.  

To upgrade:
1. Identify ALL target accounts where modules are deployed and DELETE the `seedfarmer-<project>-deployment-role` Cloudformation stack in these accounts (IAM is a global service, not regional but the Cloudformation template is regional)
2. Update your version of `seed-farmer` via
    ```code
    pip install --upgrade seed-farmer==4.0.0
     ```
3. Redeploy the `seedfarmer-<project>-deployment-role` in EVERY ACCOUNT
    ``` code
    seedfarmer bootstrap target -p <project> -t <toolchain-account-id>
    ``` 
4. Update the project policy on the next deployment (only once) *See Below*
    ```code 
    seedfarmer apply <manifest-path> --update-project-policy
    ```  

**NOTE:** If you are using your own `projectpolicy.yaml` (not using the one provided by `seed-farmer` and have defined it in your manifests) you can update your project policy with the following prior to running ***Step 4*** :

```yaml
          - Action:
            - s3:Delete*
            - s3:Put*
            - s3:Get*
            - s3:Create*
            - s3:List*
            Effect: Allow
            Resource:
            - Fn::Sub: "arn:${AWS::Partition}:s3:::seedfarmer-${ProjectName}*"
            - Fn::Sub: "arn:${AWS::Partition}:s3:::seedfarmer-${ProjectName}*/*" 
```
      
  ** *please update ${ProjectName} accordingly -- this is for you to manage*

Your existing deployment is unaffected after this change, and `seed-farmer` will continue to destroy as it previously did UNTIL the module you are looking to destroy has been sucessfully deployed with this version.  In other words, your modules WILL NOT benefit from the persisted bundle feature UNTIL they are deployed successfully with this new `seed-farmer` version.  In that regard, `seed-farmer` will continue to delete modules they way it always has (is backward compatible).


## Upgrading to 5.0.0  

This is a **BREAKING CHANGE !!!**

NOTE: When upgrading, it is highly recommended to enforce minimum required `seed-farmer` version to `5.0.0` for your projects 
using `seedfarmer_version` in ```seedfarmer.yaml```. Please refer to [Project Development](project_development.md) for instructions.

`seed-farmer` 5.0.0 introduces support for downloading modules from HTTPS archives.
This includes support for both secure HTTPS URLs which require authentication, as well as support for S3 HTTPS downloads.

In order to able to use secure HTTPS URLs or S3 HTTPS, you must upgrade the toolchain role permissions.

To upgrade:
1. Update your version of `seed-farmer` via
    ```bash
    pip install --upgrade seed-farmer==5.0.0
     ```
2. Run the bootstrap toolchain command via
    ```bash
    seedfarmer bootstrap toolchain <--as-target> --trusted-principal <trusted-principal-arn>
    ```

`seed-farmer` 5.0.0 also introduces the use of `npmMirrorSecret` to support configuring a npm mirror with credentials (see [Manifests - Mirrors](./manifests.md#mirroroverride)).

**The following upgrade is optional**

Seedkits must be upgraded if **both** of the following is true.
- Both `npmMirrorSecret` & `pypiMirrorSecret` are set.
- Mirror secrets are using explicit paths. I.e. (`my-mirror-credentials::npm` && `my-mirror-credentials::pypi`). 

**Note: You can still use this feature by specifying your secret name `my-mirror-credentials` without a path `::pypi` for both secrets.**

To upgrade:
1. Update your version of `aws-codeseeder` via
    ```bash
    pip install --upgrade aws-codeseeder==1.1.0
     ```
2. Run seedfarmer with the `--update-seedkit` flag set
    ```bash
    seedfarmer apply my/manifest/path --update-seedkit
    ```

## Upgrading to 7.0.0  

This is a **BREAKING CHANGE !!!**.

In this release, we have:
- removed support for python 3.8
- have set the `publishGenericEnvVariables` to true by default
- changed the default version of the codebuild image to `aws/codebuild/amazonlinux2-x86_64-standard:5.0`

Each of these changes constitutes a breaking change.

If you are running modules that do NOT leverage generic environment variables, you will need to set `publishGenericEnvVariables` to false in the `deployspec.yaml` of the module. [See this documentation](./module_development.mdl#deployspec-parameters-of-interest)

To update an existing project to use the new default image, you can run:
```bash
seedfarmer apply <deployment.yaml> --update-seedkit [OPTIONS] 
```
 ** We have also removed a dependency on [AWS CodeSeeder](https://github.com/awslabs/aws-codeseeder).  All login within that library is now encapsulated within SeedFarmer.  AWS CodeSeeder is still available in KTLO (Keep The Light On) status.

