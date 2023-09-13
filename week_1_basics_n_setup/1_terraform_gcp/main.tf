terraform {
  required_version = "1.5.7"
  required_providers {
    google = {
        source  = "hashicorp/google"
        version = "4.82.0" # https://github.com/hashicorp/terraform-provider-google-beta/releases
    }
  }
}

variable "project" {
  type        = string
  default     = "evocative-tide-398716"
  description = "Globally unique project id"
}

provider "google" {
    project = var.project
    region  = "us-east4" # N. Virginia
    zone    = "us-east4-a" # See regions and zones at https://cloud.google.com/compute/docs/regions-zones
}

# Data Lake Bucket
# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/storage_bucket
resource "google_storage_bucket" "data-lake-bucket" {
  name          = "dtc-data-lake-bucket_${var.project}"
  location      = "us-east4"
  storage_class = "STANDARD"
  force_destroy = true
  versioning {
    enabled = true
  }
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 # days
    }
  }
}

# Ref: https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/bigquery_dataset
resource "google_bigquery_dataset" "dataset" {
  dataset_id = "trips_data_all"
  location   = "us-east4"
  default_table_expiration_ms = 3600000 # auto delete table after 1 hour
}