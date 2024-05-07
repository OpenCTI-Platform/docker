# Setting Up Snapshot Lifecycle Management (SLM) Policy

This section guides you through the configuration of an SLM policy for automated snapshot management in Elasticsearch. The policy will schedule daily snapshots, maintain them based on defined retention rules, and store them in an S3 repository.

## Prerequisites

- A registered S3 repository in Elasticsearch as outlined in [s3 backups](./scripts/s3_backups.md).
- Elasticsearch cluster with SLM feature available and enabled.

## Step 1: Define the SLM Policy

Define an SLM policy named `daily-snapshots` that automatically creates snapshots based on a specified schedule and retention policy. Here's how you can set up this policy:

```bash
curl -X PUT "https://localhost:9200/_slm/policy/daily-snapshots" -H 'Content-Type: application/json' -d'
{
  "schedule": "0 30 1 * * ?",  // This cron expression means the snapshot will be taken at 01:30 AM every day
  "name": "<daily-snap-{now/d}>",  // Snapshot names will be dynamically generated with the date
  "repository": "opencti-backup-repo",  // The name of the repository to store the snapshots
  "config": {
    "indices": "*",  // All indices are included in the snapshot
    "ignore_unavailable": false,
    "include_global_state": true
  },
  "retention": {
    "expire_after": "30d",  // Snapshots older than 30 days will be deleted
    "min_count": 7,  // At least 7 snapshots will be retained
    "max_count": 20  // No more than 20 snapshots will be kept
  }
}'
```