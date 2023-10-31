terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # leave credentials unspecified to fall back to use google
  # Application Default Credentials (ADC).
  # see https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference#authentication-configuration
  # credentials = file("<NAME>.json")

  project = var.project
  region  = "us-east1"
}

resource "google_storage_bucket" "datalake" {
  # bucket names must be unique across all of Google Cloud Platform
  # see https://cloud.google.com/storage/docs/buckets#naming
  name     = "nyc-lyft-vs-uber-data-lake"
  location = "US"

  force_destroy = true
  storage_class = "STANDARD"
  # This is to get around constraints/storage.uniformBucketLevelAccess
  # also see https://cloud.google.com/storage/docs/uniform-bucket-level-access
  uniform_bucket_level_access = true
}

resource "google_bigquery_dataset" "warehouse" {
  dataset_id = "warehouse"
  location   = "US"

  delete_contents_on_destroy = true
}