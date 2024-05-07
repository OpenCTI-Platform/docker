# Configuring S3 Repository for Elasticsearch Backups

This section guides you through setting up an S3 repository for storing Elasticsearch snapshots. Elasticsearch uses snapshot repositories to store backups of index data that are both reliable and easy to restore.


## Prerequisites

- An active AWS account with access to the S3 service.
- An Elasticsearch cluster with permissions to access S3.
- Proper IAM permissions configured to allow Elasticsearch to read from and write to the S3 bucket.

## Step 1: Create an S3 Bucket

If not already created, set up an S3 bucket in your AWS account. This bucket will store the Elasticsearch snapshots:

```bash
aws s3 mb s3://cfa-opencti --region your-region
```

## Step 2: Register the S3 Repository
To use the S3 bucket as a snapshot repository, you need to register it with your Elasticsearch cluster. Here is how you can register the repository using the provided configuration:
```bash
curl -X PUT "localhost:9200/_snapshot/my_s3_repository" -H 'Content-Type: application/json' -d'
{
  "type": "s3",
  "settings": {
    "bucket": "cfa-opencti",
    "readonly": false
  }
}'
```

## Step 3: Take and Restore Snapshots
Taking a Snapshot
To create a snapshot in the my_s3_repository repository:

```bash
curl -X PUT "localhost:9200/_snapshot/my_s3_repository/my_snapshot_1?wait_for_completion=true"
```

## Restoring a Snapshot
To restore data from a snapshot:

```bash
curl -X POST "localhost:9200/_snapshot/my_s3_repository/my_snapshot_1/_restore"
```
